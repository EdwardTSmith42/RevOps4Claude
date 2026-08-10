# Voiceprints

Portable artifacts capturing a writer's voice — sentence rhythm, register, vocabulary, syntactic quirks. Loaded by `os-writing` and other producer skills as voice context. Produced by the `os-voiceprint` skill from sample writing.

The user does not author voiceprint files by hand. The `os-voiceprint` skill produces the portrait; the library skill saves it here with proper frontmatter.

## Frontmatter schema

```yaml
---
type: voiceprint
author: <name>
default: yes | no
scope: general | social-media | customer-email | longform | fiction-literary | fiction-noir | <other>
genre: <optional, for fiction>
source: <provenance — what content was sampled>
created: <YYYY-MM-DD>
notes: <freeform>
---
```

Required: `type`, `author`. Strongly recommended: `default`, `scope`, `created`. Optional: `genre`, `source`, `notes`.

Full guidance in `skills/os-library/references/voiceprint-schema.md`.

## Naming

Filenames follow `<author>-<scope>.md` for scope-specific voiceprints, and `<author>.md` for the user's general-scope default. Examples:

- `<name>.md` — the user's general-scope `default: yes` voiceprint (the go-to when no scope-specific exists)
- `<name>-customer-email.md` — the user's voice calibrated for customer email
- `<name>-social.md` — the user's voice for social-media posts
- `mat-mulholland.md` — an external author's voice (Mat Mulholland), scope inferred from frontmatter
- `pen-name-x-master.md` — a pen name's master voiceprint
- `pen-name-x-protagonist-nova.md` — a per-character voiceprint within the pen name's work

## The user's default voiceprint

When a writing mode needs a voiceprint and the user hasn't named one, the matcher loads the user's own voiceprint scoped to the requested output format if it exists, falling back to the user's `default: yes` `scope: general` voiceprint otherwise.

The user's name comes from `_os-user-profile.md`. To change the default voiceprint identity, update `_os-user-profile.md`'s `name` field rather than renaming files.

## When to add or update a voiceprint

Add a new voiceprint when the user wants a voice that isn't yet captured — a new scope (e.g., they start writing on a new platform with a different register), a new pen name, an external author whose voice they want to emulate.

Update an existing voiceprint when the underlying voice has evolved meaningfully. Voiceprints capture voice at a point in time; if the user's voice has shifted significantly over six months of writing, regenerating from recent material produces a more accurate voiceprint.

The `os-voiceprint` skill handles both cases. Library/save persists the result here.
