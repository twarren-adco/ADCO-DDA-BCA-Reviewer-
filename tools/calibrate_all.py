#!/usr/bin/env python3
"""
calibrate_all.py - run the scale check on every sheet of a restored job.

  python3 tools/calibrate_all.py <job> [--workers 4] [--sheets 1-50,120]

Needs output/sheet-index.json (tools/sheetindex.py). Results are appended to
output/calibration.jsonl as they finish (so an interrupted run resumes and
skips sheets already done), and summarised in output/calibration-log.md.
Raster sheets are recorded without running geometry.
"""
import argparse, json, pathlib, subprocess, sys
from concurrent.futures import ProcessPoolExecutor, as_completed

ROOT = pathlib.Path(__file__).resolve().parent.parent


def run_one(args):
    job, row = args
    base = ROOT / "projects" / job
    if row["kind"] == "raster":
        return {"sheet": row["sheet"], "verdict": "SCAN/RASTER - not measurable", "matched": 0}
    try:
        p = subprocess.run([sys.executable, str(ROOT / "tools" / "drawing.py"), "calibrate",
                            str(base / row["file"]), "-p", str(row["page_in_file"]), "--json"],
                           capture_output=True, text=True, timeout=600)
        r = json.loads(p.stdout)
        keep = {k: r.get(k) for k in ("verdict", "calibrated_scale", "scales_on_sheet", "dimension_texts",
                                         "matched", "by_scale", "median_implied_scale")}
        keep["mismatches"] = len(r.get("mismatches") or [])
        keep["sheet"] = row["sheet"]
        return keep
    except subprocess.TimeoutExpired:
        return {"sheet": row["sheet"], "verdict": "TIMEOUT - too heavy to check automatically", "matched": 0}
    except Exception as e:  # noqa: BLE001
        return {"sheet": row["sheet"], "verdict": f"ERROR - {type(e).__name__}", "matched": 0}


def parse_sheets(s):
    out = set()
    for part in s.split(","):
        a, _, b = part.partition("-")
        out.update(range(int(a), int(b or a) + 1))
    return out


def summarise(job):
    base = ROOT / "projects" / job / "output"
    idx = {r["sheet"]: r for r in json.loads((base / "sheet-index.json").read_text())}
    res = {}
    for line in (base / "calibration.jsonl").read_text().splitlines():
        r = json.loads(line); res[r["sheet"]] = r
    def short(v):
        v = v or ""
        if v.startswith("CALIBRATED"): return "CALIBRATED"
        return v.split(" - ")[0]
    counts = {}
    for r in res.values():
        counts[short(r["verdict"])] = counts.get(short(r["verdict"]), 0) + 1
    md = [f"# Calibration log – {job}", "",
          "Whole-sheet scale check (`tools/calibrate_all.py`). A sheet passes when at least 3 and at least half of its matched "
          "printed dimensions agree with one scale within ±2%, measured witness line to witness line. "
          "*MULTIPLE SCALES* sheets (several viewports) need a per-viewport check before measuring.", "",
          "Summary: " + ", ".join(f"{v} {k}" for k, v in sorted(counts.items(), key=lambda t: -t[1])), "",
          "| Sheet | Drawing | Title | Scale (printed) | Result | Agree |", "|---|---|---|---|---|---|"]
    for s in sorted(res):
        r, x = res[s], idx.get(s, {})
        agree = " / ".join(f"1:{int(b['scale'])} {b['agree']}/{b['of']}" for b in (r.get("by_scale") or []))
        result = short(r["verdict"]) + (f" 1:{int(r['calibrated_scale'])}" if r.get("calibrated_scale") else "")
        md.append(f"| {s} | {x.get('drawing','')} | {x.get('title','')[:70]} | {x.get('scale','')} | {result} | {agree} |")
    (base / "calibration-log.md").write_text("\n".join(md) + "\n")
    return counts


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("job"); ap.add_argument("--workers", type=int, default=4); ap.add_argument("--sheets")
    a = ap.parse_args()
    base = ROOT / "projects" / a.job / "output"
    rows = json.loads((base / "sheet-index.json").read_text())
    done = set()
    jl = base / "calibration.jsonl"
    if jl.exists():
        done = {json.loads(l)["sheet"] for l in jl.read_text().splitlines() if l.strip()}
    want = parse_sheets(a.sheets) if a.sheets else None
    todo = [r for r in rows if r["sheet"] not in done and (want is None or r["sheet"] in want)]
    print(f"{len(todo)} sheet(s) to check, {len(done)} already done", flush=True)
    with ProcessPoolExecutor(max_workers=a.workers) as ex, jl.open("a") as f:
        futs = [ex.submit(run_one, (a.job, r)) for r in todo]
        for n, fu in enumerate(as_completed(futs), 1):
            r = fu.result(); f.write(json.dumps(r) + "\n"); f.flush()
            if n % 20 == 0 or n == len(todo):
                print(f"{n}/{len(todo)} done", flush=True)
    print(summarise(a.job))


if __name__ == "__main__":
    main()
