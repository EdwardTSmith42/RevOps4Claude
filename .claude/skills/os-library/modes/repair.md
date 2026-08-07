---
name: os-library/repair
description: Fix incomplete or malformed frontmatter on a specific input file. Reads the body content, infers the likely correct values, proposes a corrected frontmatter block, and asks the user to confirm before writing. Triggers on "fix the frontmatter on file X," "repair this file," or follow-ups to find / list / validate when those modes surface repair flags. Do NOT trigger when the user wants to find inputs (use `find`), save a new input (use `save`), or sweep the whole collection (use `validate`).
---

# Mode — Repair

Fix frontmatter on a specific input file. Repair reads the body, infers what the frontmatter should be from context, proposes corrections, and asks the user to confirm before writing. The user always sees and approves the proposed changes — repair is never silent.

This mode handles the cleanup work that find, list, and validate flag but don't act on. Files with missing required fields, malformed enum values, or sparse-but-fixable frontmatter all flow through repair.

## When to use

Typical user invocations name a specific file to repair, ask to fix all the files flagged by the last `validate` run, or follow up on a `[needs repair]` tag surfaced in a `list` or `find` result.

Chained invocations: `find` returns a candidate with a repair flag, the user picks the candidate anyway and asks repair to fix it before a downstream skill loads the reference. `validate` produces a worklist, the user works through it one file at a time via repair.

## Inputs

- The file path to repair
- Optional: explicit instructions about what to fix (e.g., the user names a missing field and the value to use)

If the user invokes repair without specifying instructions, the mode infers what's wrong from the file's current state and proposes corrections accordingly.

## Run

The procedure runs through five steps.

**Step 1: Read the current state.** Load the file. Parse the existing frontmatter (if any). Identify the file's type from its directory placement (`os-inputs/voiceprints/` means voiceprint, `os-inputs/style-samples/<author>/` means style sample, etc.). Identify what's missing or malformed by comparing against the schema in the relevant `references/<type>-schema.md`.

**Step 2: Infer corrections.** Use multiple signals to propose values for missing or wrong fields. The directory path contributes (the parent folder of a style sample tells the author). The filename contributes (an author-prefixed voiceprint filename strongly implies that author). The body content contributes (genre, voice, source provenance often appear in the body itself). Existing frontmatter fields contribute even when partial.

For some fields, inference is reliable. Type is almost always recoverable from the directory. Author is usually recoverable from filename or directory. Other fields (scope, pattern, proven) require context the body may or may not provide — when inference is uncertain, propose the best guess and surface the uncertainty.

**Step 3: Propose the correction.** Compose the proposed frontmatter as a unified diff or full proposed block, depending on how much is changing. Show the user exactly what will change, with brief rationale per inferred value. Use the same severity vocabulary as `validate` so the user can map between modes cleanly. **Severe-fix** is high-confidence and addresses a missing required field. **Moderate-fix** addresses a malformed closed-enum value with high-confidence inference. **Mild-fix** addresses an open-enum freeform value or optional-field gap and can be left blank if the user prefers.

Each proposed correction names its severity tier and a one-line rationale describing what signal drove the inference (e.g., a required field inferred from filename is severe-fix high-confidence; a closed-enum value corrected from a near-miss is moderate-fix; an open-enum freeform value inferred from body content is mild-fix low-confidence and worth confirming).

**Step 4: Get confirmation.** Ask the user to approve, adjust, or reject. The user can accept the full proposal, accept some fields and override others, or reject and repair manually. Repair never writes without explicit approval. If the user adjusts a field, validate the adjusted value against the schema (a freeform value is fine, a malformed enum is flagged).

**Step 5: Write the corrected file.** Replace the frontmatter block with the approved version. Preserve the body content exactly — repair only touches frontmatter. Confirm the write with the file path and the final frontmatter values.

## Output

The output happens in two phases. First, the proposal phase: show the user what's currently in the file, what the inferred corrections are with rationale, and ask for confirmation. Second, after confirmation, the write phase: confirm the file was updated with the final frontmatter.

The shape, in skeleton:

```
Repair proposal for: <full path>

Current frontmatter:
- <field>: <value>
- (other fields missing)

Proposed corrections:
- <field>: <value> [<severity>, <enum-class>]
  Inferred from: <what signal drove the inference, one short clause>. <Confirm/adjust note if low confidence.>
- [...]

Approve as proposed, adjust specific fields, or supply any missing values?
```

After confirmation, the write confirmation is a single short block: the saved path and the final frontmatter as written.

## Output discipline

The proposal is the most important part of the output. The user needs to see what's being inferred and why, with confidence per field. Bullets are appropriate for the field listing — this is genuinely list-shaped enumeration. The rationale per field is one-line prose, not bulleted decoration.

After confirmation, the write confirmation is brief and scannable.

If the user rejects the proposal, repair stops. No partial writes.

## When inference fails

Some fields cannot be inferred reliably. The `source` field for voiceprints depends on knowing what was sampled to produce the artifact — repair can guess from body content if the body mentions provenance, but often can't. The `notes` field depends on user context that isn't in the file.

When inference fails for a required field, repair surfaces the gap and asks the user to supply the value. Repair does not write incomplete frontmatter and call the file fixed — that just produces a different repair flag later.

For optional fields where inference fails, repair leaves the field absent rather than fabricating. An empty optional field is fine. A fabricated one is harmful.

## Multiple repairs in sequence

If the user is working through a worklist from validate, repair runs once per file. The user can move quickly through high-confidence cases (approve, approve, approve) and slow down on low-confidence ones (adjust the scope field on this one, supply the source on this one). Each repair is independent — no batched approval that would let bad inferences slip through.

If the user wants to repair multiple files with similar issues at once (e.g., several voiceprints all missing the same field, all with clearly-inferrable values from their bodies), repair can process them in sequence with per-file confirmation. The mode does not bulk-repair without confirmation.

## Cross-mode suggestions

After a repair, useful follow-ups depend on context. If the user is mid-drafting flow and the repaired file is about to be loaded, mention that find can now use the repaired file with full confidence. If the user is working through a validate worklist, mention how many files remain. If the repair was a one-off, no postamble.
