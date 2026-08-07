# Approval tiers — when os-tune applies vs asks vs proposes

os-tune's approval discipline. Three tiers govern what os-tune does autonomously, what it asks before doing, and what it proposes with alternatives. Tiers and thresholds are configurable per user via `os-inputs/_os-setup-philosophy.md`.

## Why tiers

Without tiered approval, os-tune has two failure modes:

- **Too autonomous.** User feels the OS changing under them. Trust erodes. Eventually the user stops trusting os-tune's outputs and either disables it or starts double-checking everything (which is worse than not having os-tune at all).
- **Too cautious.** Every micro-fix needs approval. os-tune becomes a chore. The user stops invoking it. Self-optimization promise dies.

The middle ground is calibrated autonomy. os-tune is bold where stakes are low, careful where stakes are high, and transparent in both directions.

## The three tiers

### Trivial — auto-apply with audit trail

os-tune applies the change without asking. The change appears in the session output (*"made this small change"*) and logs to `os-inputs/_os-inbox.md` for later audit. User can revert from the audit trail.

**What qualifies:**

- Output formatting tweaks that conform to existing principles (a P.S. line that the skill's purpose already implies belongs there)
- Default values for non-critical fields (changing a default tone modifier from `neutral` to `warm` when the voiceprint clearly leans warm)
- Fixes that match patterns the user has already locked in (the same tweak applied 3+ times across sessions becomes a default)
- Typo or grammar fixes inside skill prose
- Removing an explicit duplicate (two near-identical mode entries; deduplicating is trivial)

**What disqualifies:**

- Anything that touches the skill's `purpose` section
- Anything that adds, removes, or reorders modes
- Anything in the skill's frontmatter (description, name, etc.)
- Anything that changes operating principles
- First-time changes to a skill (no precedent yet)

### Moderate — ask + apply

os-tune proposes the diff and asks. User says yes; os-tune applies. User says no or modifies; os-tune iterates.

**What qualifies:**

- Operating-principle additions
- Mode behavior changes (input, output, or process)
- Frontmatter changes (description updates, scope shifts)
- Threshold or default-value changes for critical fields
- New examples or edge cases added to a mode
- Voiceprint-related tweaks where the right place might be the skill or might be the voiceprint (os-tune surfaces the question)

### Large — propose + confirm + show alternatives

os-tune describes what it would do, what alternatives it considered (and why it didn't pick them), and asks the user to pick. User confirms; os-tune proceeds. User picks an alternative or says no; os-tune iterates or stops.

**What qualifies:**

- New skills (the os-skillify handoff)
- New modes added to an existing skill (`extend`)
- Changes to a skill's `purpose` section
- Skill renames or path changes
- Promoting an inbox lesson to an `AGENTS.md` principle
- Cross-skill changes (touching more than one skill in a single action)
- Anything affecting a shipped buyer-facing skill (changes that propagate beyond the user's local install)
- Deprecation of an existing skill

## Configuration via `_os-setup-philosophy.md`

The user can adjust thresholds. Sample configurations:

The knob lives in `_os-setup-philosophy.md` frontmatter under `tiered_approval`, one value per tier. Sample configurations (this is the file's actual schema — keep it in sync with the shipped file):

```yaml
# Conservative — ask about everything
tiered_approval:
  trivial: ask
  moderate: ask
  large: confirm

# Balanced (the shipped default)
tiered_approval:
  trivial: auto        # auto-apply with an audit line in the inbox
  moderate: ask
  large: confirm       # propose with alternatives, apply on explicit confirm

# Aggressive — trust the system more
tiered_approval:
  trivial: auto
  moderate: auto       # auto-apply, audit line in the inbox
  large: confirm       # large always requires confirmation
```

The default ships balanced. Users can shift to conservative or aggressive based on how much they want to be in the loop (no pun) on individual changes.

## What os-tune never does autonomously, regardless of tier

These are absolute, not configurable:

- Delete a skill, mode, or reference file
- Modify `AGENTS.md` (the operating principles file — user-only)
- Modify a buyer-facing shipped skill in a way that changes its public interface
- Change another user's customization (only the user's own customizations)
- Apply changes when the inheritance protocol couldn't load required context (graceful degradation triggers, not autonomous action)

If os-tune encounters a situation that would require one of these, it surfaces and asks regardless of tier.

## Audit trail discipline

Every tier writes to `os-inputs/_os-inbox.md` so the user can audit later. Format:

Each entry carries: date, tier in brackets, mode + target skill, one-line summary of the change, reasoning (what triggered it — frequency, user request, alternative considered), and for `moderate`/`large` entries, whether the user confirmed. For `trivial` entries, the revert anchor (snapshot or commit id) is included so the user can unwind a single autonomous change without rolling back unrelated work.

The audit trail enables:

- The user to see what os-tune has been doing without surprise
- Reverts when something goes wrong (`reflect` can also surface "this trivial-tier change has been undone twice — promote to moderate?")
- Pattern detection for the philosophy file itself (if the user keeps overriding trivial-tier changes, the threshold might be wrong for them)

## Edge cases

**The change spans tiers.** A single proposed action might be trivial for one part and large for another (e.g., a refine that adds a P.S. line — trivial — and also changes the skill's purpose statement — large). os-tune classifies as the highest tier present and asks accordingly.

**The threshold is itself contested.** If the user keeps disagreeing with os-tune's tier classification (*"that wasn't trivial, you should have asked"*), os-tune logs the disagreement and proposes adjusting the philosophy file. After 3 such corrections, os-tune suggests a philosophy review.

**Trust is being rebuilt.** If the user just rejected several trivial-tier changes, os-tune temporarily downgrades to ask-on-everything for a session or two, restoring the default once trust is re-established. Configurable in philosophy file.

## See also

- `os-inputs/_os-setup-philosophy.md` — where users configure their thresholds
- `inheritance-protocol.md` — philosophy file is one of the inheritance sources (see the protocol for the canonical list)
- `figure-it-out-routing.md` — routing decides which mode runs; tiers decide what each mode does
- `AGENTS.md` — the workspace's mutation-discipline principles this builds on
