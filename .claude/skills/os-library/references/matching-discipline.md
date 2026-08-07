# Matching Discipline

The convention for finding reference inputs in `os-inputs/`. Used by `os-library/find` directly, and by other skills (`os-writing`, fiction-oriented writing modes (in `os-editing`), `os-voiceprint`) following the same pattern from inside their own runs.

The principle is soft search, not strict matching. The user has accumulated inputs over time, frontmatter drifts, names get misremembered, and the right answer is to be forgiving rather than failing fast. Matching surfaces the best candidates available with whatever signal is present, flags any frontmatter issues as repair candidates, and lets the user proceed with the work either way.

## How matching works

Matching takes a job context (what the user is trying to produce) and returns a small ranked list of candidates per relevant input type. The job context typically includes the output format (landing page, customer email, action scene), the target voice or author (the user's default, a pen name, an external author), genre signals if applicable, and any explicit references the user named.

For each input type the job needs, the match runs in three layers from strict to lenient. Layer one looks for frontmatter matches on the most important fields. Layer two relaxes to partial matches and substring overlap on the same fields. Layer three falls back to content scanning — keywords from the job context appearing anywhere in the file body.

The candidate list comes back ranked by total signal across the three layers. A file with a strong layer-one match always ranks above a file with only a layer-three match. Within the same layer, files are ordered by recency and by `proven: yes` (for templates) when those fields are present.

## Per-type scoring

### Voiceprints

The most important fields are `author`, `scope`, and `default`. Matching prefers a voiceprint where `author` matches the job context's target author, with a `scope` matching the requested output format. If no scope-specific voiceprint exists for that author, fall back to a `default: yes` `scope: general` voiceprint for the same author. If the user named a non-self author (a pen name, an external author), match that author by name. If the user did not name an author, see the implied-author rule below.

**Implied-author rule:** when the job context names no author, the matcher uses the `name` field from `os-inputs/_os-user-profile.md` as the implied author for layer-one matching. This is how "draft a customer email" without further specification finds the user's customer-email voiceprint. The rule applies to all three confidence layers — layer one looks for `author: <user-name> + scope: <format>`, layer two relaxes to `author: <user-name>` alone, layer three falls back to content scanning. Without this rule, downstream skills would diverge on what "draft something for me" means in voiceprint terms.

A voiceprint marked `default: yes` is the user's go-to voiceprint *for that scope*. The user can have `default: yes` on multiple scope values simultaneously (general default plus customer-email default plus social-media default). The flag is a per-scope tiebreaker, not a global "use this voiceprint above all others" signal.

The signal layers for voiceprints look like this. Layer one matches `author` plus `scope` exactly. Layer two relaxes to `author` match alone, or substring matches on `author` (a short prefix of the user's query matching a hyphenated author handle). Layer three scans content for the author's name, the scope keywords, and any genre signals.

### Style samples

The most important fields are `author` and `pattern`. Matching prefers exact matches on both. If the user is producing an action scene in a specific author's voice, the match looks for `author: <author> pattern: action-scene`. If only the author matches, the candidate still ranks reasonably. If only the pattern matches (other authors have action-scene samples), the candidate ranks lower but stays in the result list as a possible adjacent reference.

### Templates

The most important fields are `format` and `proven`. Matching prefers `format` match plus `proven: yes`. A `format` match alone still ranks well. The `notes` field is scanned for context tags — a template whose notes name a specific campaign or audience type ranks higher when the job context names the same campaign or framing.

### Briefs

**Briefs do NOT use the three-layer fuzzy model the other types use.** Fuzzy matching on briefs is dangerous — surfacing a wrong-project brief loads project-specific context that poisons the work being produced. Briefs match in two modes only.

The first mode is exact-by-name. The user names the project, the matcher resolves to an exact filename in `briefs/current/` (substring match on the project field is fine here because brief filenames are typically distinctive). One brief per match.

The second mode is filtered-by-status. The user implies an active project without naming one (a phrase like "the current campaign" with enough other signal to resolve a target format). The matcher returns all `briefs/current/` files with `status: active`. If exactly one matches the implied target format, load it. If multiple match, ask the user to pick. Never silently choose among active briefs.

Archive briefs (`briefs/archive/`) match only when the user explicitly asks for historical context. The matcher does not search archive by default. A query that explicitly names archive (or names a project the user knows is historical) surfaces archive matches. A current-campaign query does not.

When no brief matches, briefs degrade gracefully but differently from other types. The calling skill proceeds without a brief loaded (briefs are usually optional rather than required) and asks whether to write a quick brief inline before continuing. There is no on-the-fly extraction chain for briefs the way there is for voiceprints — briefs are user-authored, not extracted from samples.

## Graceful degradation

When matching returns no clean candidate for a required input type, the calling skill does not silently approximate. The skill surfaces the situation to the user with three explicit options.

The first option is to proceed without that reference type. The skill notes the gap in its output ("no voiceprint loaded — voice will be generic") and produces what it can. This is the right default when the user wants a fast answer and is willing to accept lower fidelity.

The second option is to supply sample text and create the reference on the fly. This chains the calling skill into the relevant producer (`os-voiceprint` for voiceprints, template extraction for templates), produces a temporary artifact, uses it for the job at hand, and asks whether to save it for future use. The save step calls `os-library/save` which writes the artifact with proper frontmatter to the right `os-inputs/` subdirectory.

The third option is to point at an existing reference of related type. The user can request an explicit substitution (use a different author's voiceprint than the one the default-match logic would have selected, for example) — the skill honors the override and notes the substitution in its output.

The default behavior when no match exists is to ask, not to silently approximate. Silent approximation produces output that looks reasonable but is voice-generic, which is the failure mode that makes drafting outputs disappointing. Surfacing the gap respects the user's craft and gives them control.

## On-the-fly creation chains

The most common chain happens when drafting needs a voiceprint and the user hasn't supplied one and no match exists. The flow runs through six steps: drafting follows matching-discipline, no match is found, drafting asks the user with the three options above, the user supplies sample text, drafting chains into `os-voiceprint` to extract a portable artifact, drafting uses the artifact for the current job, and drafting asks whether to save the artifact via `os-library/save` for future use.

This works without any new mechanism. Each step is a normal skill invocation. The only requirement is that the producer skills (`os-voiceprint`, template-extraction in future writing modes) can be called from inside another skill's run, which is part of the harness's expected behavior.

The save-after-create step is intentionally optional. Some on-the-fly creations are one-offs the user doesn't want to keep. The skill asks rather than persisting silently.

## Frontmatter repair flow

When find encounters a file with missing or malformed frontmatter, the candidate stays in the result list but carries a "frontmatter incomplete" flag. The flag includes a brief description of what's missing or wrong. The user can act on it immediately by invoking `os-library/repair` on the file, or defer until convenient.

Repair reads the file content, infers the likely correct frontmatter values from context (the file's directory tells the type, the filename often encodes author and scope, the body content gives genre and pattern signals), proposes a corrected frontmatter block, and asks the user to confirm or adjust before writing.

Auto-repair is never silent. The user sees the proposed changes and approves them. This prevents library from "helpfully" rewriting metadata in ways the user didn't intend.

A periodic `os-library/validate` sweep produces a worklist of files needing repair, ordered by how broken they are (missing required fields most severe, malformed enum values next, missing optional fields least). The user can work through the worklist at their own pace.

## What a good match looks like

The result of `find` should give the calling skill enough information to act. For each input type the job needs, find returns one to three top candidates with their full file paths, the key frontmatter fields that drove the ranking, the confidence layer (one, two, or three), and any repair flags. The calling skill then loads the top candidate (or asks the user to pick if confidence is split between top candidates), incorporates the reference into its run, and notes which references it loaded in its output so the user can see what informed the work.

When confidence is high (layer-one match, no repair flags, top candidate clearly best), the calling skill can proceed silently with the load. When confidence is mixed (layer-two or layer-three match, repair flags present, candidates close), the calling skill surfaces the choice to the user before proceeding.

## When the convention doesn't apply

A few situations don't fit the matching pattern and should be handled directly by the calling skill rather than going through find.

If the user explicitly names a file (e.g., asking by exact filename for a specific voiceprint), load that file directly. No match logic needed.

If the user supplies sample text inline (paste the voice sample into the request), skip the inputs lookup entirely and treat the supplied sample as the reference for this run.

If the user is producing something that genuinely doesn't have a reference type in the library yet (a new genre, an unfamiliar format), the calling skill produces what it can without library involvement and may surface a suggestion to add a new reference type if the gap recurs.
