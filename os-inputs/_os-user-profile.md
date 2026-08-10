---
name: Edward
default_voiceprint_scope: default
default_org: HFD
default_brief:
---

# Your Profile

This file is read by every Personal OS skill that needs to know who you are. The `name` field drives the **implied-author rule**: when you ask the AI to "draft an email" without specifying whose voice, the matcher uses your `name` to find your voiceprint.

## What to fill in

- **`name`** — required. The string the implied-author rule uses to match voiceprints (e.g., if your `name` is `Rob`, the matcher looks for `voiceprints/rob.md` or scoped variants like `voiceprints/rob-longform.md`).
- **`default_voiceprint_scope`** — usually `default`. Override if you want a specific scope used when no scope is specified (e.g., `longform` if your default writing context is long-form essays).
- **`default_org`** — optional. If you operate under an org (Lennon Labs, Anthropic, your company), naming it here loads `os-inputs/<org>-rules.md` automatically when present.
- **`default_brief`** — optional. If you have one project that's your main work right now, naming it here loads `os-inputs/briefs/current/<slug>.md` automatically.

## Editing this file

You can edit by hand any time, or run `os-guided-setup customize` to walk through it interactively.

## What reads it

Anything that drafts in your voice, anything that needs to attribute work to you, anything that resolves "your" anything:
`os-writing`, `os-voiceprint`, `os-editing`, `os-email`, `os-audience`, `os-offer`, `os-daily-assist`, `os-tune`, `os-skillify`, and most other skills in the pack.
