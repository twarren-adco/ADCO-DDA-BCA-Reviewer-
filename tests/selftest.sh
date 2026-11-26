#!/usr/bin/env bash
# Builds a synthetic A1 sheet (1:100 plan + 1:20 detail) and checks that
# calibration passes per viewport, refuses a whole-sheet verdict with two
# scales, and flags the deliberately wrong dimension.
set -euo pipefail
cd "$(dirname "$0")/.."
T=$(mktemp -d)
trap 'rm -rf "$T"' EXIT
python3 tests/make_sample.py "$T/s.pdf" >/dev/null

fail() { echo "FAIL: $1"; exit 1; }

python3 tools/drawing.py calibrate "$T/s.pdf" -p 1 | grep -q "MULTIPLE SCALES" \
  || fail "whole sheet should refuse to calibrate"
out=$(python3 tools/drawing.py calibrate "$T/s.pdf" -p 1 --region 0,0,800,600 --scale 100)
echo "$out" | grep -q "VERDICT: CALIBRATED" || fail "plan 1:100 should calibrate"
echo "$out" | grep -q "1800 mm.*MISMATCH" || fail "wrong dimension not flagged"
echo "$out" | grep -q "printed   8000" || fail "rotated dimension not read"
python3 tools/drawing.py calibrate "$T/s.pdf" -p 1 --region 800,150,1250,600 --scale 20 \
  | grep -q "VERDICT: CALIBRATED" || fail "detail 1:20 should calibrate"
python3 tools/drawing.py calibrate "$T/s.pdf" -p 1 --region 800,150,1250,600 --scale 50 \
  | grep -q "UNRELIABLE" || fail "wrong scale should be rejected"
python3 tools/drawing.py render "$T/s.pdf" -p 1 -o "$T/r.png" --dpi 40 --grid 100 >/dev/null \
  || fail "render"
# drop zone round trip (offline): split into parts as the page does, restore, compare
python3 - "$T" <<'PY'
import base64,hashlib,json,pathlib,sys
T=pathlib.Path(sys.argv[1]); raw=(T/"s.pdf").read_bytes(); d=T/"dz"/"jobs"/"_st"/"files"; d.mkdir(parents=True)
path="drawings/A-101.pdf"; fid="f"+hashlib.sha256(path.encode()).hexdigest()[:16]; R=1000
parts=[raw[i:i+R] for i in range(0,len(raw),R)]
for n,p in enumerate(parts):
    (d/f"{fid}_{n:04d}.json").write_text(json.dumps({"file_id":fid,"part":n,"parts":len(parts),"b64":base64.b64encode(p).decode()}))
(d/"_index.json").write_text(json.dumps({"files":[{"file_id":fid,"path":path,"size":len(raw),"sha256":hashlib.sha256(raw).hexdigest(),"parts":len(parts)}]}))
PY
python3 tools/dropzone.py restore --from "$T/dz" --job _selftest >/dev/null || fail "dropzone restore"
cmp -s projects/_selftest/drawings/A-101.pdf "$T/s.pdf" || fail "restored file differs"
python3 tools/progress.py init _selftest >/dev/null || fail "progress init"
python3 tools/progress.py status _selftest | grep -q "NEXT:" || fail "progress status"
rm -rf projects/_selftest
# drop zone, file-store format: two page-range chunks, restore, check names and pages
python3 - "$T" <<'PY'
import hashlib,json,pathlib,sys,pymupdf
T=pathlib.Path(sys.argv[1]); src=pymupdf.open(T/"s.pdf")
d=T/"dz2"; (d/"jobs/X/files").mkdir(parents=True); (d/"assets").mkdir()
two=pymupdf.open(); two.insert_pdf(src); two.insert_pdf(src); raw=two.tobytes()
one=pymupdf.open(); one.insert_pdf(src); b=one.tobytes()
(d/"assets/a1.pdf").write_bytes(b); (d/"assets/a2.pdf").write_bytes(b)
h=hashlib.sha256(b).hexdigest()
idx={"format":2,"files":[{"file_id":"fz","path":"drawings/Pack.pdf","pages_total":2,"pages_label":"1-2","sha256":hashlib.sha256(raw).hexdigest(),
 "chunks":[{"asset_id":"a1","pages":[1],"size":len(b),"sha256":h},{"asset_id":"a2","pages":[2],"size":len(b),"sha256":h}]}]}
(d/"jobs/X/files/_index.json").write_text(json.dumps(idx))
PY
python3 tools/dropzone.py restore --from "$T/dz2" --job _selftest2 >/dev/null || fail "asset-format restore"
[ -f "projects/_selftest2/drawings/Pack [p1].pdf" ] && [ -f "projects/_selftest2/drawings/Pack [p2].pdf" ] || fail "chunk names"
rm -rf projects/_selftest2
# over-size sheet stored as base64 text parts: restore must rebuild identical bytes
python3 - "$T" <<'PY'
import base64,hashlib,json,os,pathlib,sys
T=pathlib.Path(sys.argv[1]); d=T/"dz3"; (d/"jobs/X/files").mkdir(parents=True); (d/"assets").mkdir()
raw=(T/"s.pdf").read_bytes()+os.urandom(5000); half=len(raw)//2
(d/"assets/p1.txt").write_text(base64.b64encode(raw[:half]).decode()); (d/"assets/p2.txt").write_text(base64.b64encode(raw[half:]).decode())
(T/"big.bin").write_bytes(raw)
idx={"format":2,"files":[{"file_id":"fb","path":"drawings/Big.pdf","pages_total":None,"pages_label":"whole file","sha256":hashlib.sha256(raw).hexdigest(),
 "chunks":[{"parts":["p1","p2"],"encoding":"base64","pages":None,"size":len(raw),"sha256":hashlib.sha256(raw).hexdigest()}]}]}
(d/"jobs/X/files/_index.json").write_text(json.dumps(idx))
PY
python3 tools/dropzone.py restore --from "$T/dz3" --job _selftest3 >/dev/null || fail "text-part restore"
cmp -s projects/_selftest3/drawings/Big.pdf "$T/big.bin" || fail "text-part bytes differ"
rm -rf projects/_selftest3
echo "all self-tests passed"
