# Source Traceability

Source traceability explains where a branch decision came from.

## Principle

Do not restate durable instructions as if they are new branch memory. Cite the durable source when it materially shaped the local decision.

This supports both positive and negative learning:

- good decisions can point to the rule or precedent that helped
- flawed decisions can point to stale or ambiguous source material

## Source Ref Format

In frontmatter, use compact strings with concrete anchors when possible:

```yaml
source_refs:
  - "AGENTS.md :: verify before done shaped proof plan"
  - "skills/dev-review/modes/manifesto-review.md :: source-of-truth clarity shaped reviewer context"
  - "tests/unit/foo.test.ts :: failing test proved direct route default mismatch"
  - "commit abc1234 :: moved output validation upstream without changing public response shape"
  - "review finding P2 'Use server time for client-ingested facts' :: changed event_at source to server receipt time"
  - "user correction 2026-04-28 :: Amplitude-specific field names should be internalized as generic display_name"
  - "conversation 2026-05-02 :: user rejected overlapping include/exclude filters because they would bloat tool-call guidance"
```

In the body, summarize the source influence:

```markdown
## Source Trace

- `AGENTS.md`: The verification-before-completion rule pushed this branch to keep before/after proof with the same scenario.
- `agentic-manifesto-review`: The decision favored an explicit source-of-truth cue over another helper abstraction.
```

## PR-Safe Handling

Private local paths and SOP names may appear in `final-branch-memory.md`.

For `reviewer-brief-input.md`, rewrite private sources into public-safe phrasing:

- "Personal verification workflow" instead of a private SOP path
- "Local branch memory" instead of a private file path
- "Existing repo pattern" instead of a private investigation note

Never paste private SOP content into a PR-safe output.

## Source Ref Quality

Prefer source refs that help a future reviewer verify the memory without reading the whole thread. Strong refs name at least one of:

- commit hash and short subject
- review finding title or explicit issue summary
- test command or test file that proved the behavior
- code file where an existing pattern was preserved or changed
- specific user decision/correction with date or compact quote
- public PR/comment link when available

Weak refs like "user requirement" or "tests passed" are acceptable only when no better anchor exists. If using a broad source, summarize the exact influence in the body.

## Conversation Trace Quality

When a decision came from discussion, prefer a compact paraphrase of the observable conversation over a generic "user requested this" ref. Good conversation traces capture:

- the user concern that raised the bar
- the agent proposal that was accepted, corrected, or narrowed
- the route not taken and why it was rejected
- the final agreement or unresolved question

Do not paste long transcript sections. Do not store hidden internal chain-of-thought. The goal is to preserve the decision journey a reviewer can learn from, especially the tempting options that were intentionally avoided.
