# Recognizable melody candidates

October 26, 2026. Recognition is a design target, not a tested listener result. The first three are simplified single-line arrangements made for this project, checked against the linked source scores for melodic contour. Accompaniment and original performance details are omitted; some rhythms, register and endings are adapted to make short prototype hooks.

| Hook | Programmed plucks | Unique pitches | Current range | First useful mechanism |
|---|---:|---:|---|---|
| Twinkle, Twinkle - opening two phrases | 14 | 6 | C5-A5 | S2 event comb; tests repeated pitches and a held-note gap. |
| Ode to Joy - opening four bars | 15 | 5 | C5-G5 | S2 event comb or later five-pitch drum bank; includes unequal onset spacing. |
| Fur Elise - opening nine-note hook | 9 | 6 | A4-E5, including D#5 | Short S2 cartridge; illustrates that a compact hook can need chromatic pitches. |
| Take On Me | Not transcribed for this prototype | Pending | Pending | Retain as a reference-supported slider candidate; verify the desired excerpt before setting a tine bank. |
| Billie Jean | Not transcribed for this prototype | Pending | Pending | Retain the modular TinkerBeat example as a design reference; note order, rhythm and repeat rate need analysis. |
| Mario theme | Not transcribed for this prototype | Pending | Pending | Reference shows a printed PLA implementation; arrange the selected hook before sizing our comb. |
| Harry Potter theme | Not transcribed for this prototype | Pending | Pending | Retain as a compact slider candidate; check chromatic requirements and exact excerpt. |

The event comb duplicates repeated pitches. A cylinder with pegs or teeth operating a fixed tuned bank can reuse a pitch, but must release and retrigger it reliably. W1/T1 rotating-tine layouts currently carry the seven-event opening `C5 C5 G5 G5 A5 A5 G5`; the longer arc after the last G supplies a held-note/loop pause.

## Source scores and arrangement notes

- **Twinkle theme:** [Mutopia, Ah Vous Dirai-Je Maman, section 9 on printed p. 7](https://www.mutopiaproject.org/ftp/MozartWA/KV265/guitar-duo-complete/guitar-duo-complete-a4.pdf). This is an arranged Mozart theme; our prototype uses the familiar traditional Twinkle contour in C5 and simplified rhythm, not the guitar duet's accompaniment or ornaments. Typeset edition credits J. J. Olson.
- **Ode to Joy:** [Mutopia score](https://www.mutopiaproject.org/ftp/BeethovenLv/ode/ode-a4.pdf). First four bars' upper melody transposed from G major to C major in the C5 register. The source credits Peter Chubb and marks the typesetting public domain.
- **Fur Elise:** [Mutopia score, p. 1](https://www.mutopiaproject.org/ftp/BeethovenLv/WoO59/fur_Elise_WoO59/fur_Elise_WoO59-a4.pdf). First nine melody events, omitting accompaniment and using an arranged pause after A4. The source credits Stelios Samelis and marks the typesetting public domain.

Downloaded source PDFs and relevant page images are retained in `sources/song-scores/` at the project root. The supplied auditions are newly synthesized simple tones, not third-party recordings.

## Reference videos already reviewed

- Harry Potter: https://youtube.com/shorts/nV9u4X7dYek?is=WeK_5N_Aj43JDjRs
- Billie Jean: https://youtube.com/shorts/lEc4aHEni4g?is=tdfq9eNd12rehmYV
- Mario: https://youtube.com/shorts/psD3SIR17wg?is=KPSG9ab3aSVrC6R1
- Take On Me: https://youtube.com/shorts/sfUIth6qXWM?is=w3UgHEAt8ZQTcboo

## Practical fit checks

S2 uses 5 mm per shortest programmed time unit. Its current spans are 70 mm for Twinkle, 140 mm for Ode and 40 mm for Fur Elise. The long universal deck accommodates all three; a song-specific pocket model can be shorter later. At constant carriage speed these distances preserve the chosen relative onset timing. Manual swipes still vary tempo.

For a rotating pitch selector, angles encode onsets and hand speed controls tempo. The JSON angles are a program sketch, not verified drum pin positions or a collision-checked melody cylinder. A tine's damping and reset time limit repeated notes. [Muro Box documents this constraint for its own mechanisms](https://murobox.com/en/app-tutorial/); its numerical limits must not be copied to our printed designs.

Listen to the synthetic auditions to choose the first hook, then assess recognizability again using recordings of the actual printed instrument. Exact note calibration must precede any claim that a song cartridge plays in tune.
