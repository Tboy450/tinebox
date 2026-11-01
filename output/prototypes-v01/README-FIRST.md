# TINEBOX v0.1 - first printable development parts

**Superseded as a first-build recommendation on October 27, 2026.** The slider and cylinder have gravity-seating errors. Read `V01-AUDIT-NOTICE.md` and use the revised `output/simple-v02/` package at the project root. This document records the earlier trial design; its original recommendations below are historical.

October 26, 2026. Snapmaker U1, 0.4 mm nozzle, standard PLA and PETG. All STL dimensions are millimetres; import at 100% scale. These are bench prototypes and rotor layout studies, not physically validated musical products. No printer-specific G-code or tested sound claim is supplied.

## What is ready for a first trial

- **S2 slider bench:** a guided carriage, replaceable picks, a clamped aligned-tip event comb, and separate PLA/PETG combs for three short melodies. Its 184 x 66 mm deck is deliberately large enough for the longest current phrase; pocket-size packaging comes later.
- **P1 cylinder contact bench:** a one-note C5 fixture with interchangeable single-peg and single-tooth drums. It tests the two contact styles before a complete melody drum is designed. A handwheel is integral with the drum.
- **W1 rotating-tine wheel:** both the wheel and tines turn past a future fixed pick. The wheel cartridge and carrier are modelled, with a seven-event Twinkle opening. Bearings, fixed-pick holder and handling enclosure remain to be designed.
- **T1 rotating-tine cylinder:** axial tines rotate with the cylinder past a future fixed pick. The rotor is modelled, with the same seven-event opening. Its frame and fixed-pick holder remain to be designed.

W1 and T1 are labelled `LAYOUT` in their filenames. They are separate from the stationary radial comb/rotating-pick idea and from P1's stationary comb/peg or tooth drum. Do not treat the rotor studies as complete assemblies.

## Start with these small prints

1. `00_compact_tuning_sample_PLA.stl` and/or `00_compact_tuning_sample_PETG.stl`: 60 x 36 mm, three candidate C5/G5/C6 tines. Print solid, in the supplied flat orientation. Flip the part for plucking so the tines have air below them; support/clamp the thick spine only. These give an initial material comparison, not final in-assembly tuning.
2. `00_fit_coupon_6p2_6p4_6p6_bores.stl`: compare the nominal 6.2, 6.4 and 6.6 mm bores against a measured 6 mm shaft or a test length of the printed shaft. Check fit before building P1.
3. Choose one mechanism and one material for the first assembly. Do not print all 33 variants.

## S2 slider: parts and assembly

Print one each:

- `S2_01_common_deck.stl`
- `S2_02_clamp_bar.stl`
- `S2_03_carriage.stl`
- `S2_04_pick_lift_0p2.stl` (default contact trial)
- `S2_00_calibration_comb_PLA.stl` or its PETG counterpart

Hardware: two M3 x 10 mm screws and two standard M3 nuts for the comb; an optional M2 x 4 mm thread-forming screw in the pick holder's small pilot. Screw sizes are nominal design choices, not a tested fit. Use light seating force on printed parts. The pick bay can be checked without tightening a retention screw.

1. Print the deck flat with its rail up. Check the shallow nut pockets and rail in the slicer. Print the separate clamp flat.
2. The comb STL is already oriented with all free tines on the bed. After printing, turn it over: the smooth bed-facing surface becomes the upper surface in the assembly. Put the thick spine under the clamp bar and point the free ends toward the rail. The varying thick roots set free length while all tips end at one Y position.
3. Insert the M3 nuts into the deck underside pockets. Seat the comb and clamp with the two M3 screws, without distorting the spine.
4. The carriage STL is oriented roof-down. Its forward pick-holder nose is an overhang: review supports there and remove them carefully. Keep support scars out of the rail channel and pick bay. This has not been sliced or printed yet.
5. Print the pick flat in its supplied orientation. Slide its thick tab into the carriage's front bay until seated; the thin wedge projects toward the tine ends. Its pilot aligns with the optional retention screw.
6. Place the carriage over the rail. Slide slowly toward increasing event positions, away from the first tine. The pick is a one-direction ramp with a trailing release edge. Lift the carriage completely clear of the tines for the return stroke.
7. Establish smooth motion using the zero-lift pick if needed. Start sound trials with the 0.2 mm nominal lift. The 0.4 mm pick is an extra geometry trial, not an instruction to increase force before checking the lower lift.
8. Record C5/G5/C6 after mounting. Update lengths from measured pitch before choosing a melody comb. The material name alone does not guarantee the notes.

The shoe is removable, not a captive rail with end stops. Hold it in place during a bench sweep. A closed body, end retention and a refined thumb grip are later design work. No automatic bidirectional music is claimed.

After calibration, swap to a material-matched `S2_05_twinkle`, `S2_05_ode` or `S2_05_elise` comb. The common mounting geometry is unchanged. Their event spacing represents relative rhythm at constant carriage speed. A person can still change tempo during a swipe; the final held note requires an end pause rather than another pluck.

## P1 cylinder bench: parts and assembly

Print one bearing deck, one shaft, one single-peg OR single-tooth drum, two washers, two shaft collars, one material-matched root stand and C5 tine, and the clamp bar. The stand and tine must use matching PLA or PETG design files.

Hardware: two M3 x 8 mm screws plus nuts for the stand feet; two M3 x 12 mm screws plus nuts for the tine clamp; optional M3 collar set screws after tapping/thread-forming their 2.5 mm pilots. The printed collars have no modelled screw threads. For a stationary bench trial, temporary shaft-end retainers are another option.

1. Print the bearing deck flat. Its transverse 6.6 mm bores have short roofs that need slicer inspection/bridging or removable support. Clean them and check free movement; do not force a mismatched shaft.
2. Print the shaft upright with a brim. The nominal 6 mm x 90 mm shaft is a prototype; straightness and finish need checking.
3. The drum STL is oriented with its large thumbwheel face down and its axis vertical. Inspect the small radial peg/tooth overhang in the slicer. Confirm that the feature survives printing before assembly.
4. Install the root stand using its external feet and two M3 x 8 screws/nuts. Load the two clamp nuts into the stand's rear-entry pockets.
5. Flip the printed tine part into assembly orientation, seat its thick spine on the stand, and secure the small clamp with the M3 x 12 screws. The free tip reaches over the top of the drum.
6. Insert the shaft through one bearing, washer, drum, second washer and the other bearing; fit the end collars. The drum rotates around the shaft; it does not need to be bonded to it. Set axial position so the single feature crosses the tine centre.
7. Turn so the peg/tooth approaches from the root side of the tine, passes underneath it and exits past the free end. At the top of the drum this means motion toward the free tip, away from the clamp.
8. Observe whether contact actually ends cleanly and the tine rings freely. The nominal 0.3 mm lift is a geometry trial, not a demonstrated fatigue-safe setting. Do not force a catch. Compare peg and tooth versions separately.

P1 produces one note/event per revolution. The complete melody drums are a later step after repeat-release, wear, mounted pitch and tolerances work. Angular event maps are in `song-programs.json`, but no full melody drum is supplied yet.

## W1 and T1: rotating-tine layout studies

- **W1:** 98 mm wheel cartridge and a separate thin carrier, with nominal M3 mounting holes. All tips lie at an 18 mm radius. The carrier sits below the free tines so a future fixed pick can approach from above. The wheel's free tines are 1.2 mm thick; do not use the older 1.0 mm stationary-radial-comb table for this rotor. Print the wheel cartridge in the supplied flipped orientation and the carrier flat. Bearing supports and the fixed-pick geometry are not included.
- **T1:** 52 mm axial rotor with a 30 mm flange. Its tines end at a common axial station and have different root positions. The fixed pick would deflect them radially as they rotate. The export has its axis upright and flange down; this makes the tine lengths run along build Z, so layer-direction performance differs from the flat-printed slider tines. Expect a separate calibration and fatigue test, or a later redesign using replaceable flat-printed tines.
- These rotating-tine layouts repeat the initial seven-note Twinkle phrase with a longer silent sector. They are not the full 14-event slider program. Their rigid core/carrier, bearings and contact arrangements can affect sound; current frequency estimates are uniform-beam starting points only.

## Materials, printing and measurement

- Keep actual nozzle diameter at 0.4 mm. Start with a consistent 0.20 mm layer height, including the first layer; 1.2 mm tines are six nominal layers when flat.
- Print the tuning parts solid with continuous lengthwise paths where the slicer allows. Use the same spool, toolhead and settings within a comparison. Exact temperatures/cooling follow the calibrated U1 standard PLA/PETG profile and spool guidance.
- Bodies can later use less infill, but keep the root/rail geometry consistent while establishing a baseline. Do not change body infill and tine dimensions together and attribute every sound change to material.
- Measure actual thickness/free length, record isolated plucks and identify the fundamental rather than an overtone. Correct a uniform tine using `L_new = L_old * sqrt(f_measured/f_target)` only if section, material and clamp stay the same.
- Keep the current calibration record separate for S2, P1, W1 and T1. The rotational mechanism does not itself tune a note, but different root supports and print directions change the effective boundary conditions.

## What digital checks establish

Every exported STL was reopened and checked for a closed mesh, consistent winding, positive volume and one connected component. All fit within the U1's nominal 270 mm build envelope. A 0.0001 mm mesh cleanup removes boolean slivers before binary STL export.

S2 was screened at six carriage positions for body/rail/comb collisions. P1's two drums were screened at 36 angular positions against fixed bodies, shaft and clamp. Small pick-to-tine intersections are deliberate nominal elastic deflections; the check does not simulate deformation, stresses, release or sound. W1/T1 are geometry/layout studies and have no complete fixed-pick motion check yet.

The collision checks are sampled, not a continuous swept-volume proof. No slicer, printer, physical fit, tuning, fatigue or acoustic test has passed yet. Validation details are in `mesh-validation.json`.

## Files and editing

- `stl/`: individual millimetre part meshes. Print these selectively.
- `develop_prototypes.py`: editable procedural source. Change the design constants and event data to regenerate; the geometry is not a vendor CAD project.
- `requirements-cad.txt`: Python dependencies. The source first checks the project's isolated `tmp/cad-libs` folder, then normal Python packages.
- `model-parameters.json`: output record of dimensions and assumed material properties, not an input configuration file.
- `song-programs.json`: explicit note/onset/duration data and preliminary cylinder angles.
- `*-assembly-view.glb`: viewing only, exported in metres per glTF convention. Use the millimetre STLs for slicing.
- `*-synthetic-melody.wav`: ideal melody auditions made with simple decaying tones. These are not recordings or predictions of a printed instrument.

The next design pass should use actual calibration results, then complete one slider body and one selected cylinder/rotating-tine mechanism. This package was not emailed to the lab.
