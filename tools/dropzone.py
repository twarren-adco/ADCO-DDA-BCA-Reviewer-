#!/usr/bin/env python3
"""
dropzone.py - rebuild a job's drawing pack from the Drawing Drop Zone page.

Drawings never go in the git repository. People drop them once on the drop
zone page; the page stores each file as base64 parts in its database, with an
index written LAST and a SHA-256 of every file. A session fetches those
documents with the ArtifactData tool and this script reassembles and verifies
them. Ported from adco-tender- SOP-19 source B.

Fetch first (Claude does this with the ArtifactData tool, not the shell):
    ArtifactData action=list  url=<drop zone url>  collection=jobs/<job>/files
                 out_dir=.tmp/dz/<job>   query.limit=1000   (page with cursor)
  For a tranche only, fetch _index plus a query:
    ArtifactData action=query collection=jobs/<job>/files
                 query.where=[["file_id","in",[...ids...]]] out_dir=...

Then:
    python3 tools/dropzone.py list    --from .tmp/dz/<job>
    python3 tools/dropzone.py restore --from .tmp/dz/<job> --job <job> [--only PATH ...]

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
        row = reassemble(e, docs, dest)
        (failed if "reason" in row else fetched).append(row)
    if wanted is not None:
        unknown = wanted - {e.get("path") for e in idx["files"]}
        if unknown:
            raise DropzoneError("not in the index: " + ", ".join(sorted(unknown)))
    if len(fetched) + len(failed) + len(skipped) != len(idx["files"]):
        raise DropzoneError("file count does not add up; refusing to write a manifest")
    manifest = {
        "source": "drawing_drop_zone",
        "job": job,
        "index_updated_at": idx.get("updated_at"),
        "restored_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "scope": "whole pack" if wanted is None else "tranche",
        "files_in_index": len(idx["files"]),
        "files_restored": len(fetched),
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
        print(f"  {f.get('file_id')}  {f.get('size', 0)/1e6:7.1f} MB  {f.get('parts'):>4} parts  "
              f"{(f.get('sha256') or '')[:10]}  {f.get('path')}")


def cmd_restore(a):
    try:
        m = restore(pathlib.Path(a.source), a.job, a.only)
    except DropzoneError as e:
        sys.exit(f"ERROR: {e}")
    print(f"restored {m['files_restored']} of {m['files_in_index']} file(s) into projects/{a.job}/"
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
    s = sub.add_parser("restore"); s.add_argument("--from", dest="source", required=True)
    s.add_argument("--job", required=True)
    s.add_argument("--only", nargs="+", metavar="PATH")
    s.set_defaults(f=cmd_restore)
    a = ap.parse_args()
    a.f(a)


if __name__ == "__main__":
    main()
