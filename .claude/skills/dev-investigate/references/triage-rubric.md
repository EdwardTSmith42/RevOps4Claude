# Triage rubric — unified terminal states

The unified triage vocabulary used across `recurring-hunt` and `latent-hunt`. **Investigate until you can confidently land on one of these four terminal states** — the rubric does not include "still investigating" as a state; that's the implicit in-progress state before triage completes.

## The four terminal states

- **`FIX_NOW`** — obvious, low-risk, in-scope bug with a credible proof path. Fix in this pass.
- **`HUMAN_DECISION`** — real and could be addressed, but the right path needs a human call (requirements conflict, tradeoff unclear, risk needs product judgment). Surface with a recommendation; don't fix unilaterally.
- **`DEFER`** — real and could be fixed but should be follow-up work (UI/UX change, risky behavior shift, architecture change, requirement ambiguity, broader pre-prod redesign). Invoke the `dev-scope-deferral` skill to capture as a deferred-investigation note.
- **`DISMISSED`** — suspicion does not survive evidence. State the contradicting evidence explicitly.

## What about "RISKY"? What about "INVESTIGATE_LOCAL"?

Legacy variants of this rubric carried divergent vocabularies — one used FIX_NOW / HUMAN_DECISION / RISKY; another used FIX_NOW / INVESTIGATE_LOCAL / DEFER / DISMISSED. The unified rubric collapses these:

- **`RISKY`** items collapse to either `HUMAN_DECISION` (if the risk needs a human call) or `DEFER` (if real but should be follow-up). The "RISKY" label was hiding which decision was actually needed; splitting forces the disambiguation.
- **`INVESTIGATE_LOCAL`** is *not* a terminal state — it's the in-progress signal that you're still investigating, not yet at a decision. The vocabulary applies only at terminal moments. While investigating, the item is "in flight"; when investigation completes, it lands on one of the four terminal states.

## Why terminal-states-only

The rationale: "Risky is either a human decision or defer — investigate until you can get to one of these four."

Terminal-states-only forces the question to resolve. "Still investigating" is a process state; once enough evidence is in, the item moves to FIX_NOW (we can act) / HUMAN_DECISION (we need product input) / DEFER (right thing, wrong time) / DISMISSED (turned out not to be a real issue). The rubric refuses to let items linger as "RISKY" forever.

## Triage vs. severity

Triage (FIX_NOW / HUMAN_DECISION / DEFER / DISMISSED) is **what to do now.** Severity (`P0–P3` per `severity-rubric.md`) is **how bad it would be unaddressed.** Always state both.

Examples:
- `P0 / FIX_NOW` — critical, fixing now.
- `P0 / HUMAN_DECISION` — critical, but path forward needs a human call.
- `P2 / DEFER` — meaningful but not urgent; capturing for follow-up.
- `P1 / DISMISSED` — looked critical, evidence says no.

## Used by

- `recurring-hunt` mode — every credible suspicion gets triaged to one of the four states.
- `latent-hunt` mode — every finding gets triaged.

## Malleability note

**Canonical:** the four terminal states (`FIX_NOW` / `HUMAN_DECISION` / `DEFER` / `DISMISSED`) and the terminal-only discipline. Adding a state ("INVESTIGATING" / "RISKY") reintroduces the in-flight ambiguity the rubric prevents.

**Adaptable:** how aggressively each state is used in different contexts. A code-review challenger might lean on HUMAN_DECISION more; a recurring-hunt run might lean on DEFER more.

