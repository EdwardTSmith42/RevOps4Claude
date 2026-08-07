# Lane status vocabulary

The required status vocabulary for evidence-collection lanes. Mandates "fallback attempted" so lanes don't get silently abandoned.

## Status values

Every lane has exactly one status:

- **`complete`** — the lane was collected fully and produced usable evidence.
- **`partial`** — the lane was attempted and produced some evidence, but not all expected artifacts. Record what was missing and why.
- **`blocked`** — the lane could not be collected at all. **Required:** the blocker reason and the fallback attempted.
- **`pending`** — the lane has not yet been attempted (only valid mid-investigation; should resolve to one of the above by report time).

## The fallback-attempted requirement

When a lane is `blocked`, the report must include:

1. **Blocker reason** — what specifically prevented collection (auth failed, replay didn't load, log retention exceeded, etc.).
2. **Fallback attempted** — what was tried instead (alternate query, different tool, request-via-other-team, etc.).

If no fallback was attempted, name that explicitly. Never silently leave a blocked lane without acknowledging it; future investigators read the lane-status matrix to know what's been tried.

## Used by

- `evidence` mode — every lane in the four-lane taxonomy gets a status.
- `pr-interrogate` mode — production correlation lanes report status.
- `recurring-hunt` mode — challenger/runtime lanes get statuses; specifically tracks `AUTH_BLOCKED` for tool-auth failures.

## Notes

- **`AUTH_BLOCKED`** is a more-specific blocker than generic `blocked` — used when a tool's auth probe fails (e.g., an external reviewer CLI returns an unauthenticated error). Distinct from `NO_SIGNAL` (ran cleanly, found nothing). Conflating them silently degrades the entire investigation.
- Status values do not have aliases. "completed" / "validated" / "done" all mean different things to different readers; the vocabulary is fixed at `complete` / `partial` / `blocked` / `pending` to keep cross-mode consistency.

## Malleability note

**Canonical:** the four status values + the fallback-attempted requirement on `blocked`. Loosening these (allowing aliases, dropping fallback-attempted) is what causes lanes to get silently abandoned.

**Adaptable:** the rendering format (matrix vs. inline annotations) and how status fields appear in the final report.

