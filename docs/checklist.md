# Review checklist

These are the **topics** to check. Clause numbers are deliberately left out:
they change between NCC editions and must be found in the library each time
with `tools/standards.py search`, never written from memory. The search terms
are only starting points.

For each item: find the governing clause, read its exemptions and referenced
Standards, then find the evidence on the drawings.

## 1. Egress (NCC Section D, provision for escape)
| Check | Evidence on drawings | Search terms |
|---|---|---|
| Number of exits per storey | GA plans | "number of exits" |
| Travel distance to an exit or point of choice | GA plans (measure along the path of travel, calibrated) | "travel distance", "point of choice" |
| Distance between alternative exits | GA plans | "distance between alternative exits" |
| Aggregate and individual exit width vs occupant numbers | GA plans, area schedule | "width of exits", "number of persons" |
| Unobstructed width of paths of travel and corridors | GA plans | "unobstructed width" |
| Dead ends | GA plans | "dead end" |
| Discharge from exits to a road or open space | Site plan | "discharge from exits" |
| Door swing direction and obstruction of the path of travel | GA plans, door schedule | "swinging doors", "direction of opening" |

## 2. Doors (egress and access)
| Check | Evidence | Search terms |
|---|---|---|
| Clear opening width on the accessible path of travel | Door schedule, enlarged plans | "clear opening" (AS 1428.1) |
| Circulation space at doorways (latch side, approach direction) | Enlarged plans, 1:50/1:20 details | "circulation space" "doorways" |
| Door hardware height and type | Door schedule, hardware schedule (usually Unable to verify) | "door furniture", "door handle" |
| Luminance contrast of door and frame | Finishes schedule (usually Unable to verify) | "luminance contrast" |
| Power-operated and sliding doors | Door schedule | "power-operated door" |
| Glazing visual indicators | Elevations, glazing details | "visual indicator", "glazing" |
| Door thresholds and level changes | Details | "threshold" |

## 3. Access for people with a disability (NCC Section D access provisions and the Premises Standards / Access Code)
| Check | Evidence | Search terms |
|---|---|---|
| Parts of the building required to be accessible, by class | project.md, GA plans | "required to be accessible" |
| Accessible entrances (number and location, principal pedestrian entrance) | Ground floor plan, site plan | "accessible entrance", "principal pedestrian entrance" |
| Continuous accessible path of travel to and within the building | Site plan, GA plans | "continuous accessible path of travel" |
| Path widths, passing spaces and turning spaces | GA plans | "passing space", "turning space" |
| Exemptions claimed (e.g. areas where access would be inappropriate) | Notes | "exemption", "inappropriate" |
| Lifts (type, car size, controls) | Lift details, GA plans | "lift", "passenger lift" |
| Tactile ground surface indicators | Plans, details | "tactile ground surface indicators" |
| Floor surfaces and slip resistance (usually Unable to verify) | Finishes schedule | "slip resistance" |

## 4. Sanitary facilities (NCC Section F and access provisions)
| Check | Evidence | Search terms |
|---|---|---|
| Number of facilities vs occupants (and EFSG ratios on SINSW jobs) | GA plans, occupant numbers | "sanitary facilities", "number of" |
| Accessible unisex sanitary compartment: number, location, distribution per floor | GA plans | "accessible unisex sanitary compartment" |
| Left- and right-handed provision | Enlarged plans | "left-handed", "right-handed" |
| Ambulant compartments | Enlarged plans | "ambulant" |
| Circulation spaces at pan, basin and door (dimensioned layouts) | 1:20/1:50 wet area details | "circulation space" "pan" |
| Pan setout (centreline to wall, front of pan) and grabrails | Details, elevations | "pan", "grabrail" |
| Basin, mirror and accessories setout | Elevations | "washbasin", "mirror" |
| Accessible showers (where provided) | Details | "shower" |
| Unisex accessible facility at the change room, or other location triggers | Plans | "change room" |
| Adult change facilities, if triggered by class and size | Plans | "accessible adult change facility" |

## 5. Ramps, walkways, stairs and balustrades
| Check | Evidence | Search terms |
|---|---|---|
| Ramp gradient and length between landings | Sections, levels on plans | "ramp", "gradient", "landing" |
| Step ramps, kerb ramps and walkways | Site plan, details | "step ramp", "kerb ramp", "walkway" |
| Ramp and stair handrails (both sides, extensions, height) | Sections, details | "handrail" |
| Stair riser and going dimensions and the 2R+G rule | Stair sections | "riser", "going" |
| Stair nosings and luminance contrast strips | Details | "nosing" |
| Balustrade height and openings, including climbable elements | Sections, details | "balustrade", "barrier", "openings" |
| Barrier where fall exceeds the trigger height | Sections, site levels | "barrier" "fall" |

## 6. Car parking and site
| Check | Evidence | Search terms |
|---|---|---|
| Number of accessible car spaces | Site plan, car park count | "accessible carparking" |
| Space and shared-area dimensions, bollard | Car park details | AS 2890.6 (if held) |
| Height clearance | Sections | "headroom" |
| Accessible path from parking and from the site boundary | Site plan | "accessible path of travel" |
| Passenger loading zones, if provided | Site plan | "passenger loading zone" |

## 7. Hearing augmentation and communication
| Check | Evidence | Search terms |
|---|---|---|
| Hearing augmentation where an inbuilt amplification system is provided | Electrical / AV drawings (usually Unable to verify) | "hearing augmentation" |
| Coverage of rooms with amplification | AV drawings | "hearing augmentation" |

## 8. Signage
| Check | Evidence | Search terms |
|---|---|---|
| Braille and tactile signs at sanitary facilities and exits | Signage schedule (usually Unable to verify) | "braille and tactile" |
| International symbols of access and deafness at entrances and facilities | Signage schedule | "international symbol" |
| Directional signage to accessible facilities and entrances | Signage schedule | "directional signage" |

## 9. Fire safety items visible on architectural drawings
| Check | Evidence | Search terms |
|---|---|---|
| Fire-isolated stairs and passageways where required | GA plans | "fire-isolated" |
| Exit signs and emergency lighting shown (often on services drawings) | Electrical | "exit sign", "emergency lighting" |
| Fire hydrant, hose reel and extinguisher locations shown | Hydraulic / fire services | "fire hydrant", "hose reel" |
| Compartment sizes vs type of construction (flag only, don't assess) | GA plans, area schedule | "fire compartment" |
Fire engineering, fire resistance levels and Performance Solutions are outside
what this pre-check can confirm. Flag them as `Performance Solution required` or
`Unable to verify`.

## 10. EFSG (SINSW projects only)
Where `project.md` says EFSG applies, check EFSG requirements that exceed the
NCC for the elements above (sanitary ratios, accessible facility provision,
door widths, corridor widths, stairs, handrails, signage). Cite EFSG clauses
verbatim from the library like any other source.
