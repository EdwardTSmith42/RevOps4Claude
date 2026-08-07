# Voiceprint Schema

Voiceprints are portable artifacts that capture a writer's voice — sentence rhythm, register, vocabulary, syntactic quirks, idiosyncratic punctuation — in a form drafting and other producer skills can load as context. They live in `os-inputs/voiceprints/`.

A voiceprint is produced by the `os-voiceprint` skill from sample writing. The user does not author voiceprints by hand. The library skill stores them, finds them, and helps repair frontmatter when it drifts.

## Frontmatter schema

```yaml
---
type: voiceprint
author: <name>
default: yes | no
scope: <scope value>
genre: <optional, for fiction>
source: <provenance — what content was sampled to produce this voiceprint>
created: <YYYY-MM-DD>
notes: <freeform>
---
```

Required: `type`, `author`. Strongly recommended: `default`, `scope`, `created`. Optional: `genre`, `source`, `notes`.

## Field guidance

**`type`** is always `voiceprint` for files in this directory.

**`author`** is the user's name for self-voiceprints (matching the `name` in `_os-user-profile.md`), or a pen name or external author's name otherwise. Use lowercase with hyphens for compound names (e.g., `firstname-lastname`, `pen-name-x`, or a single-word handle for a one-name author). The author field is the single most important matching signal — get it right, even if other fields drift.

**`default`** marks whether this is the user's go-to voiceprint for the given scope. Most users have one `default: yes` voiceprint per scope (the one that gets loaded when no specific voiceprint is requested). External authors and pen names typically don't have `default: yes` — they're only loaded when explicitly invoked. A user can have `default: yes` on the general scope and `default: yes` on the social-media scope simultaneously — defaults are scoped, not global.

**`scope`** scopes the voiceprint to a domain or format. Starter values include `general` (the user's overall voice), `social-media` (tighter, punchier register for posts), `customer-email` (warmer, more empathetic register for direct customer communication), `longform` (sustained register for articles and essays), `fiction-literary`, `fiction-noir`, `fiction-romance`, and similar fiction-specific scopes. New scopes can be added freely as the user develops new contexts. The `<other>` slot is intentional — fixed taxonomies decay.

**`genre`** is optional and applies mainly to fiction voiceprints. Examples: `urban fantasy`, `literary fiction`, `hard-boiled crime`, `regency romance`. Use natural-language values, not enums.

**`source`** describes what was sampled to produce the voiceprint — the corpus identifier with enough specificity to recreate or audit the voiceprint later. Examples by shape: for a self-voiceprint, a run of newsletter issues with a date range; for a pen-name book, the book title and which portion was sampled; for an external author, a defined collection of pieces with a date range. Provenance matters when a voiceprint surprises the user — knowing what fed it helps diagnose whether to update or replace.

**`created`** is the date the voiceprint was produced or last regenerated. Voiceprints can drift if the underlying voice evolves — `created` lets the user spot stale ones during validation.

**`notes`** is freeform. Common uses: caveats about what's deliberately excluded from the sample, calibration notes about tendencies to compensate for at draft time, and context about why the voiceprint was produced. Notes are scanned during content-fallback matching, so any keywords here help find the voiceprint later.

## File body

The frontmatter is followed by the actual voiceprint content — the prose portrait describing the voice. The voiceprint skill produces this content. Library does not modify it.

A typical voiceprint runs 800-2000 words and reads as a portrait, not a checklist. The portrait is what downstream skills load as context when they need to write in the voice. Frontmatter is metadata for finding the right voiceprint. The body is the voiceprint itself.

## Worked example

A filename pattern like `<author>-<scope>.md` (for a non-default voiceprint scoped to a specific format) might carry frontmatter shaped like this:

```yaml
---
type: voiceprint
author: <author-handle>
default: no
scope: customer-email
source: "<corpus identifier — e.g., an email sequence, date range, count>"
created: 2026-04-25
notes: "<calibration notes and the defining tells the producer should preserve>"
---

# <Author>'s voice — customer email register

[The voiceprint portrait follows — 800-2000 words of prose describing the voice. The file body is produced by os-voiceprint; the frontmatter is what library cares about.]
```

## When this voiceprint gets loaded

The matching discipline (`matching-discipline.md`) ranks voiceprints by author-and-scope match against the job context. A non-default scoped voiceprint loads when the job produces output matching its `scope` AND the author signal matches its `author` (the user explicitly names the author, the brief mentions a project tied to that author, or the genre signal strongly implies them).

If the user is producing the same output format without naming a specific non-default author, the match would prefer the user's own voiceprint for that scope (if it exists) or the user's general default voiceprint (if no scope-specific voiceprint exists for the user). Non-default voiceprints load only when their author is the explicit or strongly-implied target.

## Producing a new voiceprint

To create a new voiceprint, invoke the `os-voiceprint` skill with sample writing. It produces the portrait. Then `os-library/save` writes the file to `os-inputs/voiceprints/` with the frontmatter you provide. If the user supplies sample writing on the fly during a drafting session, the chain is: drafting calls `os-voiceprint`, the producer returns a portrait, drafting uses it, then drafting asks whether `os-library/save` should persist it for future use.

## Repairing voiceprint frontmatter

If a voiceprint file has missing or malformed frontmatter, `os-library/repair` reads the file body, infers likely values for missing fields (the body usually mentions the author and the kind of writing it captures), proposes corrections, and asks the user to confirm before writing. Repair is never silent — the user sees and approves changes.
