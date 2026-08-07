# Classification rules

How to decide which destination an open inbox entry routes to. Apply in order; the first matching rule wins. When multiple rules apply, prefer the rule that preserves user agency (Promotion > User Tracker > System Worklog > Knowledge > Trash).

## 0. Skip metadata

Before classification, skip:
- `[type: audit|lesson|reject]` — system metadata from other skills (os-tune, os-skillify)
- `[status: resolved|deferred]` — already handled
- Tag-only entries with no body (rare, but possible)

These are not items to route.

## 1. Corrections go to Promotion

`[type: correction]` entries earn promotion, not routing. Never auto-classify into Tracker / Knowledge / Trash.

For each correction entry, propose a target:

- **AGENTS.md** — when the correction names a cross-cutting principle (applies to multiple skills, generalizes a way of working). Example: a vocabulary preference that the user wants honored everywhere the AI speaks for them.
- **Skill `references/`** — when the correction names a skill-specific pattern. Example: a default behavior one skill should adopt that wouldn't make sense as a general rule.
- **SOP / dedicated doc** — when the correction names a procedure that's bigger than a reference but smaller than a skill. Example: a multi-step workflow the user does the same way every time.

Surface the entry, the proposed target, and confidence (high / medium / low based on how clearly the entry signals one target over the others). User confirms, redirects, or defers.

See `references/promotion-paths.md` for the heuristic on choosing among the three targets.

## 2. Items the user owns go to User Tracker

Use User Tracker when the entry is something the user themselves needs to do, decide, or be reminded of. Signals:

- First-person framing: "I should…", "remember to…", "follow up on…", "decide about…"
- An external-world task: contact someone, fix something, buy something, schedule something
- A user-facing project item: a piece of content to write, a feature to ship, a meeting to prep
- A personal reminder or commitment

Default section assignment:

- Time-sensitive or has a deadline → `bugs` (cross-section bucket for time-bound items)
- A specific area is named or inferable → `actions` with `area`
- A question or decision → `open-questions` with `area`
- Half-formed thought, not actionable yet → `ideas` (prose, not checklist)
- An older capture not currently relevant → `backlog`

When ambiguous between sections, ask. Don't guess on placement when it changes the user's view of priorities.

### Internal backlog vs. an external task app

A User Tracker item can land in the user's internal backlog (`os-tracker/user.md`) or in an
outside task app they use (ClickUp, Asana, Linear…). That call is **learned, not guessed**.
Before routing, consult the routing ledger at `os-inputs/_os-routing.md`:

- Matches a confirmed rule → route as the rule says (external or internal), silently.
- No match → ask one question, two options ("work board, or your own list?"), route, then
  append the confirmed rule to the ledger so it doesn't repeat.
- Never generalize a confirmed rule to an adjacent-but-different kind of task (a personal-task
  rule doesn't settle a work task) without re-asking, unless the boundary is already
  unambiguous from the user's task-system setup.
- No rule and no known answer → internal backlog (the safe default; nothing leaves the
  machine until a rule sends it out).

The full model and protocol live in `os-tracker`'s `os-tracker/references/routing.md`; the ledger is
primed by `os-tracker setup`.

## 3. Items the system owns go to System Worklog

Use System Worklog when the entry is something Personal OS itself is tracking — work-in-progress on skills, patterns the system noticed, deferred items the system needs to come back to. Signals:

- Reference to a skill being refined or extended
- An audit observation about the system itself (a calibration the user noticed a skill needs)
- A pattern that's surfaced multiple times and might earn a `refine`
- A piece of context the next session will want for continuity

Default section assignment:

- An active piece of work in flight → `actions` with `area: <skill-name>` or `area: system`
- An idea about how the system could improve → `ideas`
- A deferred follow-up the system will pick up later → `backlog`

System Worklog is hidden from `os-tracker/view` by default. os-tune reads it as inheritance.

## 4. Valuable reference goes to Knowledge

Use Knowledge when the entry is worth keeping for later reference but isn't an action the user needs to take. The point is to capture *what's valuable* from what they shared — and the source, so they can always go back to the original. Signals:

- A named framework, pattern, mental model, or methodology
- The novel, useful, counterintuitive, or genuinely interesting bits of an article, link, or paste — distilled, not the whole thing
- A piece of source material's essence worth remembering
- A cross-cutting insight that doesn't fit a single skill

For a shared link or article, capture what warrants keeping (a few crisp takeaways, ideas, or quotes) **with the source link** — heavy extraction runs as a background sub-agent (os-gold-style). Don't just drop the URL, and don't treat it as a reading-list item unless the user explicitly says they want to read it later.

Default destination: `os-knowledge/<topic>.md`. If a file with the topic exists, append; otherwise create.

When the topic isn't obvious, ask before creating a new file. (Premature topic files lead to fragmentation.)

## 5. Explicit drop goes to Trash

Use Trash when the entry is genuinely noise — a thought the user dropped in but doesn't want to act on, an experiment that didn't pan out, content that's stale.

The entry stays in `_os-inbox.md` with `*Routed to: trash*` and `[status: resolved]`. Not deleted. Historical record per the inbox conventions.

## Confidence tiers

For each entry, assign a tier:

- **Trivial** — one rule fires cleanly, no ambiguity. Batches into wholesale dry-run.
- **Moderate** — multiple rules could apply, or the section/area is unclear. Asks one-at-a-time with proposed destination + one alternative.

When in doubt, escalate to Moderate. The cost of a wrong auto-route is real; the cost of one extra ask is small.

## Example shapes (not verbatim — describing the move)

- A first-person reminder to follow up with an external party on a specific request → User Tracker, `actions`, area inferable from who the party is, high-confidence trivial.
- An observation that a particular skill's mode could use a calibration the user noticed → System Worklog, `actions`, area set to that skill name, high-confidence trivial.
- A speculative idea about a system feature that could either be acted on or filed as a concept → Knowledge or System Worklog, moderate-tier — depends on whether the user intends to act. Ask.
- A correction stating that a word, phrasing, or interaction pattern doesn't match how the user wants the system to behave generally → `[type: correction]`, Promotion path, target AGENTS.md, high-confidence (cross-cutting voice or interaction rule).
- A passing link or thought the user explicitly says they won't return to → Trash, trivial.
