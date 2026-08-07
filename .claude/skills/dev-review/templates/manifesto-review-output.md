# Manifesto-review output template

Strict-ish template for `manifesto-review` mode output.

```markdown
# Manifesto Review — <scope reviewed>

## Scope reviewed
- <file/folder/branch/PR/existing-slice>
- <one-sentence description of what was reviewed>

## Trust layer reconstructed
- Canonical truth location: <answer>
- Files/services owning behavior: <list>
- How to run + verify: <answer or "unclear — flagged for note below">
- Known contracts/invariants: <list>
- Documented gaps: <list, or "none — flagged below">

## Findings and proposed improvements (max 3-5)

### 1. <Plain-language change name>
- **What to change:** <specific, concrete>
- **Why it reduces uncertainty:** <one-sentence reason>
- **Manifesto idea supported:** <one-sentence tie back to the manifesto, not a slogan>
- **Scope and risk:** <small / medium / large; risk-low / risk-medium / risk-high>
- **Implement now or deferred:** <now / deferred — with reason if deferred>

### 2. <...>
...

### 3. <...>
...

(Max 5 items in first pass. If code is already clear enough, say so plainly here and skip.)

## Approval checkpoint
<If user already requested changes inline: skip this section and go to Implementation Summary.>
<Otherwise: "Awaiting approval before implementation. Approve all, some, or none — and I'll implement only the approved subset.">

## Implementation Summary (when changes have been applied)
- Implemented:
  - <change 1> — <files touched> — <verification: targeted tests / contract tests / file evidence>
  - ...
- Deferred (captured via scope-deferral):
  - <change> — <note path>
  - ...
- Remaining uncertainty or gaps:
  - <gap>
  - ...

## Verification
- Review-only requests: cite concrete file evidence for each recommendation (above).
- Small code changes: <targeted tests run, results>.
- Contract/boundary changes: <focused contract tests run, results>.
```

## Notes

- 3-5 improvements max in the first pass (bounded count).
- "If the code is already clear enough, say that plainly and explain why no change is worth the churn."
- Tie each recommendation back to the manifesto in a sentence, not a slogan.

## Used by

- `manifesto-review` mode of `dev-review`.
