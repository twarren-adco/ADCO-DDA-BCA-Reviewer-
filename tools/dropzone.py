#!/usr/bin/env python3
"""
dropzone.py - rebuild a job's drawing pack from the Drawing Drop Zone page.

Drawings never go in the git repository. People drop them once on the drop
zone page. Since Nov 2026 the page stores files in the artifact's asset store
(1 GiB): each file, or each chosen page range of a big file, is one PDF asset
under 18 MB with its own SHA-256. The job's index (db document
jobs/<job>/files/_index) lists every file and its chunks and is written LAST.
Older files ("legacy") were stored as base64 parts in the db and are still
restored.

Steps (Claude runs the fetches with its tools, not the shell):
 1. ArtifactData get  url=<drop zone>  collection=jobs/<job>/files  doc_id=_index
                      out_dir=.tmp/dz/<job>
 2. python3 tools/dropzone.py plan --from .tmp/dz/<job> [--only PATH ...]
      prints the asset ids to fetch (and any legacy part fetches needed)
 3. For each asset id:  Artifact read  url=<drop zone>  path=<asset id>
                        out_dir=.tmp/dz/<job>/assets
 4. python3 tools/dropzone.py restore --from .tmp/dz/<job> --job <job> [--only PATH ...]

A file stored as several chunks is restored as one PDF per chunk, named
"<name> [p7-9].pdf"; source_manifest.json maps each chunk's pages back to the
original sheet numbers.

Files land in projects/<job>/drawings/ and projects/<job>/reports/ (both
git-ignored) plus projects/<job>/output/source_manifest.json (committed).
"""
import argparse
import base64
import binascii
import hashlib
import json
import pathlib
import sys
from datetime import datetime, timezone

ROOT = pathlib.Path(__file__).resolve().parent.parent
INDEX = "_index"
ALLOWED_TOP = {"drawings", "reports"}


class DropzoneError(RuntimeError):
    pass


def _body(path):
    """A fetched document. Accepts the bare body or one wrapped in data/fields."""
    try:
        obj = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        raise DropzoneError(f"{path.name} is not valid JSON ({e.msg})")
    for key in ("data", "fields"):
        if isinstance(obj.get(key), dict) and ("b64" in obj[key] or "files" in obj[key]):
            return obj[key]
    return obj


def _docs(src):
    """doc_id -> path for every fetched document, wherever out_dir nested them."""
    found = {}
    for p in src.rglob("*.json"):
        found[p.stem] = p
    return found


def read_index(src):
    docs = _docs(src)
    if INDEX not in docs:
        raise DropzoneError(
            f"No {INDEX}.json under {src}. Fetch the collection jobs/<job>/files "
            f"with ArtifactData list + out_dir first.")
    idx = _body(docs[INDEX])
    if not isinstance(idx.get("files"), list):
        raise DropzoneError(f"{INDEX} has no files array; refusing to treat it as an empty pack")
    return idx, docs


def safe_relative(path):
    """Paths come from a browser and are not trusted."""
    p = str(path or "").replace("\\", "/").strip()
    parts = [x for x in p.split("/") if x not in ("", ".")]
    if not parts or p.startswith("/") or ".." in parts or ":" in parts[0]:
        raise DropzoneError(f"unsafe path {p!r}")
    if parts[0] not in ALLOWED_TOP:
        raise DropzoneError(f"path {p!r} must start with drawings/ or reports/")
    return pathlib.Path(*parts)


def part_ids(entry):
    n = int(entry.get("parts") or 0)
    return [f"{entry['file_id']}_{i:04d}" for i in range(n)]


def reassemble(entry, docs, dest):
    fid, path = entry.get("file_id", "?"), entry.get("path", "")
    if int(entry.get("parts") or 0) < 1:
        return {"file_id": fid, "path": path, "reason": "no_parts (interrupted upload)"}
    try:
        rel = safe_relative(path)
    except DropzoneError as e:
        return {"file_id": fid, "path": path, "reason": str(e)}
    chunks = []
    for pid in part_ids(entry):
        if pid not in docs:
            return {"file_id": fid, "path": path, "reason": f"missing_part {pid} (not fetched?)"}
        body = _body(docs[pid])
        if "b64" not in body:
            return {"file_id": fid, "path": path, "reason": f"malformed_part {pid}"}
        try:
            chunks.append(base64.b64decode(body["b64"], validate=True))
        except (binascii.Error, ValueError):
            return {"file_id": fid, "path": path, "reason": f"undecodable_part {pid}"}
    raw = b"".join(chunks)
    digest = hashlib.sha256(raw).hexdigest()
    if entry.get("sha256") and digest != entry["sha256"]:
        return {"file_id": fid, "path": path,
                "reason": "sha256_mismatch: reassembled file differs from what was dropped"}
    target = dest / rel
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(raw)
    return {"file_id": fid, "path": path, "size": len(raw), "sha256": digest,
            "sha256_verified": bool(entry.get("sha256")), "parts": int(entry["parts"]),
            "uploaded_at": entry.get("uploaded_at")}


def chunk_name(rel, pages, single_whole):
    if single_whole:
        return rel
    lab = []
    a = b = None
    for p in pages:
        if a is None:
            a = b = p
        elif p == b + 1:
            b = p
        else:
            lab.append(f"{a}" if a == b else f"{a}-{b}"); a = b = p
    lab.append(f"{a}" if a == b else f"{a}-{b}")
    return rel.with_name(f"{rel.stem} [p{','.join(lab)}]{rel.suffix}")


def find_asset(src, asset_id):
    hits = [p for p in src.rglob(f"{asset_id}*") if p.is_file() and p.suffix != ".json"]
    return hits[0] if hits else None


def restore_chunks(entry, src, dest):
    fid, path = entry.get("file_id", "?"), entry.get("path", "")
    try:
        rel = safe_relative(path)
    except DropzoneError as e:
        return [{"file_id": fid, "path": path, "reason": str(e)}]
    chunks = entry.get("chunks") or []
    single = len(chunks) == 1 and (chunks[0].get("pages") is None
                                   or len(chunks[0].get("pages") or []) == entry.get("pages_total"))
    rows = []
    for c in chunks:
        ids = c.get("parts") or [c["asset_id"]]
        files = [find_asset(src, i) for i in ids]
        if any(f is None for f in files):
            rows.append({"file_id": fid, "path": path, "asset_id": ids,
                         "reason": "asset not fetched (Artifact read path=<asset id>)"})
            continue
        if c.get("parts"):
            try:
                raw = b"".join(base64.b64decode(f.read_bytes().strip(), validate=True) for f in files)
            except (binascii.Error, ValueError):
                rows.append({"file_id": fid, "path": path, "asset_id": ids,
                             "reason": "undecodable: text parts are not valid base64"})
                continue
        else:
            raw = files[0].read_bytes()
        digest = hashlib.sha256(raw).hexdigest()
        if digest != c.get("sha256"):
            rows.append({"file_id": fid, "path": path, "asset_id": c["asset_id"],
                         "reason": "sha256_mismatch: stored chunk differs from what was dropped"})
            continue
        out_rel = chunk_name(rel, c.get("pages") or [], single)
        target = dest / out_rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(raw)
        rows.append({"file_id": fid, "path": path, "local": out_rel.as_posix(),
                     "original_pages": c.get("pages"), "stored_as": "base64 text parts" if c.get("parts") else "pdf", "size": len(raw), "sha256": digest,
                     "sha256_verified": True, "uploaded_at": entry.get("uploaded_at"),
                     "pages_total": entry.get("pages_total")})
    return rows


def cmd_plan(a):
    idx, docs = read_index(pathlib.Path(a.source))
    wanted = None if not a.only else set(a.only)
    ids, legacy = [], []
    for e in idx["files"]:
        if wanted is not None and e.get("path") not in wanted:
            continue
        if e.get("chunks"):
            for c in e["chunks"]:
                ids += [i for i in (c.get("parts") or [c["asset_id"]]) if not find_asset(pathlib.Path(a.source), i)]
        else:
            missing = [pid for pid in part_ids(e) if pid not in docs]
            if missing:
                legacy.append((e.get("path"), e.get("file_id"), len(missing)))
    print(f"{len(ids)} asset(s) to fetch with: Artifact read url=<drop zone> path=<id> out_dir={a.source}/assets")
    for i in ids:
        print("  ", i)
    for path, fid, n in legacy:
        print(f"legacy file {path}: {n} db part(s) missing; fetch documents {fid}_0000.. with ArtifactData")


def restore(src, job, only=None):
    idx, docs = read_index(src)
    dest = ROOT / "projects" / job
    dest.mkdir(parents=True, exist_ok=True)
    wanted = None if only is None else {o.replace("\\", "/") for o in only}
    fetched, failed, skipped = [], [], []
    for e in idx["files"]:
        if wanted is not None and e.get("path") not in wanted:
            skipped.append({"file_id": e.get("file_id"), "path": e.get("path")})
            continue
        if e.get("chunks"):
            for row in restore_chunks(e, src, dest):
                (failed if "reason" in row else fetched).append(row)
            continue
        row = reassemble(e, docs, dest)
        (failed if "reason" in row else fetched).append(row)
    if wanted is not None:
        unknown = wanted - {e.get("path") for e in idx["files"]}
        if unknown:
            raise DropzoneError("not in the index: " + ", ".join(sorted(unknown)))
    done_files = {r.get("file_id") for r in fetched + failed} | {r.get("file_id") for r in skipped}
    if done_files != {e.get("file_id") for e in idx["files"]}:
        raise DropzoneError("file count does not add up; refusing to write a manifest")
    manifest = {
        "source": "drawing_drop_zone",
        "job": job,
        "index_updated_at": idx.get("updated_at"),
        "restored_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "scope": "whole pack" if wanted is None else "tranche",
        "files_in_index": len(idx["files"]),
        "files_restored": len({r["file_id"] for r in fetched}),
        "pdfs_written": len(fetched),
        "restored": fetched, "not_restored": failed, "not_requested": skipped,
    }
    out = dest / "output"
    out.mkdir(exist_ok=True)
    (out / "source_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    return manifest


def cmd_list(a):
    idx, _ = read_index(pathlib.Path(a.source))
    print(f"index updated {idx.get('updated_at')}  ({len(idx['files'])} files, "
          f"{sum(f.get('size', 0) for f in idx['files'])/1e6:.1f} MB)")
    for f in sorted(idx["files"], key=lambda f: f.get("path", "")):
        how = (f"{len(f['chunks'])} chunk(s), sheets {f.get('pages_label')} of {f.get('pages_total')}"
               if f.get("chunks") else f"{f.get('parts')} legacy parts")
        print(f"  {f.get('file_id')}  {f.get('size', 0)/1e6:7.1f} MB  {how}  {f.get('path')}")


def cmd_restore(a):
    try:
        m = restore(pathlib.Path(a.source), a.job, a.only)
    except DropzoneError as e:
        sys.exit(f"ERROR: {e}")
    print(f"restored {m['files_restored']} of {m['files_in_index']} file(s) "
          f"({m['pdfs_written']} PDF(s)) into projects/{a.job}/"
          f"  [{m['scope']}]")
    for r in m["not_restored"]:
        print(f"  NOT RESTORED  {r['path']}  {r['reason']}")
    if m["not_requested"]:
        print(f"  {len(m['not_requested'])} file(s) left in the drop zone for a later session")
    print(f"manifest: projects/{a.job}/output/source_manifest.json")
    if m["not_restored"]:
        sys.exit(1)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("list"); s.add_argument("--from", dest="source", required=True)
    s.set_defaults(f=cmd_list)
    s = sub.add_parser("plan"); s.add_argument("--from", dest="source", required=True)
    s.add_argument("--only", nargs="+", metavar="PATH")
    s.set_defaults(f=cmd_plan)
    s = sub.add_parser("restore"); s.add_argument("--from", dest="source", required=True)
    s.add_argument("--job", required=True)
    s.add_argument("--only", nargs="+", metavar="PATH")
    s.set_defaults(f=cmd_restore)
    a = ap.parse_args()
    a.f(a)


if __name__ == "__main__":
    main()
