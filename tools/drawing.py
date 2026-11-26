#!/usr/bin/env python3
"""
drawing.py - read, scale and measure vector PDF drawings.

All coordinates are PDF points (1 pt = 1/72 inch) measured from the TOP-LEFT
corner of the page, x to the right, y downwards. The same system is used by
`render` (which can overlay a labelled grid), so a location seen on a rendered
image can be passed straight to `segments`, `measure` or `calibrate`.

Paper -> real conversion:  real_mm = length_pt * 25.4 / 72 * scale_denominator

Subcommands
  info       sheet size, rotation, scale strings, vector/scan check, title text
  text       dump words with coordinates (optionally inside a region)
  find       locate text matching a regex (door tags, room names, dims ...)
  segments   list vector line segments near a point / inside a region
  measure    real-world distance between two points at a given scale
  calibrate  check the scale against printed dimension strings  (REQUIRED
             before any geometry-based measurement is relied on)
  render     render a page or region to PNG, optionally with a coordinate grid
"""
import argparse
import json
import math
import re
import statistics
import sys

import pdfplumber

PT_TO_MM = 25.4 / 72.0

ISO_SIZES = {  # mm, portrait
    "A0": (841, 1189), "A1": (594, 841), "A2": (420, 594),
    "A3": (297, 420), "A4": (210, 297), "B1": (707, 1000),
}

SCALE_RE = re.compile(r"(?<![\d.])1\s*:\s*(\d{1,4})(?![\d.])")


# ----------------------------------------------------------------- helpers
def parse_region(s):
    if not s:
        return None
    v = [float(x) for x in s.split(",")]
    if len(v) != 4:
        raise SystemExit("region must be x0,y0,x1,y1 in PDF points")
    x0, y0, x1, y1 = v
    return (min(x0, x1), min(y0, y1), max(x0, x1), max(y0, y1))


def parse_point(s):
    v = [float(x) for x in s.split(",")]
    if len(v) != 2:
        raise SystemExit("point must be x,y in PDF points")
    return tuple(v)


def open_page(pdf_path, page_no):
    pdf = pdfplumber.open(pdf_path)
    if page_no < 1 or page_no > len(pdf.pages):
        raise SystemExit(f"page {page_no} out of range (1..{len(pdf.pages)})")
    return pdf, pdf.pages[page_no - 1]


def paper_size(w_pt, h_pt):
    w, h = w_pt * PT_TO_MM, h_pt * PT_TO_MM
    lo, hi = sorted((w, h))
    for name, (a, b) in ISO_SIZES.items():
        if abs(lo - a) < 6 and abs(hi - b) < 6:
            return name, w, h
    return "non-standard", w, h


def in_region(x, y, region):
    if region is None:
        return True
    x0, y0, x1, y1 = region
    return x0 <= x <= x1 and y0 <= y <= y1


def get_segments(page, region=None, min_len=0.0):
    """All straight segments from lines, rect edges and polyline curves."""
    segs = []

    def add(x0, y0, x1, y1, src):
        L = math.hypot(x1 - x0, y1 - y0)
        if L < max(min_len, 1e-6):
            return
        mx, my = (x0 + x1) / 2, (y0 + y1) / 2
        if region is not None:
            rx0, ry0, rx1, ry1 = region
            # keep if either end or midpoint is inside the region
            if not any(in_region(px, py, region) for px, py in
                       ((x0, y0), (x1, y1), (mx, my))):
                return
        segs.append({"x0": x0, "y0": y0, "x1": x1, "y1": y1, "len_pt": L,
                     "angle": math.degrees(math.atan2(y1 - y0, x1 - x0)) % 180,
                     "src": src})

    for ln in page.lines:
        pts = ln.get("pts") or [(ln["x0"], ln["top"]), (ln["x1"], ln["bottom"])]
        for (ax, ay), (bx, by) in zip(pts, pts[1:]):
            add(ax, ay, bx, by, "line")
    for r in page.rects:
        x0, x1, t, b = r["x0"], r["x1"], r["top"], r["bottom"]
        for e in ((x0, t, x1, t), (x1, t, x1, b), (x1, b, x0, b), (x0, b, x0, t)):
            add(*e, "rect")
    for c in page.curves:
        pts = c.get("pts") or []
        for (ax, ay), (bx, by) in zip(pts, pts[1:]):
            add(ax, ay, bx, by, "curve")
    return segs


def words(page, region=None):
    ws = page.extract_words(keep_blank_chars=False, use_text_flow=False,
                            extra_attrs=["upright", "size"])
    out = []
    rot_chars = [c for c in page.chars if not c.get("upright", True)]
    for w in ws:
        cx, cy = (w["x0"] + w["x1"]) / 2, (w["top"] + w["bottom"]) / 2
        if not w["upright"] and rot_chars:
            # Rebuild rotated text in reading order. Text rotated 90deg CCW
            # (matrix b > 0) reads bottom-to-top; 90deg CW reads top-to-bottom.
            cs = [c for c in rot_chars
                  if w["x0"] - 0.5 <= c["x0"] <= w["x1"] + 0.5
                  and w["top"] - 0.5 <= c["top"] <= w["bottom"] + 0.5]
            if cs:
                b = cs[0].get("matrix", (1, 0, 0, 1, 0, 0))[1]
                cs.sort(key=lambda c: c["top"], reverse=(b > 0))
                w["text"] = "".join(c["text"] for c in cs)
        if in_region(cx, cy, region):
            w["cx"], w["cy"] = cx, cy
            out.append(w)
    return out


def detect_scales(page):
    txt = page.extract_text() or ""
    found = SCALE_RE.findall(txt)
    seen = []
    for f in found:
        n = int(f)
        if n not in seen and n >= 1:
            seen.append(n)
    return seen


def pt_dist_to_seg(px, py, s):
    ax, ay, bx, by = s["x0"], s["y0"], s["x1"], s["y1"]
    dx, dy = bx - ax, by - ay
    L2 = dx * dx + dy * dy
    t = 0 if L2 == 0 else max(0, min(1, ((px - ax) * dx + (py - ay) * dy) / L2))
    qx, qy = ax + t * dx, ay + t * dy
    return math.hypot(px - qx, py - qy)


def emit(obj, as_json):
    if as_json:
        print(json.dumps(obj, indent=2, default=float))
        return True
    return False


# ----------------------------------------------------------------- commands
def cmd_info(a):
    pdf = pdfplumber.open(a.pdf)
    pages = range(1, len(pdf.pages) + 1) if a.page is None else [a.page]
    results = []
    for n in pages:
        p = pdf.pages[n - 1]
        size, wmm, hmm = paper_size(p.width, p.height)
        nchars = len(p.chars)
        segs = get_segments(p)
        nimg = len(p.images)
        img_cover = 0.0
        for im in p.images:
            img_cover += max(0, im["x1"] - im["x0"]) * max(0, im["bottom"] - im["top"])
        img_cover /= (p.width * p.height)
        if nchars == 0 and len(segs) < 20 and nimg:
            kind = "SCAN/RASTER - geometry measurement NOT possible"
        elif img_cover > 0.6 and len(segs) < 200:
            kind = "MOSTLY RASTER - treat measurements as unverifiable"
        else:
            kind = "vector"
        # title block guess: text in bottom-right 30% x 25%
        tb_region = (p.width * 0.70, p.height * 0.75, p.width, p.height)
        tb = " ".join(w["text"] for w in words(p, tb_region))
        results.append({
            "page": n, "paper": size, "w_mm": round(wmm), "h_mm": round(hmm),
            "w_pt": round(p.width, 1), "h_pt": round(p.height, 1),
            "rotation": p.rotation if hasattr(p, "rotation") else 0,
            "chars": nchars, "segments": len(segs), "images": nimg,
            "image_cover": round(img_cover, 2), "kind": kind,
            "scales_found": detect_scales(p),
            "title_block_text": tb[:400],
        })
    if emit(results, a.json):
        return
    for r in results:
        print(f"--- page {r['page']}: {r['paper']} {r['w_mm']}x{r['h_mm']} mm "
              f"({r['w_pt']}x{r['h_pt']} pt) rot={r['rotation']}")
        print(f"    content: {r['kind']}  chars={r['chars']} segments={r['segments']} "
              f"images={r['images']} (cover {r['image_cover']})")
        print(f"    scale strings: {', '.join('1:'+str(s) for s in r['scales_found']) or 'none found'}")
        print(f"    title block (bottom-right guess): {r['title_block_text']}")


def cmd_text(a):
    pdf, p = open_page(a.pdf, a.page)
    ws = words(p, parse_region(a.region))
    if emit([{k: w[k] for k in ("text", "x0", "top", "x1", "bottom", "upright", "size")}
             for w in ws], a.json):
        return
    if a.plain:
        print(p.within_bbox(parse_region(a.region)).extract_text()
              if a.region else p.extract_text())
        return
    for w in ws:
        o = "" if w["upright"] else " [rotated]"
        print(f"({w['x0']:7.1f},{w['top']:7.1f})-({w['x1']:7.1f},{w['bottom']:7.1f}) "
              f"h={w['size']:.1f} {w['text']}{o}")


def cmd_find(a):
    pdf = pdfplumber.open(a.pdf)
    rx = re.compile(a.pattern, re.I)
    pages = range(1, len(pdf.pages) + 1) if a.page is None else [a.page]
    hits = []
    for n in pages:
        for w in words(pdf.pages[n - 1]):
            if rx.search(w["text"]):
                hits.append({"page": n, "text": w["text"], "cx": round(w["cx"], 1),
                             "cy": round(w["cy"], 1), "upright": w["upright"]})
    if emit(hits, a.json):
        return
    for h in hits:
        print(f"p{h['page']:<4} ({h['cx']:7.1f},{h['cy']:7.1f})  {h['text']}")
    print(f"{len(hits)} hit(s)", file=sys.stderr)


def cmd_segments(a):
    pdf, p = open_page(a.pdf, a.page)
    region = parse_region(a.region)
    if a.near:
        x, y = parse_point(a.near)
        r = a.radius
        region = (x - r, y - r, x + r, y + r)
    segs = get_segments(p, region, a.min_len)
    if a.near:
        x, y = parse_point(a.near)
        for s in segs:
            s["dist"] = pt_dist_to_seg(x, y, s)
        segs.sort(key=lambda s: s["dist"])
    else:
        segs.sort(key=lambda s: -s["len_pt"])
    segs = segs[: a.limit]
    for s in segs:
        if a.scale:
            s["real_mm"] = s["len_pt"] * PT_TO_MM * a.scale
    if emit(segs, a.json):
        return
    for s in segs:
        extra = f"  real={s['real_mm']:.0f}mm" if a.scale else ""
        d = f"  d={s['dist']:.1f}" if "dist" in s else ""
        print(f"({s['x0']:7.1f},{s['y0']:7.1f})->({s['x1']:7.1f},{s['y1']:7.1f}) "
              f"len={s['len_pt']:7.2f}pt ang={s['angle']:5.1f}{extra}{d} [{s['src']}]")


def cmd_measure(a):
    (x0, y0), (x1, y1) = parse_point(a.p1), parse_point(a.p2)
    L = math.hypot(x1 - x0, y1 - y0)
    mm = L * PT_TO_MM * a.scale
    out = {"len_pt": L, "paper_mm": L * PT_TO_MM, "scale": a.scale, "real_mm": mm,
           "dx_real_mm": abs(x1 - x0) * PT_TO_MM * a.scale,
           "dy_real_mm": abs(y1 - y0) * PT_TO_MM * a.scale,
           "note": "Only valid if this sheet/viewport passed `calibrate` at this scale."}
    if emit(out, a.json):
        return
    print(f"paper {L:.2f} pt = {L*PT_TO_MM:.2f} mm  ->  at 1:{a.scale:g} = {mm:.0f} mm "
          f"(dx {out['dx_real_mm']:.0f}, dy {out['dy_real_mm']:.0f})")
    print(out["note"])


DIM_RE = re.compile(r"^\d{2,6}$")


def cmd_calibrate(a):
    pdf, p = open_page(a.pdf, a.page)
    region = parse_region(a.region)
    scales = [a.scale] if a.scale else detect_scales(p)
    segs = get_segments(p, region, min_len=8.0)
    ws = [w for w in words(p, region) if DIM_RE.match(w["text"])]
    ws = [w for w in ws if int(w["text"]) >= a.min_value]

    matches = []
    for w in ws:
        printed = int(w["text"])
        want_angle = 0.0 if w["upright"] else 90.0
        th = max(w["size"], 1.0)
        best = None
        for s in segs:
            da = abs(s["angle"] - want_angle)
            da = min(da, 180 - da)
            if da > 3:
                continue
            # perpendicular distance of text centre from the infinite line,
            # and whether the text centre projects inside the segment
            ax, ay, bx, by = s["x0"], s["y0"], s["x1"], s["y1"]
            dx, dy = bx - ax, by - ay
            L = s["len_pt"]
            t = ((w["cx"] - ax) * dx + (w["cy"] - ay) * dy) / (L * L)
            if t < 0.05 or t > 0.95:
                continue
            perp = abs((w["cx"] - ax) * dy - (w["cy"] - ay) * dx) / L
            if perp > th * 2.0:
                continue
            # dimension text sits roughly mid-span; prefer central + close
            score = perp + abs(t - 0.5) * th * 4
            if best is None or score < best[0]:
                best = (score, s, perp, t)
        if best:
            _, s, perp, t = best
            paper_mm = s["len_pt"] * PT_TO_MM
            matches.append({"printed": printed, "text_xy": (round(w["cx"], 1), round(w["cy"], 1)),
                            "seg": (round(s["x0"], 1), round(s["y0"], 1),
                                    round(s["x1"], 1), round(s["y1"], 1)),
                            "paper_mm": paper_mm, "implied_scale": printed / paper_mm})

    report = {"page": a.page, "region": region, "scales_on_sheet": scales,
              "dimension_texts": len(ws), "matched": len(matches)}

    implied = [m["implied_scale"] for m in matches]
    verdicts = []
    for sc in scales:
        ok = [m for m in matches if abs(m["implied_scale"] / sc - 1) <= a.tol]
        verdicts.append({"scale": sc, "agree": len(ok), "of": len(matches)})
    report["by_scale"] = verdicts
    if implied:
        report["median_implied_scale"] = statistics.median(implied)

    best = max(verdicts, key=lambda v: v["agree"]) if verdicts else None
    if len(scales) > 1:
        report["verdict"] = ("MULTIPLE SCALES - not calibrated; re-run per viewport "
                             "with --region and --scale")
    elif best and best["agree"] >= a.min_agree and best["agree"] >= 0.5 * len(matches):
        report["verdict"] = "CALIBRATED"
        report["calibrated_scale"] = best["scale"]
    elif not scales and implied:
        report["verdict"] = "NO SCALE STRING - scale inferred only, NOT verified"
    else:
        report["verdict"] = "UNRELIABLE - do not measure from geometry on this sheet/region"
    if len(scales) > 1:
        report["warning"] = ("Multiple scales on sheet: calibrate each viewport separately "
                             "using --region and --scale.")
    report["matches"] = matches
    if len(scales) == 1:
        report["mismatches"] = [m for m in matches
                                if abs(m["implied_scale"] / scales[0] - 1) > a.tol]

    if emit(report, a.json):
        return
    print(f"page {a.page}  region={region or 'whole sheet'}  scales on sheet: "
          f"{', '.join('1:'+str(s) for s in scales) or 'none'}")
    print(f"dimension strings found: {len(ws)}   matched to a dimension line: {len(matches)}")
    for m in matches[: a.show]:
        flag = ""
        if scales:
            nearest = min(scales, key=lambda sc: abs(m["implied_scale"] / sc - 1))
            flag = "  OK" if abs(m["implied_scale"] / nearest - 1) <= a.tol else "  MISMATCH"
        print(f"  printed {m['printed']:>6} mm  @({m['text_xy'][0]:.0f},{m['text_xy'][1]:.0f})  "
              f"paper {m['paper_mm']:7.2f} mm  -> implied 1:{m['implied_scale']:.1f}{flag}")
    for v in verdicts:
        print(f"scale 1:{v['scale']}: {v['agree']}/{v['of']} matches within ±{a.tol*100:.0f}%")
    if "median_implied_scale" in report:
        print(f"median implied scale 1:{report['median_implied_scale']:.1f}")
    if "warning" in report:
        print("WARNING:", report["warning"])
    if report.get("mismatches"):
        print(f"NOTE: {len(report['mismatches'])} dimension(s) disagree with the drawn geometry "
              "(overridden dimension text, NTS element, or another viewport). Trust the "
              "printed figure, but record the discrepancy.")
    print("VERDICT:", report["verdict"],
          f"(1:{report['calibrated_scale']})" if "calibrated_scale" in report else "")


def cmd_render(a):
    import pypdfium2 as pdfium
    from PIL import ImageDraw, ImageFont

    doc = pdfium.PdfDocument(a.pdf)
    page = doc[a.page - 1]
    k = a.dpi / 72.0
    img = page.render(scale=k).to_pil().convert("RGB")
    region = parse_region(a.region)
    ox, oy = 0.0, 0.0
    if region:
        x0, y0, x1, y1 = region
        img = img.crop((int(x0 * k), int(y0 * k), int(x1 * k), int(y1 * k)))
        ox, oy = x0, y0
    if a.grid:
        d = ImageDraw.Draw(img)
        try:
            font = ImageFont.load_default(size=max(10, int(a.dpi / 9)))
        except TypeError:
            font = ImageFont.load_default()
        W, H = img.size
        g = a.grid
        start_x = math.ceil(ox / g) * g
        start_y = math.ceil(oy / g) * g
        x = start_x
        while (x - ox) * k < W:
            px = (x - ox) * k
            d.line([(px, 0), (px, H)], fill=(255, 0, 255), width=1)
            d.text((px + 2, 2), f"{x:g}", fill=(200, 0, 200), font=font)
            x += g
        y = start_y
        while (y - oy) * k < H:
            py = (y - oy) * k
            d.line([(0, py), (W, py)], fill=(0, 160, 255), width=1)
            d.text((2, py + 2), f"{y:g}", fill=(0, 120, 220), font=font)
            y += g
    if img.width * img.height > a.max_pixels:
        f = math.sqrt(a.max_pixels / (img.width * img.height))
        img = img.resize((int(img.width * f), int(img.height * f)))
        print(f"downsized by {f:.2f} to stay under {a.max_pixels} px; "
              f"use --region to zoom instead", file=sys.stderr)
    img.save(a.out)
    print(f"wrote {a.out} ({img.width}x{img.height}px)"
          + (f", grid every {a.grid:g} pt (labels = PDF pt, top-left origin)" if a.grid else ""))


# ----------------------------------------------------------------- CLI
def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    def common(sp, page_required=True):
        sp.add_argument("pdf")
        if page_required:
            sp.add_argument("--page", "-p", type=int, required=True, help="1-based page")
        else:
            sp.add_argument("--page", "-p", type=int, help="1-based page (default all)")
        sp.add_argument("--json", action="store_true")

    s = sub.add_parser("info"); common(s, False); s.set_defaults(f=cmd_info)

    s = sub.add_parser("text"); common(s)
    s.add_argument("--region", help="x0,y0,x1,y1 pt")
    s.add_argument("--plain", action="store_true", help="flowing text instead of word boxes")
    s.set_defaults(f=cmd_text)

    s = sub.add_parser("find"); common(s, False)
    s.add_argument("pattern", help="regex, case-insensitive")
    s.set_defaults(f=cmd_find)

    s = sub.add_parser("segments"); common(s)
    s.add_argument("--region"); s.add_argument("--near", help="x,y pt")
    s.add_argument("--radius", type=float, default=30.0)
    s.add_argument("--min-len", type=float, default=2.0)
    s.add_argument("--scale", type=float, help="denominator, e.g. 100 for 1:100")
    s.add_argument("--limit", type=int, default=40)
    s.set_defaults(f=cmd_segments)

    s = sub.add_parser("measure")
    s.add_argument("p1"); s.add_argument("p2")
    s.add_argument("--scale", type=float, required=True)
    s.add_argument("--json", action="store_true")
    s.set_defaults(f=cmd_measure)

    s = sub.add_parser("calibrate"); common(s)
    s.add_argument("--scale", type=float, help="override scale (else read from sheet)")
    s.add_argument("--region", help="limit to one viewport x0,y0,x1,y1 pt")
    s.add_argument("--tol", type=float, default=0.02, help="agreement tolerance (0.02 = 2%%)")
    s.add_argument("--min-agree", type=int, default=3)
    s.add_argument("--min-value", type=int, default=100, help="ignore dims below this (mm)")
    s.add_argument("--show", type=int, default=25)
    s.set_defaults(f=cmd_calibrate)

    s = sub.add_parser("render"); common(s)
    s.add_argument("--out", "-o", required=True)
    s.add_argument("--dpi", type=float, default=100)
    s.add_argument("--region")
    s.add_argument("--grid", type=float, help="grid spacing in pt, e.g. 50")
    s.add_argument("--max-pixels", type=int, default=40_000_000)
    s.set_defaults(f=cmd_render)

    a = ap.parse_args()
    a.f(a)


if __name__ == "__main__":
    main()
