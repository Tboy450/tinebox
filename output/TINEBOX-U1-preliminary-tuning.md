U1 / preliminary tuning estimates

Slider + rotating comb | October 26, 2026 | Estimate set 01

Known setup and explicit assumptions

Working setup: Snapmaker U1, 0.4 mm nozzle, standard PETG or standard PLA, as requested. Snapmaker lists this nozzle size and PLA/PETG support. [1] Proceed with generic standard-material estimates; a specific brand is not required for this design stage. Printed stiffness will be calibrated with mounted test tines.

Material proxies: PETG E = 1.7 GPa, density = 1.27 g/cm^3; PLA E = 3.1 GPa, density = 1.24 g/cm^3. These are horizontal printed-specimen flexural moduli and densities from Prusament datasheets [2, 3], used as first approximations. They are not measurements of your filament or dynamic modulus at musical frequencies.

Geometry: S1 slider: 1.2 mm thick x 3.2 mm wide uniform rectangular tines. R1 rotary comb: 1.0 mm thick x 2.4 mm wide straight radial tines with individual rigid roots. No added masses, tapered flexures, dampers or plucking contact retained during ringing. Free length is measured from the effective rigid clamp to the free tip.

C-major calibration set: free lengths in millimetres

| Note | Target Hz | Slider
PETG | Slider
PLA | Rotary
PETG | Rotary
PLA |
|---|---|---|---|---|---|
| C5 | 523.25 | 20.7 | 24.2 | 18.9 | 22.1 |
| D5 | 587.33 | 19.5 | 22.8 | 17.8 | 20.9 |
| E5 | 659.26 | 18.4 | 21.6 | 16.8 | 19.7 |
| F5 | 698.46 | 17.9 | 20.9 | 16.4 | 19.1 |
| G5 | 783.99 | 16.9 | 19.8 | 15.4 | 18.0 |
| A5 | 880.00 | 16.0 | 18.7 | 14.6 | 17.0 |
| B5 | 987.77 | 15.1 | 17.6 | 13.8 | 16.1 |
| C6 | 1046.50 | 14.6 | 17.1 | 13.4 | 15.6 |

Displayed to 0.1 mm to avoid implying machining precision. This is an eight-note test scale, not a Take On Me arrangement or a final song cartridge. The structured JSON retains the calculation values for later updates.

Why the two concepts have different estimates

R1 uses thinner tines to test a smaller radial layout; at the same material and pitch, its length is sqrt(1.0/1.2) = 0.913 times S1. Rotation itself does not change pitch. With the same section, material, free length and clamp, the two mechanisms would share the same ideal-beam estimate. [4]

Individual prototype plans

S1 slider: accessible tuning first

Use removable straight tine coupons clamped to a common stiff bar on a bare deck. Start with one C5, G5 and C6 coupon for the chosen material. Keep a consistent clamp edge and screw seating. A nominal 4.4 mm centre spacing leaves 1.2 mm between 3.2 mm tines; this is a test layout, not a proven clearance.

The carriage needs to reach every actual tip location. For this calibration stage, provide a pick that can be repositioned to each test tip. A production slider must either cover the staggered tips or use an aligned-tip design. Adding tip weights or root-shaping to align tips invalidates this uniform-tine table and requires a new model/calibration.

Use an adjustable, replaceable pick and a manual lift for silent return. Begin with approximately 0.15 mm transverse engagement/lift as a low-deflection experiment, then measure clean release and actual slider force. This value is not a fatigue-safe or final acoustic specification.

R1 rotating comb: tune straight spokes independently

Use stationary inward-facing straight tines and one rotating pick. As a layout study, place every tip on an 18 mm radius. The root radius of each tine is then 18 mm plus its table length. At C5, that is about 36.9 mm for the PETG proxy or 40.1 mm for the PLA proxy. Individual root supports must act as rigid clamps; free spokes must clear the deck below.

Variable root positions let the tips share one picking radius without adding masses. Leave space outside the longest root for clamps and a rim: a roughly 95-105 mm diameter test deck is a packaging allowance, not a dimensioned design. A compact final version would need a revised section, register or mass-loaded geometry.

Print and measure three straight coupons first, then mount them on a radial-sector fixture. Compare frequencies before building a full ring. A flexible common ring, clamp movement or curved tine will need its own correction. Do not use a root radius or circular arc length as the free beam length.

If the rotary choice is the pinned drum instead

A thumbwheel drum can use the S1-style fixed tine bank and its own calibration. The drum stores note order and relative timing; it does not need a different tuning table solely because it rotates. C5-C6 diatonic notes are only a calibration example; select the actual song pitches before committing to a fixed bank.

Force and strain checks at the proposed test lift

| Design | Proxy | Vertical tine force, N | Max surface strain |
|---|---|---|---|
| Slider S1 | PETG | 0.040-0.112 | 0.126% |
| Slider S1 | PLA | 0.045-0.128 | 0.092% |
| Rotary ring R1 | PETG | 0.023-0.064 | 0.126% |
| Rotary ring R1 | PLA | 0.026-0.073 | 0.092% |

Small-deflection, ideal tip loading only. These loads exclude pick stiffness, friction, detents and drive geometry; they do not predict measured thumb effort or long-term life.

Print, measure, correct

Proposed U1 calibration print

Use the 0.4 mm nozzle and a consistent 0.20 mm layer height, including the first layer. Lay tines flat with bending thickness along Z; nominally 1.2 mm is six layers and 1.0 mm is five. Check the sliced preview for solid sections and continuous lengthwise paths. Use one spool and one toolhead for a comparison set, avoid seams at the flexing root, and keep supports off the free tine.

Use solid geometry/100% infill as the starting trial, then measure actual thickness, width and free length. Start with the calibrated U1 profile for standard PETG or PLA and follow the spool instructions for temperatures, cooling and drying. Keep the same spool and settings throughout each calibration set.

Separate calibration for each design and material

1. Measure and pluck C5, G5 and C6 test tines using the intended clamp and low lift. Record actual Hz, repeatability, and whether the strongest spectral peak is the fundamental or an overtone.
2. Calculate a first length correction: L_new = L_old x sqrt(f_measured / f_target). This applies only when section, material and clamp remain unchanged.
3. Reprint corrected samples and check the result. Once the three samples behave consistently, generate the full song-specific event comb or pitch bank.

Example: a nominal 20.7 mm PETG S1 C5 tine measured at 480 Hz instead of 523.25 Hz gives L_new about 19.8 mm. This is an illustration, not a measured result. A flat tine needs shortening in this model; a sharp tine needs lengthening or another deliberately modelled tuning change.

How uncertain are these numbers?

Frequency scales as h x sqrt(E/rho) / L^2. A hypothetical 20% decrease/increase in effective stiffness changes frequency by about -10.6%/+9.5%, already around musical semitones. At 15 mm free length, a 0.1 mm length error changes pitch by about 23 cents. These are sensitivity examples, not confidence bounds. [4, 5]

Published standard PETG examples also differ: Polymaker reports about 2.28 GPa horizontal bending modulus and 1.30 g/cm^3 [6], compared with the proxy above. That alone gives roughly 7% longer tine lengths for the same target note in this model. Mounted-sample measurements will correct for the actual printed material.

References / remaining information

1. <link href="https://wiki.snapmaker.com/en/snapmaker_u1/hot_end_guide" color="#246B78">Snapmaker U1 hotend guide</link>

2. <link href="https://prusament.com/wp-content/uploads/2022/10/PETG_Prusament_TDS_2021_10_EN.pdf" color="#246B78">Prusament PETG technical datasheet, p. 2</link>

3. <link href="https://prusament.com/wp-content/uploads/2022/10/PLA_Prusament_TDS_2021_10_EN.pdf" color="#246B78">Prusament PLA technical datasheet, p. 2</link>

4. <link href="https://help.solidworks.com/2026/english/simtutorialonline/Dynamic_Analysis_of_a_Cantilever_Beam.htm?id=1.0.1.3" color="#246B78">SOLIDWORKS: cantilever frequency model</link>

5. <link href="https://newt.phys.unsw.edu.au/jw/notes.html" color="#246B78">UNSW: pitch and cents conversion</link>

6. <link href="https://polymaker.com/wp-content/uploads/lana-downloads/TDS_Polymaker_PETG_V2.0_2025-11-17.pdf" color="#246B78">Polymaker PETG datasheet v2</link>

Next useful inputs: chosen song excerpts and mounted-sample frequencies. Continue development with standard PETG and PLA; no exact product identification is required at this stage. Neither the eight-note scale nor either mechanism has been physically validated. Body acoustic tests follow after repeatable plucking and tuning.
