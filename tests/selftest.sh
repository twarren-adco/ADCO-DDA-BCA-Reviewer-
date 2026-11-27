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

whole=$(python3 tools/drawing.py calibrate "$T/s.pdf" -p 1)
echo "$whole" | grep -q "CALIBRATED BY VIEWPORT" || fail "two-scale sheet should calibrate per viewport"
echo "$whole" | grep -q "viewport 1:100" && echo "$whole" | grep -q "viewport 1:20" || fail "both viewports should be found"
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
# grid carry-over maths: parallel lines 8000 mm apart at 1:100 -> 80 mm on paper
python3 - <<'PY' || fail "grid spacing"
import sys; sys.path.insert(0, "tools")
from grids import spacings, PT_TO_MM
pt = 80 / PT_TO_MM
lines = [{"label": "1", "angle": 90.0, "p": (100, 50)}, {"label": "2", "angle": 90.0, "p": (100 + pt, 400)},
         {"label": "RA", "angle": 160.0, "p": (300, 300)}]
sp = spacings(lines)
assert set(sp) == {"1|2"}, sp
assert abs(sp["1|2"] * PT_TO_MM * 100 - 8000) < 1, sp
PY
# joinery regressions (Kingscliff JC21-23, C-2202, JO38): chained drawer dims with
# overshooting dimension lines, a background line through the figures, diagonal
# radius dims with ticks, ceiling tags. Must calibrate at the printed 1:20.
python3 tests/make_joinery.py "$T/j.pdf"
j=$(python3 tools/drawing.py calibrate "$T/j.pdf" -p 1)
echo "$j" | grep -q "VERDICT: CALIBRATED (1:20)" || { echo "$j"; fail "joinery sheet should calibrate 1:20"; }
echo "$j" | grep -q "printed   3080\|printed   2400\|printed   2700" && fail "ceiling tag read as a dimension"
[ "$(echo "$j" | grep -c 'printed    450.*OK')" -ge 3 ] || { echo "$j"; fail "drawer stack dims should match their witness lines"; }
# printed-scale confirmation: small one-sided errors confirm the printed scale;
# a genuine contradiction (another standard scale) never does
python3 - <<'PY' || fail "printed scale confirmation"
import sys; sys.path.insert(0, "tools")
from drawing import printed_scale_confirmed as c
m = lambda *v: [{"implied_scale": x} for x in v]
assert c(m(18.4, 18.4, 18.4, 19.1, 19.0), [20], 0.02), "6-8% long readings at 1:20 should confirm 1:20"
assert c(m(50.0, 47.6, 48.1, 44.2), [50], 0.02)
assert not c(m(40.1, 39.8, 40.0, 20.0), [20], 0.02), "three dims at 1:40 contradict 1:20"
assert not c(m(25.0, 24.9, 25.2, 19.0), [20], 0.02), "1:25 is another standard scale"
assert not c(m(19.0, 19.5), [20, 50], 0.02), "two printed scales: not this rule"
PY
echo "all self-tests passed"
