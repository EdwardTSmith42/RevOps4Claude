# Book Survey Method

The survey procedure for `from-book` stage 1. Maps a book's voice landscape so the capture plan can recommend appropriate layers (master voiceprint, per-POV overlays, style samples). Survey is fast and chapter-level. Detailed analysis comes later in stage 3 only on the layers the user approves.

## What the survey produces

A short report covering five questions. The report is the input to stage 2's capture-plan recommendation. The format is documented in `../templates/book-survey-output.md`.

The five survey questions are: how many POV characters appear and which chapters belong to each, what scene types appear and how distinctively are they treated, what register variations exist across chapters, are there any structural voice anomalies (different narrators, found-document insertions, epistolary sections), what's the dominant voice that the master voiceprint will need to capture.

## How to scan

A book-length manuscript is too long to read line by line at the survey stage. The goal is mapping, not analysis. The scan procedure samples strategically:

**Chapter beginnings and endings.** Open every chapter and read the first and last 100-200 words. Chapter starts often establish POV and register quickly. Chapter ends often reveal pacing and tension-handling. Together they give a fast map across the book.

**Mid-chapter sample passages.** From every third or fourth chapter, sample one mid-chapter passage of 200-300 words. This catches scene-type variations the chapter-edge scan might miss. A book with quiet dialogue chapters and intense action chapters reveals the variation quickly when mid-chapter samples run side by side.

**Anomaly hunting.** Scan the chapter list and table of contents (if any) for chapters with unusual titles, format breaks (a chapter that's a list, a letter, a found document), or POV indicators. These are likely register-shift candidates worth flagging.

The scan covers the whole book in maybe 30-50 sample passages totaling 5-10k words, which is enough to map the voice landscape without committing to full extraction time.

## Identifying POV characters

POV identification is the most important survey output for fiction. Patterns to spot:

**Close third or first person:** The POV character is named in scene-opening prose or the narrative voice clearly belongs to a single character. Track which chapters belong to which character.

**Omniscient or distant third:** The narrator is not a character. Voice variations across chapters reflect setting or scene type more than POV. Treat as a single POV (the narrator's) for capture purposes.

**Multi-POV (close third or first):** Two or more POV characters carry chapters. Identify which character holds which chapters. Note whether the narrative voice differs across POVs (a literary multi-POV book often has subtly different voice per character, while a commercial multi-POV book often has the same narrator-voice across all POVs).

**POV shifts within a chapter:** Less common but worth flagging. May indicate intentional craft (the writer is doing head-hopping for effect) or drift (the writer didn't notice shifting). The mode flags either way. The user knows which is which.

**Frame narratives:** A chapter with a different POV than the rest (a prologue from a different character, a flashback in another voice). Flag as a register variation worth a possible style sample but probably not worth a full POV voiceprint unless the variation recurs.

The capture plan recommends a per-POV voiceprint overlay only when the POV's voice differs meaningfully from the master. A book with three close-third POVs that all read with similar register doesn't need three voiceprints — one master is enough. A book with three POVs that have distinct interior voices does need overlays.

## Identifying scene types

Scene type variation matters because some scene types have voice-distinctive treatments worth capturing as style samples. Common scene types to watch for in fiction:

**Action scenes:** Combat, chases, physical confrontation. Often paratactic short sentences, present-tense punch even in past-tense narratives, accelerated pacing. Worth a style sample if the writer has a distinctive action treatment.

**Dialogue-heavy scenes:** Two or more characters in extended conversation. Often character voice does heavy lifting, narrator pulls back. Worth a style sample if dialogue is a signature strength.

**Interior reflection:** A character thinking, processing, remembering. Often closer to the writer's lyrical or psychological register. Worth a style sample if interior writing is a strength.

**Descriptive passages:** Setting, weather, environment, atmosphere. Often where prose texture lives. Worth a style sample if descriptive writing is a strength.

**Exposition:** Worldbuilding, backstory, system rules (in genre fiction). Often a different register from scene work. Sometimes worth a style sample for genre-specific exposition (e.g., a magic-system explainer that the writer handles distinctively).

**Comic relief:** A scene where the register lightens for tonal contrast. Worth a style sample if comic moments are signature.

A scene type warrants a style sample only when the writer's treatment of it is distinctive enough that drafting would benefit from the few-shot exemplar. A generically-handled action scene doesn't need a sample. A noir-paratactic action sequence does.

## Identifying register variations

Beyond POV and scene type, some books have broader register variations worth mapping:

**Genre hybrids:** Literary thrillers, magical realism, romance with comedic register breaks. The master voiceprint may need a genre overlay (a `fiction-thriller-pacing` or `fiction-romance-comedic` overlay) that captures the secondary register.

**Time-period or chapter-format variations:** Historical chapters in one register, present-day chapters in another. Found-document chapters (letters, journal entries, transcripts) in a different format. Flag as candidates for style samples or genre-overlay voiceprints.

**Tonal arcs:** A book whose register shifts deliberately across acts (light first half, dark second half). Usually one master voiceprint is right (the dominant register), but flag the shift in survey notes for the capture plan.

## Producing the survey report

The survey report is short — 200-400 words. It answers the five questions concisely with examples drawn from the chapter list and sample passages. The report is presented to the user in stage 2 alongside the capture-plan recommendation.

A typical survey report might read like this. *"This is a 312-page urban fantasy with three close-third POV characters: protagonist Nova (chapters 1-4, 7-9, 12-15), antagonist Harvard (chapters 5-6, 10-11), and a brief frame narrator (prologue, epilogue). Nova's interior is distinctive — noir-inflected, paratactic, sensory. Harvard's interior is sparser, more observational. The frame narrator's voice differs from both and is distinct enough to flag, though the limited page count probably doesn't warrant a full voiceprint. Scene types include extended action sequences (notably chapters 2 and 14), dialogue-heavy investigation scenes (chapters 7-8), and a recurring flashback motif (Nova's childhood — chapters 3, 9, 14). The overall register is dark urban fantasy with noir signatures — tactile, grime-textured, period-appropriate slang."*

From this survey, the capture plan recommends: master voiceprint scoped `fiction-urban-fantasy`, per-POV overlay for Nova (her interior voice is distinctive), per-POV overlay for Harvard (his observational distance is distinctive), action-scene style sample, interior-reflection style sample (the flashback motif), no overlay for the frame narrator (limited content).

The user sees the survey, sees the plan, and adjusts.

## What the survey does NOT do

The survey is mapping, not extraction. The survey does not run voiceprint analysis on any layer (that happens in stage 3). The survey does not produce style sample passages (those are extracted in stage 3 once the user approves). The survey does not commit the user to any layer — the capture plan is a recommendation, not a contract.

The survey also does not exhaustively analyze the manuscript. A 100k-word book is too long for full reading at the survey stage. The 30-50 sample passages are enough to map the landscape. The user can ask for re-survey or additional sampling if the plan feels off.

## When the survey suggests skipping the from-book mode

Sometimes the survey reveals that from-book is the wrong tool. A book with no POV variation, no scene-type distinctiveness, and a single dominant register would produce a master voiceprint indistinguishable from running from-sample on a 3-5k word excerpt. In that case, the mode surfaces this finding and recommends from-sample on a representative chapter instead.

This is rare for fiction (most fiction has at least some variation worth capturing) but common for non-fiction books (a memoir or business book with one consistent voice throughout). The mode is honest about when the survey-and-layered-plan adds value vs. when it's overhead.
