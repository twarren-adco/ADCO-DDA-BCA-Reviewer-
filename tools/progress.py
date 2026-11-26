#!/usr/bin/env python3
"""
progress.py - where a review got to, so the next session resumes unasked.

Cloud containers are temporary. Drawings come back from the drop zone and the
standards index rebuilds in seconds, but the state of a half-finished review
has to be written down and committed. It lives in
projects/<job>/output/progress.json.

  python3 tools/progress.py init    <job>        # after restore: add new files/sheets, flag revised files
  python3 tools/progress.py status  <job>        # what is done, what is next, what changed
  python3 tools/progress.py mark    <job> --file A-101.pdf --pages 1-4 --stage calibrated [--note ".."]
  python3 tools/progress.py section <job> "4. Sanitary facilities" done|partial|todo [--note ".."]
  python3 tools/progress.py handover <job> "next: calibrate A-201 viewports 2-3, then sanitary"

Stages per sheet: todo -> indexed -> calibrated -> reviewed  (or skipped, with a note).
A file whose SHA-256 changed since it was last seen (a revised drawing dropped
again) has its sheets reset to todo and is reported, so stale findings are
re-checked rather than carried forward.
"""
import argparse
import json
import pathlib
import re
import sys
from datetime import datetime, timezone

import pdfplumber

ROOT = pathlib.Path(__file__).resolve().parent.parent
STAGES = ["todo", "indexed", "calibrated", "reviewed", "skipped"]
CHECKLIST = ROOT / "docs" / "checklist.md"


def now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def paths(job):
    base = ROOT / "projects" / job
    return base, base / "output" / "progress.json", base / "output" / "source_manifest.json"


def load(job):
    _, pf, _ = paths(job)
    if pf.exists():
        return json.loads(pf.read_text())
    return {"job": job, "files": {}, "sections": {}, "handover": "", "log": []}


def save(job, p):
    _, pf, _ = paths(job)
    pf.parent.mkdir(parents=True, exist_ok=True)
    p["updated_at"] = now()
    pf.write_text(json.dumps(p, indent=2) + "\n")


def checklist_sections():
    if not CHECKLIST.exists():
        return []
    return [m.group(1).strip() for m in re.finditer(r"^## (.+)$", CHECKLIST.read_text(), re.M)]


def page_range(s, n):
    out = set()
    for part in s.split(","):
        if "-" in part:
            a, b = part.split("-")
            out.update(range(int(a), int(b) + 1))
        else:
            out.add(int(part))
    bad = [x for x in out if x < 1 or x > n]
    if bad:
        sys.exit(f"pages {bad} out of range 1..{n}")
    return sorted(out)


def cmd_init(a):
    base, _, mf = paths(a.job)
    p = load(a.job)
    manifest = json.loads(mf.read_text()) if mf.exists() else {"restored": []}
    shas = {r["path"]: r["sha256"] for r in manifest.get("restored", [])}
    pdfs = sorted((base / "drawings").rglob("*.pdf")) if (base / "drawings").exists() else []
    added, revised = [], []
    for pdf in pdfs:
        rel = pdf.relative_to(base).as_posix()
        sha = shas.get(rel)
        with pdfplumber.open(pdf) as d:
            n = len(d.pages)
        cur = p["files"].get(rel)
        if cur is None:
            p["files"][rel] = {"sha256": sha, "pages": {str(i): "todo" for i in range(1, n + 1)}, "notes": {}}
            added.append(rel)
        elif sha and cur.get("sha256") and sha != cur["sha256"]:
            p["files"][rel] = {"sha256": sha, "pages": {str(i): "todo" for i in range(1, n + 1)},
                               "notes": {}, "revised_from": cur["sha256"], "revised_at": now()}
            revised.append(rel)
        elif sha and not cur.get("sha256"):
            cur["sha256"] = sha
    for s in checklist_sections():
        p["sections"].setdefault(s, {"state": "todo", "note": ""})
    if revised:
        p["log"].append({"at": now(), "event": "revised files reset to todo", "files": revised})
    save(a.job, p)
    print(f"{len(added)} new file(s), {len(revised)} revised, {len(p['files'])} tracked")
    for r in revised:
        print(f"  REVISED (findings from these sheets must be re-checked): {r}")
    missing = [f for f in p["files"] if not (base / f).exists()]
    if missing:
        print(f"  {len(missing)} tracked file(s) not on disk in this session (not restored yet):")
        for f in missing[:10]:
            print(f"    {f}")


def cmd_status(a):
    base, pf, _ = paths(a.job)
    if not pf.exists():
        sys.exit(f"No progress yet for {a.job}. Restore the drawings, then run: progress.py init {a.job}")
    p = load(a.job)
    tot = {s: 0 for s in STAGES}
    print(f"Job {a.job} - progress updated {p.get('updated_at')}")
    for f, info in sorted(p["files"].items()):
        counts = {s: 0 for s in STAGES}
        for st in info["pages"].values():
            counts[st] += 1
            tot[st] += 1
        here = "" if (base / f).exists() else "  [not restored in this session]"
        rev = "  [REVISED - re-check]" if info.get("revised_from") else ""
        summary = ", ".join(f"{v} {k}" for k, v in counts.items() if v)
        print(f"  {f}: {summary}{rev}{here}")
    print("Sheets: " + ", ".join(f"{v} {k}" for k, v in tot.items() if v))
    print("Checklist:")
    for s, v in p["sections"].items():
        note = f" - {v['note']}" if v.get("note") else ""
        print(f"  [{v['state']:<7}] {s}{note}")
    if p.get("handover"):
        print(f"Handover note: {p['handover']}")
    todo = [(f, pg) for f, i in sorted(p["files"].items()) for pg, st in i["pages"].items()
            if st not in ("reviewed", "skipped")]
    secs = [s for s, v in p["sections"].items() if v["state"] != "done"]
    if not todo and not secs:
        print("NEXT: all sheets and checklist sections done - build the register and summary.")
    else:
        if todo:
            print(f"NEXT: {len(todo)} sheet(s) not finished, starting {todo[0][0]} p{todo[0][1]}")
        if secs:
            print(f"      {len(secs)} checklist section(s) open, starting '{secs[0]}'")


def cmd_mark(a):
    p = load(a.job)
    key = next((f for f in p["files"] if f == a.file or f.endswith("/" + a.file)), None)
    if not key:
        sys.exit(f"{a.file} not tracked; run init first")
    pages = p["files"][key]["pages"]
    for pg in page_range(a.pages, len(pages)):
        pages[str(pg)] = a.stage
        if a.note:
            p["files"][key]["notes"][str(pg)] = a.note
    p["log"].append({"at": now(), "event": f"{key} p{a.pages} -> {a.stage}", "note": a.note or ""})
    save(a.job, p)
    print(f"{key} p{a.pages}: {a.stage}")


def cmd_section(a):
    p = load(a.job)
    match = [s for s in p["sections"] if s.lower().startswith(a.name.lower()) or a.name.lower() in s.lower()]
    if len(match) != 1:
        sys.exit(f"'{a.name}' matches {len(match)} sections: {match or list(p['sections'])}")
    p["sections"][match[0]] = {"state": a.state, "note": a.note or ""}
    p["log"].append({"at": now(), "event": f"section {match[0]} -> {a.state}", "note": a.note or ""})
    save(a.job, p)
    print(f"{match[0]}: {a.state}")


def cmd_handover(a):
    p = load(a.job)
    p["handover"] = a.text
    p["log"].append({"at": now(), "event": "handover", "note": a.text})
    save(a.job, p)
    print("handover note saved - commit and push now so the next session sees it")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("init"); s.add_argument("job"); s.set_defaults(f=cmd_init)
    s = sub.add_parser("status"); s.add_argument("job"); s.set_defaults(f=cmd_status)
    s = sub.add_parser("mark"); s.add_argument("job"); s.add_argument("--file", required=True)
    s.add_argument("--pages", required=True); s.add_argument("--stage", required=True, choices=STAGES)
    s.add_argument("--note"); s.set_defaults(f=cmd_mark)
    s = sub.add_parser("section"); s.add_argument("job"); s.add_argument("name")
    s.add_argument("state", choices=["todo", "partial", "done"]); s.add_argument("--note")
    s.set_defaults(f=cmd_section)
    s = sub.add_parser("handover"); s.add_argument("job"); s.add_argument("text"); s.set_defaults(f=cmd_handover)
    a = ap.parse_args()
    a.f(a)


if __name__ == "__main__":
    main()
