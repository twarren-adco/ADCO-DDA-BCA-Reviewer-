#!/usr/bin/env python3
"""Synthetic 1:20 joinery sheet reproducing scale-check mistakes found on real packs:
- a chain of drawer dimensions whose dimension line overshoots each witness line by 1 mm
- radius dimensions drawn diagonally, ending in ticks, with the line running past the ticks
- ceiling-type tags ("CL-000 / 3080") whose divider looks like a dimension line
- a viewport title "SCALE 1 : 20 @A1"
The scale check must report CALIBRATED 1:20 and must not read the tags as dimensions."""
import math, sys
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
out = sys.argv[1]
W, H = 841 * mm, 594 * mm
c = canvas.Canvas(out, pagesize=(W, H))
Y = lambda y: H - y * mm
S = 20.0
def line(x0, y0, x1, y1, w=0.25):
    c.setLineWidth(w); c.line(x0 * mm, Y(y0), x1 * mm, Y(y1))
def vdim(x, y0, y1, label, over=1.0):
    line(x, y0 - over, x, y1 + over)                     # dimension line overshoots
    for y in (y0, y1):
        line(x - 3, y, x + 2, y)                         # witness line crossing it
        line(x - 1, y + 1, x + 1, y - 1)                 # tick
    c.saveState(); c.translate((x - 1.2) * mm, Y((y0 + y1) / 2)); c.rotate(90)
    c.setFont("Helvetica", 7); c.drawCentredString(0, 0, label); c.restoreState()
# drawer stack: 450, 450, 450, 410 chained, 1:20
x, y = 120, 100
for v in (450, 450, 450, 410):
    vdim(x, y, y + v / S, str(v)); y += v / S
c.setLineWidth(0.5); c.rect(130 * mm, Y(y), 30 * mm, (y - 100) * mm)
# background line work (a stud line) running straight through the drawer figures
line(117.9, 90, 117.9, y + 10, 0.1)
for yy in (104, 118, 132, 146, 160):
    line(110, yy, 118.5, yy, 0.1)                     # hatching that crosses it
# round table: centre, radius 850 and pedestal radius 225 along one diagonal
cx, cy = 300, 200
c.circle(cx * mm, Y(cy), 850 / S * mm); c.circle(cx * mm, Y(cy), 225 / S * mm)
ang = math.radians(-35)
def rdim(r, label, sign):
    ex, ey = cx + sign * r / S * math.cos(ang), cy - sign * r / S * math.sin(ang)
    ox, oy = ex + sign * 1.0 * math.cos(ang), ey - sign * 1.0 * math.sin(ang)   # 1 mm past the tick
    line(cx, cy, ox, oy)
    tx, ty = -math.sin(ang), -math.cos(ang)
    line(ex - tx * 1.2 - math.cos(ang) * 1.2, ey - ty * 1.2 + math.sin(ang) * 1.2,
         ex + tx * 1.2 + math.cos(ang) * 1.2, ey + ty * 1.2 - math.sin(ang) * 1.2)   # tick at the edge
    mx, my = (cx + ex) / 2, (cy + ey) / 2
    c.saveState(); c.translate((mx + tx * 1.2) * mm, Y(my + ty * 1.2)); c.rotate(math.degrees(ang) if sign > 0 else math.degrees(ang))
    c.setFont("Helvetica", 7); c.drawCentredString(0, 0, label); c.restoreState()
line(cx - 1.5, cy - 1.5, cx + 1.5, cy + 1.5); line(cx - 1.5, cy + 1.5, cx + 1.5, cy - 1.5)
rdim(850, "850", -1); rdim(225, "225", 1)
# ceiling tags
for (tx_, ty_, code, h) in ((450, 120, "CL-000", "3080"), (480, 160, "CL-101", "2400"), (520, 120, "CL-000", "2700")):
    c.setLineWidth(0.4); c.roundRect((tx_ - 4.5) * mm, Y(ty_ + 4), 9 * mm, 8 * mm, 1.5 * mm)
    line(tx_ - 4.5, ty_, tx_ + 4.5, ty_)
    c.setFont("Helvetica", 6); c.drawCentredString(tx_ * mm, Y(ty_ - 1.2), code); c.drawCentredString(tx_ * mm, Y(ty_ + 3), h)
c.setFont("Helvetica", 8)
c.drawString(100 * mm, Y(260), "1  JOINERY TYPE JX01 - ELEVATION")
c.drawString(100 * mm, Y(265), "SCALE 1 : 20 @A1")
c.drawString((W / mm - 190) * mm, 30 * mm, "SCALE: As indicated @ A1 SIZE")
c.showPage(); c.save()
