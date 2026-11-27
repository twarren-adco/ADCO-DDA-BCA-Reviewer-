#!/usr/bin/env python3
"""
calibrate_all.py - run the scale check on every sheet of a restored job.

  python3 tools/calibrate_all.py <job> [--workers 4] [--sheets 1-50,120]

Needs output/sheet-index.json (tools/sheetindex.py). Results are appended to
output/calibration.jsonl as they finish (so an interrupted run resumes and
skips sheets already done), and summarised in output/calibration-log.md.
Raster sheets are recorded without running geometry.
"""
import argparse, json, pathlib, re, subprocess, sys
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
                                         "matched", "by_scale", "median_implied_scale", "viewports")}
        keep["mismatches"] = len(r.get("mismatches") or [])
        keep["sheet"] = row["sheet"]
        for k in ("level_pairs", "level_query"):
            if r.get(k):
                keep[k] = r[k]
        if (keep["verdict"] or "").startswith(("NO DIMENSIONS", "NO SCALE STRING")):
            why = nothing_to_measure(base / row["file"], row["page_in_file"], row.get("title") or "")
            if why:
                keep["previous_verdict"] = keep["verdict"]
                keep["verdict"] = "NOTHING TO MEASURE - " + why
        return keep
    except subprocess.TimeoutExpired:
        return {"sheet": row["sheet"], "verdict": "TIMEOUT - too heavy to check automatically", "matched": 0}
    except Exception as e:  # noqa: BLE001
        return {"sheet": row["sheet"], "verdict": f"ERROR - {type(e).__name__}", "matched": 0}


NOT_DRAWING = re.compile(r"COVER (SHEET|PAGE)|DRAWING (REGISTER|LIST|SCHEDULE)|LEGEND SHEET|^LEGEND", re.I)


def nothing_to_measure(pdf, page, title):
    """Cover sheets, registers, legends, sheets marked not in use and sheets with
    nothing drawn outside the title block and notes column."""
    if NOT_DRAWING.search(title):
        return "cover / register / legend sheet"
    import pymupdf
    p = pymupdf.open(pdf)[page - 1]
    if re.search(r"SHEET NOT IN USE|NOT USED|INTENTIONALLY (LEFT )?BLANK", p.get_text(), re.I):
        return "sheet marked not in use"
    W, H = p.rect.width, p.rect.height
    n = 0
    for d in p.get_drawings():
        r = d["rect"]
        if r.y1 < H * 0.86 and r.x1 < W * 0.84 and max(r.width, r.height) >= 20:
            n += 1
            if n >= 30:
                return None
    return "nothing drawn (notes / title block only)"


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
        if v.startswith("CALIBRATED FROM GRIDS"): return "From grids"
        if v.startswith("CALIBRATED FROM LEVELS"): return "From levels"
        if v.startswith("CALIBRATED FROM MATCHING"): return "Matched sheets"
        if v.startswith("SCHEDULE"): return "Schedule (text)"
        if v.startswith("NOTHING TO MEASURE"): return "Nothing to measure"
        if v.startswith("PRINTED SCALE BY VIEWPORT"): return "Printed (by viewport)"
        if v.startswith("PRINTED SCALE"): return "Printed scale"
        if v.startswith("CALIBRATED BY VIEWPORT"): return "By viewport"
        if v.startswith("CALIBRATED"): return "Calibrated"
        return {"NO DIMENSIONS": "No dimensions", "NO SCALE STRING": "No scale printed", "UNRELIABLE": "Unreliable",
                "MULTIPLE SCALES": "Mixed scales", "SCAN/RASTER": "Image"}.get(v.split(" - ")[0], v.split(" - ")[0])
    cols = ["Calibrated", "By viewport", "From grids", "From levels", "Matched sheets", "Printed scale",
            "Printed (by viewport)", "Schedule (text)", "Nothing to measure", "No dimensions", "No scale printed",
            "Unreliable", "Mixed scales", "Image"]
    names = {"0": "General / site", "1": "GA plans, RCPs, wall types", "2": "Elevations", "3": "Sections",
             "4": "Unit & common-area fitouts, wet areas", "5": "Details", "6": "Schedules", "7": "Joinery / details", "8": "FF&E schedules"}
    tab, tot = {}, {}
    for s, r in res.items():
        d = idx.get(s, {}).get("drawing", ""); n = d.split("-")[-1] if d else ""
        k = n[:1] if n[:1].isdigit() else "?"
        tab.setdefault(k, {}); c = short(r["verdict"])
        tab[k][c] = tab[k].get(c, 0) + 1; tot[c] = tot.get(c, 0) + 1
    measurable = sum(tot.get(c, 0) for c in ("Calibrated", "By viewport", "From grids", "From levels", "Matched sheets",
                                              "Printed scale", "Printed (by viewport)"))
    no_need = tot.get("Schedule (text)", 0) + tot.get("Nothing to measure", 0)
    md = [f"# Calibration log – {job}", "",
          f"**{measurable} of {len(res)} sheets can be measured from geometry.** "
          f"{no_need} more need no measuring (schedules read as text, covers, registers, legends, blank sheets); "
          f"{tot.get('Image', 0)} are images.", "",
          "Method (`tools/calibrate_all.py`, `tools/grids.py`): printed dimensions are paired with their dimension lines "
          "(any angle) and measured witness line to witness line; horizontal/vertical dimension lines need witness lines "
          "crossing both ends. A sheet passes when >=3 and >=50% of matched dimensions agree with one scale within +-2%, "
          "or, where one scale is printed, when most dimensions are within +-12% of it and no other standard scale "
          "is supported by 3 or more (standard scales are 25%+ apart, so small drafting errors can't fake one). "
          "*By viewport*: each consistent viewport (>=3 dimensions, >=65% agreement inside its area) is calibrated "
          "separately and measuring is valid only inside its listed region (`calibration.jsonl`). "
          "*From grids*: the sheet has no usable dimensions, but >=3 grid spacings (from `grid-table.json`, built from "
          "calibrated plans) agree with one scale within +-1% and with the printed scale. "
          "*Printed scale*: no dimensions or grids to check against, so the scale printed under each viewport title "
          "(e.g. 'SCALE 1 : 5 @A1') is used, accepted only because the page is the full paper size the note names "
          "(`tools/printedscale.py`). Mixed-scale sheets get a region per viewport. "
          "*From levels*: >=3 pairs of level heads on elevations/sections (FFL 0.00 / FCL 2700, RL ...) agree with one "
          "scale within +-2%. *Matched sheets*: the sheet's linework is the same as >=2 calibrated sheets "
          "(edges of equal angle with one length ratio that also line up after one shift; `tools/sheetmatch.py`). "
          "*Schedule (text)*: the figures are table cells, read as text.", "",
          "| Series | " + " | ".join(cols) + " |", "|---|" + "---|" * len(cols)]
    for k in sorted(tab):
        md.append(f"| {k}xxx {names.get(k, 'Other')} | " + " | ".join(str(tab[k].get(c, 0)) for c in cols) + " |")
    md.append("| **Total** | " + " | ".join(f"**{tot.get(c, 0)}**" for c in cols) + " |")
    md += ["", "*No dimensions*: fewer than 3 printed dimensions and no shared grid (e.g. details, joinery). "
           "*Unreliable*: dimensions disagree (mostly reflected ceiling plans and sparsely dimensioned fitouts). "
           "*Image*: mostly raster. Schedules are read as text, not measured.", ""]
    q = base / "scale-queries.md"
    if q.exists() and q.read_text().strip():
        md += ["## Queries raised by the scale check", "", q.read_text().strip(), ""]
    md += ["## Per sheet", "",
           "| Sheet | Drawing | Title | Scale (printed) | Result | Agree |", "|---|---|---|---|---|---|"]
    for s in sorted(res):
        r, x = res[s], idx.get(s, {})
        agree = r.get("grid_agree") or " / ".join(f"1:{int(b['scale'])} {b['agree']}/{b['of']}" for b in (r.get("by_scale") or []))
        result = short(r["verdict"]) + (f" 1:{int(r['calibrated_scale'])}" if r.get("calibrated_scale") else "")
        if r.get("viewports") and short(r["verdict"]) in ("By viewport", "Printed (by viewport)"):
            result += " (" + ", ".join(f"1:{v['scale']}" for v in r["viewports"]) + ")"
        md.append(f"| {s} | {x.get('drawing','')} | {x.get('title','')[:70]} | {x.get('scale','')} | {result} | {agree} |")
    (base / "calibration-log.md").write_text("\n".join(md) + "\n")
    return tot


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
