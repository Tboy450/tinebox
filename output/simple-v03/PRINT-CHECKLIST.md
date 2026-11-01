# First print and observation checklist

## Before slicing

- [ ] Choose standard PLA or PETG for one comparison set.
- [ ] Start with A's three parts, or only the shared three-length comb for a rough sound check.
- [ ] Import in millimetres at 100% scale. Preserve the supplied part orientations.
- [ ] Confirm 0.4 mm nozzle and a consistent 0.20 mm layer height, including the first layer.
- [ ] Inspect tine lines, roots, nut-pocket bridges and optional carriage support regions.
- [ ] Keep the test tines solid and clean; avoid supports on the free tines.

## Manual sound test A

- [ ] Flip the comb into assembly orientation, thick roots down and smooth bed-facing face up.
- [ ] Clamp with two M3 x 10 screws/nuts; check that the root regions sit flat.
- [ ] Pluck gently and record each tine separately.

| Material / settings | Tine free length, mm (nominal) | Actual thickness, mm | Measured fundamental, Hz | Ring / click / buzz | Notes |
|---|---:|---:|---:|---|---|
| | 26 | | | | |
| | 22 | | | | |
| | 18 | | | | |

## Slider B, only after A produces useful tones

- [ ] Confirm the carriage rests on both rails without rocking or scraping.
- [ ] Confirm the bridge clears the installed comb screw heads.
- [ ] Seat the pick on its floor and retain it with the captured M3 nut/screw.
- [ ] The minus-0.2 mm setup pick passes without touching a tine.
- [ ] With the 0.2 mm pick, observe one clean release per tine, no catch and no continuing contact during ringing.
- [ ] Lift clear for the return stroke.
- [ ] Record misses, double plucks, operating feel, release noise and visible wear; stop and revise any snag.

Only after these observations should the optional song comb be tuned and tested. A successful mesh or slicer preview is not a passed musical test.


## v0.3 split-holder additions

- Print the bridge roof-down and the holder on the supplied side orientation. Inspect internal bridges in the slicer; no support-free result is established yet.
- Print two 0.8 mm mounting spacers. Use two M3 x 8 screws and two nuts for the holder. Spacers go above the bridge beneath the screw heads; nuts go below the holder tab.
- Check the two mounting screw ends stay above the tine travel. Nominal gap is 1.2 mm to resting tines; actual hardware and print tolerances must be checked.
- Use the renamed B_05 pick files. Begin with the minus-0.2 mm clearance pick; lift the carriage for every return.
- Record measured fundamentals in calibration-template.json; the tuning utility deliberately refuses blank measurements.
- See README-FIRST.md for the complete updated assembly order; older integral-holder instructions are superseded.
