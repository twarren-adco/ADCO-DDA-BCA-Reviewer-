#!/usr/bin/env python3
"""
sheetindex.py - one row per original sheet for a restored job (fast: text and
object stats only, no geometry). Uses source_manifest.json to map chunk PDFs
back to original sheet numbers.

  python3 tools/sheetindex.py <job>          -> output/sheet-index.json + sheet-index.md
"""
import json, pathlib, re, sys
import pymupdf

ROOT = pathlib.Path(__file__).resolve().parent.parent
DWG = re.compile(r"\b([A-Z]{2,4}-[A-Z]{1,3}-[A-Z]{1,3}-\d{3,4}[A-Z]?|[A-Z]{1,3}-?\d{3,4}[A-Z]?)\b")
SCALE = re.compile(r"((?:1\s*:\s*\d+(?:\s*,\s*1\s*:\s*\d+)*)|As indicated|NTS)\s*@\s*(A\d)", re.I)
REV = re.compile(r"@\s*A\d\s*SIZE\s+([A-Z]\d{1,2})\s+(\d{2}/\d{2}/\d{2})")


def title_block(page):
    w, h = page.rect.width, page.rect.height
    clip = pymupdf.Rect(w * 0.55, h * 0.80, w, h)
    return " ".join(page.get_text("text", clip=clip).split())


def classify(page):
    area = page.rect.width * page.rect.height
    img = 0.0
    for info in page.get_image_info():
        b = pymupdf.Rect(info["bbox"]) & page.rect
        img += max(0, b.width) * max(0, b.height)
    content = sum(len(page.parent.xref_stream(x) or b"") for x in page.get_contents())
    cover = min(1.0, img / area)
    if cover > 0.6 and content < 200_000:
        kind = "raster"
    elif cover > 0.3:
        kind = "mixed"
    else:
        kind = "vector"
    return kind, round(cover, 2), content


def main(job):
    base = ROOT / "projects" / job
    m = json.loads((base / "output" / "source_manifest.json").read_text())
    rows = []
    for r in m["restored"]:
        if not r["local"].lower().endswith(".pdf"):
            continue
        doc = pymupdf.open(base / r["local"])
        pages = r.get("original_pages") or list(range(1, len(doc) + 1))
        for i, sheet in enumerate(pages):
            p = doc[i]
            tb = title_block(p)
            full = p.get_text()
            nums = [x for x in DWG.findall(tb) if "-" in x and not re.match(r"^\d", x)]
            dwg = next((x for x in nums if x.count("-") >= 2), nums[0] if nums else "")
            sc = SCALE.search(tb) or SCALE.search(full)
            rv = REV.search(tb)
            title = ""
            t = re.search(r"UNITING\s+UNITING KINGSCLIFF\s+(.*?)\s+24A Kingscliff", tb)
            if t:
                title = t.group(1)
            kind, cover, content = classify(p)
            rows.append({"sheet": sheet, "file": r["local"], "page_in_file": i + 1, "drawing": dwg,
                         "title": title, "rev": rv.group(1) if rv else "", "date": rv.group(2) if rv else "",
                         "scale": (sc.group(1) if sc else ""), "paper": sc.group(2) if sc else "",
                         "w_mm": round(p.rect.width * 25.4 / 72), "h_mm": round(p.rect.height * 25.4 / 72),
                         "kind": kind, "image_cover": cover, "content_bytes": content})
    rows.sort(key=lambda x: x["sheet"])
    out = base / "output"
    (out / "sheet-index.json").write_text(json.dumps(rows, indent=1))
    md = ["# Sheet index – " + job, "", f"{len(rows)} sheets from the drop zone (see source_manifest.json).", "",
          "| Sheet | Drawing | Title | Rev | Scale | Paper | Content |", "|---|---|---|---|---|---|---|"]
    for x in rows:
        md.append(f"| {x['sheet']} | {x['drawing']} | {x['title']} | {x['rev']} | {x['scale']} | {x['paper']} | {x['kind']} |")
    (out / "sheet-index.md").write_text("\n".join(md) + "\n")
    print(f"{len(rows)} sheets indexed -> {out/'sheet-index.md'}")


if __name__ == "__main__":
    main(sys.argv[1])
