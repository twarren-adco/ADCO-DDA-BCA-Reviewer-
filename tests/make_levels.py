#!/usr/bin/env python3
"""Synthetic A1 sheets for the scale-check fallbacks:
  levels.pdf  - three 1:50 elevations with FFL 0.00 / FCL 2700 heads, no dimensions,
                viewport titles that wrongly say "@A3", plus a door schedule table
                full of numbers and 'CL-101' ceiling tags (must not be read as levels)
  planA.pdf / planB.pdf - the same undimensioned floor plan drawn at 1:100 and 1:50"""
import random, sys
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
out = sys.argv[1]
W, H = 841 * mm, 594 * mm
c = canvas.Canvas(f"{out}/levels.pdf", pagesize=(W, H))
Y = lambda y: H - y * mm
c.setFont("Helvetica", 6)
for i, x in enumerate((40, 240, 440)):
    top, bot = 60, 60 + 2700 / 50
    c.line(x * mm, Y(top), (x + 150) * mm, Y(top)); c.line(x * mm, Y(bot), (x + 150) * mm, Y(bot))
    c.drawString(x * mm, Y(top - 1), "FCL 2700"); c.drawString(x * mm, Y(bot - 1), "FFL 0.00")
    c.rect((x + 40) * mm, Y(bot), 18 * mm, 2040 / 50 * mm)
    c.drawString(x * mm, Y(bot + 10), f"{i + 1}  CORRIDOR - ELEVATION {'ABC'[i]}")
    c.drawString(x * mm, Y(bot + 14), "SCALE 1 : 50 @A3")
    c.drawString((x + 70) * mm, Y(top + 20), "CL-101"); c.drawString((x + 70) * mm, Y(top + 24), "CL-102")
# a door schedule table: 20 rows of numbers
tx, ty = 40, 250
for r in range(21):
    c.line(tx * mm, Y(ty + r * 5), (tx + 200) * mm, Y(ty + r * 5))
for k in range(6):
    c.line((tx + k * 40) * mm, Y(ty), (tx + k * 40) * mm, Y(ty + 100))
random.seed(1)
for r in range(20):
    for k, v in enumerate((random.choice((820, 920, 1020)), 2040, random.choice((850, 950)), 1200, 60)):
        c.drawString((tx + k * 40 + 3) * mm, Y(ty + r * 5 + 3.5), str(v))
c.drawString((W / mm - 190) * mm, 30 * mm, "SCALE: As indicated @ A1 SIZE")
c.showPage(); c.save()
# one plan, two scales, no dimensions
random.seed(7)
walls = []
for _ in range(60):
    x, y = random.uniform(0, 30000), random.uniform(0, 18000)
    L = random.uniform(1500, 9000)
    walls.append((x, y, x + L, y) if random.random() < 0.5 else (x, y, x, y + L))
for name, sc in (("planA", 100), ("planB", 50)):
    c = canvas.Canvas(f"{out}/{name}.pdf", pagesize=(W, H))
    ox, oy = (30, 30) if sc == 100 else (-120, -60)       # different crop: only part fits at 1:50
    for x0, y0, x1, y1 in walls:
        c.line((ox + x0 / sc) * mm, Y(oy + y0 / sc), (ox + x1 / sc) * mm, Y(oy + y1 / sc))
    c.showPage(); c.save()
