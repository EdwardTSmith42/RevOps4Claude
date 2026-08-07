# Status vocabulary

The canonical status terms for hypotheses, invariants, and lanes. Used across `evidence`, `pr-interrogate`, and `recurring-hunt` modes — and any future skill that calls into the investigate cluster.

## Hypothesis statuses

- `proposed` — articulated but not yet tested
- `in_test` — verification step is running or pending review
- `confirmed` — supported by sufficient evidence; high confidence
- `partially_confirmed` — supported in some scenarios but not all; needs scope-narrowing
- `rejected` — contradicted by evidence
- `abstain` — evidence is genuinely incomplete; do not force confirmed/rejected

## Invariant statuses

- `proposed` — defined but not yet validated
- `pass` — invariant holds under tested conditions
- `fail` — invariant violated; investigation should follow
- `abstain` — couldn't be validated; record what would resolve

## Lane statuses

See `lane-status-vocabulary.md` for the full treatment. Quick reference:
- `complete` / `partial` / `blocked` (with blocker reason + fallback attempted) / `pending`

## No aliases rule

Do not use synonyms or near-synonyms — they cause cross-mode drift:
- ❌ `validated` (use `confirmed` for hypotheses, `pass` for invariants)
- ❌ `completed` (use `complete` for lanes, `confirmed` for hypotheses)
- ❌ `done`, `finished`, `closed` — none of these mean anything specific in this vocabulary
- ❌ `unknown` (when reporting, use `abstain` to mean "couldn't determine"; "unknown" appears only in the unknowns bucket of atomic-hypothesis output)

When you find yourself reaching for a synonym, check this list and pick the canonical term.

## Why this works

The rule is preserved by *consistent reference* — each mode cites this doc and uses these terms verbatim. Drift happens when a mode quietly invents `done` or `validated`; consistent reference prevents it.

## Used by

- `evidence` mode — hypothesis statuses in the four-bucket output.
- `pr-interrogate` mode — assumption / hypothesis statuses.
- `recurring-hunt` mode — Local Investigation hypothesis statuses + lane statuses on challenger lanes.
- Any cross-system bug-comms workflow you maintain — when consuming investigation output for posting across systems, these terms should travel unchanged into the posted content.

## Malleability note

**Canonical:** the term lists themselves. Adding a new status requires user check-in.

**Adaptable:** how richly each status is rendered (e.g., a brief "confirmed" tag vs. a paragraph explaining the supporting evidence). The label is fixed; the elaboration is flexible.

