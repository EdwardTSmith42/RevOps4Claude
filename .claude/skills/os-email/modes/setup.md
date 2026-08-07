# Mode: setup

Confirm and customize triage configuration for an account. Reads the audit artifact written by `audit`, walks the user through a short confirmation interview, creates Gmail labels with explicit approval, and writes the per-account profile.

`setup` is the second step in the user flow. `audit` runs first and provides grounded findings; `setup` turns those findings into a working configuration.

## Inputs

- Account (from MCP)
- `os-inputs/email-accounts/<account>.audit.md` — required; if missing, route to `audit` first
- `--refresh` — re-run setup against an existing profile to incorporate updated audit findings

## Procedure

### 1. Confirm account + discover tools + load audit

List the accounts available through whatever email connector is wired. Confirm which one to set up. Load the audit artifact and surface its key findings.

**Tool discovery (once per install).** Connectors for the same mailbox expose different tool names, so discover the wired connector's actual tools for each capability this skill needs — search messages/threads, fetch full message content (batch if available), list labels, create/rename labels, apply/remove labels in bulk, create filters (not all connectors can) — and record the capability-to-tool mapping in the per-account profile. Every other mode reads the mapping instead of guessing names. If a capability is missing from the connector, note it in the profile so the dependent feature degrades visibly instead of erroring; if no email connector is wired at all, help the user connect one before continuing. Principles and fuller framing: `../../_shared/references/cross-harness-adaptation.md` (Connectors vary too).

### 2. Read existing labels

Use the list-labels tool from the discovered mapping. Three possibilities:

- **None of the 7 triage labels exist.** Propose creating all 7.
- **Some exist with matching names.** Reuse them; propose creating the missing ones.
- **Similar labels exist with different names** (e.g., `Reply Needed` vs `needs-reply`). Surface the conflict; ask whether to use the existing label, rename, or create alongside.

### 3. Confirmation interview (short)

Most questions have proposed answers from the audit. The interview is confirmation, not extraction.

1. **Account purpose.** Surface the audit's read on what kind of inbox this is (creator / consultant / founder / employee / mixed) and ask the user to confirm or adjust. Used to inform agent runtime judgment, not to drive a frozen preset.
2. **Replier(s).** Just the user, or the user plus a team / shared inbox?
3. **Customer/member-facing senders.** Audit lists candidates; confirm or adjust which patterns get `needs-support`.
4. **Mixed-use vendors.** Audit lists detected mixed-use senders; user can add others.
5. **Account-specific labels.** Audit surfaces candidates (e.g., `clients`, `from-team`, `students`); user accepts/rejects each.
6. **Account-specific starting rules.** Optional. Invite the user to name anything they want always treated a specific way — recurring senders that always demand action, platform DM channels that always route to support, internal sources that always need a reply, etc.

For everything not explicitly answered, the agent uses `references/classification-rules.md` defaults.

### 4. Propose label creation (approval gate)

Show the exact list of labels that will be created (the 7 universal + any user-confirmed account-specific labels). Wait for explicit approval. After approval, create via the mapped label-management tool and confirm each.

### 5. Write the profile

Use `templates/account-profile.md` as the starting shape. Write to `os-inputs/email-accounts/<account>.md`.

Filename convention: slugify the email address by replacing `@` with `-at-` and `.` with `-`. Example: `you@example.com` → `you-at-example-com.md`.

The profile captures only the user's confirmed customizations. Universal rules live in the skill references and are loaded at runtime.

### 6. Optional: dry-run first-sweep

Offer to run `first-sweep --dry-run --limit 25` immediately. This is the second wow moment — the buyer sees their actual inbox classified using their just-confirmed configuration. No labels applied yet; the report is read-only.

## Output

- Created labels in Gmail (with approval)
- `os-inputs/email-accounts/<account>.md` written
- Optional dry-run preview

## Approval gates

- Label creation: explicit approval before any label-creating tool call.
- Profile write: show the file content; confirm before writing.
- Dry-run sample: read-only by definition.

## Refresh path

`setup --refresh` re-runs the interview against an updated audit. Used when:

- Inbox patterns have shifted (new clients, new platforms, new noise sources).
- The user wants to reconsider account-specific labels.
- The user adds a new email account to triage.

Refresh preserves existing sender filters and account-specific rules unless the user explicitly removes them.
