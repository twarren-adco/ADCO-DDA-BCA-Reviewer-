#!/usr/bin/env python3
"""
grids.py - carry a project's structural grid from calibrated sheets to sheets
that have no dimensions of their own.

The grid is the same on every plan. On a sheet that passed the scale check, the
spacing between two grid lines (e.g. grid 9 to grid 10) is a known real
distance. On a sheet with no dimensions, the same pair of grid lines can be
measured on paper; real / paper gives the sheet's scale. If several grid pairs
agree with one standard scale, and that matches the printed scale, the sheet
is treated as calibrated ("CALIBRATED FROM GRIDS").

  python3 tools/grids.py detect <pdf> -p N            # list grid lines found on a sheet
  python3 tools/grids.py learn  <job>                 # build output/grid-table.json from calibrated sheets
  python3 tools/grids.py check  <job> [--sheets ...]  # calibrate other sheets against the table

Grid bubbles: a closed, roughly circular shape 15-45 pt across with a single
short label inside (A, 12, R5, RA ...). The grid line is the line through the
bubble centre along which other line work runs. A label appearing at both ends
of one line is one grid line.
"""
import argparse, json, math, pathlib, re, statistics, subprocess, sys
from collections import defaultdict

import pymupdf

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
from drawing import STANDARD_SCALES  # noqa: E402

PT_TO_MM = 25.4 / 72
LABEL = re.compile(r"^(?:[A-Z]{1,2}|R[A-Z]|R\d{1,2}|\d{1,2}[A-Z]?)$")


def _ang(dx, dy):
    return math.degrees(math.atan2(dy, dx)) % 180


def detect(pdf, page_no):
    doc = pymupdf.open(pdf)
    p = doc[page_no - 1]
    words = [w for w in p.get_text("words") if LABEL.match(w[4])]
    draws = p.get_drawings()
    segs = []
    bubbles = []
    for dr in draws:
        rc = dr["rect"]
        items = dr["items"]
        if 15 < rc.width < 45 and abs(rc.width - rc.height) < 2 and len(items) >= 8:
            cx, cy = (rc.x0 + rc.x1) / 2, (rc.y0 + rc.y1) / 2
            inside = [w for w in words if rc.x0 < (w[0] + w[2]) / 2 < rc.x1 and rc.y0 < (w[1] + w[3]) / 2 < rc.y1]
            if len(inside) == 1:
                bubbles.append({"label": inside[0][4], "c": (cx, cy), "r": rc.width / 2})
                continue
        for it in items:
            if it[0] == "l":
                a, b = it[1], it[2]
                L = math.hypot(b.x - a.x, b.y - a.y)
                if L > 3:
                    segs.append((a.x, a.y, b.x, b.y, L))
    # grid line through each bubble: collinear line work running away from it
    lines = {}
    for bu in bubbles:
        cx, cy = bu["c"]; r = bu["r"]
        votes = defaultdict(float)
        for (x0, y0, x1, y1, L) in segs:
            # only line work starting near the bubble rim
            d0 = math.hypot(x0 - cx, y0 - cy); d1 = math.hypot(x1 - cx, y1 - cy)
            if min(d0, d1) > r + 40 or min(d0, d1) < r * 0.8:
                continue
            dx, dy = x1 - x0, y1 - y0
            perp = abs((cx - x0) * dy - (cy - y0) * dx) / L
            if perp < 1.0:
                votes[round(_ang(dx, dy), 1)] += L
        if not votes:
            continue
        ang = max(votes, key=votes.get)
        if votes[ang] < 20:
            continue
        key = bu["label"]
        prev = lines.get(key)
        if prev and abs((prev["angle"] - ang + 90) % 180 - 90) > 1:
            key = key + "*"          # same label on a different family: keep apart
        lines.setdefault(key, {"label": key, "angle": ang, "points": []})["points"].append((cx, cy))
    return [dict(v, p=v["points"][0]) for v in lines.values()]


def spacings(lines):
    """Perpendicular paper distance (pt) for every pair of parallel grid lines."""
    out = {}
    for i, a in enumerate(lines):
        for b in lines[i + 1:]:
            if abs((a["angle"] - b["angle"] + 90) % 180 - 90) > 0.5:
                continue
            t = math.radians(a["angle"])
            nx, ny = -math.sin(t), math.cos(t)
            d = abs((b["p"][0] - a["p"][0]) * nx + (b["p"][1] - a["p"][1]) * ny)
            if d < 5:
                continue
            k = "|".join(sorted([a["label"], b["label"]]))
            out[k] = d
    return out


def _load(job):
    base = ROOT / "projects" / job
    idx = {r["sheet"]: r for r in json.loads((base / "output" / "sheet-index.json").read_text())}
    res = {}
    for l in (base / "output" / "calibration.jsonl").read_text().splitlines():
        r = json.loads(l); res[r["sheet"]] = r
    return base, idx, res


def cmd_detect(a):
    ls = detect(a.pdf, a.page)
    for g in sorted(ls, key=lambda g: (round(g["angle"]), g["label"])):
        print(f"grid {g['label']:>4}  angle {g['angle']:6.1f}  at ({g['p'][0]:.0f},{g['p'][1]:.0f})  bubbles {len(g['points'])}")
    print(f"{len(ls)} grid line(s)")


def cmd_learn(a):
    base, idx, res = _load(a.job)
    acc = defaultdict(list)
    used = 0
    for s, r in sorted(res.items()):
        sc = r.get("calibrated_scale")
        if not sc or not (r.get("verdict") or "").startswith("CALIBRATED") or "VIEWPORT" in (r.get("verdict") or ""):
            continue
        row = idx[s]
        if not row["drawing"] or row["drawing"].split("-")[-1][:1] != "1":     # plans only
            continue
        ls = detect(base / row["file"], row["page_in_file"])
        sp = spacings(ls)
        if not sp:
            continue
        used += 1
        for k, d in sp.items():
            acc[k].append((d * PT_TO_MM * sc, s))
    table = {}
    for k, vals in acc.items():
        mm = [v for v, _ in vals]
        med = statistics.median(mm)
        agree = [v for v in mm if abs(v / med - 1) < 0.005]
        if len(agree) >= 2 and len(agree) >= 0.75 * len(mm):
            table[k] = {"mm": round(statistics.median(agree)), "sheets": sorted({s for v, s in vals if abs(v / med - 1) < 0.005})}
    out = base / "output" / "grid-table.json"
    out.write_text(json.dumps(table, indent=1))
    print(f"grid table: {len(table)} grid pair(s) agreed across calibrated plans ({used} sheets used) -> {out}")


def cmd_check(a):
    base, idx, res = _load(a.job)
    table = json.loads((base / "output" / "grid-table.json").read_text())
    want = None
    if a.sheets:
        want = set()
        for part in a.sheets.split(","):
            x, _, y = part.partition("-"); want.update(range(int(x), int(y or x) + 1))
    results = []
    for s, r in sorted(res.items()):
        if want is not None and s not in want:
            continue
        v = r.get("verdict") or ""
        if want is None and v.startswith(("CALIBRATED", "SCHEDULE", "NOTHING TO MEASURE")):
            continue
        row = idx[s]
        if row["kind"] == "raster":
            continue
        ls = detect(base / row["file"], row["page_in_file"])
        sp = spacings(ls)
        implied = [(table[k]["mm"] / (d * PT_TO_MM), k) for k, d in sp.items() if k in table]
        out = {"sheet": s, "drawing": row["drawing"], "printed": row["scale"], "grid_pairs": len(implied)}
        best = None
        for sc in STANDARD_SCALES:
            ok = [k for v, k in implied if abs(v / sc - 1) <= 0.01]
            if not best or len(ok) > len(best[1]):
                best = (sc, ok)
        printed = re.findall(r"1\s*:\s*(\d+)", row["scale"] or "")
        if best and len(best[1]) >= 3 and len(best[1]) >= 0.7 * len(implied):
            out["scale"] = best[0]; out["agree"] = f"{len(best[1])}/{len(implied)}"
            matches_printed = (not printed) or str(best[0]) in printed
            out["verdict"] = ("CALIBRATED FROM GRIDS" if matches_printed
                              else f"GRIDS SAY 1:{best[0]} BUT SHEET SAYS {row['scale']} - query")
        else:
            out["verdict"] = "NOT CALIBRATED - too few shared grid pairs" if len(implied) < 3 else "NOT CALIBRATED - grid pairs disagree"
        results.append(out)
        print(f"sheet {s:>3} {row['drawing']:<18} printed {row['scale']:<12} pairs {len(implied):>3}  -> {out['verdict']}"
              + (f" 1:{out['scale']} ({out['agree']})" if out.get("scale") else ""), flush=True)
    # write accepted results into calibration.jsonl so the log and printedscale.py see them
    jl = base / "output" / "calibration.jsonl"
    rows = [json.loads(l) for l in jl.read_text().splitlines() if l.strip()]
    got = {x["sheet"]: x for x in results if x["verdict"] == "CALIBRATED FROM GRIDS"}
    for r in rows:
        x = got.get(r["sheet"])
        if x and not (r.get("verdict") or "").startswith("CALIBRATED"):
            r["previous_verdict"] = r.get("verdict")
            r["verdict"] = (f"CALIBRATED FROM GRIDS - scale confirmed by {x['agree']} grid spacings "
                            "from calibrated plans (output/grid-table.json)")
            r["calibrated_scale"] = x["scale"]; r["grid_agree"] = x["agree"]
    jl.write_text("".join(json.dumps(r) + "\n" for r in rows))
    p = base / "output" / "grid-calibration.json"
    old = json.loads(p.read_text()) if p.exists() else {}
    old.update({str(x["sheet"]): x for x in results})
    p.write_text(json.dumps(old, indent=1))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("detect"); s.add_argument("pdf"); s.add_argument("-p", "--page", type=int, required=True); s.set_defaults(f=cmd_detect)
    s = sub.add_parser("learn"); s.add_argument("job"); s.set_defaults(f=cmd_learn)
    s = sub.add_parser("check"); s.add_argument("job"); s.add_argument("--sheets"); s.set_defaults(f=cmd_check)
    a = ap.parse_args(); a.f(a)


if __name__ == "__main__":
    main()
