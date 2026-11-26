# ADCO BCA / DDA Drawing Reviewer

A repeatable process for Claude Code (on the web at claude.ai/code) to pre-check
architectural drawing packs against the BCA (NCC Volume One), the DDA Premises
Standards / Access Code, AS 1428.1 and, for SINSW jobs, the EFSG. The output is
a compliance register in Excel.

> **Pre-check only.** It catches issues early and helps write RFIs. It does not
> replace the certifier, BCA consultant, access consultant or fire engineer.

## One-off setup
1. Add the standards PDFs to `standards/` (see `standards/README.md`). Keep this
   repository **private**.
2. Start a session at claude.ai/code on this repository and ask:
   *"Index the standards library."*

## Running a review
1. On GitHub, copy `projects/_template` to `projects/<job-code>/` and fill in
   `project.md`. The easiest way is to create `projects/<job-code>/project.md`
   with **Add file → Create new file** and paste in the template.
2. Open the **[Drawing Drop Zone](https://claude.ai/artifact/Eqb8s89wfE8o8u39d9MAs8)**,
   create the same job code, tick the classification check and drag in the
   drawing PDFs (whole folders work). Switch to **Consultant reports** to add
   BCA or access reports for comparison. No splitting is needed, and drawings
   never go into GitHub. Use vector PDFs exported from Revit/ArchiCAD, not scans.
   Dropping a revised drawing with the same name replaces the old one, and the
   next session flags its sheets for re-checking.
3. Start a session at claude.ai/code on this repository and say, for example:
   *"Restore job <job-code> from the drop zone and run the review, architectural GAs and wet areas first."*
   If a session ends part-way through, start a new one and say *"carry on with <job-code>"*:
   progress, a handover note and the cumulative findings are committed as it goes.
4. Claude commits the results to its working branch under
   `projects/<job-code>/output/`:
   - `<job>-compliance-register.xlsx`: the register (Cover, Summary, Register)
   - `review-summary.md`: key issues, information gaps and suggested RFIs
   - `sheet-index.md` and `calibration-log.md`: what was reviewed and how reliably it was scaled
   - `comparison.md`: when consultant reports are provided
5. Follow-ups work in the same session: *"Re-check door D12 on A-210"*,
   *"Add the stairs and balustrade checks"*, *"Draft RFIs for the non-compliant items"*.

## How it works
- **Reading:** text, dimension strings and tags come straight out of the vector PDF.
  Sheets are rendered as images with a coordinate grid so layout and geometry
  can be cross-checked.
- **Scaling:** the scale is read from the sheet, then **calibrated** against
  printed dimensions (each drawn dimension line is measured and compared to its
  text). A viewport only counts as reliable if at least three dimensions agree
  within 2%. Printed dimensions always win. Visual estimates never support
  "Compliant".
- **Requirements:** quoted verbatim from the PDFs in `standards/`, with clause
  references. Anything not in the library is marked `NOT IN LIBRARY`, never
  quoted from memory.
- **Statuses:** Compliant / Non-compliant / Not shown on drawings /
  Unable to verify / Performance Solution required.

The rules Claude follows are in `CLAUDE.md`, the items it checks are in
`docs/checklist.md`, and the scripts are in `tools/`.

## Data handling
Claude is approved for Public and Internal information only under the ADCO AI
Acceptable Use Policy. Before uploading a pack, check its classification. Strip
client commercial details from title blocks if needed, use job codes instead of
client names, and never put contract values, personal data or credentials here.

## Self-test
```bash
bash tests/selftest.sh
```
