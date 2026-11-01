# Video review and future acoustic development

Reviewed October 26, 2026. These project notes are NOT part of the outgoing lab email or its attachments. The user asked to keep the fuller-sound development in the project.

## Review boundary

All four supplied Shorts were opened in the browser, their visible devices and playback frames inspected, and their titles/channels/descriptions read. This is a visual and mechanism review. There is no captured, calibrated audio or measured spectrum, loudness, decay, pitch accuracy, material stiffness or internal CAD. Do not claim that we have objectively heard or measured a superior design. Songs and graphics are references, not chosen arrangements.

## Reference-by-reference findings

1. Harry Potter theme, Stan 3D / @stan.3dprints: https://youtube.com/shorts/nV9u4X7dYek?is=WeK_5N_Aj43JDjRs
   - A small framed comb with a top sliding control is visible. The title credits kida.
   - Useful features: protected frame, accessible control and compact handheld interaction.
   - Development inference: isolate a rigid tuning clamp from the grip shell; make the picking part replaceable; check release at different hand speeds. No internal release mechanism or material properties were established.

2. Billie Jean / TinkerBeat, TinkerTwist - 3D Printing: https://youtube.com/shorts/lEc4aHEni4g?is=tdfq9eNd12rehmYV
   - Playback shows a separate comb-shaped song insert presented to a larger body with a wheel/control below. It suggests a modular song interface, but the hidden transmission/contact mechanism was not verified.
   - Useful features: distinguish song media from a reusable housing and give the hand a clear control area.
   - Development inference: investigate a positively located cartridge with a repeatable clamp and tune after seating. A wheel alone does not establish how repeated pitches or rhythm are encoded.

3. Mario fidget, gcodelab / @gcodelab_official: https://youtube.com/shorts/psD3SIR17wg?is=KPSG9ab3aSVrC6R1
   - An elongated framed tine row and separate build-plate parts are visible. Creator description identifies a Bambu Lab A1, matte PLA by EXTRUDR and a MakerWorld kida model.
   - This is creator-reported evidence of a PLA implementation, not evidence that our proposed dimensions will tune correctly on the U1.
   - Useful features: extra row length accommodates more events. Tradeoff: pocket size, travel length and root stiffness.

4. Take On Me, TinkerTwist - 3D Printing: https://youtube.com/shorts/sfUIth6qXWM?is=w3UgHEAt8ZQTcboo
   - The black/gold framed tine device and top slot match the reference screen photograph supplied by the user.
   - Useful features: simple visual note sequence and an obvious thumb travel direction.
   - Development inference: preserve clear hand placement, provide tuning access and leave the vibrating areas clear of fingers. The title's precision claim is not an independent tuning measurement.

## Improve sound as an experimentally tested design objective

The goal is fuller, less thin sound with useful low/mid presence, clear note attack, balanced notes and manageable mechanical noise. It is separate from the songs in the reference clips. More openings or a larger empty cavity do not guarantee improvement, and an acoustic body will not create missing melody pitches.

1. Establish a repeatable pluck first. Use a replaceable compliant pick with adjustable engagement. A larger pluck may give more energy but also adds force, stress, impact noise and damping; use measurements rather than maximum lift.
2. Design a deliberate vibration path from the comb clamp to a radiating panel. A rigid mount can transfer energy to a larger surface; avoid accidentally isolating it with a soft gasket. Coupling can also shorten sustain or shift tuning, so measure notes after final mounting.
3. Compare one thin replaceable soundboard with the ordinary rigid shell, using the same comb and pluck. Candidate panels include printed PLA, printed PETG, and later a thin wood insert if a hybrid build is acceptable. Try a larger panel as a desktop/docking option when pocket size limits radiation. Panel modes may favour some notes, so test the complete register.
4. Make chamber depth and the back panel interchangeable. Compare open back, closed back and one controlled port before adding decorative openings. Use a constant panel/clamp while changing volume, then a constant cavity while changing port geometry. Helmholtz-type tuning is a possible narrow-band experiment, not a broadband bass promise.
5. Keep grip pads on structural areas and provide clearance around vibrating panels. Compare hand-held and table-supported operation: a hand can damp the soundboard, while a table can change the radiating structure.
6. Reduce slider rattle, gear chatter and detent clicks separately from the musical path. Make detents removable during sound tests. Damp an unwanted shell rattle locally; damping the comb or its soundboard may also remove desired ringing.
7. For a future metal-tine option, compare a bought/tuned comb or a documented steel coupon against the printed baseline. Added mass or shaped roots can change pitch and overtones, but invalidate the uniform-tine table. Keep current standard PLA and PETG development active.

## Controlled comparison plan

- Begin with one mounted comb, C5/G5/C6 test notes and fixed pick geometry. Use an instrumented or otherwise repeatable release; hand swipes alone are too variable for ranking small changes.
- Record a fixed microphone position and distance, fixed gain with automatic gain/processing disabled where possible, and the same room. Preserve raw WAV files rather than comparing platform-processed Shorts.
- Compare the baseline bare deck, panel-only radiator, body/back variants and optional dock one factor at a time. Keep a few repetitions per note and capture handling noise separately.
- Track fundamental frequency, spectrum, low/mid-to-high energy balance, decay and note-to-note level variation. Uncalibrated recordings support relative comparisons under the same setup, not absolute sound-pressure claims.
- Listen to matched-playback-level versions for tonal quality, and separately compare raw recordings for output level. A louder sample alone should not be labelled fuller or better.
- Build a final multi-note cartridge only after checking whether the preferred body improves one note at the expense of others.

## Supporting primary sources

- Reuge FAQ, resonance on a wooden surface and lid effects: https://www.reuge.com/en/foire-aux-questions
- Muro Box comb development, root shaping and tip-mass tuning: https://murobox.com/en/our-story/the-comb/
- Existing project tuning brief: output/pdf/TINEBOX-U1-preliminary-tuning.pdf (model estimates, not measured results).

All adaptations above are proposals to validate. No acoustic improvement has been demonstrated yet.
