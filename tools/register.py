#!/usr/bin/env python3
"""
register.py - build the compliance register (.xlsx) from a findings JSON file.

  python3 tools/register.py projects/<job>/output/findings.json \
          projects/<job>/output/<job>-compliance-register.xlsx

findings.json:
{
  "project": {"name": "...", "pack": "...", "revision": "...", "ncc_edition": "...",
              "building_class": "...", "reviewer_notes": "..."},
  "findings": [
    {"id": "ACC-001", "category": "Accessible sanitary", "item": "Unisex accessible WC L1",
     "sheet": "A-201 Rev C", "location": "Grid C/4",
     "source": "AS 1428.1-2021", "clause": "15.2.3",
     "requirement": "<verbatim quote>",
     "drawing_shows": "...", "basis": "Printed dimension | Calibrated geometry (1:50) | Visual",
     "status": "Non-compliant", "action": "RFI: ...", "confidence": "High|Medium|Low"}
  ]
}
"""
import datetime
import json
import sys

from openpyxl import Workbook
from openpyxl.formatting.rule import FormulaRule
from openpyxl.styles import Alignment, Font, PatternFill, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation

STATUSES = ["Compliant", "Non-compliant", "Not shown on drawings",
            "Unable to verify", "Performance Solution required"]
FILLS = {"Compliant": "C6EFCE", "Non-compliant": "FFC7CE",
         "Not shown on drawings": "FFEB9C", "Unable to verify": "D9D9D9",
         "Performance Solution required": "BDD7EE"}
COLS = [("ID", "id", 10), ("Category", "category", 18), ("Item", "item", 30),
        ("Sheet / Rev", "sheet", 14), ("Location", "location", 14),
        ("Source document", "source", 18), ("Clause", "clause", 10),
        ("Requirement (verbatim)", "requirement", 60),
        ("Drawing shows", "drawing_shows", 45), ("Measurement basis", "basis", 20),
        ("Status", "status", 18), ("Action / RFI", "action", 40),
        ("Confidence", "confidence", 11)]

DISCLAIMER = ("Pre-check only. Prepared with AI assistance from the drawings listed, to identify "
              "potential issues and inform RFIs. It is not a BCA/NCC compliance assessment, access "
              "audit or certification and does not replace the registered certifier, BCA consultant, "
              "access consultant or fire engineer. Items marked 'Unable to verify' require "
              "information not available on the drawings.")


def main(src, dst):
    data = json.loads(open(src).read())
    proj, findings = data.get("project", {}), data.get("findings", [])
    bad = [f.get("id") for f in findings if f.get("status") not in STATUSES]
    if bad:
        sys.exit(f"Invalid status on: {bad}. Allowed: {STATUSES}")

    wb = Workbook()
    thin = Side(style="thin", color="BFBFBF")
    border = Border(left=thin, right=thin, top=thin, bottom=thin)
    hdr_fill = PatternFill("solid", fgColor="1F3864")

    # --- Cover
    c = wb.active
    c.title = "Cover"
    c["A1"] = "BCA / DDA Drawing Compliance Pre-check"
    c["A1"].font = Font(size=16, bold=True)
    rows = [("Project", proj.get("name", "")), ("Drawing pack", proj.get("pack", "")),
            ("Revision / date of pack", proj.get("revision", "")),
            ("NCC edition applied", proj.get("ncc_edition", "")),
            ("Building class(es)", proj.get("building_class", "")),
            ("Other standards applied", proj.get("other_standards", "")),
            ("Register generated", datetime.date.today().isoformat()),
            ("Notes", proj.get("reviewer_notes", ""))]
    for i, (k, v) in enumerate(rows, 3):
        c.cell(i, 1, k).font = Font(bold=True)
        c.cell(i, 2, v).alignment = Alignment(wrap_text=True, vertical="top")
    r = len(rows) + 4
    c.cell(r, 1, "Disclaimer").font = Font(bold=True)
    c.cell(r, 2, DISCLAIMER).alignment = Alignment(wrap_text=True, vertical="top")
    c.row_dimensions[r].height = 90
    c.column_dimensions["A"].width = 26
    c.column_dimensions["B"].width = 100

    # --- Register
    ws = wb.create_sheet("Register")
    for j, (h, _, w) in enumerate(COLS, 1):
        cell = ws.cell(1, j, h)
        cell.font = Font(bold=True, color="FFFFFF")
        cell.fill = hdr_fill
        cell.alignment = Alignment(wrap_text=True, vertical="center")
        cell.border = border
        ws.column_dimensions[cell.column_letter].width = w
    for i, f in enumerate(findings, 2):
        for j, (_, key, _) in enumerate(COLS, 1):
            cell = ws.cell(i, j, f.get(key, ""))
            cell.alignment = Alignment(wrap_text=True, vertical="top")
            cell.border = border
    last = max(2, len(findings) + 1)
    status_col = [h for h, _, _ in COLS].index("Status") + 1
    sc = ws.cell(1, status_col).column_letter
    dv = DataValidation(type="list", formula1='"' + ",".join(STATUSES) + '"', allow_blank=True)
    ws.add_data_validation(dv)
    dv.add(f"{sc}2:{sc}{last + 200}")
    end_col = ws.cell(1, len(COLS)).column_letter
    for s, color in FILLS.items():
        ws.conditional_formatting.add(
            f"A2:{end_col}{last + 200}",
            FormulaRule(formula=[f'${sc}2="{s}"'], fill=PatternFill("solid", fgColor=color)))
    ws.freeze_panes = "D2"
    ws.auto_filter.ref = f"A1:{end_col}{last}"

    # --- Summary
    sm = wb.create_sheet("Summary", 1)
    sm["A1"] = "Status"; sm["B1"] = "Count"
    for cell in (sm["A1"], sm["B1"]):
        cell.font = Font(bold=True, color="FFFFFF"); cell.fill = hdr_fill
    for i, s in enumerate(STATUSES, 2):
        sm.cell(i, 1, s).fill = PatternFill("solid", fgColor=FILLS[s])
        sm.cell(i, 2, f'=COUNTIF(Register!{sc}:{sc},A{i})')
    t = len(STATUSES) + 2
    sm.cell(t, 1, "Total").font = Font(bold=True)
    sm.cell(t, 2, f"=SUM(B2:B{t-1})").font = Font(bold=True)
    sm.column_dimensions["A"].width = 32

    wb.save(dst)
    print(f"wrote {dst}  ({len(findings)} findings)")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])
