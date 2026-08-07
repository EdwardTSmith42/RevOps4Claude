---
name: os-library/find
description: Soft fuzzy match for a job context — return ranked candidates per input type plus repair flags for any frontmatter issues. The core matching engine of the library. Triggers on "what voiceprint should I use for X," "find me a template for Y," "what style samples fit Z." Do NOT trigger when the user wants to inspect their full collection (use `list`), is saving a new input (use `save`), or wants to fix a specific file's frontmatter (use `repair`).
---

# Mode — Find

The core matching engine. Given a job context, find returns a small ranked list of candidate references per input type the job needs, with confidence and any repair flags.

Find is invoked directly by the user when they want help picking a reference for a specific job. It is also followed (as a convention) by other skills doing internal matching — writing modes, fiction modes, `os-voiceprint` when chaining. Other skills follow the matching discipline rather than calling find as an RPC. The discipline is documented in `../references/matching-discipline.md`.

## When to use

Typical invocations describe a job and ask which reference fits: a voiceprint for a specific output format, a template for a campaign type, a style sample for a particular scene type in a specific author's voice, or a brief for an in-flight project.

The mode helps when the user can describe the job but doesn't remember which file to load. Strict matching (asking for a file by exact name) is just `list` with a filter — find earns its keep when the query is descriptive rather than nominal.

## Inputs

- A job context: what the user is trying to produce (output format), the target voice or author, genre signals if applicable, and any explicit references the user named
- Optional: which input types to search (defaults to all four — voiceprints, style samples, templates, briefs)
- Optional: how many candidates to return per type (defaults to top 3)

## Run

The procedure runs through five steps.

**Step 1: Parse the job context.** Extract output format (landing page, customer email, action scene, etc.), target author or voice (the user's default if not specified, or a named author), genre signals (if mentioned), and any explicit reference names the user supplied. If the user named explicit references, those are loaded directly without going through scoring — find acknowledges them and skips ahead to step 5.

**Step 2: Scan the relevant inputs subdirectories.** For each input type the job needs, list candidate files. For voiceprints, scan `os-inputs/voiceprints/`. For style samples, scan `os-inputs/style-samples/<author>/` if author is known, else all author folders. For templates, scan `os-inputs/templates/`. For briefs, scan `os-inputs/briefs/current/` (and only `archive/` if the job context explicitly asks for historical context).

**Step 3: Score each candidate.** Apply the three-layer scoring from `../references/matching-discipline.md`. Layer one matches frontmatter exactly on the most important fields (voiceprint: author + scope; style sample: author + pattern; template: format + proven; brief: project). Layer two relaxes to partial or substring matches on the same fields. Layer three falls back to content scanning — keywords from the job context appearing anywhere in the file body. Higher layers always rank above lower layers. Ties within a layer break by recency (or by `proven: yes` for templates).

**Step 4: Flag frontmatter issues.** For any candidate with missing or malformed frontmatter, attach a repair flag describing what's wrong. The candidate stays in the result list — bookkeeping never blocks the work — but the user sees the issue. Severity: missing required fields are most severe, malformed enum values next, missing optional fields least.

**Step 5: Return the ranked list.** Top 1-3 candidates per input type, each entry showing the file path, the match-driving fields, the confidence layer, and any repair flags. If no candidates match for a type, follow the graceful-degradation pattern: surface the gap explicitly with the three options (proceed without, supply sample for on-the-fly creation, point at related reference).

## Output

A structured result organized by input type. Each type's section shows top candidates with confidence and flags.

Each section names the type, then enumerates candidates ranked top-first. Per candidate, show: the file path, the match-driving frontmatter fields, the confidence layer (layer 1 / 2 / 3), and a one-line rationale describing why this ranks where it does (which fields matched, what tiebreaker won). Repair flags, if any, attach to the candidate line.

When no candidates match for a type, replace the enumerated list with the three graceful-degradation options: proceed without that reference type (note the resulting fidelity cost), supply sample text and chain into the on-the-fly producer, or point at an existing reference of related type as an explicit substitution.

The shape, in skeleton:

```
## Voiceprint match (top N)

1. **<filename>** — confidence: layer <1|2|3> (<which fields matched>)
   - Path: <full path under os-inputs/>
   - Key fields: <author>, <scope>, <default if set>
   - Why this ranks here: <one line on what drove the rank>
   [repair flag if present]

## Style sample match
No matches found. Options:
1. Proceed without (note fidelity cost)
2. Supply a 200-500 word passage and chain into on-the-fly creation
3. Point at a related-author or related-pattern sample as substitute
```

If the user invoked find without a clear job context (a vague query like "what's good"), the mode asks for clarification rather than guessing — find works best with at least one signal (output format, author, or both).

## Output discipline

Find produces a structured result the calling skill or user can act on. No preamble. Each type section uses prose intros where useful but lists candidates in scannable enumerated form (this is genuinely list-shaped enumeration). Confidence layer is named explicitly so the user understands the match strength. Repair flags are surfaced, not buried.

When confidence is high (layer-one match, no repair flags, top candidate clearly best), find can recommend a single load without asking the user. When confidence is mixed (layer-two or layer-three matches, repair flags, candidates close), find asks the user to pick before any downstream skill loads the reference.

## Graceful degradation paths

The matching-discipline reference covers the full graceful-degradation flow — three options when no clean match exists, on-the-fly creation chains when the user supplies sample text, override patterns when the user wants a related reference. Find surfaces these options rather than approximating silently. See `../references/matching-discipline.md` for the full discipline.

## Cross-mode suggestions

After find returns a result, the user typically loads the chosen references and proceeds with the job. When postamble is warranted, point at adjacent modes briefly and in plain prose — not as quoted boilerplate. Point at `list` when the user looks like they want to browse what else is available, at `repair` when the result carries repair flags worth addressing now, and at the on-the-fly creation chain (supply sample text → `os-voiceprint` → `os-library/save`) when no clean match exists and the user wants to fill the gap.
