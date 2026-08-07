# Iteration Discipline

How writing modes handle iteration. Three patterns — prior-output-plus-direction, batch-then-pick, section-targeted revision — cover the bulk of how real writing work develops.

The skill is built to support iteration without enforcing it. Whether multiple passes materially improve output is a question for measurement in real use, not an assertion in the skill. The patterns below are available — the user invokes them as the work calls for.

## Pattern 1 — Prior-output-plus-direction

The most common iteration shape. The user supplies the previous version of the piece plus a one-line description of what to change. Writing treats prior output as the starting state and revises in the direction supplied.

**When to use:** the piece is broadly right but needs specific changes. Tighten the opening, make paragraph three more concrete, swap a vague claim for a specific number, add an objection-handling section, soften the close.

**How the mode runs:**

The mode reads the prior output as context, identifying the structure and voice already established. The mode reads the revision direction and identifies which parts of the prior output need changing. The mode produces a revised version that incorporates the requested changes while preserving everything not flagged for change. The mode notes briefly what changed from the prior version.

**Discipline:** preserve everything not flagged. If the user said "tighten the opening," don't rewrite the close. Iteration accumulates trust. Surprise rewrites of unflagged sections erode it.

If a requested change has implications for other parts of the piece (the new opening contradicts what comes next, the swapped claim invalidates a later section), the mode surfaces the implication rather than silently propagating changes. *"Tightening the opening to lead with the CMO question would change paragraph 3's transition — revise that too?"*

## Pattern 2 — Batch-then-pick

The user wants multiple variants of the same piece to compare and pick from. Hooks are the canonical case (3 hook options for a post), but the pattern works for subject lines, opening paragraphs, alternative section structures, alternative CTAs.

**When to use:** the user is exploring options, not refining a known direction. They want the mode to surface possibilities they haven't considered.

**How the mode runs:**

The mode produces N variants in parallel. Each variant takes a different angle, structure, or emphasis from the others — not minor word-swaps but genuinely different approaches. The mode briefly notes what makes each variant distinct so the user can compare. The user picks the variant that lands. A follow-up invocation refines that one specifically (often using prior-output-plus-direction).

**Discipline:** variants must be genuinely different. Three hooks that are minor variations on the same approach is not a useful battery — that's one hook with cosmetic re-phrasings. The mode produces structurally distinct options: a curiosity-gap hook, a pattern-interrupt hook, a stakes-raising hook. Three different angles, not three rewrites.

The mode caps batch size at 5 variants by default. More than that crowds the user's attention and produces diminishing returns. If the user explicitly asks for "10 variants," the mode produces 10 but warns that picking-from-10 is harder than picking-from-5.

## Pattern 3 — Section-targeted revision

Long-form pieces (landing pages, longform articles, email sequences) often need revision on a specific section without disturbing the rest. The user names the section, and the mode produces a replacement for just that section while preserving the surrounding work.

**When to use:** a multi-section piece is mostly working, but one section is weak. Revise the close. Rewrite email 4 of the sequence. Replace the social-proof block. Strengthen the objection-handling section.

**How the mode runs:**

The mode reads the full prior output to understand how the targeted section connects to its neighbors (what the prior section sets up, what the next section depends on). The mode produces a replacement for the targeted section that preserves the connections. The mode notes briefly what the new section does differently, and surfaces any implications for adjacent sections that the user might want to follow up on.

**Discipline:** stay in the targeted section unless implications warrant otherwise. If the user said "revise the close," don't also revise the headline. If the new section needs adjacent sections to adjust (the new close calls back to a different through-line), surface that explicitly rather than silently revising.

For email sequences specifically, section-targeted revision often means email-targeted revision. "Revise email 4" replaces email 4 while preserving emails 1-3 and 5-N. The mode reads the full sequence to keep the campaign-level voice and arc consistent.

## Combining patterns

Real iteration often combines patterns across rounds. A user might:

- Run a hook-mode batch (pattern 2) to produce 5 hook options for a post
- Pick one and run longform-article with the hook as the opener
- Iterate on the article once with prior-output-plus-direction (pattern 1) to tighten paragraph 3
- Run section-targeted revision (pattern 3) on the close
- Run os-editing/assessment to score the result, then iterate once more on the top recommendation

The patterns are tools the user combines as the piece develops. The mode supports any combination without requiring a fixed workflow.

## What iteration is NOT

Iteration is not infinite. A piece can be over-iterated — every pass producing diminishing returns until the writer's voice gets edited out. The mode doesn't refuse to iterate, but the user is the one with the judgment about when to stop.

Iteration is not blank-slate rewriting. If the prior output is so off-direction that the user wants to start over, that's not iteration — that's a fresh production. The mode treats those as new invocations rather than as iterations on the prior version.

Iteration is not a substitute for a clear brief. A piece that needs five rounds of iteration to land usually had a brief that was too vague at the start. The mode doesn't refuse to iterate when this happens, but it can flag — *"this is round 5 of revisions — the brief might benefit from more specificity before round 6."*

## Surfacing what changed

After every iteration round, the mode briefly notes what changed and what stayed. *"Tightened the opening from 4 sentences to 2. Preserved the close and middle sections. The new opening leads with the specific outcome rather than the meta-claim about results."*

This makes the iteration auditable. The user sees what shifted between rounds, can verify nothing unintended changed, and knows where to look if the new version doesn't feel right.
