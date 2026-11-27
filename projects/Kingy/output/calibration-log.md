# Calibration log – Kingy

**482 of 581 sheets can be measured from geometry.**

Method (`tools/calibrate_all.py`, `tools/grids.py`): printed dimensions are paired with their dimension lines (any angle) and measured witness line to witness line; horizontal/vertical dimension lines need witness lines crossing both ends. A sheet passes when >=3 and >=50% of matched dimensions agree with one scale within +-2%. *By viewport*: each consistent viewport (>=3 dimensions, >=65% agreement inside its area) is calibrated separately and measuring is valid only inside its listed region (`calibration.jsonl`). *From grids*: the sheet has no usable dimensions, but >=3 grid spacings (from `grid-table.json`, built from calibrated plans) agree with one scale within +-1% and with the printed scale. *Printed scale*: no dimensions or grids to check against, so the scale printed under each viewport title (e.g. 'SCALE 1 : 5 @A1') is used, accepted only because the page is the full paper size the note names (`tools/printedscale.py`). Mixed-scale sheets get a region per viewport.

| Series | Calibrated | By viewport | From grids | Printed scale | Printed (by viewport) | No dimensions | No scale printed | Unreliable | Mixed scales | Image |
|---|---|---|---|---|---|---|---|---|---|---|
| 0xxx General / site | 7 | 0 | 0 | 0 | 0 | 15 | 1 | 0 | 0 | 4 |
| 1xxx GA plans, RCPs, wall types | 108 | 19 | 53 | 3 | 0 | 0 | 0 | 0 | 0 | 0 |
| 2xxx Elevations | 17 | 0 | 0 | 5 | 0 | 0 | 0 | 1 | 0 | 22 |
| 3xxx Sections | 10 | 2 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| 4xxx Unit & common-area fitouts, wet areas | 89 | 2 | 1 | 54 | 0 | 6 | 0 | 1 | 0 | 0 |
| 5xxx Details | 8 | 4 | 0 | 24 | 3 | 1 | 0 | 1 | 0 | 11 |
| 6xxx Schedules | 5 | 10 | 0 | 2 | 0 | 0 | 9 | 17 | 0 | 0 |
| 7xxx Joinery / details | 39 | 3 | 0 | 1 | 0 | 0 | 0 | 4 | 0 | 1 |
| 8xxx FF&E schedules | 0 | 3 | 0 | 0 | 0 | 1 | 3 | 0 | 0 | 0 |
| ?xxx Other | 2 | 0 | 5 | 2 | 0 | 0 | 1 | 0 | 0 | 0 |
| **Total** | **285** | **43** | **59** | **91** | **4** | **23** | **14** | **24** | **0** | **38** |

*No dimensions*: fewer than 3 printed dimensions and no shared grid (e.g. details, joinery). *Unreliable*: dimensions disagree (mostly reflected ceiling plans and sparsely dimensioned fitouts). *Image*: mostly raster. Schedules are read as text, not measured.

## Queries raised by the scale check

- **C-4101 to C-4104 and C-4107 (sheets 268-272), Building C common-area fitouts:** viewports labelled "SCALE 1 : 50 @A3" on A1 sheets (841 x 594 mm). Either the views are effectively 1:25 on these sheets or the labels are wrong. Not measured until the architect confirms.

## Per sheet

| Sheet | Drawing | Title | Scale (printed) | Result | Agree |
|---|---|---|---|---|---|
| 1 | PLA-AR-OA-0000 | COVER SHEET |  | No dimensions |  |
| 2 | PLA-AR-OA-0001 | DRAWING REGISTER |  | No dimensions |  |
| 3 | PLA-AR-OA-0002 | SITE PLAN | As indicated | No dimensions |  |
| 4 | PLA-AR-OA-0004 | SITE SETOUT PLAN | 1 : 400 | Calibrated 1:400 | 1:400 73/77 |
| 5 | PLA-AR-OA-0005 | SITE PLAN EASEMENTS | As indicated | No scale printed |  |
| 6 | PLA-AR-OA-0006 | SUBSTATION PLANS | 1 : 100 | Calibrated 1:100 | 1:100 22/22 |
| 7 | PLA-AR-OA-0007 | SUBSTATION ELEVATION | 1 : 100 | Calibrated 1:100 | 1:100 14/14 |
| 8 | PLA-AR-OA-0007 | SUBSTATION ELEVATION | 1 : 100 | Calibrated 1:100 | 1:100 14/14 |
| 9 | PLA-AR-OA-0008 | PRECAST EDGE EXTRUSION SCHEDULE - SHEET 01 | 1 : 5 | Calibrated 1:5 | 1:5 32/32 |
| 10 | PLA-AR-OA-0009 | PRECAST EDGE EXTRUSION SCHEDULE - SHEET 02 | 1 : 5 | Calibrated 1:5 | 1:5 33/34 |
| 11 | PLA-AR-OA-0009 | PRECAST EDGE EXTRUSION SCHEDULE - SHEET 02 | 1 : 5 | Calibrated 1:5 | 1:5 33/34 |
| 12 | PLA-AR-OA-0010 | DEMOLITION PLAN | 1 : 500 | Image |  |
| 13 | PLA-AR-OA-0010 | DEMOLITION PLAN | 1 : 500 | Image |  |
| 14 | PLA-AR-OA-0011 | TEMPORARY WORKS PLAN | As indicated | Image |  |
| 15 | PLA-AR-OA-0012 | SEPARABLE PORTIONS | As indicated | Image |  |
| 16 | PLA-AR-OA-1000 | GENERAL ARRANGEMENT PLAN - GROUND FLOOR | As indicated | Calibrated 1:400 | 1:400 81/85 |
| 17 | PLA-AR-OA-1003 | GENERAL ARRANGEMENT PLAN - LEVEL 03 | 1 : 400 | Calibrated 1:400 | 1:400 80/85 |
| 18 | PLA-AR-OA-1004 | GENERAL ARRANGEMENT PLAN - ROOF | 1 : 400 | Calibrated 1:400 | 1:400 81/86 |
| 19 | PLA-AR-OA-1050 | GENERAL ARRANGEMENT PLAN - GROUND - STAGE 1 | 1 : 300 | Calibrated 1:300 | 1:300 68/71 |
| 20 | PLA-AR-OA-1050B | GENERAL ARRANGEMENT PLAN - BASEMENT - STAGE 1 | As indicated | From grids 1:400 | 210/280 |
| 21 | PLA-AR-OA-1051 | GENERAL ARRANGEMENT PLAN - LEVEL 01 - STAGE 1 | 1 : 300 | Calibrated 1:300 | 1:300 66/72 |
| 22 | PLA-AR-OA-1052 | GENERAL ARRANGEMENT PLAN - LEVEL 02 - STAGE 1 | 1 : 300 | Calibrated 1:300 | 1:300 66/71 |
| 23 | PLA-AR-OA-1053 | GENERAL ARRANGEMENT PLAN - LEVEL 03 - STAGE 1 | 1 : 300 | Calibrated 1:300 | 1:300 66/71 |
| 24 | PLA-AR-OA-1054 | GENERAL ARRANGEMENT PLAN - ROOF - STAGE 1 | 1 : 300 | Calibrated 1:300 | 1:300 65/71 |
| 25 | PLA-AR-OA-1201 | OVERALL BASEMENT FIRE RESISTANCE PLAN - BASEMENT | As indicated | Calibrated 1:300 | 1:300 42/42 |
| 26 | PLA-AR-OA-1300 | CONCRETE PROFILE - GROUND FLOOR | 1 : 400 | Calibrated 1:400 | 1:400 83/87 |
| 27 | PLA-AR-OA-1300B | CONCRETE PROFILE PLAN - BASEMENT | 1 : 400 | Calibrated 1:400 | 1:400 67/67 |
| 28 | PLA-AR-OA-1400 | WALL TYPE SCHEDULE SHEET 01 | 1:10 | Calibrated 1:10 | 1:10 13/13 |
| 29 | PLA-AR-OA-1402 | WALL TYPE SCHEDULE SHEET 03 | 1:10 | Calibrated 1:10 | 1:10 6/6 |
| 30 | PLA-AR-OA-1403 | WALL TYPE SCHEDULE SHEET 04 | 1:10 | Printed scale 1:10 | 1:10 1/1 |
| 31 | PLA-AR-OA-1404 | WALL TYPE SCHEDULE SHEET 05 | 1:10 | Printed scale 1:10 | 1:10 0/0 |
| 32 | PLA-AR-OA-1405 | WALL TYPE SCHEDULE SHEET 06 | 1:10 | Printed scale 1:10 | 1:10 0/0 |
| 33 | PLA-AR-OA-2000 | ELEVATIONS | As indicated | Calibrated 1:400 | 1:400 16/16 |
| 34 | PLA-AR-OA-2100 | SECTIONS | As indicated | Calibrated 1:400 | 1:400 8/8 |
| 35 | PLA-AR-OA-5000 | FACADE SECTION TYPICAL DETAILS - SHEET 01 | 1 : 5 | By viewport (1:5) | 1:100 0/5 / 1:5 5/5 |
| 36 | PLA-AR-OA-5001 | FACADE SECTION TYPICAL DETAILS - SHEET 02 | As indicated | Printed (by viewport) (1:2, 1:5, 1:5, 1:5, 1:5) | 1:2 1/3 / 1:5 2/3 |
| 37 | PLA-AR-OA-5002 | FACADE SECTION TYPICAL DETAILS - SHEET 03 | 1 : 2 | Printed scale 1:2 | 1:2 2/2 |
| 38 | PLA-AR-OA-5050 | FACADE PLAN TYPICAL DETAILS - SHEET 01 | 1 : 2 | Printed scale 1:2 | 1:2 0/0 |
| 39 | PLA-AR-OA-5100 | EXTERNAL DETAILS - SHEET 01 | 1 : 10 | Printed scale 1:10 | 1:10 0/0 |
| 40 | PLA-AR-OA-5101 | EXTERNAL DETAILS - SHEET 02 | 1 : 10 | Printed scale 1:10 | 1:100 0/1 / 1:10 1/1 |
| 41 | PLA-AR-OA-5102 | EXTERNAL DETAILS - SHEET 03 | 1 : 10 | By viewport (1:10) | 1:100 0/3 / 1:10 3/3 |
| 42 | PLA-AR-OA-5103 | EXTERNAL DETAILS - SHEET 04 | 1 : 10 | Calibrated 1:10 | 1:10 6/6 |
| 43 | PLA-AR-OA-5104 | EXTERNAL DETAILS - SHEET 05 | 1 : 10 | Calibrated 1:10 | 1:10 12/16 |
| 44 | PLA-AR-OA-5200 | WATERPROOFING DETAILS - SHEET 01 | 1 : 20 | Printed scale 1:20 | 1:20 0/0 |
| 45 | PLA-AR-OA-5201 | WATERPROOFING DETAILS - SHEET 02 | 1 : 5 | By viewport (1:5) | 1:50 0/5 / 1:2 1/5 / 1:5 4/5 |
| 46 | PLA-AR-OA-5300 | INTERNAL WALL DETAILS - SHEET 01 | 1 : 5 | Printed scale 1:5 | 1:5 0/0 |
| 47 | PLA-AR-OA-5400 | FLOOR THRESHOLD DETAILS - SHEET 01 | 1 : 5 | Printed scale 1:5 | 1:5 0/0 |
| 48 | PLA-AR-OA-5401 | FLOOR THRESHOLD DETAILS - SHEET 02 | 1 : 5 | Printed scale 1:5 | 1:5 2/2 |
| 49 | PLA-AR-OA-5402 | FLOOR THRESHOLD DETAILS - SHEET 03 | 1 : 5 | Printed scale 1:5 | 1:5 0/0 |
| 50 | PLA-AR-OA-5500 | DOOR DETAILS - SHEET 01 | 1 : 2 | Printed scale 1:2 | 1:2 0/0 |
| 51 | PLA-AR-OA-5501 | DOOR DETAILS - SHEET 02 | 1 : 2 | Printed scale 1:2 | 1:2 0/0 |
| 52 | PLA-AR-OA-5502 | DOOR DETAILS - SHEET 03 | 1 : 2 | Printed scale 1:2 | 1:2 0/0 |
| 53 | PLA-AR-OA-5503 | DOOR DETAILS - SHEET 04 | As indicated | Printed (by viewport) (1:5, 1:10) | 1:5 0/2 / 1:10 2/2 |
| 54 | PLA-AR-OA-5600 | JOINERY DETAILS - SHEET 01 | 1 : 5 | Calibrated 1:5 | 1:5 3/3 |
| 55 | PLA-AR-OA-5601 | JOINERY DETAILS - SHEET 02 | 1 : 2 | Printed scale 1:2 | 1:2 2/2 |
| 56 | PLA-AR-OA-5602 | JOINERY DETAILS - SHEET 03 | As indicated | Printed (by viewport) (1:5, 1:5, 1:5, 1:2, 1:5, 1:5, 1:5) | 1:5 0/0 / 1:2 0/0 |
| 57 | PLA-AR-OA-5700 | CEILING DETAILS - SHEET 01 | 1 : 5 | Printed scale 1:5 | 1:5 0/0 |
| 58 | PLA-AR-OA-6001 | DOOR SCHEDULE - STAGE 1 |  | By viewport (1:125) |  |
| 59 | PLA-AR-OA-6002 | DOOR TYPE DETAILS | As indicated | By viewport (1:125) |  |
| 60 | PLA-AR-OA-6003 | OVERALL DOOR TYPE SCHEDULE | 1 : 100 | Unreliable | 1:100 1/269 |
| 61 | PLA-AR-OA-6004 | OVERALL DOOR TYPE SCHEDULE | 1 : 100 | Unreliable | 1:100 6/301 |
| 62 | PLA-AR-OA-6005 | OVERALL DOOR TYPE SCHEDULE | 1 : 100 | By viewport (1:125) | 1:100 4/94 |
| 63 | PLA-AR-OA-8000 | STORAGE SCHEDULE - SHEET 01 | 1 : 100 | By viewport (1:125) | 1:100 2/249 |
| 64 | PLA-AR-OA-8001 | STORAGE SCHEDULE - SHEET 02 |  | No dimensions |  |
| 65 | PLA-AR-OA-8100 | JOINERY SCHEDULE - SHEET 1 |  | No scale printed |  |
| 66 | PLA-AR-OA-8101 | JOINERY SCHEDULE - SHEET 2 |  | No scale printed |  |
| 67 | PLA-AR-OA-8102 | JOINERY SCHEDULE - SHEET 3 |  | No scale printed |  |
| 68 | PLA-AR-OA-8103 | JOINERY SCHEDULE - SHEET 4 |  | By viewport (1:150) |  |
| 69 | PLA-AR-OA-8103 | JOINERY SCHEDULE - SHEET 4 |  | By viewport (1:150) |  |
| 70 | PLA-AR-A-0000 | COVER SHEET |  | No dimensions |  |
| 71 | PLA-AR-A-0001 | LEGEND SHEET | As indicated | No dimensions | 1:100 0/0 |
| 72 | PLA-AR-A-0003 | DRAWING REGISTER |  | No dimensions |  |
| 73 | PLA-AR-A-1001 | GENERAL ARRANGEMENT PLAN - LEVEL 01 | 1 : 100 | Calibrated 1:100 | 1:100 8/9 |
| 74 | PLA-AR-A-1002 | GENERAL ARRANGEMENT PLAN - ROOF | 1 : 100 | Calibrated 1:100 | 1:100 8/8 |
| 75 | PLA-AR-A-1100 | GENERAL REFLECTED CEILING PLANS - GROUND | As indicated | Calibrated 1:100 | 1:100 8/10 |
| 76 | PLA-AR-A-1101 | GENERAL REFLECTED CEILING PLANS - LEVEL 01 | As indicated | Calibrated 1:100 | 1:100 9/9 |
| 77 | PLA-AR-A-1200 | FIRE RESISTANCE LEVEL PLANS - GROUND | 1 : 100 | Calibrated 1:100 | 1:100 8/8 |
| 78 | PLA-AR-A-1201 | FIRE RESISTANCE LEVEL PLANS - LEVEL 01 | 1 : 100 | Calibrated 1:100 | 1:100 8/8 |
| 79 | PLA-AR-A-1202X | FIRE RESISTANCE LEVEL PLANS - ROOF | 1 : 100 | From grids 1:100 | 21/21 |
| 80 | PLA-AR-A-1300 | CONCRETE PROFILE PLANS - GROUND | 1 : 100 | By viewport (1:100) | 1:100 8/8 / 1:75 0/8 |
| 81 | PLA-AR-A-1301 | CONCRETE PROFILE PLANS - LEVEL 01 | 1 : 100 | By viewport (1:100) | 1:100 8/8 / 1:50 0/8 |
| 82 | PLA-AR-A-1400 | WALL SETOUT PLANS - GROUND | 1 : 100 | Calibrated 1:100 | 1:100 8/8 |
| 83 | PLA-AR-A-1401 | WALL SETOUT PLANS - LEVEL 01 | 1 : 100 | Calibrated 1:100 | 1:100 8/8 |
| 84 | PLA-AR-A-1402 | WALL SETOUT PLANS - ROOF | 1 : 100 | Calibrated 1:100 | 1:100 8/8 |
| 85 | PLA-AR-A-1500 | WATERPROOFING PLANS - GROUND | 1 : 100 | Calibrated 1:100 | 1:100 8/8 |
| 86 | PLA-AR-A-1501 | WATERPROOFING PLANS - LEVEL 01 | 1 : 100 | Calibrated 1:100 | 1:100 8/8 |
| 87 | PLA-AR-A-1502 | WATERPROOFING PLANS - ROOF | 1 : 100 | Calibrated 1:100 | 1:100 8/8 |
| 88 | PLA-AR-A-2000 | ELEVATION - NORTH & SOUTH | 1 : 100 | Image |  |
| 89 | PLA-AR-A-2001 | ELEVATION - EAST & WEST | 1 : 100 | Image |  |
| 90 | PLA-AR-A-2100 | SECTION 01-02 | 1 : 100 | Image |  |
| 91 | PLA-AR-A-2200 | DETAIL FACADE SECTIONS - SHEET 01 | 1 : 20 | Calibrated 1:20 | 1:20 7/7 |
| 92 | PLA-AR-A-2201 | DETAIL FACADE SECTIONS - SHEET 02 | 1 : 20 | Image |  |
| 93 | PLA-AR-A-2202 | DETAIL FACADE SECTIONS - SHEET 03 | 1 : 20 | Calibrated 1:20 | 1:20 4/4 |
| 94 | PLA-AR-A-2203 | DETAIL FACADE SECTIONS - SHEET 04 | 1 : 20 | Image |  |
| 95 | PLA-AR-A-3000 | CORES, STAIRS & RAMPS - SHEET 01 | As indicated | By viewport (1:50) | 1:100 0/85 / 1:50 64/85 |
| 96 | PLA-AR-A-4000 | APARTMENT TYPE - T01_PLAN & RCP | As indicated | Calibrated 1:50 | 1:50 8/11 |
| 97 | PLA-AR-A-4001 | APARTMENT TYPE - T02_PLAN & RCP | As indicated | Calibrated 1:50 | 1:50 7/13 |
| 98 | PLA-AR-A-4002 | APARTMENT TYPE - T03_PLAN & RCP | As indicated | Calibrated 1:50 | 1:50 9/11 |
| 99 | PLA-AR-A-4101 | COMMON AREA FITOUTS - GF CORRIDOR_ELEVATIONS | 1 : 50 | Printed scale 1:50 | 1:50 0/0 |
| 100 | PLA-AR-A-4102 | COMMON AREA FITOUTS - L1 CORRIDOR_PLAN & RCP | 1 : 50 | Printed scale 1:50 | 1:50 0/0 |
| 101 | PLA-AR-A-4103 | COMMON AREA FITOUTS - L1 CORRIDOR_ELEVATIONS | 1 : 50 | Printed scale 1:50 | 1:50 0/0 |
| 102 | PLA-AR-A-4105 | COMMON AREA FITOUTS - BIN ROOM_PLAN, RCP & ELEVATION | 1 : 50 | Printed scale 1:50 | 1:50 2/2 |
| 103 | PLA-AR-A-4801 | WET AREA FITOUTS B01 | As indicated | Calibrated 1:20 | 1:20 31/34 |
| 104 | PLA-AR-A-4802 | WET AREA FITOUTS L01 | As indicated | Calibrated 1:20 | 1:20 7/8 |
| 105 | PLA-AR-A-4901 | KITCHEN FITOUTS - K01 | As indicated | Calibrated 1:20 | 1:20 19/28 |
| 106 | PLA-AR-A-5000 | FACADE SECTION DETAILS - SHEET 01 | As indicated | Printed scale 1:5 | 1:100 0/0 / 1:5 0/0 |
| 107 | PLA-AR-A-5001 | FACADE SECTION DETAILS - SHEET 02 | As indicated | Printed scale 1:5 | 1:100 0/0 / 1:5 0/0 |
| 108 | PLA-AR-A-5004 | FACADE SECTION DETAILS - SHEET 05 | As indicated | Calibrated 1:5 | 1:5 3/4 |
| 109 | PLA-AR-A-5005 | FACADE SECTION DETAILS - SHEET 06 | As indicated | Printed scale 1:5 | 1:5 2/2 |
| 110 | PLA-AR-A-5100 | PLAN DETAILS - SHEET 01 | 1 : 5 | Printed scale 1:5 | 1:5 0/0 |
| 111 | PLA-AR-A-6000 | WINDOW MASTER SCHEDULE - SHEET 01 | 1 : 100 | Unreliable | 1:100 14/141 |
| 112 | PLA-AR-A-6001 | WINDOW TYPE SCHEDULE - SHEET 02 | As indicated | By viewport (1:50, 1:150, 1:200) |  |
| 113 | PLA-AR-A-6100 | DOOR MASTER SCHEDULE | 1 : 100 | Unreliable | 1:100 1/294 |
| 114 | PLA-AR-A-6101 | DOOR TYPE SCHEDULE | As indicated | No scale printed |  |
| 115 | PLA-AR-A-6102 | DOOR TYPE SCHEDULE | As indicated | By viewport (1:125) |  |
| 116 | PLA-AR-A-6200 | BALUSTRADE SCHEDULE | As indicated | Calibrated 1:20 | 1:20 19/26 |
| 117 | PLA-AR-A-6201 | LOUVRE SCREEN | As indicated | Printed scale 1:20 | 1:20 1/1 |
| 118 | PLA-AR-A-7001 | JOINERY DETAILS- JR01 - JC01 | As indicated | By viewport (1:20) | 1:20 4/10 |
| 119 | PLA-AR-A-7002 | JOINERY DETAILS - JC02-JC03 | 1 : 20 | Calibrated 1:20 | 1:20 4/8 |
| 120 | PLA-AR-B-0000 | COVER SHEET |  | No dimensions |  |
| 121 | PLA-AR-B-0001 | LEGEND SHEET | As indicated | No dimensions | 1:100 0/0 |
| 122 | PLA-AR-B-0002 | DRAWING REGISTER |  | No dimensions |  |
| 123 | PLA-AR-B-1000 | GENERAL ARRANGEMENT PLAN - GROUND | 1 : 100 | From grids 1:100 | 29/29 |
| 124 | PLA-AR-B-1000B | GENERAL ARRANGEMENT PLAN - BASEMENT | 1 : 100 | Calibrated 1:100 | 1:100 8/8 |
| 125 | PLA-AR-B-1001 | GENERAL ARRANGEMENT PLAN - LEVEL 01 | 1 : 100 | Calibrated 1:100 | 1:100 8/10 |
| 126 | PLA-AR-B-1002 | GENERAL ARRANGEMENT PLAN - LEVEL 02 | 1 : 100 | Calibrated 1:100 | 1:100 10/11 |
| 127 | PLA-AR-B-1003 | GENERAL ARRANGEMENT PLAN - LEVEL 03 | 1 : 100 | Calibrated 1:100 | 1:100 4/6 |
| 128 | PLA-AR-B-1004 | GENERAL ARRANGEMENT PLAN - ROOF | 1 : 100 | Calibrated 1:100 | 1:100 5/5 |
| 129 | PLA-AR-B-1100 | GENERAL REFLECTED CEILING PLANS - GROUND | As indicated | Calibrated 1:100 | 1:100 8/8 |
| 130 | PLA-AR-B-1100B | GENERAL REFLECTED CEILING PLANS - BASEMENT | As indicated | Calibrated 1:100 | 1:100 7/8 |
| 131 | PLA-AR-B-1102 | GENERAL REFLECTED CEILING PLANS - LEVEL 02 | As indicated | Calibrated 1:100 | 1:100 8/8 |
| 132 | PLA-AR-B-1103 | GENERAL REFLECTED CEILING PLANS - LEVEL 03 | As indicated | Calibrated 1:100 | 1:100 8/8 |
| 133 | PLA-AR-B-1200 | FIRE RESISTANCE LEVEL PLANS - GROUND | 1 : 100 | Calibrated 1:100 | 1:100 8/8 |
| 134 | PLA-AR-B-1200B | FIRE RESISTANCE LEVEL PLANS - BASEMENT | 1 : 100 | Calibrated 1:100 | 1:100 8/8 |
| 135 | PLA-AR-B-1201 | FIRE RESISTANCE LEVEL PLANS - LEVEL 01 | 1 : 100 | Calibrated 1:100 | 1:100 8/8 |
| 136 | PLA-AR-B-1202 | FIRE RESISTANCE LEVEL PLANS - LEVEL 02 | 1 : 100 | Calibrated 1:100 | 1:100 8/8 |
| 137 | PLA-AR-B-1203 | FIRE RESISTANCE LEVEL PLANS - LEVEL 03 | 1 : 100 | Calibrated 1:100 | 1:100 8/8 |
| 138 | PLA-AR-B-1300 | CONCRETE PROFILE PLANS - GROUND | 1 : 100 | By viewport (1:100) | 1:75 0/11 / 1:20 0/11 / 1:100 8/11 |
| 139 | PLA-AR-B-1300B | CONCRETE PROFILE PLANS - BASEMENT | 1 : 100 | Calibrated 1:100 | 1:100 8/8 |
| 140 | PLA-AR-B-1301 | CONCRETE PROFILE PLANS - LEVEL 01 | 1 : 100 | Calibrated 1:100 | 1:100 8/8 |
| 141 | PLA-AR-B-1302 | CONCRETE PROFILE PLANS - LEVEL 02 | 1 : 100 | Calibrated 1:100 | 1:100 8/8 |
| 142 | PLA-AR-B-1303 | CONCRETE PROFILE PLANS - LEVEL 03 | 1 : 100 | By viewport (1:100) | 1:100 8/8 / 1:75 0/8 |
| 143 | PLA-AR-B-1400 | WALL SETOUT PLANS - GROUND | 1 : 100 | Calibrated 1:100 | 1:100 8/8 |
| 144 | PLA-AR-B-1400B | WALL SETOUT PLANS - BASEMENT | 1 : 100 | Calibrated 1:100 | 1:100 8/8 |
| 145 | PLA-AR-B-1401 | WALL SETOUT PLANS - LEVEL 01 | 1 : 100 | Calibrated 1:100 | 1:100 9/9 |
| 146 | PLA-AR-B-1402 | WALL SETOUT PLANS - LEVEL 02 | 1 : 100 | Calibrated 1:100 | 1:100 8/8 |
| 147 | PLA-AR-B-1403 | WALL SETOUT PLANS - LEVEL 03 | 1 : 100 | Calibrated 1:100 | 1:100 8/8 |
| 148 | PLA-AR-B-1404 | WALL SETOUT PLANS - ROOF | 1 : 100 | Calibrated 1:100 | 1:100 8/8 |
| 149 | PLA-AR-B-1500 | WATERPROOFING PLANS - GROUND | 1 : 100 | Calibrated 1:100 | 1:100 6/6 |
| 150 | PLA-AR-B-1500B | WATERPROOFING PLANS - BASEMENT | 1 : 100 | Calibrated 1:100 | 1:100 8/8 |
| 151 | PLA-AR-B-1502 | WATERPROOFING PLANS - LEVEL 02 | 1 : 100 | Calibrated 1:100 | 1:100 8/8 |
| 152 | PLA-AR-B-1503 | WATERPROOFING PLANS - LEVEL 03 | 1 : 100 | Calibrated 1:100 | 1:100 8/8 |
| 153 | PLA-AR-B-1504 | WATERPROOFING PLANS - ROOF | 1 : 100 | Calibrated 1:100 | 1:100 8/8 |
| 154 | PLA-AR-B-2001 | ELEVATION - NORTH & SOUTH | 1 : 100 | Calibrated 1:100 | 1:100 12/12 |
| 155 | PLA-AR-B-2100 | SECTION 01 | 1 : 100 | Calibrated 1:100 | 1:100 21/21 |
| 156 | PLA-AR-B-2200 | DETAIL FACADE SECTIONS - SHEET 01 | 1 : 20 | Image |  |
| 157 | PLA-AR-B-2201 | DETAIL FACADE SECTIONS - SHEET 02 | 1 : 20 | Image |  |
| 158 | PLA-AR-B-2202 | DETAIL FACADE SECTIONS - SHEET 03 | 1 : 20 | Image |  |
| 159 | PLA-AR-B-2203 | DETAIL FACADE SECTIONS - SHEET 04 | 1 : 20 | Image |  |
| 160 | PLA-AR-B-2204X | DETAIL FACADE SECTIONS - SHEET 05 | 1 : 20 | Printed scale 1:20 | 1:20 0/0 |
| 161 | PLA-AR-B-3000 | CORES, STAIRS & RAMPS - SHEET 01 | As indicated | Calibrated 1:50 | 1:50 113/124 |
| 162 | PLA-AR-B-3001 | CORES, STAIRS & RAMPS - SHEET 02 | As indicated | Calibrated 1:50 | 1:50 67/79 |
| 163 | PLA-AR-B-3002 | CORES, STAIRS & RAMPS - SHEET 03 | As indicated | Calibrated 1:50 | 1:50 57/76 |
| 164 | PLA-AR-B-4001 | APARTMENT TYPE - T02_PLAN & RCP | As indicated | Calibrated 1:50 | 1:50 10/13 |
| 165 | PLA-AR-B-4002 | APARTMENT TYPE - T03_PLAN & RCP | As indicated | Calibrated 1:50 | 1:50 13/16 |
| 166 | PLA-AR-B-4003 | APARTMENT TYPE - T04_PLAN & RCP | As indicated | Calibrated 1:50 | 1:50 11/12 |
| 167 | PLA-AR-B-4004 | APARTMENT TYPE - T05.S_PLAN & RCP | As indicated | Calibrated 1:50 | 1:50 9/11 |
| 168 | PLA-AR-B-4005 | APARTMENT TYPE - T06_PLAN & RCP | As indicated | Calibrated 1:50 | 1:50 10/13 |
| 169 | PLA-AR-B-4008 | APARTMENT TYPE - T09_PLAN & RCP | As indicated | Calibrated 1:50 | 1:50 18/21 |
| 170 | PLA-AR-B-4009 | APARTMENT TYPE - T10_PLAN & RCP | As indicated | Calibrated 1:50 | 1:50 15/23 |
| 171 | PLA-AR-B-4010 | APARTMENT TYPE - T11_PLAN & RCP | As indicated | Calibrated 1:50 | 1:50 14/17 |
| 172 | PLA-AR-B-4100 | COMMON AREA FITOUTS - GF CORRIDOR_PLAN | 1 : 50 | Printed scale 1:50 | 1:50 0/0 |
| 173 | PLA-AR-B-4101 | COMMON AREA FITOUTS - GF CORRIDOR_RCP | As indicated | Printed scale 1:50 | 1:50 0/0 |
| 174 | PLA-AR-B-4102 | COMMON AREA FITOUTS - L01-02 CORRIDOR_PLAN | 1 : 50 | Printed scale 1:50 | 1:50 0/0 |
| 175 | PLA-AR-B-4103 | COMMON AREA FITOUTS - L01-02 CORRIDOR_RCP | As indicated | Printed scale 1:50 | 1:50 0/0 |
| 176 | PLA-AR-B-4106 | COMMON AREA FITOUTS - GF CORRIDOR_ELEVATIONS | 1 : 50 | Printed scale 1:50 | 1:50 0/0 |
| 177 | PLA-AR-B-4107 | COMMON AREA FITOUTS - L01-02 CORRIDOR_ELEVATIONS | 1 : 50 | Printed scale 1:50 | 1:50 0/0 |
| 178 | PLA-AR-B-4108 | COMMON AREA FITOUTS - L03 CORRIDOR_ELEVATIONS | 1 : 50 | Printed scale 1:50 | 1:50 0/0 |
| 179 | PLA-AR-B-4110 | COMMON AREA FITOUTS - MSB _ PLAN, RCP & ELEVATIONS | 1 : 50 | Printed scale 1:50 | 1:50 0/0 |
| 180 | PLA-AR-B-4801 | WET AREA FITOUTS - B21.B | As indicated | Calibrated 1:20 | 1:20 15/16 |
| 181 | PLA-AR-B-4801 | WET AREA FITOUTS - B21.B | As indicated | Calibrated 1:20 | 1:20 15/16 |
| 182 | PLA-AR-B-4802 | WET AREA FITOUS - B41.A | As indicated | Calibrated 1:20 | 1:20 12/13 |
| 183 | PLA-AR-B-4803 | WET AREA FITOUS - B41.B | As indicated | Calibrated 1:20 | 1:20 18/20 |
| 184 | PLA-AR-B-4803 | WET AREA FITOUS - B41.B | As indicated | Calibrated 1:20 | 1:20 18/20 |
| 185 | PLA-AR-B-4804 | WET AREA FITOUS - B41.C | As indicated | Calibrated 1:20 | 1:20 17/20 |
| 186 | PLA-AR-B-4902 | KITCHEN FITOUTS - K22 | As indicated | Calibrated 1:20 | 1:20 18/29 |
| 187 | PLA-AR-B-5000 | FACADE SECTION DETAILS - SHEET 01 | As indicated | Image |  |
| 188 | PLA-AR-B-5001 | FACADE SECTION DETAILS - SHEET 02 | As indicated | Image |  |
| 189 | PLA-AR-B-5002 | FACADE SECTION DETAILS - SHEET 03 | As indicated | Image |  |
| 190 | PLA-AR-B-5003 | FACADE SECTION DETAILS - SHEET 04 | As indicated | Image |  |
| 191 | PLA-AR-B-5004 | FACADE SECTION DETAILS - SHEET 05 | As indicated | Image |  |
| 192 | PLA-AR-B-5100 | PLAN DETAILS - SHEET 01 | 1 : 5 | Printed scale 1:5 | 1:5 0/0 |
| 193 | PLA-AR-B-5101 | PLAN DETAILS - SHEET 02 | 1 : 5 | Printed scale 1:5 | 1:5 1/1 |
| 194 | PLA-AR-B-6000 | WINDOW MASTER SCHEDULE - SHEET 01 | 1 : 100 | Unreliable | 1:100 8/400 |
| 195 | PLA-AR-B-6002 | WINDOW ELEVATIONS SCHEDULE - SHEET 03 | As indicated | By viewport (1:150) |  |
| 196 | PLA-AR-B-6100 | DOOR MASTER SCHEDULE - SHEET 01 | 1 : 100 | Unreliable | 1:100 4/306 |
| 197 | PLA-AR-B-6101 | DOOR MASTER SCHEDULE - SHEET 02 | 1 : 100 | Unreliable | 1:100 6/271 |
| 198 | PLA-AR-B-6101 | DOOR MASTER SCHEDULE - SHEET 02 | 1 : 100 | Unreliable | 1:100 6/271 |
| 199 | PLA-AR-B-6102 | DOOR ELEVATION SCHEDULE - SHEET 01 | As indicated | No scale printed |  |
| 200 | PLA-AR-B-6103 | DOOR ELEVATION SCHEDULE - SHEET 02 | As indicated | By viewport (1:125) |  |
| 201 | PLA-AR-B-6200 | BALUSTRADE SCHEDULE | As indicated | Calibrated 1:20 | 1:20 12/17 |
| 202 | PLA-AR-B-6201 | LOUVRE SCREEN | As indicated | Printed scale 1:20 | 1:20 1/1 |
| 203 | PLA-AR-B-7001 | JOINERY DETAILS JR25 | As indicated | Image |  |
| 204 | PLA-AR-B-7002 | JOINERY DETAILS - JM21 | As indicated | Calibrated 1:20 | 1:20 7/7 |
| 205 | PLA-AR-C-0000 | COVER SHEET |  | No dimensions |  |
| 206 | PLA-AR-C-0001 | LEGEND SHEET | As indicated | No dimensions | 1:100 0/0 |
| 207 | PLA-AR-C-0002 | DRAWING REGISTER |  | No dimensions |  |
| 208 | PLA-AR-C-1000 | GENERAL ARRANGEMENT PLAN - GROUND | 1 : 100 | By viewport (1:100) | 1:20 0/17 / 1:100 11/17 |
| 209 | PLA-AR-C-1001 | GENERAL ARRANGEMENT PLAN - LEVEL 01 | 1 : 100 | Calibrated 1:100 | 1:100 12/14 |
| 210 | PLA-AR-C-1002 | GENERAL ARRANGEMENT PLAN - LEVEL 02 | 1 : 100 | Calibrated 1:100 | 1:100 12/13 |
| 211 | PLA-AR-C-1003 | GENERAL ARRANGEMENT PLAN - LEVEL 03 | 1 : 100 | Calibrated 1:100 | 1:100 12/18 |
| 212 | PLA-AR-C-1004 | GENERAL ARRANGEMENT PLAN - ROOF | 1 : 100 | Calibrated 1:100 | 1:100 12/12 |
| 213 | PLA-AR-C-1100 | GENERAL REFLECTED CEILING PLANS - GROUND | 1 : 100 | Calibrated 1:100 | 1:100 12/22 |
| 214 | PLA-AR-C-1101 | GENERAL REFLECTED CEILING PLANS - LEVEL 01 | 1 : 100 | Calibrated 1:100 | 1:100 12/22 |
| 215 | PLA-AR-C-1102 | GENERAL REFLECTED CEILING PLANS - LEVEL 02 | 1 : 100 | Calibrated 1:100 | 1:100 12/20 |
| 216 | PLA-AR-C-1103 | GENERAL REFLECTED CEILING PLANS - LEVEL 03 | 1 : 100 | Calibrated 1:100 | 1:100 12/16 |
| 217 | PLA-AR-C-1200 | FIRE RESISTANCE LEVEL PLANS - GROUND | 1 : 100 | Calibrated 1:100 | 1:100 9/9 |
| 218 | PLA-AR-C-1201 | FIRE RESISTANCE LEVEL PLANS - LEVEL 01 | 1 : 100 | Calibrated 1:100 | 1:100 12/12 |
| 219 | PLA-AR-C-1202 | FIRE RESISTANCE LEVEL PLANS - LEVEL 02 | 1 : 100 | Calibrated 1:100 | 1:100 12/12 |
| 220 | PLA-AR-C-1203 | FIRE RESISTANCE LEVEL PLANS - LEVEL 03 | 1 : 100 | Calibrated 1:100 | 1:100 12/12 |
| 221 | PLA-AR-C-1204X | FIRE RESISTANCE LEVEL PLANS - ROOF | 1 : 100 | Calibrated 1:100 | 1:100 12/12 |
| 222 | PLA-AR-C-1300B | CONCRETE PROFILE PLANS - BASEMENT | 1 : 100 | Calibrated 1:100 | 1:100 12/12 |
| 223 | PLA-AR-C-1301 | CONCRETE PROFILE PLANS - LEVEL 01 | 1 : 100 | By viewport (1:100) | 1:50 0/12 / 1:75 0/12 / 1:100 12/12 |
| 224 | PLA-AR-C-1303 | CONCRETE PROFILE PLANS - LEVEL 03 | 1 : 100 | By viewport (1:100) | 1:100 12/12 / 1:75 0/12 / 1:10 0/12 |
| 225 | PLA-AR-C-1304 | CONCRETE PROFILE PLANS - ROOF | 1 : 100 | From grids 1:100 | 51/51 |
| 226 | PLA-AR-C-1400 | WALL SETOUT PLANS - GROUND | 1 : 100 | Calibrated 1:100 | 1:100 12/12 |
| 227 | PLA-AR-C-1401 | WALL SETOUT PLANS - LEVEL 01 | 1 : 100 | Calibrated 1:100 | 1:100 12/12 |
| 228 | PLA-AR-C-1402 | WALL SETOUT PLANS - LEVEL 02 | 1 : 100 | Calibrated 1:100 | 1:100 12/12 |
| 229 | PLA-AR-C-1404 | WALL SETOUT PLANS - ROOF | 1 : 100 | Calibrated 1:100 | 1:100 12/12 |
| 230 |  | WALL SCHEDULE |  | No scale printed |  |
| 231 | PLA-AR-C-1500 | WATERPROOFING PLANS - GROUND | 1 : 100 | Calibrated 1:100 | 1:100 11/11 |
| 232 | PLA-AR-C-1500B | WATERPROOFING PLANS -BASEMENT | 1 : 100 | Calibrated 1:100 | 1:100 12/12 |
| 233 | PLA-AR-C-1501 | WATERPROOFING PLANS - LEVEL 01 | 1 : 100 | Calibrated 1:100 | 1:100 12/12 |
| 234 | PLA-AR-C-1502 | WATERPROOFING PLANS - LEVEL 02 | 1 : 100 | Calibrated 1:100 | 1:100 12/12 |
| 235 | PLA-AR-C-1504 | WATERPROOFING PLANS - ROOF | 1 : 100 | Calibrated 1:100 | 1:100 12/12 |
| 236 | PLA-AR-C-2000 | ELEVATION - NORTH & SOUTH | 1 : 100 | Calibrated 1:100 | 1:100 16/16 |
| 237 | PLA-AR-C-2001 | ELEVATION - EAST | 1 : 100 | Calibrated 1:100 | 1:100 15/15 |
| 238 | PLA-AR-C-2002 | ELEVATION - WEST | 1 : 100 | Calibrated 1:100 | 1:100 13/13 |
| 239 | PLA-AR-C-2100 | SECTIONS 1 & 2 | 1 : 100 | Calibrated 1:100 | 1:100 22/22 |
| 240 | PLA-AR-C-2200 | DETAIL FACADE SECTIONS - SHEET 01 | 1 : 20 | Calibrated 1:20 | 1:20 9/10 |
| 241 | PLA-AR-C-2201 | DETAIL FACADE SECTIONS - SHEET 02 | 1 : 20 | Calibrated 1:20 | 1:20 6/6 |
| 242 | PLA-AR-C-2202 | DETAIL FACADE SECTIONS - SHEET 03 | 1 : 20 | Unreliable | 1:20 2/4 |
| 243 | PLA-AR-C-2203 | DETAIL FACADE SECTIONS - SHEET 04 | 1 : 20 | Printed scale 1:20 | 1:20 2/2 |
| 244 | PLA-AR-C-2205 | DETAIL FACADE SECTIONS - SHEET 06 | 1 : 20 | Calibrated 1:20 | 1:20 5/7 |
| 245 | PLA-AR-C-2206 | DETAIL FACADE SECTIONS - SHEET 07 | 1 : 20 | Calibrated 1:20 | 1:20 3/3 |
| 246 | PLA-AR-C-2207 | DETAIL FACADE SECTIONS - SHEET 08 | 1 : 20 | Printed scale 1:20 | 1:20 2/2 |
| 247 | PLA-AR-C-3000 | CORES, STAIRS & RAMPS - SHEET 01 / FS C1 | As indicated | Calibrated 1:50 | 1:50 97/111 |
| 248 | PLA-AR-C-3001 | CORES, STAIRS & RAMPS - SHEET 02 / FS C2 | As indicated | Calibrated 1:50 | 1:50 76/84 |
| 249 | PLA-AR-C-3002 | CORES, STAIRS & RAMPS - SHEET 03 - LIFT C1& C2 | As indicated | By viewport (1:50) | 1:100 0/99 / 1:50 87/99 |
| 250 | PLA-AR-C-4003 | APARTMENT TYPE - T04.P_PLAN & RCP | As indicated | Calibrated 1:50 | 1:50 14/21 |
| 251 | PLA-AR-C-4004 | APARTMENT TYPE - T05_PLAN & RCP | As indicated | Calibrated 1:50 | 1:50 12/13 |
| 252 | PLA-AR-C-4005 | APARTMENT TYPE - T06_PLAN & RCP | As indicated | Calibrated 1:50 | 1:50 11/16 |
| 253 | PLA-AR-C-4006 | APARTMENT TYPE - T07_PLAN & RCP | As indicated | Calibrated 1:50 | 1:50 9/14 |
| 254 | PLA-AR-C-4007 | APARTMENT TYPE - T08_PLAN & RCP | As indicated | Calibrated 1:50 | 1:50 17/23 |
| 255 | PLA-AR-C-4008 | APARTMENT TYPE - T09.P_PLAN & RCP | As indicated | Calibrated 1:50 | 1:50 17/19 |
| 256 | PLA-AR-C-4009 | APARTMENT TYPE - T10_PLAN & RCP | As indicated | Calibrated 1:50 | 1:50 8/11 |
| 257 | PLA-AR-C-4010 | APARTMENT TYPE - T11_PLAN & RCP | As indicated | Calibrated 1:50 | 1:50 12/19 |
| 258 | PLA-AR-C-4011 | APARTMENT TYPE - T12_PLAN & RCP | As indicated | Calibrated 1:50 | 1:50 12/19 |
| 259 | PLA-AR-C-4012 | APARTMENT TYPE - T13_PLAN & RCP | As indicated | Calibrated 1:50 | 1:50 15/21 |
| 260 | PLA-AR-C-4013 | APARTMENT TYPE - T14_PLAN & RCP | As indicated | Calibrated 1:50 | 1:50 12/16 |
| 261 | PLA-AR-C-4014 | APARTMENT TYPE - T15_PLAN & RCP | As indicated | Calibrated 1:50 | 1:50 14/15 |
| 262 | PLA-AR-C-4015 | APARTMENT TYPE - T16_PLAN & RCP | As indicated | Calibrated 1:50 | 1:50 18/18 |
| 263 | PLA-AR-C-4016 | APARTMENT TYPE - T17_PLAN & RCP | As indicated | Calibrated 1:50 | 1:50 10/16 |
| 264 | PLA-AR-C-4017 | APARTMENT TYPE - T18_PLAN & RCP | As indicated | Calibrated 1:50 | 1:50 14/17 |
| 265 | PLA-AR-C-4018 | APARTMENT TYPE - T19_PLAN & RCP | As indicated | Calibrated 1:50 | 1:50 13/15 |
| 266 | PLA-AR-C-4028 | APARTMENT TYPE - T02.S_PLAN & RCP | As indicated | Calibrated 1:50 | 1:50 8/11 |
| 267 | PLA-AR-C-4029 | APARTMENT TYPE - T04.S_PLAN & RCP | As indicated | Calibrated 1:50 | 1:50 14/19 |
| 268 | PLA-AR-C-4101 | COMMON AREA FITOUTS - GF CORRIDOR_ELEVATIONS | 1 : 50 | No dimensions | 1:50 0/0 |
| 269 | PLA-AR-C-4102 | COMMON AREA FITOUTS - L1-2 CORRIDOR_PLAN & RCP | As indicated | No dimensions | 1:50 0/0 |
| 270 | PLA-AR-C-4103 | COMMON AREA FITOUTS - L1-2 CORRIDOR_ELEVATIONS | 1 : 50 | No dimensions | 1:50 0/0 |
| 271 | PLA-AR-C-4104 | COMMON AREA FITOUTS - L3 CORRIDOR_PLAN & RCP | As indicated | No dimensions | 1:50 0/0 |
| 272 | PLA-AR-C-4107 | COMMON AREA FITOUTS - COMMS_PLAN, RCP& ELEVATIONS | As indicated | No dimensions | 1:50 0/0 |
| 273 | PLA-AR-C-4108 | COMMON AREA FITOUTS - MSB_PLAN, RCP& ELEVATIONS | As indicated | Calibrated 1:50 | 1:50 5/5 |
| 274 | PLA-AR-C-4802 | WET AREA FITOUTS - B22 | As indicated | Calibrated 1:20 | 1:20 29/32 |
| 275 | PLA-AR-C-4803 | WET AREA FITOUTS - B42 | As indicated | Calibrated 1:20 | 1:20 22/25 |
| 276 | PLA-AR-C-4804 | WET AREA FITOUTS - L21 | As indicated | Calibrated 1:20 | 1:20 8/9 |
| 277 | PLA-AR-C-4805 | WET AREA FITOUTS - B43 | As indicated | Calibrated 1:20 | 1:20 13/13 |
| 278 | PLA-AR-C-4806 | WET AREA FITOUTS - B23 | As indicated | Calibrated 1:20 | 1:20 9/10 |
| 279 | PLA-AR-C-4901 | KITCHEN FITOUTS - K21 | As indicated | Calibrated 1:20 | 1:20 6/12 |
| 280 | PLA-AR-C-4911 | KITCHEN FITOUTS - K41 | As indicated | Calibrated 1:20 | 1:20 5/9 |
| 281 | PLA-AR-C-4922 | KITCHEN FITOUTS - KI22 | As indicated | Calibrated 1:20 | 1:20 8/8 |
| 282 | PLA-AR-C-4931 | KITCHEN FITOUTS - KI41 | As indicated | Calibrated 1:20 | 1:20 6/6 |
| 283 | PLA-AR-C-4932 | KITCHEN FITOUTS - KI42 | As indicated | Calibrated 1:20 | 1:20 6/6 |
| 284 | PLA-AR-C-5000 | FACADE SECTION DETAILS - SHEET 01 | As indicated | Printed scale 1:5 | 1:5 1/1 |
| 285 | PLA-AR-C-5100 | PLAN DETAILS - SHEET 01 | 1 : 5 | Printed scale 1:5 | 1:5 0/0 |
| 286 | PLA-AR-C-5102 | PLAN DETAILS - SHEET 03 |  | No dimensions |  |
| 287 | PLA-AR-C-6002 | WINDOW ELEVATIONS SCHEDULE - SHEET 03 | As indicated | No scale printed |  |
| 288 | PLA-AR-C-6100 | DOOR SCHEDULE - SHEET 01 | 1 : 100 | Unreliable | 1:100 6/324 |
| 289 | PLA-AR-C-6101 | DOOR SCHEDULE - SHEET 02 | 1 : 100 | Unreliable | 1:100 2/310 |
| 290 | PLA-AR-C-6102 | DOOR SCHEDULE - SHEET 03 | 1 : 100 | Unreliable | 1:100 2/338 |
| 291 | PLA-AR-C-6104 | DOOR SCHEDULE - SHEET 05 | As indicated | No scale printed |  |
| 292 | PLA-AR-C-6104 | DOOR SCHEDULE - SHEET 05 | As indicated | No scale printed |  |
| 293 | PLA-AR-C-6200 | BALUSTRADE SCHEDULE | As indicated | Calibrated 1:20 | 1:20 15/22 |
| 294 | PLA-AR-C-6201 | LOUVRE SCREENS | As indicated | Calibrated 1:20 | 1:20 4/4 |
| 295 | PLA-AR-C-7002 | JOINERY DETAILS - JR22 | As indicated | Calibrated 1:20 | 1:20 8/13 |
| 296 | PLA-AR-C-7003 | JOINERY DETAILS - JR23 - JR24 | As indicated | Calibrated 1:20 | 1:20 4/4 |
| 297 | PLA-AR-C-7011 | JOINERY DETAILS - JC21 | As indicated | Unreliable | 1:20 0/5 |
| 298 | PLA-AR-C-7012 | JOINERY DETAILS - JC22 | As indicated | Unreliable | 1:20 1/6 |
| 299 | PLA-AR-C-7013 | JOINERY DETAILS - JC23 | As indicated | Unreliable | 1:20 1/3 |
| 300 | PLA-AR-C-7021 | JOINERY DETAILS - JCA | 1 : 20 | Calibrated 1:20 | 1:20 9/9 |
| 301 | PLA-AR-RAC-0000 | COVER PAGE |  | No dimensions |  |
| 302 | PLA-AR-RAC-0001 | LEGEND SHEET |  | No dimensions | 1:100 0/0 |
| 303 | PLA-AR-RAC-0002 | DRAWING REGISTER |  | No dimensions |  |
| 304 | PLA-AR-RAC-1000 | OVERALL GENERAL ARRANGEMENT PLAN - GROUND | 1:200 | Calibrated 1:200 | 1:200 7/13 |
| 305 | PLA-AR-RAC-1000B | OVERALL GENERAL ARRANGEMENT PLAN - BASEMENT | 1:200 | Calibrated 1:200 | 1:200 24/26 |
| 306 | PLA-AR-RAC-1001 | OVERALL GENERAL ARRANGEMENT PLAN - LEVEL 01 | 1:200 | Calibrated 1:200 | 1:200 8/15 |
| 307 | PLA-AR-RAC-1002 | OVERALL GENERAL ARRANGEMENT PLAN - LEVEL 02 | 1:200 | Calibrated 1:200 | 1:200 7/13 |
| 308 | PLA-AR-RAC-1003 | OVERALL GENERAL ARRANGEMENT PLAN - LEVEL 03 | 1:200 | Calibrated 1:200 | 1:200 7/11 |
| 309 | PLA-AR-RAC-1004 | OVERALL GENERAL ARRANGEMENT PLAN - ROOF | 1:200 | Calibrated 1:200 | 1:200 7/11 |
| 310 |  |  | 1 : 100 | From grids 1:100 | 41/53 |
| 311 |  | GENERAL ARRANGEMENT PLAN - BASEMENT - ZONE A | As indicated | From grids 1:100 | 46/57 |
| 312 |  | GENERAL ARRANGEMENT PLAN - BASEMENT - ZONE B | As indicated | From grids 1:100 | 58/58 |
| 313 | PLA-AR-RAC-1051 | GENERAL ARRANGEMENT PLAN - GROUND - ZONE B | 1 : 100 | From grids 1:100 | 58/64 |
| 314 | PLA-AR-RAC-1052 | GENERAL ARRANGEMENT PLAN - LEVEL 01 - ZONE A | 1 : 100 | From grids 1:100 | 77/78 |
| 315 | PLA-AR-RAC-1054 | GENERAL ARRANGEMENT PLAN - LEVEL 02 - ZONE A | 1 : 100 | From grids 1:100 | 77/78 |
| 316 | PLA-AR-RAC-1055 | GENERAL ARRANGEMENT PLAN - LEVEL 02 - ZONE B | 1 : 100 | From grids 1:100 | 51/51 |
| 317 | PLA-AR-RAC-1056 | GENERAL ARRANGEMENT PLAN - LEVEL 03 - ZONE A | 1 : 100 | From grids 1:100 | 77/78 |
| 318 | PLA-AR-RAC-1057 | GENERAL ARRANGEMENT PLAN - LEVEL 03 - ZONE B | 1 : 100 | From grids 1:100 | 51/51 |
| 319 | PLA-AR-RAC-1058 | GENERAL ARRANGEMENT PLAN - ROOF - ZONE A | 1 : 100 | From grids 1:100 | 77/78 |
| 320 | PLA-AR-RAC-1059 | GENERAL ARRANGEMENT PLAN - ROOF - ZONE B | 1 : 100 | From grids 1:100 | 58/58 |
| 321 | PLA-AR-RAC-1100 | OVERALL REFLECTED CEILING PLANS - GROUND | 1:200 | From grids 1:200 | 169/169 |
| 322 | PLA-AR-RAC-1100B | OVERALL REFLECTED CEILING PLANS - BASEMENT | 1:200 | From grids 1:200 | 156/172 |
| 323 | PLA-AR-RAC-1101 | OVERALL REFLECTED CEILING PLANS - LEVEL 01 | 1:200 | From grids 1:200 | 169/169 |
| 324 | PLA-AR-RAC-1102 | OVERALL REFLECTED CEILING PLANS - LEVEL 02 | As indicated | From grids 1:200 | 169/169 |
| 325 | PLA-AR-RAC-1103 | OVERALL REFLECTED CEILING PLANS - LEVEL 03 | As indicated | From grids 1:200 | 169/169 |
| 326 | PLA-AR-RAC-1150 | GENERAL REFLECTED CEILING PLANS - GROUND - ZONE A | 1 : 100 | From grids 1:100 | 69/76 |
| 327 | A-4000 | GENERAL REFLECTED CEILING PLANS - BASEMENT - ZONE A | 1 : 100 | Printed scale 1:100 | 1:100 0/1 |
| 328 | A-4000 | GENERAL REFLECTED CEILING PLANS - BASEMENT - ZONE B | 1 : 100 | From grids 1:100 | 43/43 |
| 329 | PLA-AR-RAC-1151 | GENERAL REFLECTED CEILING PLANS - GROUND - ZONE B | 1 : 100 | From grids 1:100 | 43/43 |
| 330 | PLA-AR-RAC-1152 | GENERAL REFLECTED CEILING PLANS - LEVEL 01 - ZONE A | 1 : 100 | From grids 1:100 | 69/71 |
| 331 | PLA-AR-RAC-1153 | GENERAL REFLECTED CEILING PLANS - LEVEL 01 - ZONE B | 1 : 100 | From grids 1:100 | 36/36 |
| 332 | PLA-AR-RAC-1154 | GENERAL REFLECTED CEILING PLANS - LEVEL 02 - ZONE A | 1 : 100 | From grids 1:100 | 71/73 |
| 333 | PLA-AR-RAC-1155 | GENERAL REFLECTED CEILING PLANS - LEVEL 02 - ZONE B | 1 : 100 | From grids 1:100 | 36/36 |
| 334 | PLA-AR-RAC-1156 | GENERAL REFLECTED CEILING PLANS - LEVEL 03 - ZONE A | 1 : 100 | From grids 1:100 | 71/73 |
| 335 | PLA-AR-RAC-1157 | GENERAL REFLECTED CEILING PLANS - LEVEL 03 - ZONE B | 1 : 100 | From grids 1:100 | 30/32 |
| 336 | PLA-AR-RAC-1200 | OVERALL FIRE RESISTANCE LEVEL PLANS - GROUND | As indicated | From grids 1:200 | 149/150 |
| 337 | PLA-AR-RAC-1200B | OVERALL FIRE RESISTANCE LEVEL PLANS - BASEMENT | As indicated | From grids 1:200 | 133/133 |
| 338 | PLA-AR-RAC-1201 | OVERALL FIRE RESISTANCE LEVEL PLANS - LEVEL 01 | As indicated | From grids 1:200 | 169/169 |
| 339 | PLA-AR-RAC-1202 | OVERALL FIRE RESISTANCE LEVEL PLANS - LEVEL 02 | As indicated | From grids 1:200 | 169/169 |
| 340 | PLA-AR-RAC-1203 | OVERALL FIRE RESISTANCE LEVEL PLANS - LEVEL 03 | As indicated | From grids 1:200 | 169/169 |
| 341 | PLA-AR-RAC-1204 | OVERALL FIRE RESISTANCE LEVEL PLANS - ROOF | As indicated | From grids 1:200 | 169/169 |
| 342 | PLA-AR-RAC-1250 | FIRE RESISTANCE PLAN - GROUND LEVEL - ZONE A | 1 : 100 | From grids 1:100 | 40/56 |
| 343 |  | FIRE RESISTANCE LEVEL PLAN - BASEMENT - ZONE A | 1 : 100 | Printed scale 1:100 | 1:100 0/0 |
| 344 |  | FIRE RESISTANCE LEVEL PLAN - BASEMENT - ZONE B | 1 : 100 | From grids 1:100 | 43/43 |
| 345 | PLA-AR-RAC-1251 | FIRE RESISTANCE PLAN - GROUND LEVEL - ZONE B | 1 : 100 | From grids 1:100 | 43/43 |
| 346 | PLA-AR-RAC-1252 | FIRE RESISTANCE LEVEL PLAN - LEVEL 01 - ZONE A | 1 : 100 | From grids 1:100 | 79/79 |
| 347 | PLA-AR-RAC-1253 | FIRE RESISTANCE LEVEL PLAN - LEVEL 01 - ZONE B | 1 : 100 | From grids 1:100 | 36/36 |
| 348 | PLA-AR-RAC-1254 | FIRE RESISTANCE LEVEL PLAN - LEVEL 02 - ZONE A | 1 : 100 | From grids 1:100 | 79/79 |
| 349 | PLA-AR-RAC-1255 | FIRE RESISTANCE LEVEL PLAN - LEVEL 02 - ZONE B | 1 : 100 | From grids 1:100 | 36/36 |
| 350 | PLA-AR-RAC-1256 | FIRE RESISTANCE LEVEL PLAN - LEVEL 03 - ZONE A | 1 : 100 | From grids 1:100 | 79/79 |
| 351 | PLA-AR-RAC-1257 | FIRE RESISTANCE LEVEL PLAN - LEVEL 03 - ZONE B | 1 : 100 | From grids 1:100 | 36/36 |
| 352 | PLA-AR-RAC-1258 | FIRE RESISTANCE LEVEL PLAN - ROOF - ZONE A | 1 : 100 | From grids 1:100 | 79/79 |
| 353 | PLA-AR-RAC-1259 | FIRE RESISTANCE LEVEL PLAN - ROOF - ZONE B | 1 : 100 | From grids 1:100 | 36/36 |
| 354 | PLA-AR-RAC-1300 | OVERALL CONCRETE PROFILE PLANS - GROUND | As indicated | By viewport (1:50, 1:200) | 1:100 0/39 |
| 355 | PLA-AR-RAC-1300B | OVERALL CONCRETE PROFILE PLANS - BASEMENT | As indicated | By viewport (1:200) | 1:100 0/21 |
| 356 | PLA-AR-RAC-1301 | OVERALL CONCRETE PROFILE PLANS - LEVEL 01 | As indicated | From grids 1:200 | 169/169 |
| 357 | PLA-AR-RAC-1302 | OVERALL CONCRETE PROFILE PLANS - LEVEL 02 | As indicated | By viewport (1:200) | 1:100 0/34 |
| 358 | PLA-AR-RAC-1303 | OVERALL CONCRETE PROFILE PLANS - LEVEL 03 | As indicated | By viewport (1:200) | 1:100 0/34 |
| 359 | PLA-AR-RAC-1304 | OVERALL CONCRETE PROFILE PLANS - ROOF | As indicated | By viewport (1:200) | 1:100 0/39 |
| 360 | PLA-AR-RAC-1350 | CONCRETE PROFILE PLANS - GROUND - ZONE A | 1 : 100 | Calibrated 1:100 | 1:100 22/29 |
| 361 |  | CONCRETE PROFILE PLANS - BASEMENT - ZONE A | 1 : 100 | Calibrated 1:100 | 1:100 12/12 |
| 362 |  | CONCRETE PROFILE PLANS - BASEMENT - ZONE B | 1 : 100 | Calibrated 1:100 | 1:100 12/12 |
| 363 | PLA-AR-RAC-1351 | CONCRETE PROFILE PLANS - GROUND - ZONE B | 1 : 100 | Calibrated 1:100 | 1:100 12/14 |
| 364 | PLA-AR-RAC-1352 | CONCRETE PROFILE PLANS - LEVEL 01 - ZONE A | 1 : 100 | From grids 1:100 | 79/79 |
| 365 | PLA-AR-RAC-1353 | CONCRETE PROFILE PLANS - LEVEL 01 - ZONE B | 1 : 100 | By viewport (1:100) | 1:100 12/12 / 1:75 0/12 |
| 366 | PLA-AR-RAC-1354 | CONCRETE PROFILE PLANS - LEVEL 02 - ZONE A | 1 : 100 | By viewport (1:100) | 1:50 0/25 / 1:100 23/25 |
| 367 | PLA-AR-RAC-1355 | CONCRETE PROFILE PLANS - LEVEL 02 - ZONE B | 1 : 100 | By viewport (1:100) | 1:50 0/12 / 1:100 12/12 |
| 368 | PLA-AR-RAC-1356 | CONCRETE PROFILE PLANS - LEVEL 03 - ZONE A | 1 : 100 | By viewport (1:100) | 1:50 0/25 / 1:100 23/25 |
| 369 | PLA-AR-RAC-1357 | CONCRETE PROFILE PLANS - LEVEL 03 - ZONE B | 1 : 100 | By viewport (1:100) | 1:50 0/12 / 1:100 12/12 |
| 370 | PLA-AR-RAC-1358 | CONCRETE PROFILE PLANS - ROOF - ZONE A | 1 : 100 | By viewport (1:100) | 1:100 22/29 / 1:50 0/29 / 1:75 0/29 |
| 371 | PLA-AR-RAC-1359 | CONCRETE PROFILE PLANS - ROOF - ZONE B | 1 : 100 | By viewport (1:100) | 1:25 0/12 / 1:50 0/12 / 1:100 12/12 |
| 372 | PLA-AR-RAC-1400 | OVERALL WALL SETOUT PLANS - GROUND | 1:200 | Calibrated 1:200 | 1:200 28/32 |
| 373 | PLA-AR-RAC-1400B | OVERALL WALL SETOUT PLANS - BASEMENT | As indicated | Calibrated 1:200 | 1:200 28/32 |
| 374 | PLA-AR-RAC-1401 | OVERALL WALL SETOUT PLANS - LEVEL 01 | As indicated | Calibrated 1:200 | 1:200 28/33 |
| 375 | PLA-AR-RAC-1402 | OVERALL WALL SETOUT PLANS - LEVEL 02 | As indicated | Calibrated 1:200 | 1:200 28/32 |
| 376 | PLA-AR-RAC-1403 | OVERALL WALL SETOUT PLANS - LEVEL 03 | As indicated | Calibrated 1:200 | 1:200 28/32 |
| 377 | PLA-AR-RAC-1404 | OVERALL WALL SETOUT PLANS - ROOF | As indicated | Calibrated 1:200 | 1:200 28/32 |
| 378 | PLA-AR-RAC-1450 | WALL SETOUT PLAN - GROUND LEVEL - ZONE A | 1 : 100 | Calibrated 1:100 | 1:100 12/12 |
| 379 | BW-190 | WALL SETOUT PLAN - BASEMENT - ZONE A | 1 : 100 | Calibrated 1:100 | 1:100 18/18 |
| 380 | A-1200 | WALL SETOUT PLAN - BASEMENT - ZONE B | 1 : 100 | From grids 1:100 | 43/43 |
| 381 | PLA-AR-RAC-1451 | WALL SETOUT PLAN - GROUND LEVEL - ZONE B | 1 : 100 | From grids 1:100 | 43/43 |
| 382 | PLA-AR-RAC-1452 | WALL SETOUT PLAN - LEVEL 01 - ZONE A | 1 : 100 | Calibrated 1:100 | 1:100 12/12 |
| 383 | PLA-AR-RAC-1453 | WALL SETOUT PLAN - LEVEL 01 - ZONE B | 1 : 100 | Calibrated 1:100 | 1:100 5/5 |
| 384 | PLA-AR-RAC-1454 | WALL SETOUT PLAN - LEVEL 02 - ZONE A | 1 : 100 | Calibrated 1:100 | 1:100 10/10 |
| 385 | PLA-AR-RAC-1455 | WALL SETOUT PLAN - LEVEL 02 - ZONE B | 1 : 100 | Calibrated 1:100 | 1:100 5/5 |
| 386 | PLA-AR-RAC-1456 | WALL SETOUT PLAN - LEVEL 03 - ZONE A | 1 : 100 | Calibrated 1:100 | 1:100 12/12 |
| 387 | PLA-AR-RAC-1457 | WALL SETOUT PLAN - LEVEL 03 - ZONE B | 1 : 100 | Calibrated 1:100 | 1:100 5/5 |
| 388 | PLA-AR-RAC-1458 | WALL SETOUT PLAN - ROOF - ZONE A | 1 : 100 | Calibrated 1:100 | 1:100 24/24 |
| 389 | PLA-AR-RAC-1459 | WALL SETOUT PLAN - ROOF - ZONE B | 1 : 100 | Calibrated 1:100 | 1:100 22/22 |
| 390 | PLA-AR-RAC-1500 | OVERALL WATERPROOFING PLAN - GROUND | As indicated | Calibrated 1:200 | 1:200 28/32 |
| 391 | PLA-AR-RAC-1500B | OVERALL WATERPROOFING PLAN - BASEMENT | As indicated | Calibrated 1:200 | 1:200 28/32 |
| 392 | PLA-AR-RAC-1501 | OVERALL WATERPROOFING PLAN - LEVEL 01 | As indicated | Calibrated 1:200 | 1:200 28/32 |
| 393 | PLA-AR-RAC-1502 | OVERALL WATERPROOFING PLAN - LEVEL 02 | As indicated | Calibrated 1:200 | 1:200 27/31 |
| 394 | PLA-AR-RAC-1503 | OVERALL WATERPROOFING PLAN - LEVEL 03 | As indicated | Calibrated 1:200 | 1:200 28/32 |
| 395 | PLA-AR-RAC-1504 | OVERALL WATERPROOFING PLAN - ROOF | As indicated | Calibrated 1:200 | 1:200 28/32 |
| 396 | PLA-AR-RAC-1550 | WATERPROOFING PLAN - GROUND LEVEL - ZONE A | 1 : 100 | From grids 1:100 | 36/51 |
| 397 |  | WATERPROOFING PLAN - BASEMENT - ZONE A | 1 : 100 | Printed scale 1:100 | 1:100 0/0 |
| 398 |  | WATERPROOFING PLAN - BASEMENT - ZONE B | 1 : 100 | From grids 1:100 | 36/36 |
| 399 | PLA-AR-RAC-1551 | WATERPROOFING PLAN - GROUND LEVEL - ZONE B | 1 : 100 | From grids 1:100 | 36/36 |
| 400 | PLA-AR-RAC-1552 | WATERPROOFING PLAN - LEVEL 01 - ZONE A | 1 : 100 | Calibrated 1:100 | 1:100 10/10 |
| 401 | PLA-AR-RAC-1553 | WATERPROOFING PLAN - LEVEL 01 - ZONE B | 1 : 100 | From grids 1:100 | 25/25 |
| 402 | PLA-AR-RAC-1554 | WATERPROOFING PLAN - LEVEL 02 - ZONE A | 1 : 100 | Calibrated 1:100 | 1:100 3/3 |
| 403 | PLA-AR-RAC-1555 | WATERPROOFING PLAN - LEVEL 02 - ZONE B | 1 : 100 | From grids 1:100 | 21/21 |
| 404 | PLA-AR-RAC-1556 | WATERPROOFING PLAN - LEVEL 03 - ZONE A | 1 : 100 | From grids 1:100 | 79/79 |
| 405 | PLA-AR-RAC-1557 | WATERPROOFING PLAN - LEVEL 03 - ZONE B | 1 : 100 | From grids 1:100 | 21/21 |
| 406 | PLA-AR-RAC-1558 | WATERPROOFING PLAN - ROOF - ZONE A | 1 : 100 | From grids 1:100 | 79/79 |
| 407 | PLA-AR-RAC-1559 | WATERPROOFING PLAN - ROOF - ZONE B | 1 : 100 | From grids 1:100 | 21/21 |
| 408 | PLA-AR-RAC-2000 | ELEVATION - EAST & WEST OVERALL | As indicated | Calibrated 1:200 | 1:200 18/18 |
| 409 | PLA-AR-RAC-2001 | ELEVATION - EAST PART 1 ALIGNED GRID RA & R1 | As indicated | Calibrated 1:100 | 1:100 10/10 |
| 410 | PLA-AR-RAC-2002 | ELEVATION - EAST PART 2 ALIGNED GRID RA & R1 | As indicated | Image |  |
| 411 | PLA-AR-RAC-2003 | ELEVATION - EAST PART 3 ALONG GRID RA & R1_3 | As indicated | Image |  |
| 412 | PLA-AR-RAC-2004 | ELEVATION - WEST PART 1 ALIGNED GRID RA & R1 | As indicated | Image |  |
| 413 | PLA-AR-RAC-2005 | ELEVATION - WEST PART 2 ALIGNED GRID A & 1 | As indicated | Image |  |
| 414 | PLA-AR-RAC-2006 | ELEVATION - SOUTH | As indicated | Image |  |
| 415 | PLA-AR-RAC-2007 | ELEVATION - NORTH | As indicated | Calibrated 1:100 | 1:100 31/31 |
| 416 | PLA-AR-RAC-2100 | SECTION 01 & 02 | 1 : 100 | Image |  |
| 417 | PLA-AR-RAC-2200 | DETAIL FACADE SECTIONS - SHEET 01 | 1 : 20 | Image |  |
| 418 | PLA-AR-RAC-2201 | DETAIL FACADE SECTIONS - SHEET 02 | 1 : 20 | Image |  |
| 419 | PLA-AR-RAC-2202 | DETAIL FACADE SECTIONS - SHEET 03 | 1 : 20 | Image |  |
| 420 | PLA-AR-RAC-2203 | DETAIL FACADE SECTIONS - SHEET 04 | 1 : 20 | Image |  |
| 421 | PLA-AR-RAC-2204 | DETAIL FACADE SECTIONS - SHEET 05 | 1 : 20 | Image |  |
| 422 | PLA-AR-RAC-2205 | DETAIL FACADE SECTIONS - SHEET 06 | 1 : 20 | Image |  |
| 423 | PLA-AR-RAC-2206 | DETAIL FACADE SECTIONS - SHEET 07 | 1 : 20 | Printed scale 1:20 | 1:20 1/1 |
| 424 | PLA-AR-RAC-2208 | DETAIL FACADE SECTIONS - SHEET 09 | 1 : 20 | Printed scale 1:20 | 1:20 1/1 |
| 425 | PLA-AR-RAC-2209 | DETAIL FACADE SECTIONS - SHEET 10 | 1 : 20 | Image |  |
| 426 | PLA-AR-RAC-3000 | CORES, STAIRS & RAMPS - SHEET 01 / FS RAC 1 | As indicated | Calibrated 1:50 | 1:50 107/117 |
| 427 | PLA-AR-RAC-3001 | CORES, STAIRS & RAMPS - SHEET 02 / FS RAC 2 | As indicated | Calibrated 1:50 | 1:50 143/160 |
| 428 | PLA-AR-RAC-3002 | CORES, STAIRS & RAMPS - SHEET 03 / FS RAC 3 | As indicated | Calibrated 1:50 | 1:50 70/83 |
| 429 | PLA-AR-RAC-3003 | CORES, STAIRS & RAMPS - SHEET 04 / FS RAC 4 | As indicated | Calibrated 1:50 | 1:50 66/77 |
| 430 | PLA-AR-RAC-3004 | CORES, STAIRS & RAMPS - SHEET 05 / LIFT R1 & R2 | As indicated | Calibrated 1:50 | 1:50 46/47 |
| 431 | PLA-AR-RAC-3005 | CORES, STAIRS & RAMPS - SHEET 06 / CARPARK DRIVEWAY | As indicated | Printed (by viewport) (1:100, 1:50, 1:50) | 1:50 0/0 / 1:100 0/0 |
| 432 | PLA-AR-RAC-4000 | RAC BEDROOM - TYPE MATRIX | As indicated | Calibrated 1:50 | 1:50 30/31 |
| 433 | PLA-AR-RAC-4001 | RAC BEDROOM - TYPE T01 PLAN & RCP | As indicated | Calibrated 1:20 | 1:20 9/9 |
| 434 | PLA-AR-RAC-4003 | RAC BEDROOM - TYPE T02 PLAN & RCP | As indicated | Calibrated 1:20 | 1:20 7/10 |
| 435 | PLA-AR-RAC-4004 | RAC BEDROOM - TYPE T03 PLAN & RCP | As indicated | Calibrated 1:20 | 1:20 7/7 |
| 436 | PLA-AR-RAC-4006 | RAC BEDROOM - TYPE T05 PLAN & RCP | As indicated | Calibrated 1:20 | 1:20 6/9 |
| 437 | PLA-AR-RAC-4007 | RAC BEDROOM - TYPE T06 PLAN & RCP | As indicated | Calibrated 1:20 | 1:20 8/8 |
| 438 | PLA-AR-RAC-4011 | RAC BEDROOM - TYPE T01 ELEVATIONS | As indicated | Calibrated 1:20 | 1:20 15/16 |
| 439 | PLA-AR-RAC-4012 | RAC BEDROOM - TYPE T02 ELEVATIONS | As indicated | Calibrated 1:20 | 1:20 4/4 |
| 440 | PLA-AR-RAC-4013 | RAC BEDROOM - TYPE T03 ELEVATIONS | As indicated | Calibrated 1:20 | 1:20 5/5 |
| 441 | PLA-AR-RAC-4014 | RAC BEDROOM - TYPE T04 ELEVATIONS |  | No dimensions |  |
| 442 | PLA-AR-RAC-4015 | RAC BEDROOM - TYPE T05 ELEVATIONS | As indicated | Calibrated 1:20 | 1:20 4/4 |
| 443 | PLA-AR-RAC-4016 | RAC BEDROOM - TYPE T06 ELEVATIONS | As indicated | Calibrated 1:20 | 1:20 5/5 |
| 444 | PLA-AR-RAC-4100 | COMMON AREA FITOUT - SF01-02 RECEPTION & CAFE - PLAN | As indicated | Calibrated 1:50 | 1:50 4/4 |
| 445 | PLA-AR-RAC-4101 | COMMON AREA FITOUT - SF01-02 RECEPTION & CAFE - RCP | As indicated | Printed scale 1:50 | 1:50 0/0 |
| 446 | PLA-AR-RAC-4102 | COMMON AREA FITOUT - SF01-02 RECEPTION & CAFE- ELEVATIONS | As indicated | Printed scale 1:50 | 1:50 0/0 |
| 447 | PLA-AR-RAC-4103 | COMMON AREA FITOUT - SF01-02 RECEPTION & CAFE- ELEVATION 2 | As indicated | Printed scale 1:50 | 1:50 0/0 |
| 448 | PLA-AR-RAC-4112 | COMMON AREA FITOUT - SF10 QUIET ROOMS - PLAN, RCP & ELEVATIONS | As indicated | Calibrated 1:50 | 1:50 3/3 |
| 449 | PLA-AR-RAC-4100 | COMMON AREA FITOUT - IL22 CLUBROOM - PLANS | As indicated | Printed scale 1:50 | 1:50 0/0 |
| 450 | PLA-AR-RAC-4114 | COMMON AREA FITOUT - IL22 CLUBROOM - RCP | As indicated | Printed scale 1:50 | 1:50 0/0 |
| 451 | PLA-AR-RAC-4115 | COMMON AREA FITOUT - IL22 CLUBROOM - ELEVATIONS | As indicated | Printed scale 1:50 | 1:50 0/0 |
| 452 | PLA-AR-RAC-4116 | COMMON AREA FITOUT - IL23 GYM - PLAN & RCP | As indicated | Printed scale 1:50 | 1:50 0/0 |
| 453 | PLA-AR-RAC-4117 | COMMON AREA FITOUT - IL23 GYM - ELEVATIONS 2 | As indicated | Printed scale 1:50 | 1:50 0/0 |
| 454 | PLA-AR-RAC-4117 | COMMON AREA FITOUT - IL23 GYM - ELEVATIONS | As indicated | Printed scale 1:50 | 1:50 0/0 |
| 455 | PLA-AR-RAC-4118 | COMMON AREA FITOUT - IL24 CINEMA_PLAN, RCP & ELEVATIONS | As indicated | Printed scale 1:50 | 1:50 1/1 |
| 456 | PLA-AR-RAC-4119 | COMMON AREA FITOUT - SB01 CENTRAL KITCHEN_PLAN & RCP | As indicated | Calibrated 1:50 | 1:50 3/4 |
| 457 | PLA-AR-RAC-4120 | COMMON AREA FITOUT - SB01 CENTRAL KITCHEN_ELEVATIONS 2 | As indicated | Unreliable | 1:50 1/4 |
| 458 | PLA-AR-RAC-4120 | COMMON AREA FITOUT - SB01 CENTRAL KITCHEN_ELEVATIONS | As indicated | Printed scale 1:50 | 1:50 0/0 |
| 459 | PLA-AR-RAC-4121 | COMMON AREA FITOUT - SB03 CENTRAL STORE ROOMS_PLAN & RCP | As indicated | Printed scale 1:50 | 1:50 0/0 |
| 460 | PLA-AR-RAC-4122 | COMMON AREA FITOUT - SB03 CENTRAL STORE ROOMS_ELEVATIONS | As indicated | Printed scale 1:50 | 1:50 0/0 |
| 461 | PLA-AR-RAC-4123 | COMMON AREA FITOUT - SB04 CLN / CHEM STORE_PLAN, RCP & ELEVATIONS | As indicated | Printed scale 1:50 | 1:50 1/1 |
| 462 | PLA-AR-RAC-4124 | COMMON AREA FITOUT - SB06 WASTE_PLAN, RCP & ELEVATIONS | As indicated | Calibrated 1:50 | 1:50 5/5 |
| 463 | PLA-AR-RAC-4126 | COMMON AREA FITOUT - SB09 STAFF ROOM_PLAN, RCP & ELEVATIONS | As indicated | Printed scale 1:50 | 1:50 0/0 |
| 464 | PLA-AR-RAC-4127 | COMMON AREA FITOUT - SB12 BUILDING MAINTENANCE_PLAN, RCP & ELEVATIONS | As indicated | Printed scale 1:50 | 1:50 0/0 |
| 465 | PLA-AR-RAC-4128 | COMMON AREA FITOUT - HHF01.GF LIFT LOBBY / CORRIDOR_PLAN & RCP | As indicated | Printed scale 1:50 | 1:50 0/0 |
| 466 | PLA-AR-RAC-4129 | COMMON AREA FITOUT - HHF01.GF LIFT LOBBY / CORRIDOR_ELEVATIONS | As indicated | Printed scale 1:50 | 1:50 0/0 |
| 467 | PLA-AR-RAC-4130 | COMMON AREA FITOUT - HHB03 DIRTY LINEN STORE_PLAN, RCP & ELEVATIONS | As indicated | Calibrated 1:50 | 1:50 6/6 |
| 468 | PLA-AR-RAC-4131 | COMMON AREA FITOUT - HHB09 GF STAFF CORRIDOR_PLAN & RCP | As indicated | Printed scale 1:50 | 1:50 2/2 |
| 469 | PLA-AR-RAC-4132 | COMMON AREA FITOUT - HHB09 GF STAFF CORRIDOR_ELEVATIONS | As indicated | Printed scale 1:50 | 1:50 0/0 |
| 470 | PLA-AR-RAC-4134 | COMMON AREA FITOUT - COMMS & MSB_ ELEVATIONS | As indicated | Printed scale 1:50 | 1:50 0/0 |
| 471 | PLA-AR-RAC-4134 | COMMON AREA FITOUT - COMMS & MSB_PLAN & RCP | As indicated | Printed scale 1:50 | 1:50 0/0 |
| 472 | PLA-AR-RAC-4135 | COMMON AREA FITOUT - HHF01.TYP LIFT LOBBY / CORRIDOR_PLAN, RCP & ELEVA | As indicated | Printed scale 1:50 | 1:50 0/0 |
| 473 | PLA-AR-RAC-4137 | COMMON AREA FITOUT - HHF02.TYP SITTING ROOM_PLAN, RCP & ELEVATIONS | As indicated | Printed scale 1:50 | 1:50 0/0 |
| 474 | PLA-AR-RAC-4138 | COMMON AREA FITOUT - HHF03/04 LIVING DINING ROOM NORTH - PLAN, RCP & E | As indicated | Printed scale 1:50 | 1:50 0/0 |
| 475 | PLA-AR-RAC-4139 | COMMON AREA FITOUT - HHF03/04 LIVING DINING ROOM SOUTH - PLAN, RCP & E | As indicated | Printed scale 1:50 | 1:50 0/0 |
| 476 | PLA-AR-RAC-4140 | COMMON AREA FITOUT - HHF05 KITCHEN NORTH - PLAN, RCP & ELEVATIONS | As indicated | Printed scale 1:50 | 1:50 0/0 |
| 477 | PLA-AR-RAC-4141 | COMMON AREA FITOUT - HHF05 KITCHEN SOUTH - PLAN, RCP & ELEVATIONS | As indicated | Printed scale 1:50 | 1:50 0/0 |
| 478 | PLA-AR-RAC-4142 | COMMON AREA FITOUT - HHF09.TYP RESIDENT HALLWAY - PLAN & RCP | As indicated | Printed scale 1:50 | 1:50 0/2 |
| 479 | PLA-AR-RAC-4143 | COMMON AREA FITOUT - HHF09.TYP RESIDENT HALLWAY - ELEVATIONS | As indicated | Printed scale 1:50 | 1:50 1/1 |
| 480 | PLA-AR-RAC-4144 | COMMON AREA FITOUT - HHF11 LIFTER STORES - PLAN, RCP & ELEVATIONS | As indicated | Calibrated 1:50 | 1:50 4/4 |
| 481 | PLA-AR-RAC-4145 | COMMON AREA FITOUT - HHB01 CLINICAL ROOM - PLAN, RCP & ELEVATIONS | As indicated | Calibrated 1:50 | 1:50 10/10 |
| 482 | PLA-AR-RAC-4146 | COMMON AREA FITOUT - HHB02 DIRTY UTILITY - PLAN, RCP & ELEVATIONS | As indicated | Calibrated 1:50 | 1:50 3/3 |
| 483 | PLA-AR-RAC-4147 | COMMON AREA FITOUT - HHB04 CLEAN LINEN STORES_PLAN, RCP & ELEVATIONS | As indicated | Printed scale 1:50 | 1:50 2/2 |
| 484 | PLA-AR-RAC-4148 | COMMON AREA FITOUT - HHB05 BULK STORE_PLAN, RCP & ELEVATIONS | As indicated | Printed scale 1:50 | 1:50 2/2 |
| 485 | PLA-AR-RAC-4149 | COMMON AREA FITOUT - HHB06/07 EQUIP & CLN'S STORE_PLAN, RCP & ELEVATIO | As indicated | Calibrated 1:50 | 1:50 8/8 |
| 486 | PLA-AR-RAC-4150 | COMMON AREA FITOUT - HHB09.TYP STAFF CORRIDOR_PLAN & RCP | As indicated | Printed scale 1:50 | 1:50 0/0 |
| 487 | PLA-AR-RAC-4151 | COMMON AREA FITOUT - HHB09.TYP STAFF CORRIDOR_ELEVATIONS | As indicated | Printed scale 1:50 | 1:50 0/0 |
| 488 | PLA-AR-RAC-4152 | COMMON AREA FITOUT - SITE FOH CORRIDOR | As indicated | Printed scale 1:50 | 1:50 0/0 |
| 489 | PLA-AR-RAC-4153 | COMMON AREA FITOUT - SITE BOH CORRIDOR | As indicated | Printed scale 1:50 | 1:50 0/0 |
| 490 | PLA-AR-RAC-4700 | COMMON WET AREA FITOUT - CLUBROOM AMENITIES_PLAN | As indicated | Calibrated 1:20 | 1:20 16/26 |
| 491 | PLA-AR-RAC-4701 | COMMON WET AREA FITOUT - CLUBROOM AMENITIES_ RCP | As indicated | Printed scale 1:20 | 1:20 0/0 |
| 492 | PLA-AR-RAC-4702 | COMMON WET AREA FITOUT - CLUBROOM AMENITIES_ACC ELEVATIONS | As indicated | Calibrated 1:20 | 1:20 8/8 |
| 493 | PLA-AR-RAC-4703 | COMMON WET AREA FITOUT - CLUBROOM AMENITIES_F.W.C ELEVATIONS | As indicated | Calibrated 1:20 | 1:20 15/16 |
| 494 | PLA-AR-RAC-4704 | COMMON WET AREA FITOUT - CLUBROOM AMENITIES_M.WC ELEVATIONS | As indicated | Calibrated 1:20 | 1:20 6/6 |
| 495 | PLA-AR-RAC-4705 | COMMON WET AREA FITOUT - MPR AMENITIES_PLAN | As indicated | Calibrated 1:20 | 1:20 10/15 |
| 496 | PLA-AR-RAC-4706 | COMMON WET AREA FITOUT - MPR AMENITIES_ RCP | As indicated | Printed scale 1:20 | 1:20 0/0 |
| 497 | PLA-AR-RAC-4707 | COMMON WET AREA FITOUT - MPR AMENITIES_ACC ELEVATIONS | As indicated | Calibrated 1:20 | 1:20 6/6 |
| 498 | PLA-AR-RAC-4708 | COMMON WET AREA FITOUT - MPR AMENITIES_F.W.C ELEVATIONS | As indicated | Calibrated 1:20 | 1:20 3/3 |
| 499 | PLA-AR-RAC-4709 | COMMON WET AREA FITOUT - MPR AMENITIES_M.WC ELEVATIONS | As indicated | Calibrated 1:20 | 1:20 8/8 |
| 500 | PLA-AR-RAC-4710 | COMMON WET AREA FITOUT - GYM AMENITIES_PLAN & RCP | As indicated | Calibrated 1:20 | 1:20 7/7 |
| 501 | PLA-AR-RAC-4711 | COMMON WET AREA FITOUT - GYM AMENITIES_ELEVATIONS | As indicated | Calibrated 1:20 | 1:20 11/11 |
| 502 | PLA-AR-RAC-4712 | COMMON WET AREA FITOUT - ADMIN EOT AMENITIES_PLAN & RCP | As indicated | Calibrated 1:20 | 1:20 16/22 |
| 503 | PLA-AR-RAC-4713 | COMMON WET AREA FITOUT - ADMIN EOT AMENITIES_RCP | As indicated | Printed scale 1:20 | 1:20 0/0 |
| 504 | PLA-AR-RAC-4714 | COMMON WET AREA FITOUT - ADMIN EOT AMENITIES_M.WC ELEVATIONS | As indicated | Calibrated 1:20 | 1:20 10/10 |
| 505 | PLA-AR-RAC-4715 | COMMON WET AREA FITOUT - ADMIN EOT AMENITIES_F.WC ELEVATIONS | As indicated | Calibrated 1:20 | 1:20 4/4 |
| 506 | PLA-AR-RAC-4716 | COMMON WET AREA FITOUT - ADMIN EOT AMENITIES_ACC ELEVATIONS | As indicated | Calibrated 1:20 | 1:20 4/4 |
| 507 | PLA-AR-RAC-4717 | COMMON WET AREA FITOUT - HHF06 WC'S_NORTH PLAN, RCP & ELEVATIONS | As indicated | Calibrated 1:20 | 1:20 8/8 |
| 508 | PLA-AR-RAC-4718 | COMMON WET AREA FITOUT - HHF06 WC'S_SOUTH PLAN, RCP & ELEVATIONS | As indicated | Calibrated 1:20 | 1:20 5/5 |
| 509 | PLA-AR-RAC-4719 | COMMON WET AREA FITOUT - HHF07 RESI LAUNDRIES_NORTH PLAN, RCP & ELEVAT | As indicated | Calibrated 1:20 | 1:20 20/20 |
| 510 | PLA-AR-RAC-4720 | COMMON WET AREA FITOUT - HHF07 RESI LAUNDRIES_SOUTH PLAN, RCP & ELEVAT | 1 : 20 | Calibrated 1:20 | 1:20 4/4 |
| 511 | PLA-AR-RAC-4721 | COMMON WET AREA FITOUT - HHB10 STAFF WC_PLAN, RCP & ELEVATIONS | As indicated | Calibrated 1:20 | 1:20 8/8 |
| 512 | PLA-AR-RAC-4722 | COMMON WET AREA FITOUT - HHB08 HAND WASH STATION_PLAN & ELEVATION | As indicated | Printed scale 1:20 | 1:20 1/2 |
| 513 | PLA-AR-RAC-4723 | COMMON WET AREA FITOUT - HHF10 HAND WASH STATION_PLAN & ELEVATION | 1 : 20 | Printed scale 1:20 | 1:20 2/2 |
| 514 | PLA-AR-RAC-4800 | RAC ENSUITE - TYPE MATRIX | As indicated | By viewport (1:20) | 1:100 0/3 / 1:20 3/3 |
| 515 | PLA-AR-RAC-4801 | RAC ENSUITE - TYPE EN01 PLAN & RCP | 1:20 | By viewport (1:20) | 1:100 0/36 / 1:20 30/36 |
| 516 | PLA-AR-RAC-5000 | FACADE SECTION DETAILS - SHEET 01 | As indicated | Calibrated 1:5 | 1:5 7/7 |
| 517 | PLA-AR-RAC-5001 | FACADE SECTION DETAILS - SHEET 02 | As indicated | Printed scale 1:5 | 1:5 0/0 |
| 518 | PLA-AR-RAC-5002 | FACADE SECTION DETAILS - SHEET 03 | As indicated | Calibrated 1:5 | 1:5 3/3 |
| 519 | PLA-AR-RAC-5003 | FACADE SECTION DETAILS - SHEET 04 | As indicated | By viewport (1:5) | 1:100 0/3 / 1:5 3/3 |
| 520 | PLA-AR-RAC-5004 | FACADE SECTION DETAILS - SHEET 05 | As indicated | Image |  |
| 521 | PLA-AR-RAC-5005 | FACADE SECTION DETAILS - SHEET 06 | As indicated | Image |  |
| 522 | PLA-AR-RAC-5006 | FACADE SECTION DETAILS - SHEET 07 | As indicated | Image |  |
| 523 | PLA-AR-RAC-5007 | FACADE SECTION DETAILS - SHEET 08 | As indicated | Image |  |
| 524 | PLA-AR-RAC-5009 | FACADE SECTION DETAILS - SHEET 10 | As indicated | Image |  |
| 525 | PLA-AR-RAC-5010 | FACADE SECTION DETAILS - SHEET 11 | As indicated | Image |  |
| 526 | PLA-AR-RAC-5011 | FACADE SECTION DETAILS - SHEET 12 | 1 : 5 | Printed scale 1:5 | 1:5 0/0 |
| 527 | PLA-AR-RAC-5100 | PLAN DETAILS - SHEET 01 | 1 : 50 | Calibrated 1:50 | 1:50 7/11 |
| 528 | PLA-AR-RAC-5101 | PLAN DETAILS - SHEET 02 | 1 : 5 | Unreliable | 1:5 2/3 |
| 529 | PLA-AR-RAC-5102 | PLAN DETAILS - SHEET 03 | 1 : 5 | Calibrated 1:5 | 1:5 10/10 |
| 530 | PLA-AR-RAC-6000 | WINDOW LIST SCHEDULE - SHEET 01 | 1 : 100 | Unreliable | 1:100 0/624 |
| 531 | PLA-AR-RAC-6001 | WINDOW ELEVATIONS SCHEDULE - SHEET 02 | As indicated | No scale printed |  |
| 532 | PLA-AR-RAC-6002 | WINDOW ELEVATIONS SCHEDULE - SHEET 03 | As indicated | No scale printed |  |
| 533 | PLA-AR-RAC-6100 | DOOR SCHEDULE - SHEET 01 | 1 : 100 | Unreliable | 1:100 17/377 |
| 534 | PLA-AR-RAC-6101 | DOOR SCHEDULE - SHEET 02 | 1 : 100 | Unreliable | 1:100 43/384 |
| 535 | PLA-AR-RAC-6102 | DOOR SCHEDULE - SHEET 03 | 1 : 100 | Unreliable | 1:100 40/372 |
| 536 | PLA-AR-RAC-6103 | DOOR SCHEDULE - SHEET 04 | 1 : 100 | Unreliable | 1:100 37/352 |
| 537 | PLA-AR-RAC-6104 | DOOR SCHEDULE - SHEET 05 | As indicated | By viewport (1:50, 1:125) |  |
| 538 | PLA-AR-RAC-6105 | DOOR SCHEDULE - SHEET 06 | As indicated | By viewport (1:125) |  |
| 539 | PLA-AR-RAC-6106 | DOOR SCHEDULE - SHEET 07 | As indicated | No scale printed |  |
| 540 | PLA-AR-RAC-6150 | JOINERY DOOR SCHEDULE - SHEET 01 | 1 : 100 | Unreliable | 1:100 0/59 |
| 541 | PLA-AR-RAC-6151 | JOINERY DOOR SCHEDULE - SHEET 02 | As indicated | No scale printed |  |
| 542 | PLA-AR-RAC-6200 | BALUSTRADE SCHEDULE | As indicated | Calibrated 1:20 | 1:20 17/28 |
| 543 | PLA-AR-RAC-6201 | LOUVRE SCREEN | As indicated | By viewport (1:20) | 1:20 4/11 |
| 544 | PLA-AR-RAC-7000 | RAC JOINERY DETAILS - TYPE JR01 | 1 : 20 | Calibrated 1:20 | 1:20 31/44 |
| 545 | PLA-AR-RAC-7001 | RAC JOINERY DETAILS - TYPE JR02 | 1 : 20 | Calibrated 1:20 | 1:20 11/11 |
| 546 | PLA-AR-RAC-7101 | COMMON AREA JOINERY DETAILS - TYPE JO01 RECEPTION BACKLINE | 1 : 20 | Calibrated 1:20 | 1:20 12/13 |
| 547 | PLA-AR-RAC-7102 | COMMON AREA JOINERY DETAILS - TYPE JO02 RECEPTION DESK | 1 : 20 | Calibrated 1:20 | 1:20 6/7 |
| 548 | PLA-AR-RAC-7103 | COMMON AREA JOINERY DETAILS - TYPE JO03 CAFÉ BACKLINE | As indicated | By viewport (1:20) | 1:20 8/9 / 1:50 0/9 |
| 549 | PLA-AR-RAC-7104 | COMMON AREA JOINERY DETAILS - TYPE JO04 CAFÉ ISLAND BENCH | 1 : 20 | Calibrated 1:20 | 1:20 13/16 |
| 550 | PLA-AR-RAC-7105 | COMMON AREA JOINERY DETAILS - TYPE JO05 CAFÉ BOH BENCH | 1 : 20 | Calibrated 1:20 | 1:20 30/30 |
| 551 | PLA-AR-RAC-7106 | COMMON AREA JOINERY DETAILS - TYPE JK06 MPR KITCHENETTE | As indicated | By viewport (1:20) | 1:20 9/10 / 1:50 1/10 |
| 552 | PLA-AR-RAC-7107 | COMMON AREA JOINERY DETAILS - TYPE JO07 MPR STORE CUPBOARD | 1 : 20 | Calibrated 1:20 | 1:20 3/3 |
| 553 | PLA-AR-RAC-7109 | COMMON AREA JOINERY DETAILS - TYPE JO09 TRAINING ROOM KITCHENETTE | 1 : 20 | Calibrated 1:20 | 1:20 10/10 |
| 554 | PLA-AR-RAC-7111 | COMMON AREA JOINERY DETAILS - TYPE JO11 HAIR SALON FOH CUPBOARD | 1 : 20 | Calibrated 1:20 | 1:20 14/15 |
| 555 | PLA-AR-RAC-7112 | COMMON AREA JOINERY DETAILS - TYPE JK12 CLUBROOM KITCHEN BACKLINE | 1 : 20 | Calibrated 1:20 | 1:20 23/32 |
| 556 | PLA-AR-RAC-7113 | COMMON AREA JOINERY DETAILS - TYPE JKI13 CLUBROOM KITCHEN ISLAND | 1 : 20 | Calibrated 1:20 | 1:20 16/16 |
| 557 | PLA-AR-RAC-7115 | COMMON AREA JOINERY DETAILS - TYPE JO15 CLUBROOM PRIVATE DINING CREDEN | 1 : 20 | Calibrated 1:20 | 1:20 16/17 |
| 558 | PLA-AR-RAC-7116 | COMMON AREA JOINERY DETAILS - TYPE JO16 CLUBROOM TV BOOKCASE | 1 : 20 | Calibrated 1:20 | 1:20 10/12 |
| 559 | PLA-AR-RAC-7118 | COMMON AREA JOINERY DETAILS - TYPE JO18 GYM RECEPTION DESK | 1 : 20 | Calibrated 1:20 | 1:20 9/9 |
| 560 | PLA-AR-RAC-7118 | COMMON AREA JOINERY DETAILS - TYPE JO18 GYM RECEPTION DESK | 1 : 20 | Calibrated 1:20 | 1:20 9/9 |
| 561 | PLA-AR-RAC-7120 | COMMON AREA JOINERY DETAILS - TYPE JO20 GYM BANQUETTE SEAT | 1 : 20 | Printed scale 1:20 | 1:20 2/2 |
| 562 | PLA-AR-RAC-7121 | COMMON AREA JOINERY DETAILS - TYPE JO21 CINEMA KITCHENETTE | 1 : 20 | Calibrated 1:20 | 1:20 11/11 |
| 563 | PLA-AR-RAC-7122 | COMMON AREA JOINERY DETAILS - TYPE JO22 STAFF ADMIN PRINTING | 1 : 20 | Calibrated 1:20 | 1:20 10/10 |
| 564 | PLA-AR-RAC-7123 | COMMON AREA JOINERY DETAILS - TYPE JO23 STAFF BREAKOUT DESK | 1 : 20 | Calibrated 1:20 | 1:20 7/7 |
| 565 | PLA-AR-RAC-7124 | COMMON AREA JOINERY DETAILS - TYPE JO24 STAFF BREAKOUT KITCHEN | 1 : 20 | Calibrated 1:20 | 1:20 3/4 |
| 566 | PLA-AR-RAC-7126 | COMMON AREA JOINERY DETAILS - TYPE JO26 MPR CHAPEL BACKLINE | 1 : 20 | Calibrated 1:20 | 1:20 15/15 |
| 567 | PLA-AR-RAC-7127 | COMMON AREA JOINERY DETAILS - TYPE JO27 HOUSEHOLD LIVING FIRE | 1 : 20 | Calibrated 1:20 | 1:20 8/11 |
| 568 | PLA-AR-RAC-7129 | COMMON AREA JOINERY DETAILS - TYPE JK29 HOUSEHOLD NORTH KITCHEN BACKLI | 1 : 20 | Calibrated 1:20 | 1:20 19/28 |
| 569 | PLA-AR-RAC-7130 | COMMON AREA JOINERY DETAILS - TYPE JKI30 HOUSEHOLD NORTH KITCHEN ISLAN | 1 : 20 | Calibrated 1:20 | 1:20 19/20 |
| 570 | PLA-AR-RAC-7131 | COMMON AREA JOINERY DETAILS - TYPE JK31 HOUSEHOLD SOUTH KITCHEN BACKLI | 1 : 20 | Calibrated 1:20 | 1:20 13/22 |
| 571 | PLA-AR-RAC-7132 | COMMON AREA JOINERY DETAILS - TYPE JKI32 HOUSEHOLD SOUTH KITCHEN ISLAN | 1 : 20 | Calibrated 1:20 | 1:20 7/7 |
| 572 | PLA-AR-RAC-7133 | COMMON AREA JOINERY DETAILS - TYPE JK33 HOUSEHOLD NORTH KITCHEN STORE | 1 : 20 | Calibrated 1:20 | 1:20 4/5 |
| 573 | PLA-AR-RAC-7134 | COMMON AREA JOINERY DETAILS - TYPE JO34 BATHROOM COMMON TYPICAL VANITY | 1 : 20 | Calibrated 1:20 | 1:20 7/7 |
| 574 | PLA-AR-RAC-7135 | COMMON AREA JOINERY DETAILS - TYPE JO35 BATHROOM COMMON LOCKERS | 1 : 20 | Calibrated 1:20 | 1:20 8/8 |
| 575 | PLA-AR-RAC-7136 | COMMON AREA JOINERY DETAILS - TYPE JO36 HOUSEHOLD RESIDENT TYPICAL LAU | 1 : 20 | Calibrated 1:20 | 1:20 15/17 |
| 576 | PLA-AR-RAC-7137 | COMMON AREA JOINERY DETAILS - TYPE JO37 MEMORY BOX | 1 : 20 | Unreliable | 1:20 1/3 |
| 577 | PLA-AR-RAC-7138 | COMMON AREA JOINERY DETAILS - TYPE JO38 RECEPTION ROUND TABLE | 1 : 20 | Calibrated 1:20 | 1:20 4/4 |
| 578 | PLA-AR-RAC-7140 | COMMON AREA JOINERY DETAILS - TYPE JO40 HAIR SALON STYLING STATION | 1 : 20 | Calibrated 1:20 | 1:20 3/3 |
| 579 | PLA-AR-RAC-7141 | COMMON AREA JOINERY DETAILS - TYPE JO40 HAIR SALON MIRROR | 1 : 20 | Calibrated 1:20 | 1:20 13/15 |
| 580 | PLA-AR-RAC-7143 | COMMON AREA JOINERY DETAILS - TYPE JO43 TYPICAL LAUNDRY WORK BENCH & I | 1 : 20 | Calibrated 1:20 | 1:20 5/5 |
| 581 | PLA-AR-RAC-7144 | COMMON AREA JOINERY DETAILS - TYPE JO44, JO45, JO46, JO47 - CLINICAL R | 1 : 20 | Calibrated 1:20 | 1:20 19/25 |
