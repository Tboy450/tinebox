# TINEBOX C-01

A 3D-printable musical fidget built around a comb of printed, tuned tines, developed for standard PLA and PETG.

**Status:** early prototype. The parts are digitally checked but not yet printed and sound-tested, so treat the
tuning tables as starting estimates.

## Start here

- [`output/simple-v03/`](output/simple-v03/): the current first-build package. Read `README-FIRST.md` before printing.
  - **A:** a manual three-tine sound test.
  - **B:** a dual-rail slider that plucks the same comb.
- [`output/simple-v02/`](output/simple-v02/): the previous first-build package.
- [`output/prototypes-v01/`](output/prototypes-v01/): early mechanisms. These include a slider bench, a one-note peg/tooth
  cylinder fixture, rotating-tine wheel and cylinder layouts, material samples and synthetic melody previews.
  `V01-AUDIT-NOTICE.md` lists the known v0.1 seating errors.
- [`PROJECT_SCOPE.md`](PROJECT_SCOPE.md): the concept family, design rules and next steps.

## Tools

- `calibrate_comb.py` fits measured tine frequencies to a frequency model and predicts lengths for a short melody comb.
- `build_simple_v03.py`, `build_simple_v02.py` and `develop_prototypes.py` generate the printable models.
