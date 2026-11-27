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
# Drawing scales architects actually use. Anything else matching "1:n" is
# usually a ramp or fall gradient (1:4, 1:8, 1:14, 1:20 is ambiguous but kept).
STANDARD_SCALES = [1, 2, 5, 10, 20, 25, 50, 75, 100, 125, 150, 200, 250, 300,
                   400, 500, 750, 1000, 1250, 1500, 2000, 2500, 5000]


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
        if n not in seen and n in STANDARD_SCALES:
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
    try:
        import pymupdf  # same top-left page coordinates as render/calibrate
        doc = pymupdf.open(a.pdf)
        pg = doc[a.page - 1]
        clip = pymupdf.Rect(*parse_region(a.region)) if a.region else None
        if a.plain:
            print(pg.get_text("text", clip=clip, sort=True))
            return
        out = [{"text": w[4], "x0": w[0], "top": w[1], "x1": w[2], "bottom": w[3]}
               for w in pg.get_text("words", clip=clip, sort=True)]
        if emit(out, a.json):
            return
        for w in out:
            print(f"({w['x0']:7.1f},{w['top']:7.1f})-({w['x1']:7.1f},{w['bottom']:7.1f}) {w['text']}")
        return
    except ImportError:
        pass
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
    rx = re.compile(a.pattern, re.I)
    try:
        import pymupdf
        n_pages = len(pymupdf.open(a.pdf))
        get_words = lambda n: page_geometry(a.pdf, n, None, min_len=1e9)[2]
    except ImportError:
        pdf = pdfplumber.open(a.pdf)
        n_pages = len(pdf.pages)
        get_words = lambda n: words(pdf.pages[n - 1])
    pages = range(1, n_pages + 1) if a.page is None else [a.page]
    hits = []
    for n in pages:
        for w in get_words(n):
            if rx.search(w["text"]):
                hits.append({"page": n, "text": w["text"], "cx": round(w["cx"], 1),
                             "cy": round(w["cy"], 1), "upright": w["upright"]})
    if emit(hits, a.json):
        return
    for h in hits:
        print(f"p{h['page']:<4} ({h['cx']:7.1f},{h['cy']:7.1f})  {h['text']}")
    print(f"{len(hits)} hit(s)", file=sys.stderr)


def cmd_segments(a):
    region = parse_region(a.region)
    if a.near:
        x, y = parse_point(a.near)
        r = a.radius
        region = (x - r, y - r, x + r, y + r)
    _, segs, _ = page_geometry(a.pdf, a.page, region, min_len=a.min_len)
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


def _mupdf_geometry(pdf_path, page_no, region, min_len):
    """Fast path for heavy sheets (hundreds of thousands of paths)."""
    import pymupdf
    doc = pymupdf.open(pdf_path)
    p = doc[page_no - 1]
    txt = p.get_text()
    scales = []
    for f in SCALE_RE.findall(txt):
        if int(f) not in scales and int(f) in STANDARD_SCALES:
            scales.append(int(f))
    segs = []
    for d in p.get_drawings():
        for it in d["items"]:
            kind = it[0]
            if kind == "l":
                pts = [it[1], it[2]]
            elif kind == "re":
                r = it[1]
                pts = [r.tl, r.tr, r.br, r.bl, r.tl]
            elif kind == "qu":
                q = it[1]
                pts = [q.ul, q.ur, q.lr, q.ll, q.ul]
            else:
                continue
            for A, B in zip(pts, pts[1:]):
                L = math.hypot(B.x - A.x, B.y - A.y)
                if L < min_len:
                    continue
                mx, my = (A.x + B.x) / 2, (A.y + B.y) / 2
                if region and not any(in_region(px, py, region)
                                      for px, py in ((A.x, A.y), (B.x, B.y), (mx, my))):
                    continue
                segs.append({"x0": A.x, "y0": A.y, "x1": B.x, "y1": B.y, "len_pt": L,
                             "angle": math.degrees(math.atan2(B.y - A.y, B.x - A.x)) % 180,
                             "src": kind})
    ws = []
    for b in p.get_text("dict")["blocks"]:
        if b.get("type") != 0:
            continue
        for ln in b["lines"]:
            for sp in ln["spans"]:
                t = sp["text"].strip()
                if not t:
                    continue
                x0, y0, x1, y1 = sp["bbox"]
                cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
                if not in_region(cx, cy, region):
                    continue
                dx, dy = ln["dir"]
                ws.append({"text": t, "cx": cx, "cy": cy, "size": sp["size"],
                           "upright": abs(dx) >= abs(dy),
                           "angle": math.degrees(math.atan2(dy, dx)) % 180})
    return scales, segs, ws


def _plumber_geometry(pdf_path, page_no, region, min_len):
    pdf, p = open_page(pdf_path, page_no)
    return detect_scales(p), get_segments(p, region, min_len=min_len), words(p, region)


def page_geometry(pdf_path, page_no, region, min_len=8.0):
    try:
        import pymupdf  # noqa: F401
        return _mupdf_geometry(pdf_path, page_no, region, min_len)
    except ImportError:
        return _plumber_geometry(pdf_path, page_no, region, min_len)


def _index_segments(segs):
    """Split into near-horizontal / near-vertical lists sorted by their constant
    coordinate, so each dimension string only tests nearby lines."""
    import bisect
    hor, ver = [], []
    CELL = 40.0
    grid = {}
    for s in segs:
        a = s["angle"]
        if min(a, 180 - a) <= 3:
            hor.append(((s["y0"] + s["y1"]) / 2, s))
        elif abs(a - 90) <= 3:
            ver.append(((s["x0"] + s["x1"]) / 2, s))
        elif s["len_pt"] >= 8.0:
            # angled segment (skewed buildings): register it in every grid cell it crosses
            n = max(1, int(s["len_pt"] / (CELL / 2)))
            seen = set()
            for i in range(n + 1):
                x = s["x0"] + (s["x1"] - s["x0"]) * i / n
                y = s["y0"] + (s["y1"] - s["y0"]) * i / n
                key = (int(x // CELL), int(y // CELL))
                if key not in seen:
                    seen.add(key); grid.setdefault(key, []).append(s)
    hor.sort(key=lambda t: t[0]); ver.sort(key=lambda t: t[0])
    hk = [t[0] for t in hor]; vk = [t[0] for t in ver]

    def near(upright, cx, cy, tol, angle=None):
        if angle is not None and min(angle, 180 - angle) > 3 and abs(angle - 90) > 3:
            out, seen = [], set()
            r = int(tol // CELL) + 1
            gx, gy = int(cx // CELL), int(cy // CELL)
            for ix in range(gx - r, gx + r + 1):
                for iy in range(gy - r, gy + r + 1):
                    for s2 in grid.get((ix, iy), ()):
                        if id(s2) not in seen:
                            seen.add(id(s2)); out.append(s2)
            return out
        keys, items, c = (hk, hor, cy) if upright else (vk, ver, cx)
        lo, hi = bisect.bisect_left(keys, c - tol), bisect.bisect_right(keys, c + tol)
        return [items[i][1] for i in range(lo, hi)]

    def crossers(horizontal_line, lo_key, hi_key, at, tol=1.0):
        """Perpendicular segments whose constant coordinate lies in [lo, hi]
        and which pass through `at` (the dimension line's own coordinate)."""
        keys, items = (vk, ver) if horizontal_line else (hk, hor)
        i0, i1 = bisect.bisect_left(keys, lo_key), bisect.bisect_right(keys, hi_key)
        spans = {}
        for i in range(i0, i1):
            k, s2 = items[i]
            a0, a1 = ((s2["y0"], s2["y1"]) if horizontal_line else (s2["x0"], s2["x1"]))
            lo_, hi_ = min(a0, a1), max(a0, a1)
            if lo_ - tol <= at <= hi_ + tol:
                kk = round(k * 2) / 2          # merge collinear pieces of one witness line
                cur = spans.get(kk)
                spans[kk] = (min(lo_, cur[0]), max(hi_, cur[1])) if cur else (lo_, hi_)
        # a witness line crosses the dimension line: it extends past it on both sides
        return [k for k, (lo_, hi_) in spans.items() if lo_ < at - 0.7 and hi_ > at + 0.7]
    near.crossers = crossers
    allgrid = {}

    def all_near(x, y, r):
        if not allgrid:
            for s2 in segs:
                for px, py in ((s2["x0"], s2["y0"]), (s2["x1"], s2["y1"]),
                               ((s2["x0"] + s2["x1"]) / 2, (s2["y0"] + s2["y1"]) / 2)):
                    allgrid.setdefault((int(px // 20), int(py // 20)), []).append(s2)
        out, seen = [], set()
        k = int(r // 20) + 1
        for ix in range(int(x // 20) - k, int(x // 20) + k + 1):
            for iy in range(int(y // 20) - k, int(y // 20) + k + 1):
                for s2 in allgrid.get((ix, iy), ()):
                    if id(s2) not in seen:
                        seen.add(id(s2)); out.append(s2)
        return out
    near.all_near = all_near
    return near


def tick_length(near, s):
    """Angled dimension (radius, diameter, skewed grid): measure between the tick
    marks or crossing lines nearest each end, instead of the whole drawn line,
    which runs past the ticks. Falls back to the segment length."""
    x0, y0, x1, y1, L = s["x0"], s["y0"], s["x1"], s["y1"], s["len_pt"]
    dx, dy = (x1 - x0) / L, (y1 - y0) / L
    best = {0: None, 1: None}
    for end, (ex, ey) in enumerate(((x0, y0), (x1, y1))):
        for s2 in near.all_near(ex, ey, max(3.0, 0.08 * L)):
            if s2 is s or s2["len_pt"] > 0.5 * L:
                continue
            a2 = abs(((s2["angle"] - s["angle"]) % 180))
            if min(a2, 180 - a2) < 20:           # must cross, not run along
                continue
            # intersection of s2 with the dimension line
            ux, uy = s2["x1"] - s2["x0"], s2["y1"] - s2["y0"]
            den = dx * uy - dy * ux
            if abs(den) < 1e-9:
                continue
            t = ((s2["x0"] - x0) * uy - (s2["y0"] - y0) * ux) / den      # along s, in pt
            u = ((s2["x0"] - x0) * dy - (s2["y0"] - y0) * dx) / den      # along s2, 0..1
            if not (-0.05 <= u <= 1.05):
                continue
            target = 0.0 if end == 0 else L
            if abs(t - target) <= max(3.0, 0.08 * L):
                if best[end] is None or abs(t - target) < abs(best[end] - target):
                    best[end] = t
    if best[0] is not None and best[1] is not None and best[1] - best[0] > 0.5 * L:
        return best[1] - best[0], True
    return L, False


def witness_length(near, s):
    """Distance between the witness (extension) lines at each end of a matched
    dimension line. Revit and ArchiCAD draw the dimension line a little past its
    witness lines, so the drawn segment overstates the dimension. Falls back to
    the segment length when no witness line is found near both ends."""
    horizontal = min(s["angle"], 180 - s["angle"]) <= 3
    if not horizontal and abs(s["angle"] - 90) > 3:
        return tick_length(near, s)
    if horizontal:
        a, b, at = sorted((s["x0"], s["x1"])) + [(s["y0"] + s["y1"]) / 2]
    else:
        a, b, at = sorted((s["y0"], s["y1"])) + [(s["x0"] + s["x1"]) / 2]
    L = b - a
    slack = max(0.06 * L, 2.0)
    ks = near.crossers(horizontal, a - 0.5, b + 0.5, at)
    left = [k for k in ks if a - 0.5 <= k <= a + slack]
    right = [k for k in ks if b - slack <= k <= b + 0.5]
    if left and right:
        w = max(right) - min(left)
        # outermost witness pair inside the line ends
        w = min(right, key=lambda k: abs(k - b)) - min(left, key=lambda k: abs(k - a))
        if w > 0.5 * L:
            return w, True
    return L, False


def _closed_box(near, w, s, offs, th):
    """Short sides at both ends of segment s, no longer than the box height:
    the outline of a tag, not the long witness lines of a dimension."""
    import math as _m
    ux, uy = (s["x1"] - s["x0"]) / s["len_pt"], (s["y1"] - s["y0"]) / s["len_pt"]
    caps = 0
    for ex, ey in ((s["x0"], s["y0"]), (s["x1"], s["y1"])):
        found = False
        for s3 in near(not w["upright"], ex, ey, 4.0, (s["angle"] + 90) % 180):
            da = abs(((s3["angle"] - s["angle"]) % 180) - 90)
            if da > 2 or s3["len_pt"] > offs + th:
                continue
            for px, py in ((s3["x0"], s3["y0"]), (s3["x1"], s3["y1"])):
                along = (px - ex) * ux + (py - ey) * uy
                if abs(along) < 4.0 and _m.hypot(px - ex, py - ey) < offs + th:
                    found = True
            if found:
                break
        caps += found
    return caps == 2


def find_viewports(matches, tol, min_agree):
    """Sheets often carry several viewports at different scales (plan 1:50,
    elevations 1:20, a key plan 1:500). Group the matched dimensions by the
    standard scale they agree with; a group is accepted as a viewport when it has
    at least `min_agree` members and they make up >= 65% of all matched
    dimensions inside the group's own bounding box (so two scales sharing one
    area are refused)."""
    found = []
    for sc in STANDARD_SCALES:
        grp = [m for m in matches if abs(m["implied_scale"] / sc - 1) <= tol]
        if len(grp) < max(3, min_agree):
            continue
        xs = [m["text_xy"][0] for m in grp]; ys = [m["text_xy"][1] for m in grp]
        box = (min(xs) - 30, min(ys) - 30, max(xs) + 30, max(ys) + 30)
        inside = [m for m in matches if box[0] <= m["text_xy"][0] <= box[2] and box[1] <= m["text_xy"][1] <= box[3]]
        if len(grp) >= 0.65 * len(inside):
            found.append({"scale": sc, "region": [round(v) for v in box], "agree": len(grp), "of": len(inside)})
    return found


def cmd_calibrate(a):
    region = parse_region(a.region)
    # short lines are kept so witness lines (often ~2 mm) can be found;
    # the dimension line itself must still be >= 8 pt
    page_scales, segs, all_words = page_geometry(a.pdf, a.page, region, min_len=1.5)
    scales = [a.scale] if a.scale else page_scales
    ws = [w for w in all_words if DIM_RE.match(w["text"])]
    ws = [w for w in ws if int(w["text"]) >= a.min_value]
    if not a.region and segs:
        # ignore the title block strip along the bottom of the sheet (project numbers, dates)
        page_h = max(max(sg["y0"], sg["y1"]) for sg in segs)
        ws = [w for w in ws if w["cy"] < page_h * 0.93]
    near = _index_segments(segs)
    tag_words = all_words

    matches = []
    for w in ws:
        printed = int(w["text"])
        want_angle = w.get("angle", 0.0 if w["upright"] else 90.0)
        th = max(w["size"], 1.0)
        best = None
        for s in near(w["upright"], w["cx"], w["cy"], th * 2.0, want_angle):
            if s["len_pt"] < 8.0:
                continue
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
                # a tag box (e.g. ceiling type "CL-000 / 3080") has a line of the
                # same length on the far side of the text; a dimension line doesn't
                side = (w["cx"] - ax) * dy - (w["cy"] - ay) * dx
                boxed = False
                if not boxed:
                    # text centred on the other side of the same line: a two-line tag
                    for w2 in tag_words:
                        if w2 is w or DIM_RE.match(w2["text"]) or not re.search(r"[A-Za-z]", w2["text"]):
                            continue
                        t3 = ((w2["cx"] - ax) * dx + (w2["cy"] - ay) * dy) / (L * L)
                        side3 = (w2["cx"] - ax) * dy - (w2["cy"] - ay) * dx
                        if abs(t3 - 0.5) < 0.15 and side * side3 < 0 and abs(side3) / L < th * 1.6:
                            boxed = True
                            break
                if boxed:
                    continue
            if best is None or score < best[0]:
                best = (score, s, perp, t)
        if best:
            _, s, perp, t = best
            wl, used_witness = witness_length(near, s)
            axis = min(s["angle"], 180 - s["angle"]) <= 3 or abs(s["angle"] - 90) <= 3
            if axis and not used_witness:
                continue    # a box edge or tick mark next to a number, not a dimension line
            paper_mm = wl * PT_TO_MM
            matches.append({"printed": printed, "text_xy": (round(w["cx"], 1), round(w["cy"], 1)),
                            "seg": (round(s["x0"], 1), round(s["y0"], 1),
                                    round(s["x1"], 1), round(s["y1"], 1)),
                            "paper_mm": paper_mm, "implied_scale": printed / paper_mm,
                            "witness": used_witness})

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
    viewports = find_viewports(matches, a.tol, a.min_agree) if not a.region else []
    report["viewports"] = viewports
    if len(matches) < a.min_agree:
        report["verdict"] = "NO DIMENSIONS - too few printed dimensions to check the scale"
    elif len(scales) > 1 and viewports:
        report["verdict"] = "CALIBRATED BY VIEWPORT - measure only inside the listed regions"
    elif len(scales) > 1:
        report["verdict"] = ("MULTIPLE SCALES - not calibrated; re-run per viewport "
                             "with --region and --scale")
    elif best and best["agree"] >= a.min_agree and best["agree"] >= 0.5 * len(matches):
        report["verdict"] = "CALIBRATED"
        report["calibrated_scale"] = best["scale"]
    elif not scales and implied:
        # "As indicated" sheets print no scale. Test every standard scale against
        # the printed dimensions; accept one only on the same agreement rule.
        trial = []
        for sc in STANDARD_SCALES:
            ok = sum(1 for m in matches if abs(m["implied_scale"] / sc - 1) <= a.tol)
            trial.append((ok, sc))
        ok, sc = max(trial)
        if ok >= max(a.min_agree, 5) and ok >= 0.5 * len(matches):
            report["verdict"] = "CALIBRATED - scale inferred from printed dimensions (none printed)"
            report["calibrated_scale"] = sc
            report["by_scale"] = [{"scale": sc, "agree": ok, "of": len(matches), "inferred": True}]
        else:
            report["verdict"] = "NO SCALE STRING - scale inferred only, NOT verified"
    elif viewports:
        report["verdict"] = "CALIBRATED BY VIEWPORT - measure only inside the listed regions"
    else:
        report["verdict"] = "UNRELIABLE - do not measure from geometry on this sheet/region"
    if report["verdict"].startswith("NO SCALE STRING") and viewports:
        report["verdict"] = "CALIBRATED BY VIEWPORT - measure only inside the listed regions"
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
    for v in report.get("viewports") or []:
        print(f"viewport 1:{v['scale']}  region {','.join(map(str, v['region']))}  {v['agree']}/{v['of']} agree")
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
