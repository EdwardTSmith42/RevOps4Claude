---
name: dev-super-review
description: >-
  Campaign-scale audit of a large branch or feature: decompose into reviewable
  slices, run parallel reviewer sub-agents against a multi-category rubric,
  track every finding in a stable-ID ledger, route product calls to a human
  decision queue, fix through skeptic-gated lanes, re-sweep repaired surfaces,
  and pin discovered platform quirks as permanent tests. Use this whenever a
  branch is too large to review in one sitting, before merging a long-lived
  feature branch, when the user asks for a "deep review", "full audit",
  "release-grade review", "super review", or "go through this whole branch" —
  even if they don't say "campaign". Also use when a review has produced many
  findings that now need orchestrated fixing. Do NOT use for a single PR or
  commit (dev-review), for investigating one bug (dev-investigate), or for
  critiquing a plan (dev-fresh-eyes).
version: 0.1.0
category: Troubleshooting
display_name: Super Review
tagline: Campaign-scale audit for branches too big to review in one sitting.
packs:
  - dev-pack
icon: 'phosphor:MagnifyingGlassPlus'
when_to_use: >-
  Reach for this when a branch or feature has outgrown a single review pass.
  It decomposes the change into reviewable slices, fans reviewer sub-agents
  across a multi-category rubric, tracks every finding in a stable-ID ledger,
  routes product judgment calls to you, and fixes through skeptic-gated lanes
  with re-sweeps until the ledger is clean. For a single commit or PR, use
  Code Review instead.
---

# dev-super-review

Audit a large branch the way a skeptical CTO would, using many agents: find
everything, decide deliberately, fix in parallel, and refuse to believe your
own fixes until an independent agent fails to refute them. Derived from a real
131-finding release audit; the workflow below is the distilled sequence.

## Workflow overview

```
0. Baseline        — full suites + generated-artifact regen-and-diff, banked
1. Slice           — 8-12 concern-shaped slices, one reviewer agent each
2. Ledger          — every finding gets a stable ID and a status
3. Decide          — needs-decision queue batched to the human
4. Fix             — parallel lanes; orchestrator commits; skeptic gate per commit
5. Second sweep    — fresh agents re-review every repaired surface
6. Pin & record    — engine truths become tests; docs/PR synced to the ledger
```

Phases 2–4 interleave in practice (the ledger lives; gates mint new findings).
Checkpoint with `dev-checkpoint` between waves.

## Phase 0 — Bank the baseline

Do this before any reviewer spawns. Skipping it cost the source campaign a
full investigation later.

1. Run the FULL test suites — every workspace, not just the feature's — and
   save the list of already-failing tests. This is the only way to tell
   pre-existing debt from your regressions later.
2. Regenerate all generated artifacts (SDK clients, API specs, route tables)
   and diff against the committed copies. Treat committed generated code as
   unverified until regenerated: on the source campaign it was months stale,
   exported 76 phantom types, and concealed a live runtime bug.
3. Note the merge target, the branch point, and any other lanes pushing to the
   same branch. Pull before every working session.

## Phase 1 — Slice and spawn reviewers

Slice by concern, not by directory. Target 8–12 slices; each must fit one
agent's context with room to read deeply. Two slice types are mandatory
because file-based chunking never produces them:

- **Loop trace**: follow one full round-trip of the core protocol (e.g.
  edit → save → conflict → recover) through every layer. Seam defects — the
  expensive ones — only show up here.
- **Release & generated artifacts**: migrations, deploy paths, CI wiring,
  provenance of machine-written files.

Spawn one fresh sub-agent per slice. Each carries:
- the shared rubric (`references/rubric.md`),
- slice-specific focus questions you write,
- the instruction that it READS and REPORTS — it never edits, never runs git
  mutations, and returns findings as structured entries.

Run slices in parallel waves sized to your budget. When a reviewer discovers a
new defect *class*, add a rubric addendum so later slices check for it.

## Phase 2 — Maintain the ledger

One markdown file is the campaign's system of record. Entry format and status
vocabulary are in `references/ledger.md`. The rules that keep it honest:

- Stable IDs (`<PROJ>-REV-###`), never reused. Commits, code comments, and
  conversation all reference findings by ID.
- Statuses from a fixed list: `open | needs-decision | accepted-risk |
  deferred | fixed | duplicate-of`.
- Same root cause found twice → update "Also seen in", don't mint a duplicate.
- `fixed` requires a Decision line: who decided, when, what trade-offs were
  accepted, and the implementing commit hash.
- Anyone may mint findings at any time — skeptic gates and fix lanes included.
  A defect found while fixing another defect gets its own ID even on the last
  day.
- Re-derive before you rely: when acting on an older entry, verify its claims
  against commit history first. On the source campaign a finding's
  attribution was simply wrong, and the investigation that re-derived it from
  `git log` changed the fix.

## Phase 3 — Route decisions to the human

Sweep `needs-decision` entries into a batch. For each, present: the tension in
plain language, the options, your recommendation, and what each choice costs.
The human ratifies in minutes; never make a product call inside a fix lane
because it pattern-matched to a bug.

When commit archaeology later *answers* an intent question (the human's own
merged PR states the intent), present the evidence with a recommendation —
that converts an open investigation into a ten-second ratification.

## Phase 4 — Fix lanes and skeptic gates

**Lane rules** (each clause closes a failure that actually happened):
- Lanes implement but never commit — zero git mutations.
- One writer per fileset; the orchestrator partitions files before spawning so
  no two lanes touch the same file.
- Lanes run the focused tests themselves and return raw evidence, not prose
  summaries.

**Orchestrator rules:**
- Stage explicit paths only — never `git add -A` in a worktree shared by
  lanes.
- Commit bodies use `Why / Changed / Kept / Evidence` sections. "Kept" is
  load-bearing: it records what you deliberately did NOT change, which is what
  the next reviewer needs most.

**Skeptic gate — one per commit, no exceptions:**

Spawn a fresh agent that did not write the fix. Tell it, verbatim: its job is
to REFUTE the fix; default to suspicion; only pass what it cannot break. Give
it the lane's claims and these attack angles, plus its own:
- Can the change mask the original error? (catch blocks, fallbacks)
- Is the abstraction layer right? (runtime-aware client vs legacy path)
- Are the new tests capable of failing? (break the code mentally — would they
  notice?)
- Did the lane grep for ALL consumers, including ones reachable only through
  generated indexes or dynamic access?
- Does a quality gate in the repo (lint --fix, codegen hooks, ratchets) undo
  or mask the change at commit time?
- Re-run the verification commands yourself; never accept claimed output.

The gate returns PASS/FAIL with numbered defects and blocker/nit severity.
Fix blockers and re-verify before committing; apply or explicitly decline nits
in the commit body. On the source campaign the gate caught 7 real defects in 7
gated waves that green test suites missed. If your gate has never failed
anything, it is prompted wrong.

## Phase 5 — Second adversarial sweep

After the fix waves: fresh agents (not the fixers) re-review every file
touched by fix commits, same rubric. The target is paint-is-wet defects —
introduced or exposed by the fixes. Then re-run the full suites and diff
against the Phase 0 baseline; every newly-red test is yours to explain.

## Phase 6 — Pin engine truths, sync the record

**Engine truths** are platform behaviors that violated reasonable assumptions
(ORM silently dropping LIMIT on UPDATE; renderer dropping flex gap; framework
discarding setStatus on rejected promises; session scope filters killing tools
that unit tests swore were registered). For each:
1. Pin it with a permanent test that fails if the platform changes.
2. Add it to a "don't relearn" list carried into future sessions.

**Record sync** — three documents must agree at close: the ledger, the
release-readiness doc, and the PR description. The PR description is
team-facing: plain language, a reading-list of links, no personal-workflow
jargon. Re-derive every count from the ledger; a stale count is the first
symptom of drift.

## Evidence rules (all phases)

Each rule below produced a real false claim when violated:

1. Piped commands lie about exit status — run unpiped to a log or use
   pipefail, then read the log.
2. `grep` searches content, not filenames; multi-glob shell lines abort on the
   first no-match. Verify existence with one `ls` per path.
3. A test you haven't seen fail proves nothing — break the code and watch.
4. Count-based gates (error ratchets) mask one-fixed/one-introduced swaps —
   diff the sorted error lists, not the totals.
5. Pick the proof mode per fix: differential (bug), acceptance (new behavior),
   non-regression (polish).
6. Abstain when evidence is incomplete — an intent question gets an
   investigation and a recommendation, not a guess.

## Example finding (ledger entry)

```markdown
### ACME-REV-042 - Org-scoped tools unreachable in every production session

Status: fixed
Severity: P1
Primary slice: Agent tools and prompt routing
Category: Seam & boundary behavior

Files:
- apps/server/src/mcp/mcpServer.ts

Problem:
Tools declaring requiredScopes ["organization:read"] are filtered out before
agent include-lists are consulted: the generic scopes clients send expand
through categoryToScopeMap, which has no "organization" entry. Config and
unit suites stay green because they test the arrays, never the session path.

Recommended fix:
Add the map entry; add a regression test that drives the REAL session path
(createSession → handleListTools) with generic scopes.

Decision: 2026-06-11 — fixed with a session-path differential test.
Commit 1a2b3c4d5.
```

## Design Rationale

- **Finding, deciding, fixing, and believing are done by different agents**
  because the failure mode of single-agent review is self-grading: the author
  of a fix is structurally unable to refute it. The skeptic gate earned
  permanent status by repeatedly catching what green suites could not.
- **The ledger uses stable IDs** because a campaign outlives any one context
  window; IDs are how a commit, a code comment, and a conversation a week
  apart refer to the same fact.
- **Slices are concern-shaped, not file-shaped** because the expensive bugs on
  the source campaign were seam bugs — runtime filters silently killing
  surfaces whose per-module unit tests were green.
- **Phase 0 exists because it was missing on the source campaign**:
  pre-existing failures surfaced mid-campaign and cost a full investigation to
  attribute, and stale committed codegen concealed a live runtime bug. Both
  are cheap to bank up front and expensive to discover late.
- **The rubric is allowed to grow mid-campaign** because the most valuable
  review categories (prompt-contract drift, failure-window hygiene) were
  discovered during review, not designed before it. A frozen rubric caps the
  campaign at its day-one understanding.
- **TBD**: the size threshold below which `dev-review`'s single-pass fanout
  suffices is judgment, not formula. Current heuristic: if the diff summary
  alone would overflow one reviewer's context, run the campaign.

## References

- `references/rubric.md` — the multi-category rubric every reviewer carries
- `references/ledger.md` — ledger entry format, status vocabulary, sync rules

## Related skills

dev-review (single-scope reviews — the layer below), dev-investigate (deep
evidence work on individual findings), dev-test-design (proof-mode choice),
dev-checkpoint (reorientation between waves), dev-branch-memory (carrying
campaign state across threads).
