#!/usr/bin/env python3
"""
printedscale.py - use the scale printed on each viewport title when a sheet has
nothing else to check its scale against.

Revit/ArchiCAD print each view's scale under its title, e.g.
"1  CORRIDOR WALL JUNCTION DETAIL / SCALE 1 : 5 @A1". A vector PDF exported at
full size reproduces that scale exactly, so it is accepted when:
  * the page really is the paper size the note names (e.g. "@A1" on an
    841 x 594 mm page, within 3 mm) - this catches sets printed or saved to A3;
  * no printed dimension on the sheet contradicts it (the sheet must not be
    UNRELIABLE from its own dimensions).

  python3 tools/printedscale.py <pdf> -p N            # show the viewport scale labels found
  python3 tools/printedscale.py --job <job>           # apply to every sheet not already calibrated

Where all viewport titles on a sheet share one scale, the whole sheet takes it.
Where they differ, each title governs the area above it (Revit places titles
under the view, left-aligned); regions are written to calibration.jsonl.
"""
import argparse, json, pathlib, re, sys

import pymupdf

ROOT = pathlib.Path(__file__).resolve().parent.parent
PAPER = {"A0": (1189, 841), "A1": (841, 594), "A2": (594, 420), "A3": (420, 297), "A4": (297, 210)}
LABEL = re.compile(r"SCALE\s*[:\-]?\s*1\s*:\s*(\d{1,4})\s*@\s*(A[0-4])", re.I)
TB = re.compile(r"(1\s*:\s*\d{1,4}(?:\s*,\s*1\s*:\s*\d{1,4})*)\s*@\s*(A[0-4])\s*SIZE", re.I)


def labels(pdf, page_no):
    p = pymupdf.open(pdf)[page_no - 1]
    w_mm, h_mm = p.rect.width * 25.4 / 72, p.rect.height * 25.4 / 72
    out = []
    for b in p.get_text("dict")["blocks"]:
        if b.get("type") != 0:
            continue
        for ln in b["lines"]:
            text = "".join(sp["text"] for sp in ln["spans"])
            for m in LABEL.finditer(text):
                x0, y0, x1, y1 = ln["bbox"]
                out.append({"scale": int(m.group(1)), "paper": m.group(2).upper(), "x": round(x0), "y": round(y0)})
    tb = TB.search(p.get_text())
    return out, (w_mm, h_mm), (tb.group(1), tb.group(2).upper()) if tb else None


def paper_ok(size, paper):
    a, b = PAPER[paper]
    w, h = sorted(size, reverse=True)
    return abs(w - a) <= 3 and abs(h - b) <= 3


def regions(lbls, size_pt):
    """Each label governs the area above it, from its x to the next label to the right
    on roughly the same row, up to the previous row of labels."""
    W, H = size_pt
    rows = sorted(lbls, key=lambda l: l["y"])
    out = []
    for l in rows:
        above = [o for o in rows if o["y"] < l["y"] - 40 and abs(o["x"] - l["x"]) < W * 0.25]
        top = max((o["y"] + 20 for o in above), default=0)
        right_neighbours = [o["x"] for o in rows if abs(o["y"] - l["y"]) < 120 and o["x"] > l["x"] + 50]
        right = min(right_neighbours, default=W * 0.85) - 10
        out.append({"scale": l["scale"], "region": [max(0, l["x"] - 40), top, round(right), l["y"] + 30]})
    return out


def judge(pdf, page_no):
    lbls, size_mm, tb = labels(pdf, page_no)
    res = {"labels": lbls}
    papers = {l["paper"] for l in lbls} | ({tb[1]} if tb else set())
    if not lbls:
        # no viewport titles: fall back to the title block when it states one scale
        if tb and "," not in tb[0]:
            sc = int(re.search(r"1\s*:\s*(\d+)", tb[0]).group(1))
            if not paper_ok(size_mm, tb[1]):
                res["verdict"] = (f"PRINTED SCALE NOT USABLE - title block says @{tb[1]} but page is "
                                  f"{size_mm[0]:.0f}x{size_mm[1]:.0f} mm (reduced or resized print)")
            else:
                res["verdict"] = f"PRINTED SCALE - title block states 1:{sc} on a full-size {tb[1]} sheet (no viewport titles)"
                res["calibrated_scale"] = sc
            return res
        res["verdict"] = "NO VIEWPORT SCALE LABELS"
        return res
    bad = [p for p in papers if not paper_ok(size_mm, p)]
    if bad:
        res["verdict"] = (f"PRINTED SCALE NOT USABLE - note says @{'/'.join(sorted(papers))} but page is "
                          f"{size_mm[0]:.0f}x{size_mm[1]:.0f} mm (reduced or resized print)")
        return res
    scales = sorted({l["scale"] for l in lbls})
    if len(scales) == 1:
        res["verdict"] = f"PRINTED SCALE - every viewport labelled 1:{scales[0]} on a full-size {next(iter(papers))} sheet"
        res["calibrated_scale"] = scales[0]
    else:
        W, H = size_mm[0] * 72 / 25.4, size_mm[1] * 72 / 25.4
        res["verdict"] = ("PRINTED SCALE BY VIEWPORT - " + ", ".join(f"1:{s}" for s in scales)
                          + f" on a full-size {next(iter(papers))} sheet; measure only inside a viewport's region")
        res["viewports"] = regions(lbls, (W, H))
    return res


def apply_job(job):
    base = ROOT / "projects" / job
    idx = {r["sheet"]: r for r in json.loads((base / "output" / "sheet-index.json").read_text())}
    p = base / "output" / "calibration.jsonl"
    rows = [json.loads(l) for l in p.read_text().splitlines()]
    counts = {}
    for r in rows:
        v = r.get("verdict") or ""
        if v.startswith(("CALIBRATED", "SCAN/RASTER", "UNRELIABLE", "SCHEDULE", "NOTHING TO MEASURE")):
            continue          # already confirmed, not vector, or contradicted by its own dimensions
        row = idx[r["sheet"]]
        j = judge(base / row["file"], row["page_in_file"])
        key = j["verdict"].split(" - ")[0]
        counts[key] = counts.get(key, 0) + 1
        if key.startswith("PRINTED SCALE") and "NOT USABLE" not in key:
            r["previous_verdict"] = v
            r["verdict"] = j["verdict"]
            if j.get("calibrated_scale"):
                r["calibrated_scale"] = j["calibrated_scale"]
            if j.get("viewports"):
                r["viewports"] = j["viewports"]
            r["viewport_labels"] = j["labels"]
        print(f"sheet {r['sheet']:>3} {row['drawing']:<18} {j['verdict'][:110]}", flush=True)
    p.write_text("".join(json.dumps(r) + "\n" for r in rows))
    print(counts)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("pdf", nargs="?"); ap.add_argument("-p", "--page", type=int); ap.add_argument("--job")
    a = ap.parse_args()
    if a.job:
        apply_job(a.job)
    else:
        print(json.dumps(judge(a.pdf, a.page), indent=1))


if __name__ == "__main__":
    main()
