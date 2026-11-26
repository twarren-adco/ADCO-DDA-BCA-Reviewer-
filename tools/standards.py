#!/usr/bin/env python3
"""
standards.py - index and search the standards library so requirements can be
quoted VERBATIM with a document + page reference.

  python3 tools/standards.py index            # (re)build text cache of standards/*.pdf
  python3 tools/standards.py list             # what is in the library
  python3 tools/standards.py search "circulation space" [--doc 1428] [--context 400]
  python3 tools/standards.py page "AS 1428.1-2021.pdf" 37     # full text of one page

The cache lives in standards/.cache (git-ignored). Page numbers reported are
PDF page numbers (1-based), which may differ from the printed page number;
always cite clause numbers as printed in the quoted text.
"""
import argparse
import json
import pathlib
import re
import sys

import pdfplumber

ROOT = pathlib.Path(__file__).resolve().parent.parent
LIB = ROOT / "standards"
CACHE = LIB / ".cache"


def pdfs():
    return sorted(p for p in LIB.rglob("*.pdf") if ".cache" not in p.parts)


def cache_file(pdf):
    rel = pdf.relative_to(LIB).as_posix().replace("/", "__")
    return CACHE / (rel + ".json")


def cmd_index(a):
    CACHE.mkdir(parents=True, exist_ok=True)
    for pdf in pdfs():
        cf = cache_file(pdf)
        if cf.exists() and cf.stat().st_mtime >= pdf.stat().st_mtime and not a.force:
            print(f"cached  {pdf.relative_to(LIB)}")
            continue
        pages = []
        with pdfplumber.open(pdf) as doc:
            for i, pg in enumerate(doc.pages, 1):
                pages.append(pg.extract_text() or "")
        empty = sum(1 for t in pages if len(t.strip()) < 20)
        cf.write_text(json.dumps({"file": str(pdf.relative_to(LIB)), "pages": pages}))
        warn = f"  WARNING: {empty}/{len(pages)} pages have no text (scanned? needs OCR)" if empty > len(pages) * 0.2 else ""
        print(f"indexed {pdf.relative_to(LIB)}  ({len(pages)} pages){warn}")


def load():
    out = []
    for cf in sorted(CACHE.glob("*.json")):
        out.append(json.loads(cf.read_text()))
    if not out:
        sys.exit("Library not indexed (or empty). Put PDFs in standards/ and run: "
                 "python3 tools/standards.py index")
    return out


def cmd_list(a):
    for d in load():
        print(f"{d['file']}  ({len(d['pages'])} pages)")


def cmd_search(a):
    rx = re.compile(a.query if a.regex else re.escape(a.query).replace(r"\ ", r"\s+"), re.I)
    n = 0
    for d in load():
        if a.doc and a.doc.lower() not in d["file"].lower():
            continue
        for i, t in enumerate(d["pages"], 1):
            for m in rx.finditer(t):
                s, e = max(0, m.start() - a.context), min(len(t), m.end() + a.context)
                print(f"=== {d['file']}  PDF page {i}")
                print(t[s:e].strip())
                print()
                n += 1
                if n >= a.limit:
                    print(f"[stopped at {a.limit} hits; narrow with --doc or a longer query]")
                    return
    print(f"{n} hit(s)", file=sys.stderr)


def cmd_page(a):
    for d in load():
        if a.doc.lower() in d["file"].lower():
            print(f"=== {d['file']}  PDF page {a.page}")
            print(d["pages"][a.page - 1])
            return
    sys.exit("document not found; see `list`")


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("index"); s.add_argument("--force", action="store_true"); s.set_defaults(f=cmd_index)
    s = sub.add_parser("list"); s.set_defaults(f=cmd_list)
    s = sub.add_parser("search"); s.add_argument("query")
    s.add_argument("--doc", help="substring of file name to restrict to")
    s.add_argument("--regex", action="store_true")
    s.add_argument("--context", type=int, default=300)
    s.add_argument("--limit", type=int, default=20)
    s.set_defaults(f=cmd_search)
    s = sub.add_parser("page"); s.add_argument("doc"); s.add_argument("page", type=int); s.set_defaults(f=cmd_page)
    a = ap.parse_args()
    a.f(a)


if __name__ == "__main__":
    main()
