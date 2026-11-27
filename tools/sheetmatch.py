#!/usr/bin/env python3
"""
sheetmatch.py - calibrate a sheet that has no dimensions, grids or levels of its
own by matching its linework against sheets whose scale is already confirmed.

The same building appears on many sheets (site plan, GA plans, fitout plans).
Every straight edge on the target that also appears on a reference sheet, at
the same angle, has length ratio  target/reference = reference scale / target
scale. Unrelated edges give ratios scattered at random; the shared ones pile up
at one value. A ratio is accepted when:
  * >= 15 of those edges also line up after one common shift (a real copy of
    the same linework), and at least 2x as many as for any other ratio;
  * reference scale / ratio lands within 1% of a standard scale;
  * at least 2 reference sheets give the same scale and none gives another;
  * it agrees with any scale printed on the target (otherwise it is a query).
Accepted sheets are written to calibration.jsonl as
"CALIBRATED FROM MATCHING SHEETS".

  python3 tools/sheetmatch.py <job> [--sheets 3,5,269]
"""
import argparse, collections, json, math, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
from drawing import STANDARD_SCALES, page_geometry  # noqa: E402

TARGET_VERDICTS = ("NO DIMENSIONS", "NO SCALE STRING", "UNRELIABLE", "MULTIPLE SCALES")


def edges(pdf, page):
    _, sg, _ = page_geometry(pdf, page, None, min_len=20)
    if not sg:
        return []
    H = max(max(q["y0"], q["y1"]) for q in sg)
    W = max(max(q["x0"], q["x1"]) for q in sg)
    # leave out the title block strip and the notes column
    sg = [q for q in sg if max(q["y0"], q["y1"]) < H * 0.86 and max(q["x0"], q["x1"]) < W * 0.84]
    d = {}
    for q in sg:
        mx, my = (q["x0"] + q["x1"]) / 2, (q["y0"] + q["y1"]) / 2
        d[(round(q["angle"], 1), round(q["len_pt"]), round(mx), round(my))] = (q["angle"], q["len_pt"], mx, my)
    # hatching and repeated elements (identical edges many times over) swamp the
    # vote with chance ratios; keep the distinctive edges
    mult = collections.Counter((round(e[0]), round(e[1])) for e in d.values())
    return [e for e in d.values() if mult[(round(e[0]), round(e[1]))] <= 4]


def _pairs(A, B, tol_ang=0.3):
    by = collections.defaultdict(list)
    for e in B:
        by[round(e[0]) % 180].append(e)
    for e in A:
        for k in (round(e[0]) - 1, round(e[0]), round(e[0]) + 1):
            for f in by.get(k % 180, []):
                if abs((e[0] - f[0] + 90) % 180 - 90) < tol_ang:
                    yield e, f


def best_ratio(A, B, top=30):
    """Shared linework: edges of equal angle whose length ratio is the same AND
    whose positions agree after one shift. Returns (ratio, aligned edges,
    aligned edges of the best other ratio)."""
    votes = collections.Counter()
    pairs = []
    for e, f in _pairs(A, B):
        r = e[1] / f[1]
        if 0.1 < r < 10 and e[1] >= 30:
            k = round(math.log(r) * 1000)
            votes[k] += 1
            pairs.append((k, e, f))
    if not votes:
        return None
    pooled = {k: sum(votes.get(k + d, 0) for d in (-1, 0, 1)) for k in votes}
    cands = []
    for k in sorted(pooled, key=pooled.get, reverse=True):
        if all(abs(k - c) > 3 for c in cands):
            cands.append(k)
        if len(cands) >= top:
            break
    scored = []
    for k in cands:
        r = math.exp(k / 1000)
        shift = collections.Counter()
        for k2, e, f in pairs:
            if abs(k2 - k) <= 1:
                shift[(round((e[2] - r * f[2]) / 4), round((e[3] - r * f[3]) / 4))] += 1
        n = 0
        if shift:
            (sx, sy), _ = shift.most_common(1)[0]
            n = sum(shift.get((sx + dx, sy + dy), 0) for dx in (-1, 0, 1) for dy in (-1, 0, 1))
        scored.append((n, r))
    scored.sort(reverse=True)
    n1, r1 = scored[0]
    n2 = max((n for n, r in scored[1:] if abs(math.log(r / r1)) > 0.003), default=0)
    return r1, n1, n2


def snap(sc):
    for s in STANDARD_SCALES:
        if abs(sc / s - 1) <= 0.01:
            return s
    return None


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("job"); ap.add_argument("--sheets"); ap.add_argument("--max-refs", type=int, default=12)
    a = ap.parse_args()
    base = ROOT / "projects" / a.job
    idx = {r["sheet"]: r for r in json.loads((base / "output" / "sheet-index.json").read_text())}
    jl = base / "output" / "calibration.jsonl"
    rows = [json.loads(l) for l in jl.read_text().splitlines() if l.strip()]
    res = {r["sheet"]: r for r in rows}
    want = None
    if a.sheets:
        want = set()
        for part in a.sheets.split(","):
            x, _, y = part.partition("-"); want.update(range(int(x), int(y or x) + 1))

    def series(s):
        d = idx[s].get("drawing") or ""
        m = re.match(r".*-(OA|A|B|C|RAC)-(\d)", d)
        return (m.group(1), m.group(2)) if m else (None, None)

    refs = [s for s, r in res.items() if (r.get("verdict") or "").startswith("CALIBRATED")
            and "VIEWPORT" not in r["verdict"] and r.get("calibrated_scale") and idx[s]["kind"] != "raster"]
    targets = [s for s, r in res.items() if (r.get("verdict") or "").startswith(TARGET_VERDICTS)
               and idx[s]["kind"] != "raster" and (want is None or s in want) and not r.get("tables_only")]
    cache = {}

    def E(s):
        if s not in cache:
            cache[s] = edges(base / idx[s]["file"], idx[s]["page_in_file"])
        return cache[s]

    for t in sorted(targets):
        bld, ser = series(t)
        # references: same building, plans first, then the same series, then the overall (OA) plans
        cand = sorted(refs, key=lambda s: (series(s)[0] != bld, series(s)[1] != "1", series(s)[1] != ser,
                                           series(s)[0] != "OA", abs(s - t)))[: a.max_refs]
        At = E(t)
        if len(At) < 30:
            print(f"sheet {t:>3} {idx[t]['drawing']:<18} too little linework to match", flush=True)
            continue
        found = []
        for s in cand:
            br = best_ratio(At, E(s))
            if not br:
                continue
            r, n, n2 = br
            sc = snap(res[s]["calibrated_scale"] / r)
            if n >= 15 and n >= 2 * max(n2, 1) and sc:
                found.append({"ref": s, "drawing": idx[s]["drawing"], "ref_scale": res[s]["calibrated_scale"],
                              "ratio": round(r, 4), "votes": n, "runner_up": n2, "scale": sc})
        scales = collections.Counter(f["scale"] for f in found)
        printed = [int(x) for x in re.findall(r"1\s*:\s*(\d+)", idx[t].get("scale") or "")]
        r = res[t]
        if len(scales) == 1 and len(found) >= 2:
            sc = next(iter(scales))
            refs_txt = ", ".join(f"{f['drawing']} 1:{int(f['ref_scale'])} ({f['votes']} edges)" for f in found[:3])
            if printed and sc not in printed:
                r["match_query"] = f"linework matches 1:{sc} ({refs_txt}) but the sheet prints {idx[t]['scale']}"
                msg = "QUERY - " + r["match_query"]
            else:
                r["previous_verdict"] = r.get("verdict")
                r["verdict"] = (f"CALIBRATED FROM MATCHING SHEETS - linework matches {len(found)} calibrated "
                                f"sheet(s) at 1:{sc}: {refs_txt}")
                r["calibrated_scale"] = sc
                r["sheet_matches"] = found
                msg = r["verdict"]
        elif len(scales) > 1:
            msg = "NOT CALIBRATED - references disagree: " + ", ".join(f"1:{k} x{v}" for k, v in scales.items())
        else:
            msg = f"NOT CALIBRATED - {len(found)} matching reference(s)"
        print(f"sheet {t:>3} {idx[t]['drawing']:<18} {msg[:150]}", flush=True)
    jl.write_text("".join(json.dumps(r) + "\n" for r in rows))


if __name__ == "__main__":
    main()
