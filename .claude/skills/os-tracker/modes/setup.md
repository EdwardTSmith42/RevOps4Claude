# Mode: setup

## Job

Connect an outside task system (if the user has one) and prime task routing — so captured
tasks land in the right place. The deliverable is the routing ledger at
`os-inputs/_os-routing.md`, not a finished rulebook. Routing is **learned over time**, so
setup does the minimum to start: wire the external system, confirm the safe default, and
explain how the system will ask and learn as real tasks come up.

## When this runs

- *"Help me use ClickUp"* / *"connect Asana"* / *"send my tasks to <app>"* — the most common trigger.
- *"Set up task routing"* / *"where should my tasks go"* — the Getting Started item.
- Any time the user wants to change where tasks go, or undo an external connection.

## What setup does NOT do

It does not interrogate the user for a full routing table up front. Pre-stating every
work-keyword and project is exactly the kind of cold configuration this design rejects —
people don't know their own rules in the abstract, and a guessed table is wrong the first
time real work doesn't fit it. Setup connects the plumbing and sets the default; the rules
fill in through use, one confirmed decision at a time.

## The flow

Read `references/routing.md` for the model before running. Then, conversationally:

**1. Do you keep tasks anywhere outside this system?**
Ask plainly. Many users won't — and that's a complete setup: everything stays in the
internal backlog, nothing leaves the machine, and you're done after step 4. If they do
(ClickUp, Asana, Linear, Todoist, Things, a work board, etc.), get the name.

**2. Connect it — or be honest that you can't yet.**
Check what's actually wired in this harness: an MCP or tool for that system, or credentials
the user can point at. If the integration is present, confirm reach (can you see their lists
/ projects?) and record *where* external tasks should land by default (which list/project).
If it isn't present, say so plainly — name what would need wiring (the relevant MCP or tool
for their app) and offer to set routing up as "external, manual" so the system at least
knows the intent and can hand the user the task to file themselves until the integration
exists. Never imply you can write to a system you can't reach.

**3. Capture only the rules the user volunteers — don't mine for them.**
If, in connecting their app, the user states something clear ("anything for the team goes to
ClickUp, personal stuff stays here"), write it as a confirmed rule. If they don't volunteer,
don't dig. One or two obvious rules is plenty; the rest is learned.

**4. Set the default and explain the learning.**
Confirm the safe default in plain language: until a rule sends a kind of task outward, it
stays in the internal backlog. Then tell them how it'll actually work — the first time a new
kind of task comes up where the destination isn't settled, the system asks once, routes it,
and remembers. The questions taper off. They can edit the ledger by hand anytime.

## Writing the ledger

Write `os-inputs/_os-routing.md` (create from the shipped default if needed; it already
ships in the workspace). Per workspace mutation discipline, dry-run the change first.

- **External system** section: what's connected and where external tasks land — or "None
  connected" if internal-only.
- **Confirmed routing rules**: only what the user actually confirmed this session. Stamp
  each with the date and the evidence (what made it confirmed).
- Leave **Still unknown** and the AI-facing protocol intact — the protocol is how every
  later routing decision consults this file.

## Tone

This is a two-minute conversation, not a wizard. Lead with the value (your tasks end up
where you'd look for them), keep it to the questions that matter, and make clear that
*not* connecting anything is a perfectly good answer. Pace the user — a couple of questions,
not ten.
