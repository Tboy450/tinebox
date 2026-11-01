# TINEBOX simple v0.2 - start here

October 27, 2026. Two deliberately small first-build fixtures for standard PLA or PETG on a Snapmaker U1 with a 0.4 mm nozzle. **These are completed digital test fixtures, not physically proven instruments.** Begin with A; B is the next mechanical trial if the tines produce useful tones.

## A. Manual three-tine sound test

This removes the slider, axle and peg variables. It asks whether the actual printed cantilevers ring clearly, and what frequencies they produce when mounted.

**Print one of each:**

- `A_01_manual_base.stl` - 80 x 50 x 4 mm.
- `01_shared_three_length_comb_26_22_18mm.stl` - 60 x 36 x 4 mm overall; free tines are 3.2 mm wide and 1.2 mm thick.
- `02_shared_clamp_bar.stl` - 60 x 8 x 2 mm.

Or open `A_manual_test_plate.3mf`, which arranges these three objects in their proposed printing orientations. It contains geometry and placement, not a saved Snapmaker printer/material profile or G-code.

Hardware: **two M3 x 10 mm screws and two M3 nuts**. The reserved head envelope is at most 6 mm diameter x 3.2 mm high. Compare your hardware and the small `00_M3_fit_coupon.stl` if fit is uncertain. Its hole row is 3.2, 3.4 and 3.6 mm; its hex-pocket row is 5.7, 5.9 and 6.1 mm across flats. The designs use 3.4 mm screw holes and about 5.72 mm across-flat nut pockets.

### Printing

1. Import at **millimetres, 100% scale**. Do not scale parts to fit each other.
2. Use the calibrated U1 profile and the spool's standard PLA/PETG settings. Start with 0.20 mm layers, including the first layer. The 1.2 mm tines are six nominal layers.
3. Print the comb solid, with no sparse infill or supports on the free tines. Inspect the sliced paths: no missing lines, gaps or seam blobs at the bending roots. The base and clamp can also be solid for this small baseline test.
4. The comb STL has already been flipped for printing. Its broad common face and the free tines lie on the bed; raised root regions build above that face.
5. The base is flat and the clamp is flat. The underside nut-pocket ceilings are short bridges; inspect their toolpaths. No slicer has been run on these files yet.

### Assembly and first test

1. After printing, **turn the comb over**. The smooth bed-facing face becomes its upper face. The thick spine and root regions go down onto the base; the thin free tines have approximately 2.8 mm of air below them.
2. Point the tips away from the clamp. With the spine nearest you, the long/left, middle and short/right tine lengths are 26, 22 and 18 mm. These are **unassigned test pitches**, not a promise of three named notes.
3. Put the nuts in the base underside pockets, place the comb and clamp, and seat the two screws gently and evenly. Keep the root regions flat; do not bow the comb with tightening force.
4. Pluck one tip gently with a fingernail or flexible pick. Record isolated plucks from all three tines at the same microphone position. Note the material, actual thickness/free length, measured fundamental, and whether the note rings or mostly clicks.
5. The **bare comb alone** can be an even smaller first print: turn it over onto a hard flat surface, support the thick spine/root regions and pluck gently with air under the free tines. That is only a rough material check. Use the mounted fixture for repeatable tuning measurements.

Do not assign final song lengths from the generic material name. If the basic tines do not ring usefully, change the section/root/print process and test again before spending filament on a musical mechanism.

## B. Dual-rail slider test

B reuses A's comb and clamp. The carriage sits on two rails, one on each side of the comb. The musical contact is between the supports instead of hanging beyond a single rail. A metal nut and screw retain the separately printed pick against its seating floor.

**Additional prints:**

- `B_01_dual_rail_base.stl` - 80 x 64 mm, 14 mm tall at the rails.
- `B_02_bridge_carriage.stl`.
- `B_03_pick_lift_minus_0p2.stl` - clearance/setup pick.
- `B_03_pick_lift_0p2.stl` - first contact trial.

`B_slider_test_plate.3mf` arranges these and the shared comb/clamp. If you already printed the shared parts, remove their duplicates from the plate before slicing.

**Additional hardware:** one M3 nut and one M3 x 6 mm screw for the pick clamp. This uses a captured metal nut, not a modelled plastic thread. The screw is an adjusting clamp: its head may stand above the orange bridge. The bridge includes a larger access hole around that screw head.

### Printing and assembly

1. Print the base flat, with both rails upward. Keep their bearing surfaces clean and undistorted.
2. The carriage is exported roof-down. Its forward pick-holder nose overhang needs slicer review and likely local support. Avoid or remove support residue in the guide channels, nut slot and pick seating surface. The free acoustic pick is a separate flat print, so its ramp does not need to be printed on support.
3. Install the shared comb and clamp as in A. Install both clamp screws **before** placing the carriage. Nominal screw-head clearance under the bridge is 0.8 mm; check your actual heads.
4. Load the third M3 nut through the side slot of the pick holder. Insert the clearance pick's thick tab through the front opening until it is seated; the thin wedge points toward the tine tips. Press its underside against the holder floor and bring the M3 screw down gently onto the flat tab. Do not tighten it against a gap or crush the tab.
5. Place the carriage over **both** rails. It should rest on its flat roof lands and move smoothly under light hand pressure. Check it for rocking, catching and printing scars. It is a removable test carriage, not a captured slider with finished end stops.
6. Sweep the clearance pick across the three tines. It should pass without plucking. If it touches or snags, correct the seat/fit before using a taller pick.
7. Lift the carriage off, install the 0.2 mm contact pick, and sweep slowly toward increasing tine positions. The ramp leads, the upright trailing edge releases. Its thin blade is intended to lift each tine slightly from below near the free end.
8. **Lift the entire carriage clear for the return.** Bidirectional music and automatic return are not implemented. Do not force a catch.
9. Listen/record and inspect the release closely. If the carriage rocks, the pick drags on a ringing tine or the sound is mostly a click, record that as a failed trial and revise the contact geometry. Digital overlap is not proof of a good pluck.

The zero-lift and 0.4 mm picks are additional comparison variants. They are not needed for the first plate, and a larger lift is not automatically a better sound.

## Optional first musical phrase

`OPTIONAL_twinkle_opening_PLA.stl` and its PETG counterpart encode `C5 C5 G5 G5 A5 A5 G5`, with an end pause. They use the same clamp and base. The repeated pitches have repeated tines.

These lengths still use the earlier **illustrative** material properties. They are supplied for development, not as tuned results. Measure the three-length sample first; update the source's tuning model with measured mounted data before expecting a recognizable in-tune phrase. The plain three-length comb remains the recommended first print.

## What changed from v0.1

- Removed the slider's modelled 0.3 mm floating roof gap, which could cancel its nominal 0.2 mm engagement when the shoe settled.
- Added a second rail, with the pick contact between the support lines. The ideal static vertical reactions at both rails are positive; this reduces the cantilevered rocking problem of the old single-rail shoe.
- Changed the pick floor into a contact datum. Clearance is on the sides and above the tab; the tab should not float vertically when clamped.
- Thickened the holder floor and used a captured metal nut instead of a tiny tapped plastic retention feature.
- Reserved and checked space for clamp screw heads and the pick-clamping screw.
- Reduced the first fixtures from the old 184 mm deck to an 80 mm base.
- The old cylinder has two clearances that can cancel its contact lift. It is excluded from this print batch. A clamped-shaft/adjustable-comb redesign remains later work.

## Validation and limits

The 12 STL variants were reopened and checked for watertightness, winding, a single connected part and positive volume. The carriage was checked every 0.5 mm over the current test travel against the deck, plain comb, clamp, seated pick and hardware envelopes. The arranged 3MF plates were round-trip imported independently and checked for object count, millimetre bounds and separated parts.

An ideal ramp-contact profile checks that the proposed shape has a release edge. It is not an elastic, frictional, fatigue, thermal, slicing or acoustic simulation. Actual print flatness, clearances, screw fit, note frequency, tone and reliable release are still untested. See `validation.json`, `print-plate-checks.json`, `parameters.json` and `contact-envelope.json` for the exact scope.

Use the STLs or arranged 3MF plates for slicing. No bed temperature, nozzle temperature, supports, filament or printer G-code is embedded in the plates. Review these in your U1 slicer before any print. The editable source and geometry helpers are included in the ZIP.

## Development order

1. A: establish whether each material gives useful tones and record mounted frequencies.
2. B: establish repeatable clean release with a small engagement.
3. Recalculate one short song comb from those measurements.
4. Then finish a handheld case and revisit the cylinder and rotating-tine branches.

No new email or print order has been sent. Fuller-sound experiments and the broader concept family remain in the project.
