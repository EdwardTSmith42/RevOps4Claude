# Branch brief — `<branch-slug>`

> Saved at `docs/change-briefs/open/<branch-slug>.md` (or repo-local equivalent). Preserve authored prose on rerun — only diff stats / metadata refresh.

## Why now

<the trigger that made this work necessary now: Sentry issue, customer report, deadline, incident>

## Bug / Problem

<what's broken or missing in plain language>

## Outcome

<what users / reviewers should expect after this lands>

## Evidence / Error Data

<at least one of: Sentry/log/API snippets with links, OR Verbatim Signals (quoted user/customer/internal statements). Be concrete — generic boilerplate fails validation.>

## Verbatim Signals

<optional; quoted user / customer / internal statements>

## Plain-Language Fix

<what this fixes for users, written so someone new to the codebase can understand it>

## User-Facing Bug Fixes

<bug-fix PRs only — one or more plain-language bullets describing each regression/fix from the user-experience perspective>

- <plain-language fix bullet>
- <plain-language fix bullet>

## Scope

<minimal low-risk scope — what's in, what's intentionally not>

## Risk / Blast Radius

<medium/high-risk PRs only — what could break, what's the blast radius, what's been verified>

## Rollout / Rollback

<medium/high-risk PRs only — staged rollout plan, rollback path>

## Monitoring

<medium/high-risk PRs only — what dashboards / alerts to watch post-merge>

## Open Questions

<unresolved decisions that reviewers or the user should weigh in on>

## Reviewer-Facing Sections (preferred over deterministic fallbacks)

> Author these in the brief itself. The PR body builder uses these verbatim — they are the reviewer-orientation prose the PR depends on.

### Reviewer Summary

<1-3 short paragraphs or bullets that explain outcome, code shape, and why the reviewer should care>

### Reviewer Guide

<3-7 bullets ordered with "Start with", "Then check", "Then confirm" — point to the few files that carry the story>

### Big Picture

<before / after system or flow explanation>

### Why This Shape

<why this approach was chosen, what blast radius was avoided, what stayed familiar>

### How It Works

<ordered mechanism: state ownership, error path, lifecycle>

### Patterns Preserved

<boundaries, contracts, utilities, and practices intentionally kept (especially in high-blast-radius areas)>

### Patterns Changed

<responsibilities or contracts intentionally moved, tightened, or made explicit>

### Mental Model

<one framing idea that makes the diff easier to read>

### File Notes

- `<path>`: <why this file matters to the review>
- `<path>`: <what contract or invariant the file owns>
