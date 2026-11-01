TINEBOX / improved concepts

Development brief v2 | October 26, 2026 | Mechanism proposals, not print-ready plans

What can improve before we know the material

Separate three functions: tuned elements set the available notes; the mechanism chooses when they play; the body shapes how the sound reaches the listener. Different fidget actions need different ways to encode a song. Avoid forcing every option into the original 13-tine slider.

| Concept | Best fit | How songs change | Main unresolved issue |
|---|---|---|---|
| A. Swipe cartridge | Short hooks and a simple thumb gesture | Swap the tuned event comb; repeated notes get repeated tines. | Reliable pick release; event spacing and hand-controlled tempo. |
| B. Rotating comb ring | Continuous turning with a short repeating phrase | Swap a radial event-comb cartridge. | More experimental: radial tuning, pick-arm stiffness and ring packing. |
| C. Thumbwheel drum | Longer phrases and repeated notes using fewer tuned teeth | Swap a pinned drum; keep a compatible tuned comb. | Pin manufacture, alignment, retrigger damping and drive effort. |
| D. Strip-fed player | Many editable songs and longer arrangements | Swap a punched strip; keep the tuned comb and reader. | Packaging, paper feed and the note set supported by the reader. |

My starting recommendation

Build A to explore the fidget feel, and develop C for song flexibility. Keep B as a compact rotary experiment. D offers a practical reference mechanism if using bought musical parts is acceptable. An existing working drum or strip mechanism is a stronger baseline than a completely new printed plucking system. [2, 3]

Improvements shared by the concepts

Use a rigid, repeatable comb clamp; a replaceable pick/contact part; accessible adjustment of engagement height; and tactile feedback kept separate from the tuning clamp. Attach sound-body variants to the same structural base so acoustic comparisons do not accidentally change tine free length or clamp stiffness.

A soft mounting layer under the comb may reduce vibration transfer. Keep the comb-to-base path deliberate, and place enclosure seals or anti-rattle features elsewhere unless an isolation experiment is intended. Body volume is one variable alongside panel stiffness, openings and structural coupling. [4]

A + B / direct musical fidgets

A. Swipe cartridge - simplify the pick path

Action: move one carriage across a stationary row. Start with conventional free-length tuning. Once plucking works, compare an aligned-tip comb with locally shaped flexures or securely attached tip masses. Do not assume that equal-length uniform tines will produce different notes without those other changes. Mass/root-shaping tuning has real music-box precedent. [1]

Song improvement: make each cartridge an event sequence, including repeated-pitch tines and deliberate gaps for timing. Do not force all songs onto evenly spaced teeth. A cartridge-specific tactile strip can follow its event locations.

Return improvement: prototype a thumb-operated lift-to-return pick holder first. That gives a deliberate silent reset without relying on an untested bidirectional ramp. Later test a compliant pick and passive return bypass. If the return does pluck, it plays the notes in reverse order.

First experiment: three notes spanning low, middle and high stiffness, one adjustable replaceable pick, and an exposed bare deck. Check clean release and slider effort before choosing the final number of events. A short event comb will not reproduce an entire song.

B. Rotating comb ring - a short loop without a return stroke

Action: rotate a central thumb dial carrying a pick past stationary inward-facing tines. The circular cartridge contains the ordered events. A repeated note still needs another tine; this is not a reusable keyboard bank.

Improvements: use an outer locating rim for repeatable cartridge seating, an adjustable pick arm, and an optional detent ring that can be removed during sound testing. Leave an intentional silent sector at the loop join when the arrangement needs a pause.

Tradeoff: a common picking radius simplifies reach, but different tine flexures/masses must fit behind it. Do not bend straight comb geometry into a ring and reuse its tuning table. Begin with a three-tine sector; ring size, event count and tuning range remain open.

Drawings are mechanism maps, not cross-sections or dimensional CAD. They omit guards, bearings, fasteners and contact details.

C + D / more flexible song storage

C. Thumbwheel drum - keep the notes, swap the program

Action: turn a wheel connected to a pinned cylinder beside a fixed tuned comb. Each tine is a pitch; pin position along the cylinder selects it, and angular position sets the onset. The same tine can be used repeatedly, subject to retrigger spacing. This follows an established music-box architecture. [2]

Improvements: key the drum to a start position, provide a protected wheel edge for the thumb, and design the bearing/comb alignment as one rigid module. Start with a one-direction drive and removable end support. Any ratchet or detent must be tested for noise and added torque.

Song change: a compatible drum can change event order and rhythm without retuning the comb. A song requiring an absent pitch still needs transposition, arrangement changes, or a different tuned bank. Do not promise any song on one small comb.

Prototype path: first use an existing working comb/drum module inside a printed ergonomic body if suitable parts are available. For a custom drum, test one pinned track and a single tine, including repeated plucks and damping, before a whole tune. Printed pins and all-printed tines remain experiments.

D. Strip-fed player - editable songs with a rolling action

Action: a thumbwheel or crank feeds a punched paper strip through a mechanical reader. Holes encode notes and timing; the reader actuates a fixed tuned comb. Commercial paper-strip music boxes demonstrate this approach. [3]

Improvements: add a fold-flat wheel handle, a supported entry guide and a clear start mark. A protective strip sleeve or spool cassette can be explored after straight feeding works. An endless loop needs its own bend-radius, seam and feed test.

Tradeoff: this is a rolling musical object with loose media, rather than the original compact swipe. Using an existing reader/comb avoids inventing the hole-to-pluck mechanism at the same time as tuning the instrument.

For either C or D, hand speed still controls overall tempo. The pattern stores relative timing; a governor, motor or deliberate beat indexing would be an additional subsystem. Closely repeated notes may buzz or fail without appropriate release and damping. [2]

Measurements / songs / next steps

What information is needed, and when

| Information | Why it matters |
|---|---|
| Printer model, nozzle diameter, filament type/brand; willingness to use metal parts | Chooses a realistic process, clearance trials and the tuning route. No dimensions should be finalized from filament name alone. |
| If a physical comb exists: free lengths from clamp to tip, width, bending thickness, clamp position and added weights | Provides a first mechanical model. A ruler photo helps with layout; calipers help with thickness. The eBay photograph alone cannot supply these values. |
| If testing printed tines: orientation, layer height, wall/infill settings and measured sample dimensions | Printed stiffness depends on the actual print. Test with the same process intended for the finished part. |
| A recording or measured frequency from each mounted test tine | This is the most useful tuning calibration. Use the intended clamp, isolated plucks and a spectrum/tuner; distinguish the fundamental from overtones. |
| Preferred action, approximate pocket size and 2-3 exact song hooks | Determines whether short event combs are sufficient or a reusable note bank with a drum/strip is the better route. |

How we will choose and fit songs

For each requested excerpt, list the exact pitches, repeated onsets, rests and relative durations. Then check: available pitch range; number of events; shortest time between repeats; comfortable stroke/turn; and whether transposition preserves recognizability. A hook may fit even when the full arrangement does not.

For A/B, count every pluck as an event and duplicate its pitch when needed. For C/D, count unique pitches separately from events and respect the mechanism's repeat-rate and media limits. Start with a simple ascending pattern and a repeated-note pattern, then test Take On Me or another chosen hook. No song arrangement is validated yet.

Tuning workflow

Measure three mounted samples before generating a final tuning chart. For an otherwise unchanged uniform tine, L_new = L_old x sqrt(f_measured / f_target) gives a first length estimate. Tip masses, shaped flexures and changing clamps need additional calibration. Reserve a tuning adjustment rather than assuming the first print will be in tune. [1, 5]

References and status

1. <link href="https://murobox.com/en/our-story/the-comb/" color="#246B78">Muro Box: comb development and mass/root tuning</link>

2. <link href="https://www.bettermusicboxes.com/products/movements/installation/music-box-movement-instructions.asp" color="#246B78">Music Box Attic: Sankyo movement installation and damping</link>

3. <link href="https://kikkerland.com/products/make-your-own-music-box-kit" color="#246B78">Kikkerland: punched-strip music-box mechanism</link>

4. <link href="https://www.reuge.com/en/foire-aux-questions" color="#246B78">Reuge: soundboard coupling and enclosure effects</link>

5. <link href="https://help.solidworks.com/2026/english/simtutorialonline/Dynamic_Analysis_of_a_Cantilever_Beam.htm?id=1.0.1.3" color="#246B78">SOLIDWORKS: uniform cantilever frequency model</link>

Original concept improvements in this brief are engineering proposals. Manufacturer references establish underlying principles or existing architectures, not the performance of these proposed fidgets. Exact dimensions, materials, tuning, song compatibility and life testing remain pending.
