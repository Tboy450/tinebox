# Musical fidget project - current scope

Updated October 26, 2026 from the user's design direction.

## October 27 priority: simple first builds

The current first-build package is `output/simple-v02/`. It contains a manual three-tine sound fixture and a compact dual-rail slider fixture sharing a comb/clamp interface. The first comb has fixed 26/22/18 mm lengths with no assigned pitches; actual mounted measurements come before song tuning. Arranged core 3MF plates and a first-print checklist are included.

The v0.1 slider and cylinder had gravity-seating errors that their original mesh checks did not reveal. See `output/prototypes-v01/V01-AUDIT-NOTICE.md`. The cylinder and rotating-tine family remain active concepts, but the old cylinder is not in the recommended first print batch. v0.2 is digitally checked, not physically validated or sliced yet.

## Working setup

- Snapmaker U1 with a 0.4 mm nozzle.
- Develop with standard PLA and standard PETG. Exact brand identification is not required to continue concept development.
- Preserve a variety of mechanisms and body designs; do not narrow the project to the two concepts illustrated in the first lab email.
- Each prototype needs tuning and contact tests in its actual material and mounting arrangement. Current tuning tables are starting estimates only.

## Active concept family

| Concept | Musical arrangement and interaction | Main development question |
|---|---|---|
| Sliding pick across a stationary event comb | A swipe plays the ordered tines; repeated events use repeated tines. Swap the event cartridge. | Reliable release, tip reach, comfortable travel and a deliberate return action. |
| Stationary radial event comb with a rotating pick | A dial sweeps one pick around the ordered tines. Swap the radial cartridge. | Individual root support, picking radius, ring size and tuning after mounting. |
| Rotating wheel carrying its tines, with a fixed plucker | The entire tine wheel rotates past a stationary pick. Each repeated event has its own tine. | Root support, carrier clearance, spindle and fixed-pick design. W1 rotor layout started. |
| Rotating cylinder carrying axial tines, with a fixed plucker | The cylinder and its differently tuned tines rotate together past a stationary pick. | Radial deflection, layers/print direction, replaceable tine mounting and fixed-pick design. T1 rotor layout started. |
| Pegged cylinder beside a stationary tuned comb | Pegs select teeth and encode their order and relative timing. A thumbwheel, crank or another drive can turn the cylinder. | Printed peg profile, comb alignment, release clearance, repeated-note behaviour and drum replacement. |
| Toothed cylinder beside a stationary tuned comb | Teeth or discrete cam features lift and release selected comb tines as the cylinder turns. | Whether each feature actually releases the tine cleanly, avoids rubbing during ringing, and encodes the intended sequence. |
| Strip-fed musical mechanism | A fed strip selects events on a reusable tuned bank. | Reader/feeding complexity, supported pitches and handheld packaging. Retain as an additional option. |

The pegged and toothed cylinders share a classic comb-and-rotating-actuator architecture. They may become two interchangeable contact/sleeve variants on one test fixture. Keep both available until tests establish their differences. A continuous toothed roller that plucks every tooth at a fixed interval is only a repeating pattern; a melody needs deliberately positioned features or another selection mechanism.

A thumbwheel is also a possible handle for turning a drum. The choice of handle does not determine whether the musical mechanism is a radial comb, a pegged cylinder or a toothed cylinder.

Earlier variants recovered from the original chat/PDF also remain in the backlog: dual-row event combs with explicitly phased plucking, scale-run and pentatonic cartridges, interchangeable shell styles, miniature string harp/zither, string cassette and flexible-pick slider. Printed tine, metal-tine and string branches need separate tuning; shell skins are a styling family rather than another musical mechanism.

## Current concrete development

October 27 continuation: the current simple package is `output/simple-v03/`. The manual sound fixture A is unchanged from v0.2. Slider B separates the side-printed pick holder from the roof-down bridge, adds two M3 x 8 fasteners with printed 0.8 mm spacers, and reserves space for their ends above the tines. Digital checks cover the revised geometry; slicing, fit and sound remain untested. Read its README before printing. Older prototype mechanisms remain exploratory.

`calibrate_comb.py` now fits mounted three-length measurements to an inverse-square frequency model, screens inconsistent readings and exports a predicted seven-event Twinkle comb only when the fixture range permits. The blank calibration template contains no assumed measurements. Software checks use explicitly synthetic numbers only. No final song comb has been physically tuned, and equal event spacing still relies on hand-controlled rhythm. Next physical gate: print A in one standard material, test whether the tines ring, then record their fundamentals before building B or tuning a melody.

`output/prototypes-v01/` contains the S2 slider bench, P1 one-note peg/tooth cylinder fixture, W1/T1 rotating-tine rotor layouts, material samples, three simplified melody programs and synthetic melody auditions. The editable procedural source is `develop_prototypes.py`. These are digitally checked meshes and early assemblies; physical calibration, slicing, fit, fatigue and sound tests remain open. Read `README-FIRST.md` before choosing a print.

First melody candidates are Twinkle, Ode to Joy and Fur Elise. Keep Take On Me, Billie Jean, Mario and Harry Potter as additional reference-supported arrangement candidates. No full melody cylinder or final acoustic body has been completed yet.

## Redesign for the current materials

- Treat printed tines, pegs and contact parts as material-specific prototypes. Do not copy the dimensions or deflection of a steel music-box comb and label it tuned for PLA/PETG.
- Keep the tuned comb and the actuator replaceable so tine tuning can be developed separately from peg/tooth geometry.
- Compare PLA and PETG versions of a small mounted test set with consistent geometry and print settings. Measure frequency, release, operating force, wear and tuning drift.
- Begin cylinder work with one tine and one peg/tooth feature, then add repeated events and a short sequence. Confirm clean contact loss before building a full tune.
- The same uniform-tine frequency estimate can be a starting point across mechanisms if material, section, free length and clamp are unchanged. Actual mount compliance, mass changes, retained contact and different tine shapes require separate calibration.
- Retain interchangeable backs, soundboards and body forms for later acoustic comparison. Fuller sound remains a project development goal; no improvement is demonstrated yet.

## Future material branches

- Metal tines: an explicitly welcome future experiment when suitable stock or a tuned comb becomes available. Revisit tuning, picking engagement, mounting and fabrication for that material.
- Stringed fidget pluckers: retain harp/zither, string-cassette and slider/rotary plucker ideas for a future tensioned-string branch. Anchors, tuning adjustment and frame loading need their own design.
- These future branches do not replace the current PLA/PETG work.

## Communication record

The October 26 lab email contained the project introduction, slider/radial concept picture, two reference photos and four video links. It was sent and verified. The fuller-sound development plan remains local, as requested. This scope update does not send a further email.

## Relevant files

- `output/TINEBOX-U1-preliminary-tuning.md`: assumptions and sample lengths for the current slider/radial tine sections.
- `output/TINEBOX-video-review-and-acoustic-development.md`: visual review of all four Shorts and internal acoustic experiments.
- `output/lab-project-package/email-sent.json`: verified outbound package record.
