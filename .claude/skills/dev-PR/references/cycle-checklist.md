# PR cycle checklist

Three lifecycle stages with explicit out-loud self-answers. The point of out-loud is to prevent rubber-stamping — the agent naming each answer, with evidence, forces a real check. The user is not asked to confirm items; unverifiable items are flagged as such.

## Begin (start of PR-prep work)

Confirm before authoring the brief:

- **Branch is not protected** (`main`, `develop`, `release/*`). If it is, hard-stop and say why; proceed only on the user's explicit unprompted instruction (`--allow-protected-branch` semantics).
- **PR author will be you** (not someone else's branch). Skip enforcement when the open PR author is not the current `gh` user.
- **Scope is bounded** — there's one coherent thing this branch does, not three unrelated things bundled together.
- **Evidence exists or will exist** for the brief — Sentry issue, customer report, log snippet, verbatim signal, or screenshot.

## During (mid-implementation)

Run periodically as work progresses:

- **Brief is being kept current** — when scope shifts, update the brief; don't let the brief drift behind the code.
- **Reviewer-facing sections are being authored** — `Big Picture`, `How It Works`, `Patterns Kept vs Changed`, etc. Don't leave these for the last minute.
- **Generated artifacts identified** — swagger.json, generated SDK files, lockfile changes flagged early.
- **Tests track behavior, not implementation** — added tests cover user-visible behavior or invariants, not just internals.

## Pre-open (immediately before `gh pr create`)

Out-loud self-answers (with evidence) required to gate PR creation:

| Item | Confirms |
|---|---|
| `state-model` | Data shape and ownership boundaries verified |
| `error-path-simple` | Failure modes considered; no swallowed errors |
| `canonical-utilities` | Reused existing helpers vs. reinventing |
| `scope-focused` | Nothing unrelated bundled in |
| `nonself-audit` | A reviewer who didn't write this could understand it from the brief |
| `out-loud-checklist` | This list itself was actually walked through, not skipped |
| `lockfiles-required` | If lockfiles changed, the dependency change is intentional (not churn) |

If any item is unanswered, **block PR creation**. The block is recoverable; an unintended PR isn't.

## Lockfile discipline

Default: no lockfiles in PR (`yarn.lock`, `package-lock.json`, `uv.lock`, `Cargo.lock`, etc.).

If the change requires a lockfile update:
1. Confirm the dependency change is intentional (not unrelated regen).
2. Determine `lockfiles-required` from the branch's own history; escalate to the user only if intent is undeterminable.
3. Mention the dependency change in the brief's `Patterns Changed` section.

If lockfiles are present and intent can't be established: **block PR creation** until intent is established or the churn is removed.

## Malleability note

The pre-open confirmation list is **canonical** — the seven items reflect a gate-discipline pattern validated across many real PRs.

The mid-implementation guidance and protected-branch handling are **adaptable** — different repos / orgs have different conventions for protected branches, brief locations, and what counts as "scope creep."
