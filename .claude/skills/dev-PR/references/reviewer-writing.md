# Reviewer-Oriented PR Writing

Use this reference when authoring PR brief sections that will become reviewer-facing PR body content.

## Goal

Help a reviewer understand the change quickly enough to trust it:

- what changed
- why this shape was chosen
- which patterns stayed the same
- which patterns changed on purpose
- where to start reading
- what proof or guardrails matter

This is not a changelog. It is orientation plus confidence.

## Default Writing Shape

- `Reviewer Summary`: 1-3 short paragraphs or bullets that explain outcome, code shape, and why the reviewer should care.
- `Reviewer Guide`: 3-7 bullets that tell the reviewer where to start and what each file proves.
- `Big Picture`: before/after system or flow explanation.
- `Why This Shape`: why this approach was chosen, what blast radius was avoided, and what stayed familiar.
- `How It Works`: ordered mechanism, state ownership, error path, and lifecycle.
- `Patterns Preserved`: boundaries, contracts, utilities, and practices intentionally kept.
- `Patterns Changed`: responsibilities or contracts intentionally moved or tightened.
- `Mental Model`: one framing idea that makes the diff easier to read.

## Writing Rules

- Lead with user impact and system shape, not metadata.
- Explain why a file matters, not just that it changed.
- For critical files, say what contract or invariant the file owns.
- Call out preserved patterns explicitly when touching high-blast-radius code.
- Say what changed intentionally so reviewers do not mistake it for accidental drift.
- Prefer “before / after / why” framing over “implemented X in file Y”.
- Keep section text human and high-signal; let links and file names support the story.

## Summary Rules

- Do not lead with `Detail level`, `Evidence`, or other bookkeeping unless a human specifically needs it first.
- If it is a bug fix, open with the visible regressions/fixes in plain language.
- If it is a feature or infrastructure-heavy change, open with the new behavior and the code-shape decision.

## Reviewer Guide Rules

- Point to the few files that carry the story.
- Use ordered prompts such as `Start with`, `Then check`, `Then confirm`.
- Mention supporting files as a group instead of dumping the whole diff.
- Include tests only when they prove a specific edge or invariant.

## Pattern Notes Rules

- `Patterns Preserved` should answer: what familiar architecture or utilities still anchor this change?
- `Patterns Changed` should answer: what responsibility moved, tightened, or became explicit?
- If a high-risk file changed, name the safety property that was preserved.

## Do / Do Not

Do:

- explain rationale, not just implementation
- mention preserved contracts in high-risk areas
- tell the reviewer what to read first
- show that good practices were followed with concrete statements

Do not:

- narrate every touched file
- restate the PR title in five different ways
- hide important contract changes inside vague summary bullets
- confuse “lots of code shipped” with “lots of text dumped”
