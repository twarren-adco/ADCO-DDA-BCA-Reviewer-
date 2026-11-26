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
echo "all self-tests passed"
