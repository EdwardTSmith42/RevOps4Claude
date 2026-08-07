---
name: os-voiceprint/import
description: Ingest an existing voiceprint into the library with proper frontmatter. The user supplies voiceprint text produced by a previous tool or earlier voiceprint version, and the mode wraps it in the library voiceprint schema and saves through os-library/save. Triggers on "import this voiceprint," "save this old voiceprint," "file this voiceprint into the library." Do NOT trigger when producing a new voiceprint from sample writing (use `from-sample`) or from a book (use `from-book`).
---

# Mode — Import

Ingest an existing voiceprint into the library. The user has a voiceprint produced before the library convention existed (a v0.3 voiceprint output saved as raw text, an artifact from another tool, a hand-curated voice description). The mode wraps it in the library voiceprint schema and saves it.

This is mostly form-filling. The voiceprint content already exists. The mode just establishes proper frontmatter so os-library/find can discover it and downstream skills can load it.

## When to use

The user has voiceprint text on hand and wants it in the library. Common scenarios: voiceprints produced by voiceprint v0.3 before library existed, voiceprints produced manually or through external tools, voiceprints inherited from a different system the user is migrating from.

If the voiceprint text is good as-is, this mode handles it. If the text needs rework (because the existing version doesn't match the current schema's portrait shape, for example), `from-sample` with the voiceprint's source material is the better path.

## Inputs

- **Required:** The voiceprint text (pasted content, or a file path the user supplies)
- **Required (or asked):** `author` — the name to file the voiceprint under. If the user is the author, defaults to `name` from `_os-user-profile.md`. For pen names or external authors, asked explicitly.
- **Required (or asked):** `scope` — what scope this voiceprint covers (`general`, `customer-email`, `social-media`, `longform`, `fiction-<genre>`, etc.). Asked if not inferable from the voiceprint's content.
- **Optional:** `default` — only relevant for self-voiceprints. Asked if the user is the author and didn't specify.
- **Optional:** `genre` — for fiction voiceprints. Asked if the scope implies fiction.
- **Optional:** `source` — provenance description. The mode infers if the user said where the voiceprint came from ("from my v0.3 run last month on the newsletter corpus"). Otherwise asked.
- **Optional:** `notes` — calibration notes. Often the imported voiceprint already includes notes inline. The mode can extract them.

## Run

The procedure runs through four steps.

**Step 1: Parse the voiceprint text.** Identify whether the text already follows a two-section structure (`# Analysis` + `# Voiceprint`) or is a single block. v0.3 outputs typically have the two-section structure. Earlier or external voiceprints may not. If the text has both sections, preserve the split. If it's a single block, treat it as the Voiceprint portrait body and skip the Analysis (mark notes that the imported voiceprint lacks an analysis layer for audit).

**Step 2: Gather frontmatter values.** For each required and recommended field, either infer from context or ask the user. Specifically:

- `type: voiceprint` — always.
- `author` — default to user-profile name if the user implied this is their voiceprint. Ask if it's a pen name or external author.
- `default` — if author is the user, ask. Otherwise default to no.
- `scope` — try to infer from the voiceprint's content (a portrait that mentions customer emails, sales-copy, or formal-business register implies `customer-email` or similar). If unclear, ask with the starter list as options.
- `genre` — for fiction voiceprints (the body mentions characters, scenes, narrative POV), infer if obvious or ask.
- `source` — ask for a brief provenance description ("v0.3 voiceprint from May 2026 on Q4 newsletter corpus" / "external voiceprint from Anthropic example"). If the user has no clear answer, leave blank with a note that source is unknown.
- `created` — today's date if the original creation date is unknown. If the user knows the original date, use it.
- `notes` — extract inline calibration notes from the voiceprint body if any exist. Otherwise ask for any caveats the user wants captured.

**Step 3: Compose the file.** Build the file with frontmatter on top, the parsed Analysis section if present, and the Voiceprint portrait body. The composed file matches the library voiceprint schema in `../../os-library/references/voiceprint-schema.md`.

```
---
type: voiceprint
author: <name>
default: yes | no
scope: <scope>
genre: <optional>
source: <provenance>
created: <YYYY-MM-DD>
notes: <freeform>
---

# Analysis [if present in source]

[parsed Analysis content]

# Voiceprint

## {Nickname [if present, otherwise asked]}

[parsed Voiceprint portrait body]
```

If the imported voiceprint lacks a nickname, ask the user to supply one (it's a useful identifier for the artifact). If the user prefers, the mode can suggest one based on the portrait's content.

**Step 4: Save through library.** Invoke os-library/save to write the composed file. Save validates the frontmatter, generates the filename per convention (`<author>-<scope>.md`, or `<author>.md` for general-scope user defaults), and confirms the write.

## Output

The file written to `os-inputs/voiceprints/<filename>.md`, with confirmation of the path, the frontmatter values, and a brief note on what was inferred vs. what the user supplied. If any frontmatter values were inferred with low confidence, the mode flags them as candidates for `os-library/repair` review later.

Example output:

```
Imported and saved: os-inputs/voiceprints/<author>-customer-email.md

Frontmatter (you supplied / inferred):
- type: voiceprint
- author: <user-profile name>
- default: yes (you confirmed)
- scope: customer-email (you supplied)
- source: "voiceprint from a prior newsletter corpus" (you supplied)
- created: <today>
- notes: "Calibrated for the warm direct-customer register, not the formal business register" (extracted from the voiceprint body)

The imported voiceprint already had a # Voiceprint section with the nickname "Newsletter Voice." Preserved as-is.
The imported voiceprint did NOT have a # Analysis section. The audit layer is missing — consider re-running from-sample on the original corpus if you want analysis preserved.
```

## Output discipline

Import preserves the source content as much as possible. The mode does not rewrite the Voiceprint portrait or modify the Analysis content. Frontmatter is the only addition. If the imported voiceprint reads as substandard (era-tells, source-leak, generic phrasing), the mode flags the issue but still imports — fixing the content is a separate operation (re-run from-sample on the original source, or hand-edit the file).

## Cross-mode suggestions

After import, common follow-ups depend on context. If the user wants to verify the imported voiceprint surfaces correctly, point at os-library/find with the relevant scope. If the imported voiceprint reads weak (era-tells, source-leak), suggest re-running from-sample on the original source material to produce a stronger version. If the user has multiple imports to do, do them one at a time rather than batching — each voiceprint needs its own frontmatter values.

## Design rationale

This mode exists for the inaugural population step. A buyer arriving with voiceprints produced by other tools, by a previous voiceprint version, or by hand-curation needs a way to land them in the library with proper frontmatter. Without import, every existing voiceprint requires manual file composition with hand-typed frontmatter — friction at exactly the moment the user is trying to start using the library.

Import does not validate or improve the imported voiceprint's quality. The voiceprint content goes through verbatim. Only frontmatter is added. This is deliberate — the user knows the existing voiceprint's quality, and the mode's job is filing, not editing. If the user wants to improve a voiceprint, they re-run from-sample on the source material.

The mode is interactive (asks for missing frontmatter values) rather than fully automated because frontmatter inference is unreliable for fields like `scope`, `default`, and `source`. Asking once at import time produces correct frontmatter. Auto-guessing produces drift the user has to repair later.

Once the library has been in use for a while, this mode becomes rare — most voiceprints will be produced through from-sample or from-book and saved fresh. Keep import as a long-tail utility for special cases (external voiceprints, manual curation, system migrations).
