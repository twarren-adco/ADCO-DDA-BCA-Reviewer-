#!/usr/bin/env python3
"""Generate a synthetic vector drawing for self-testing the tools.

A1 landscape sheet: a 1:100 plan viewport (left) and a 1:20 detail (right),
with dimension strings, a door tag and a title block. One dimension on the
plan is deliberately overwritten ("NTS" style) to check mismatch detection.
"""
import sys
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas

out = sys.argv[1] if len(sys.argv) > 1 else "sample.pdf"
W, H = 841 * mm, 594 * mm
c = canvas.Canvas(out, pagesize=(W, H))


def Y(y):  # reportlab origin is bottom-left; we think in top-left
    return H - y


def dim_h(x0, x1, y, label, scale):
    """horizontal dimension; x0/x1/y in paper mm from top-left."""
    c.setLineWidth(0.25)
    c.line(x0 * mm, Y(y * mm), x1 * mm, Y(y * mm))
    for x in (x0, x1):
        c.line(x * mm, Y((y - 2) * mm), x * mm, Y((y + 2) * mm))  # ext/tick
    c.setFont("Helvetica", 7)
    c.drawCentredString((x0 + x1) / 2 * mm, Y((y - 1) * mm), label)


def dim_v(x, y0, y1, label):
    c.setLineWidth(0.25)
    c.line(x * mm, Y(y0 * mm), x * mm, Y(y1 * mm))
    for y in (y0, y1):
        c.line((x - 2) * mm, Y(y * mm), (x + 2) * mm, Y(y * mm))
    c.saveState()
    c.translate((x - 1) * mm, Y((y0 + y1) / 2 * mm))
    c.rotate(90)
    c.setFont("Helvetica", 7)
    c.drawCentredString(0, 0, label)
    c.restoreState()


# ---- plan at 1:100: a 12000 x 8000 room starting at paper (60,80) mm
S = 100
ox, oy = 60, 80
c.setLineWidth(1)
c.rect(ox * mm, Y((oy + 80) * mm), 120 * mm, 80 * mm)
dim_h(ox, ox + 120, oy - 10, "12000", S)
dim_h(ox, ox + 45, oy + 95, "4500", S)
dim_h(ox + 45, ox + 120, oy + 95, "7500", S)
dim_v(ox - 10, oy, oy + 80, "8000")
dim_h(ox + 60, ox + 69.5, oy + 40, "950", S)      # door clear width 950
dim_h(ox + 10, ox + 25, oy + 60, "1800", S)       # wrong on purpose: line is 1500
c.setFont("Helvetica", 8)
c.drawString((ox + 62) * mm, Y((oy + 36) * mm), "D01")
c.drawString((ox + 20) * mm, Y((oy + 20) * mm), "ACCESSIBLE WC")
c.setFont("Helvetica-Bold", 10)
c.drawString(ox * mm, Y((oy + 115) * mm), "GROUND FLOOR PLAN  1:100")

# ---- detail at 1:20 at paper (300,80) mm: 2300 x 1900 sanitary room
S2 = 20
dx, dy = 300, 80
c.setLineWidth(1)
c.rect(dx * mm, Y((dy + 95) * mm), 115 * mm, 95 * mm)
dim_h(dx, dx + 115, dy - 10, "2300", S2)
dim_v(dx - 10, dy, dy + 95, "1900")
dim_h(dx + 20, dx + 60, dy + 50, "800", S2)
dim_h(dx + 5, dx + 37.5, dy + 80, "650", S2)
c.setFont("Helvetica-Bold", 10)
c.drawString(dx * mm, Y((dy + 115) * mm), "DETAIL 1 - ACCESSIBLE WC  1:20")

# ---- title block bottom-right
c.setLineWidth(0.5)
c.rect((W / mm - 200) * mm, 10 * mm, 190 * mm, 50 * mm)
c.setFont("Helvetica", 9)
c.drawString((W / mm - 195) * mm, 50 * mm, "PROJECT: SAMPLE SCHOOL UPGRADE")
c.drawString((W / mm - 195) * mm, 40 * mm, "DWG No: A-101   REV: C")
c.drawString((W / mm - 195) * mm, 30 * mm, "SCALE: 1:100, 1:20 @ A1")
c.drawString((W / mm - 195) * mm, 20 * mm, "GROUND FLOOR PLAN AND DETAILS")
c.showPage()
c.save()
print("wrote", out)
