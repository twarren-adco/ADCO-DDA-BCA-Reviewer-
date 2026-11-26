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
echo "all self-tests passed"
