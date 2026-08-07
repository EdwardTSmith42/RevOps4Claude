# Turning on skill-usage logging

Optional. Everything works without it — this is the difference between your OS noticing *"you keep asking for this"* and also noticing *"…and the skill you already have keeps needing the same correction."*

**Malleability note.** The wiring below is Claude Code's; adapt it freely to whatever your harness calls the same thing. What's canonical is the shape: a harness-run command, fed the tool payload, appending one line. Don't replace it with an instruction asking the AI to write the line itself. That approach does work while a workspace is actively tended — it records mode and outcome, which a hook can't see — but it decays silently once attention moves elsewhere, and the decay is invisible until someone checks. Use the hook as the floor; treat an agent-written log as a bonus on top, never as the thing you're relying on.

## When to bring it up

Not during install. Someone setting up for the first time has no patterns yet, and an optional logging toggle in the first ten minutes is noise competing with the thing they actually came for.

The right moments are when it's already relevant:

- `reflect` runs and finds no invocation log — mention it once, in a line, as the thing that would make the next run sharper.
- `os-weekly-tuneup/setup` is configuring the weekly pass anyway.
- The user asks why a pattern wasn't spotted, or asks what the OS knows about their usage.

One mention, then drop it. If they say no, that's answered — don't re-offer at the next opportunity.

## What to tell them

Short and honest: it keeps a local record of which skills you run and the opening of what you asked, so your OS can spot which ones you lean on and which keep needing the same fix. It's a file on your own disk, nothing leaves the machine, and turning it off is deleting three lines of config.

The part worth saying plainly, because it's the part people care about: **it records the opening of your requests.** That's the whole point — the phrasing is what reveals a repeated ask — and it's also the reason someone might reasonably decline.

## Claude Code

Add to `~/.claude/settings.json`:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Skill",
        "hooks": [
          {
            "type": "command",
            "command": "python3 <skills-dir>/os-tune/scripts/log_skill_usage.py",
            "timeout": 10
          }
        ]
      }
    ]
  }
}
```

Substitute the real path to the installed skill. If a `PostToolUse` array already exists, add this entry to it rather than replacing it — clobbering someone's existing hooks to enable an optional feature is the kind of thing that ends trust in a tool.

**Check for one you already have.** Some people wire an equivalent hook themselves before Personal OS ever offers one. Two hooks on the same event both fire, so every invocation lands twice and the frequency counts — the whole reason for logging — come out doubled. Look at the existing `PostToolUse` entries first; if one already logs skill invocations, keep it and skip this, or replace it deliberately. Don't add a second one alongside.

Takes effect on the next session. Verify by running any skill, then checking that `~/.claude/skill-usage.jsonl` grew a line.

## Other harnesses

Any post-tool event that runs a command and passes the tool payload on stdin works. The script reads JSON from stdin and looks for a skill name under `tool_input.skill` (also accepting `skill_name`, `name`, and camelCase spellings), so a harness whose payload differs may need a small shim rather than a different design.

If the harness has no such event, say so plainly rather than approximating with an instruction. `reflect` works from memories alone; what's lost is frequency, not the core.

## Where the log lives

`~/.claude/skill-usage.jsonl` by default, overridable with `OS_SKILL_USAGE_LOG`.

Deliberately *outside* the workspace, because skill use spans every project and a per-workspace log would only ever see a slice. The trade-off: it doesn't travel with the workspace and `os-autosave` doesn't cover it. That's acceptable because it's a derived record — `distill` folds what matters into `os-memory/`, which does travel.

## Turning it off

Delete the hook entry. The log stops growing; nothing else changes. The existing file is the user's to keep or delete, and it's plain JSONL either way.

## What it never does

- Never records the assistant's output, tool results, or file contents. A row carries the skill name, the opening of your request (up to 200 characters — for a short request, all of it), the working directory the call ran in, and the harness's id for the call. The working directory is a full path, so it can carry a client or project name; worth knowing before you wire this up.
- Never fails loudly. Any error exits cleanly with nothing written; a logging side-effect must never break a turn.
- Never writes an entry it can't identify. A payload with no skill name produces no row, so the counts stay honest and an empty log means something real.
