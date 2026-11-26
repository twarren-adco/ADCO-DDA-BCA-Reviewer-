# Calibration log – Kingy

Method: `tools/drawing.py calibrate` (whole sheet). Each printed dimension is paired with its dimension line and measured witness line to witness line; a sheet passes when ≥3 and ≥50% of matched dimensions agree with one scale within ±2%. Where the title block says *As indicated*, standard scales are tested against the dimensions instead.

| Page | Drawing | Printed scale | Dims matched | Agree | Result | Use for measuring? |
|---|---|---|---|---|---|---|
| 1 | PLA-AR-OA-0002 | As indicated | 1 | – | NO SCALE STRING | No – too few dimensions |
| 2 | PLA-AR-OA-0005 | As indicated | 17 | – | NO SCALE STRING | No |
| 3 | PLA-AR-OA-0010 | 1:500 | 1 | 1:500 0/1 | UNRELIABLE | No – too few dimensions |
| 4 | PLA-AR-OA-0010 | 1:500 | 1 | 1:500 0/1 | UNRELIABLE | No – too few dimensions |
| 5 | PLA-AR-OA-0011 | As indicated | 2 | – | NO SCALE STRING | No – too few dimensions |
| 6 | PLA-AR-OA-0012 | As indicated | 2 | – | NO SCALE STRING | No – too few dimensions |
| 7 | PLA-AR-OA-1000 | As indicated | 92 | 1:400 72/92 | CALIBRATED 1:400 (inferred, none printed) | Yes – resolution ≈ ±120 mm (0.3 mm on paper) |
| 8 | PLA-AR-OA-1003 | 1:400 | 87 | 1:400 72/87 | CALIBRATED 1:400 | Yes – resolution ≈ ±120 mm (0.3 mm on paper) |
| 9 | PLA-AR-OA-1004 | 1:400 | 87 | 1:400 73/87 | CALIBRATED 1:400 | Yes – resolution ≈ ±120 mm (0.3 mm on paper) |
| 10 | PLA-AR-OA-1050 | 1:300 | 72 | 1:300 62/72 | CALIBRATED 1:300 | Yes – resolution ≈ ±90 mm (0.3 mm on paper) |
| 11 | PLA-AR-OA-1050B | As indicated | 140 | – | REFUSED – second, hidden copy of the plan at ~75% size (embedded form object 'MWFOForm') mixes 1:300 and 1:400 dimensions | No |
| 12 | PLA-AR-OA-1051 | 1:300 | 73 | 1:300 60/73 | CALIBRATED 1:300 | Yes – resolution ≈ ±90 mm (0.3 mm on paper) |
| 13 | PLA-AR-OA-1052 | 1:300 | 73 | 1:300 59/73 | CALIBRATED 1:300 | Yes – resolution ≈ ±90 mm (0.3 mm on paper) |
| 14 | PLA-AR-OA-1053 | 1:300 | 70 | 1:300 58/70 | CALIBRATED 1:300 | Yes – resolution ≈ ±90 mm (0.3 mm on paper) |
| 15 | PLA-AR-OA-1054 | 1:300 | 73 | 1:300 60/73 | CALIBRATED 1:300 | Yes – resolution ≈ ±90 mm (0.3 mm on paper) |
| 16 | PLA-AR-OA-1201 | As indicated | 43 | 1:300 42/43 | CALIBRATED 1:300 (inferred, none printed) | Yes – resolution ≈ ±90 mm (0.3 mm on paper) |
| 17 | PLA-AR-OA-1300 | 1:400 | 84 | 1:400 76/84 | CALIBRATED 1:400 | Yes – resolution ≈ ±120 mm (0.3 mm on paper) |
| 18 | PLA-AR-OA-1300B | 1:400 | 68 | 1:400 66/68 | CALIBRATED 1:400 | Yes – resolution ≈ ±120 mm (0.3 mm on paper) |

Notes:
- Roughly 10–20% of dimensions on passing sheets were paired with the wrong line (e.g. a grid line or tick); these are matching noise, not drawing errors, and do not affect the verdict.
- At 1:300–1:400 the sheets are suitable for overall layout, travel distances, car park and path-of-travel checks, not for door clear widths, circulation spaces or sanitary layouts (need 1:50 / 1:20).
