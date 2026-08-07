# Severity rubric

The P0–P3 severity vocabulary used across `latent-hunt` and `recurring-hunt`.

## The four levels

- **`P0/P1`** — correctness, data loss, authorization, duplicate side effects, broken handoffs. Action-required immediately or near-immediately.
- **`P2`** — latent reliability or stale-state risks likely to produce bugs later. Action-required but not blocking.
- **`P3`** — cleanup or maintainability issues, only if they plausibly hide defects. Otherwise drop.

## Calibration heuristics

### P0/P1 indicators

- User-visible data loss or corruption.
- Authorization bypass (user A sees/edits user B's data).
- Duplicate side effects (same email sent twice, same charge applied twice).
- Broken handoffs that block downstream flows entirely.

### P2 indicators

- A retry/idempotency gap that hasn't manifested yet but will under load.
- Stale state in a cache/SWR layer that produces inconsistent UI for some users.
- Performance cliff that would manifest at higher scale.

### P3 indicators

- Code smells, naming issues, structural messiness — only worth surfacing if they plausibly hide a defect.
- Otherwise: drop. Don't sweep cleanup work into a bug-hunt finding.

## Severity vs. triage

Severity (P0–P3) is **how bad is this if it ships unaddressed.** Triage (`FIX_NOW` / `HUMAN_DECISION` / `DEFER` / `DISMISSED`) is **what do we do now.** They're related but distinct:

- A `P0` finding might be `HUMAN_DECISION` (we can't fix it without a product call).
- A `P2` finding might be `FIX_NOW` (it's small and we have a clean fix path).
- A `P3` finding is usually `DISMISSED` (doesn't survive evidence) unless there's a hidden defect.

Always state both: the severity AND the triage state.

## Used by

- `latent-hunt` mode — Step 6 (Rank what matters).
- `recurring-hunt` mode — accompanies the triage rubric for severity language when ranking helps.

## Malleability note

**Canonical:** the four-level vocabulary (P0/P1/P2/P3) and the criteria above. Promoting a P2 to P1 without evidence inflates the report.

**Adaptable:** how aggressively to surface P3s. In `latent-hunt`, P3s usually drop unless they plausibly hide defects. In other contexts (architectural reviews, refactor plans), P3s might be more central.

