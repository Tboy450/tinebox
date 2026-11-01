# v0.1 assembly correction - October 27, 2026

The v0.1 S2 slider and P1 cylinder assemblies are superseded as first-build recommendations. Their mesh checks did not account for gravity seating of the loose fits:

- S2's 0.3 mm roof gap could remove its intended 0.2 mm pick engagement.
- P1's two 0.3 mm radial clearances could let its drum settle 0.6 mm below the modelled position, cancelling its intended 0.3 mm lift.

The revised first-build set is in `output/simple-v02/` at the project root. Start with its manual three-tine fixture; the second fixture uses a two-rail slider and explicit pick/rail seating datums. The cylinder needs a later clamped-shaft/adjustable-comb redesign.

The old ZIP is preserved as an historical development snapshot. The wheel and tine-cylinder remain exploratory layouts, not working product designs.
