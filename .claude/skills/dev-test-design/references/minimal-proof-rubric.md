# Minimal Proof Rubric

Judge a proposed proof plan against these questions before implementing it.

## Minimality

- does the plan name one primary proof artifact first?
- does it avoid a broad scenario matrix when one stronger proof shape exists?
- can the main risk be closed without adding a second lane?

## Diagnostic Value

- if the proof fails, will we know what kind of behavior is broken?
- does the proof bind to the real boundary instead of a convenience helper?
- would the proof catch a realistic wrong implementation?

## Fail-First Quality

- for bugs and refactors, does the plan include disconfirming evidence?
- for migrations, can the old and new behavior be compared on the same input?
- for flaky/opaque work, is there a bounded temporary signal-gathering step?

## Regression Fence

- does the plan protect one important adjacent behavior?
- is the regression fence tied to a stable public contract or law?
- does it avoid duplicating the primary proof artifact?

## Execution Cost

- can the proof run quickly enough to be used during iteration?
- are any slower lanes justified by named risk?
- does the plan avoid browser or end-to-end cost when a smaller proof shape would do?

## Good Signals

- one explicit behavior claim
- one primary proof mode
- one disconfirming check
- one or two artifacts total
- clear `what not to test`

## Bad Signals

- "add more tests"
- "run the full suite and see"
- giant checklists without a clear primary risk
- browser proof chosen because it feels realistic, not because it is necessary
