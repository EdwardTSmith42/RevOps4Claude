# Library Integration

How voiceprint modes write through os-library/save with proper frontmatter. Used by all voiceprint-producing modes (from-sample, from-book, import, and update) to ensure produced artifacts land in `os-inputs/voiceprints/` (and `os-inputs/style-samples/` for from-book) with validated frontmatter. The one difference for `update` is that it overwrites an existing voiceprint file rather than creating a new one (same `<author>-<scope>.md`, bumped `created`) — see the note in the handoff section.

This reference is the producer side of the library convention. The library's `os-library/references/matching-discipline.md` is the consumer side. Together they form the complete contract: voiceprint produces with valid frontmatter, library finds and ranks based on that frontmatter, downstream skills load the right voiceprint for the right job.

## When to write through os-library/save vs. inline

The default is to write through os-library/save. Persisting a voiceprint that the user can't find later is worse than producing one inline that the user copies to their own location.

Two exceptions matter. The first is on-the-fly creation during another skill's run. When drafting needs a voiceprint and none exists, drafting chains into os-voiceprint/from-sample with sample text supplied by the user. The voiceprint produced may be one-off (the user wanted to draft this one piece and doesn't expect to need this voice again) or worth keeping. The mode asks before saving rather than persisting silently.

The second is when the user explicitly says "show me but don't save." Some users want to see what the voiceprint looks like before deciding whether to file it. Honor this. Produce the artifact, present it, then ask whether to save. Library/save is invoked only on confirmation.

In all other cases — explicit `from-sample`, `from-book`, `import`, or `update` invocations — write through os-library/save by default.

## The save handoff

The voiceprint mode produces two things: the voiceprint content (the file body) and proposed frontmatter values. Library/save receives both, validates the frontmatter against the schema, generates the filename per convention, writes the file, and confirms.

The handoff specifically:

1. The voiceprint mode composes the full file body. For from-sample, this is the # Analysis section plus the # Voiceprint portrait. For from-book, it's the same shape per voiceprint layer. For import, it's the parsed sections from the imported text. For update, it's the freshly re-extracted # Analysis plus # Voiceprint portrait, written to the *same filename* as the voiceprint being refreshed — an intentional overwrite, with `created` bumped to today and the room-vs-person verdict noted in `source` or `notes`. Update never writes a sibling voiceprint; siblings are only ever flagged for a separate update pass.
2. The voiceprint mode proposes frontmatter values per the voiceprint schema in `../../os-library/references/voiceprint-schema.md`. Required fields (`type`, `author`) must be present. Recommended fields (`default`, `scope`, `created`) are filled per the inference rules below. If unclear, the mode asks the user.
3. The voiceprint mode invokes os-library/save with the body and frontmatter.
4. Library/save runs its validation, generates the filename, writes to `os-inputs/voiceprints/<filename>.md`, and returns a confirmation with the file path and any warnings.
5. The voiceprint mode surfaces the confirmation to the user.

The chain is straightforward when the user is invoking voiceprint directly. When voiceprint is itself chained from another skill (drafting needs a voiceprint), the calling skill receives the voiceprint-and-save outcome as one nested operation.

## Frontmatter inference rules

The voiceprint mode tries to infer frontmatter values from context before asking the user. Specifically:

**`type`** is always `voiceprint`. No inference needed.

**`author`** defaults to the user's name from `os-inputs/_os-user-profile.md` when the source material is the user's own writing. The mode infers user-authorship from context (the user said "my emails," "my newsletter," "my book") or asks if ambiguous. For pen names and external authors, the user supplies the name explicitly.

**`default`** for self-voiceprints, ask the user. For non-self voiceprints (pen names, external authors), default to `no`. The user can override.

**`scope`** is inferred from source content:
- Customer emails or warm direct communication → `customer-email`
- Social posts (LinkedIn, X, Bluesky) → `social-media`
- Articles, essays, longform → `longform`
- Fiction prose → `fiction-<genre>` (e.g., `fiction-noir`, `fiction-literary`, `fiction-romance`)
- General self-voiceprint with no specific calibration → `general`
- Other contexts → ask, with the starter list as guidance

If the user has multiple voiceprints under the same author, the scope value is what differentiates them at find time.

**`genre`** is supplied for fiction voiceprints. The mode infers from content if obvious (a noir manuscript names noir conventions) or asks.

**`source`** describes what was sampled. The mode produces this from the actual sample shape: "9 emails from Q4 newsletter sequence" / "transcript of keynote talk + 3 LinkedIn posts" / "Pen Name X — Book One, full manuscript." Source provenance helps the user remember why this voiceprint was produced and what to expect from it.

**`created`** is today's date for fresh voiceprints. For imports, ask the user if they know the original creation date. Default to today if unknown.

**`notes`** captures calibration notes the voiceprint reflects: what the voiceprint excludes, what register it covers, any caveats the downstream consumer should know. The mode produces these from the Analysis (which surfaces calibration choices) or asks if needed.

## Filename conventions

Library/save handles filename generation per the convention in `../../os-library/modes/save.md`:

- `<author>.md` — the user's general-scope `default: yes` voiceprint
- `<author>-<scope>.md` — scope-specific voiceprints
- `<author>-pov-<character>.md` — per-POV voiceprint overlays from from-book
- `<author>-master.md` — explicit master voiceprint when the user has multiple book-derived voiceprints under the same author

The voiceprint mode does not generate the filename itself. It supplies frontmatter and lets os-library/save apply the convention. This keeps filename logic centralized in one place.

## Multi-file output (from-book specifically)

When from-book produces a layered output (master voiceprint + per-POV overlays + style samples), each artifact is saved through a separate os-library/save invocation. The mode does not bundle them into a single save call — each artifact has its own path, its own frontmatter, its own confirmation.

Style samples produced by from-book follow the style-sample schema (`../../os-library/references/style-sample-schema.md`), not the voiceprint schema. The save handoff for style samples uses style-sample frontmatter (`type: style-sample`, `author`, `pattern`, `genre`, `source`, `length`, `notes`). The body is the verbatim source passage.

## When os-library/save is unavailable or the user wants raw output

If the user explicitly asks for the voiceprint without saving (e.g., "produce a voiceprint but I'll file it myself"), produce the file content with frontmatter and present it as text. The user can save it manually. This is the manual-curation path. Library/find will still pick up the file when the user files it correctly.

If on-the-fly creation chains into voiceprint and the user opts not to save (one-off use), the voiceprint content is used in the calling skill's run and discarded after. No file is written. The user can still save later by invoking from-sample again with the same source material if they decide they want to keep it.

## Validation feedback

Library/save returns warnings when frontmatter is incomplete or freeform. The voiceprint mode surfaces these warnings to the user in its confirmation. Common warnings: missing optional fields like `notes`, freeform values on open-enum fields like `scope` (acceptable but flagged for awareness), unfamiliar genre values for fiction voiceprints.

The voiceprint mode does not block on warnings. The save persists. The user sees the warnings and can address them via os-library/repair if desired.

## Why integrate with the library at all

The library exists so voiceprints have a home and a discovery path. Without integration, every voiceprint produced is text the user has to file manually with frontmatter typed by hand. That friction means voiceprints get lost or filed inconsistently, which means os-library/find doesn't reliably surface the right voiceprint when downstream skills need one, which means drafting and editing fall back to generic register, which means the user notices the work feeling generic.

The library + voiceprint integration is the connection that makes voice fidelity work across the rest of the skill pack. Voiceprint is the primary producer. Library is the storage and discovery layer. Downstream skills are the consumers. The chain only works if the producer side writes with valid frontmatter.
