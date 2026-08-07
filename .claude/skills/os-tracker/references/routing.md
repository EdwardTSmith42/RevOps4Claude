# Task routing — the model

How Personal OS decides where a task goes. This is the canonical reference; `os-tracker`'s
`setup` mode primes it, and Capture (and any direct-route during chat) consults it on every
task. The live state — what's connected, what's been confirmed — lives in the user's ledger
at `os-inputs/_os-routing.md`.

## The destinations

The capture layer already routes everything the user drops into one of five buckets, in
priority order, first match wins: **Promotion → User Tracker → System Worklog → Knowledge →
Trash.** Routing in this doc concerns one split *inside* User Tracker:

| You hand it… | It goes to | Why |
|---|---|---|
| a work / team / client task | **External system** (e.g. ClickUp) | you live in that app — it should land where your team sees it |
| a personal or small task | **Internal backlog** (`os-tracker/user.md`) | you'd never want it on the work board |
| a fact for the AI to remember | Knowledge | not a task at all — "for the AI, not to track" |
| Personal OS's own work | System Worklog | the system owns it, not you |
| a correction | Promotion | → AGENTS / a skill, never a task |

"AI memory" is not a new destination — it's Knowledge. The only thing this model adds is the
external-vs-internal call.

## Learned, not pre-stated

The external-vs-internal call is **learned through use**, not configured from a table the
user fills out up front. The reasoning: people don't reliably know their own routing rules
in the abstract, and a guessed table is wrong the first time a real task doesn't fit it.
Asking at the moment a real task appears is cheap, accurate, and self-documenting.

So the rules accumulate one confirmed decision at a time. Setup connects the external system
and sets the default; the ledger fills in as tasks come up.

## The protocol (consult on every task)

1. **Match first.** If the task clearly fits a confirmed rule in the ledger, route it
   silently — external or internal as the rule says.

2. **No match → ask once.** One question, two plain options ("work board, or your own
   list?"). Skip the question only if the answer is already known from elsewhere (the user
   settled this kind during `setup`, or while exploring their task app). Route per the
   answer, then **append a confirmed rule** so the question doesn't repeat. (The append is
   low-ceremony — the user just answered, so record it directly; no separate dry-run for the
   one-line ledger note.)

3. **Don't over-generalize.** A rule covers the *kind of task it names*, not adjacent kinds.
   A rule confirmed for a personal task does not settle a work task that shows up later, and
   vice versa — different kind, ask again (briefly). Exception: when exploring the user's
   task system has already made the boundary unambiguous, route and note it rather than
   asking.

4. **Be clear about confirmed vs. open.** A question means *this kind isn't settled yet* — a
   one-time calibration, not indecision. The early system asks more; a seasoned one barely
   asks at all.

5. **Safe default.** No matching rule and no known answer → internal backlog. Nothing leaves
   the machine until a confirmed rule sends it out.

## Honesty about reach

Never route a task to an external system you can't actually write to. If the integration
isn't wired, either keep it internal or route it "external, manual" — hand the user the task
to file themselves — and say which. Same discipline as reminders: don't imply a task reached
a place it didn't.
