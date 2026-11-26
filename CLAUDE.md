# ADCO BCA / DDA Drawing Review: instructions for Claude

You are doing a **pre-check** of architectural drawing packs for compliance with
the BCA (NCC Volume One) and the DDA Premises Standards (Access Code), plus the
Australian Standards they call up (AS 1428.1 etc.) and, on SINSW jobs, the EFSG.
This pre-check catches issues early and sharpens RFIs. It is **not** a compliance
assessment, access audit or certification. Never describe it as one.

## Non-negotiable rules

1. **Never quote or cite a requirement from memory.** Every requirement in the
   register must be copied verbatim from a document in `standards/`, found with
   `tools/standards.py`, and cited with document, edition and clause as printed.
   If the source is not in the library, say so: set Source to
   `NOT IN LIBRARY`, leave Requirement blank, describe the topic in
   Item, and use status `Unable to verify`. Do not paraphrase a clause you
   cannot see.
2. **Use the right edition.** Use the NCC edition stated in the project's
   `project.md` (it depends on the approval/lodgement date). If the library holds a
   different edition, stop and tell the user before reviewing.
3. **The measurement hierarchy, in order:**
   1. a dimension printed on the drawing;
   2. a measurement from vector geometry, **only** on a sheet or viewport that
      has passed `tools/drawing.py calibrate` at the scale used;
   3. a visual estimate, which can never support `Compliant`. Record it as
      `Unable to verify` with the estimate in "Drawing shows".
   Record the basis used in the "Measurement basis" column for every
   dimensional finding.
4. **Calibrate before measuring.** Each sheet/viewport gets calibrated before any
   geometry measurement. If calibration is `UNRELIABLE`, has multiple scales and
   no region, or the sheet is a scan, do not measure geometry on it. Log every
   calibration result in `output/calibration-log.md`.
5. **Clear dimensions, not nominal ones.** Door widths, circulation spaces and
   corridor widths are clear dimensions. If the drawing only gives nominal or
   structural opening sizes, say so and use `Unable to verify` unless the clear
   dimension can be derived with certainty.
6. **Don't over-claim.** Luminance contrast, slip resistance, hardware types,
   operating forces, hearing augmentation performance, signage content, fire
   engineering and Performance Solutions cannot be confirmed from drawings.
   Mark them `Unable to verify` or `Performance Solution required` and say what
   information is needed.
7. **Data handling (ADCO AI Acceptable Use Policy).** This tool is approved for
   Public and Internal information only. If a pack or project file appears to
   contain Confidential information (client commercial terms, contract or tender
   values, personal staff data, credentials, unreleased financials), flag it
   once to the user and suggest redaction before continuing.

## Where drawings come from: the Drawing Drop Zone

Drawings and consultant reports **never go into git** (`projects/*/drawings/` and
`projects/*/reports/` are git-ignored). People drop them once on the Drawing
Drop Zone page, under a job code:

**https://claude.ai/artifact/Eqb8s89wfE8o8u39d9MAs8**

To restore a job's files into this container:

1. Fetch with the ArtifactData tool: `action: list`, `url` as above,
   `collection: jobs/<job>/files`, `query: {limit: 1000}`,
   `out_dir: .tmp/dz/<job>`. If the result gives a `next_cursor`, repeat with
   `query.cursor` until there is none.
2. `python3 tools/dropzone.py restore --from .tmp/dz/<job> --job <job>`
   Every file is checked against the fingerprint taken when it was dropped. A
   file listed under NOT RESTORED is missing or corrupt: tell the user, don't
   review around it silently.
3. For a very large pack, restore a tranche: `dropzone.py list` first, then
   fetch `_index` plus a `query` with `where: [["file_id","in",[...]]]` (up
   to 30 ids) and restore with `--only <paths>`.

If the job doesn't exist on the page, ask the user to create it and drop the
pack. Never ask them to commit drawings to the repository.

## Sessions end: save progress as you go

The container is wiped after inactivity. Anything not pushed is lost.

**At session start**, for the job in question:
1. Restore drawings from the drop zone (above). Run `standards.py index`.
2. `python3 tools/progress.py init <job>`, then `progress.py status <job>`.
   Resume from the handover note and the NEXT line without asking the user to
   re-explain. If init reports REVISED files, the earlier findings for those
   sheets must be re-checked against the new revision. Tell the user.

**While working**, record each step as it finishes:
`progress.py mark <job> --file <pdf> --pages <n-m> --stage indexed|calibrated|reviewed|skipped`
and `progress.py section <job> "<checklist section>" done|partial --note "..."`.
Keep `findings.json` cumulative.

**Checkpoint** (commit and push to the working branch) after each batch of
sheets or each checklist section, and at least every 30 minutes of work.
Before stopping, write `progress.py handover <job> "<what to do next>"` and
push. A checkpoint commits `output/` only (never drawings, reports or renders).

## Status categories (use exactly these)

| Status | Use when |
|---|---|
| Compliant | Drawing clearly shows the requirement met, by printed dimension or calibrated geometry |
| Non-compliant | Drawing clearly shows the requirement not met |
| Not shown on drawings | The element or information should be shown but is absent |
| Unable to verify | Can't be judged from drawings (wrong info type, visual only, unreliable scale, source not in library) |
| Performance Solution required | Departs from DTS and appears to rely on, or need, a Performance Solution |

## Folder layout

```
standards/                 source documents (NCC, Premises Standards, AS 1428.x, EFSG ...)
projects/<job>/project.md  project facts: class, NCC edition, EFSG yes/no, scope
projects/<job>/drawings/   the drawing pack, restored from the drop zone (git-ignored)
projects/<job>/reports/    consultant reports, restored from the drop zone (git-ignored)
projects/<job>/output/     everything you produce, incl. progress.json and source_manifest.json
web/dropzone.html          source of the Drawing Drop Zone page
docs/checklist.md          the review checklist
tools/                     scripts (see below)
```

## Tools

All coordinates are PDF points from the top-left of the sheet.
`real mm = pt × 25.4 / 72 × scale`.

```
python3 tools/drawing.py info <pdf>                       # sheet sizes, scales, vector vs scan, title block
python3 tools/drawing.py render <pdf> -p N -o out.png --grid 50 [--region x0,y0,x1,y1] [--dpi 150]
python3 tools/drawing.py text <pdf> -p N [--region ...] [--plain]
python3 tools/drawing.py find <pdf> "D0\d+|ACCESSIBLE"    # locate tags/text, all pages
python3 tools/drawing.py calibrate <pdf> -p N [--region ...] [--scale 50]
python3 tools/drawing.py segments <pdf> -p N --near x,y --scale 50
python3 tools/drawing.py measure x1,y1 x2,y2 --scale 50
python3 tools/standards.py index | list | search "phrase" [--doc 1428] | page <doc> <n>
python3 tools/register.py output/findings.json output/<job>-compliance-register.xlsx
python3 tools/dropzone.py list|restore --from .tmp/dz/<job> [--job <job>] [--only PATH ...]
python3 tools/progress.py init|status|mark|section|handover <job> ...
```

Rendering tips: render the whole sheet at low dpi (50 to 75) with `--grid 100` to
get your bearings, then zoom with `--region` at 150 to 200 dpi and a finer grid.
Read the grid labels to get coordinates for `segments`, `calibrate --region` or
`measure`. Keep renders in `output/renders/` and don't commit them unless asked.

## Review procedure

When the user says something like "run the review on <job>" or "sheets X to Y":

1. **Intake.** Do the session-start steps above. Read `projects/<job>/project.md`. If building class, NCC edition,
   or EFSG applicability is missing, ask before going further. Run
   `standards.py list` and confirm the library covers what's needed. Index it if
   it hasn't been indexed.
2. **Sheet index.** Run `drawing.py info` on every PDF. Write
   `output/sheet-index.md`: file, page, drawing number, title, revision, paper
   size, scale(s), vector/scan. Flag scans and sheets with no scale.
3. **Calibrate.** For each plan/section/detail sheet in scope, calibrate every
   viewport you will measure from. Log the results.
4. **Review against the checklist.** Work through `docs/checklist.md` element by
   element (not sheet by sheet), cross-referencing GAs, sections, details,
   schedules and wet-area layouts. For each check:
   - search the library for the governing clause and read the surrounding text,
     including exemptions, concessions and referenced Standards;
   - find the evidence on the drawings (printed dimension first);
   - record a finding with a verbatim quote, what the drawing shows, the basis,
     the status and a suggested action or RFI wording.
   Record compliant items as well. The register should show what was checked,
   not just failures.
5. **Register.** Write `output/findings.json` (format in `tools/register.py`)
   and build the `.xlsx`. ID prefixes: `EGR` egress, `DOR` doors, `ACC`
   access/paths of travel, `SAN` sanitary, `RMP` ramps, `STR` stairs and
   balustrades, `CPK` car parking, `HRG` hearing augmentation, `SGN` signage,
   `FIR` fire services and safety, `GEN` general.
6. **Summary.** Write `output/review-summary.md`: scope reviewed, sheets
   excluded and why, calibration problems, top issues (Non-compliant and
   Performance Solution items), information gaps, and suggested RFIs.
7. **Compare (pilot jobs).** If `reports/` contains consultant reports, write
   `output/comparison.md`: items both found, items only the consultant found
   (my misses), and items only I found. Be candid about misses.
8. **Commit and push** the outputs (not drawings, reports or renders) to the
   working branch and tell the user where the register is.

For large packs, work in batches by discipline or sheet range, and keep
`findings.json` cumulative so the register can be rebuilt at any point.

## Style of findings

- "Drawing shows" states facts: "Clear opening dimensioned 850 between door
  stop and leaf (A-201, grid C4)". It doesn't say "seems OK".
- Actions are short and specific and can be pasted into an RFI.
- Plain Australian English. No jargon that the design team wouldn't use.
