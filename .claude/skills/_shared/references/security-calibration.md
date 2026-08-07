# Security calibration — turning the plain-language floor into real enforcement

The catastrophic-action floor lives in two forms. In `os-inputs/_os-preferences.md` it's written the way a person thinks about it — *don't let it `rm -rf` my home directory*. In the harness it has to be written the way that harness actually enforces things. This reference is the translation between them.

Keep the plain-language side plain. The user edits that one; nobody should have to learn a matcher syntax to say what they don't want deleted.

## Verify before you write

**Formats below were confirmed 2026-08-03.** Permission syntax is a moving part of every harness, and a rule written in a format the harness no longer parses is worse than no rule — it sits there looking like protection.

Before writing the floor, check that the format still holds. The current docs are the source of truth, not this file:

- Claude Code — `https://code.claude.com/docs/en/settings`
- Codex — `https://learn.chatgpt.com/docs/config-file/config-basic`

If the format has moved, follow the docs and say so in one line rather than writing what's here. If you can't reach the docs, write the floor as documented below and tell the user it's worth a re-check.

## Claude Code

Rules go in a `settings.json` `permissions.deny` array. Create-or-merge; never clobber an existing array. The user scope (`~/.claude/settings.json`) covers every project; the project scope (`.claude/settings.json`) covers one repo and is committed. Rules **merge** across scopes rather than override, so adding to one never silently disables another.

The rule form is `ToolName(pattern)`, where `*` is a wildcard:

| The floor, in plain language | Enforced form |
|---|---|
| Never `rm -rf` anything | `Bash(rm -rf *)` |
| Never `rm -rf` root or home | `Bash(rm -rf /*)`, `Bash(rm -rf ~*)`, `Bash(rm -rf $HOME*)` |
| Never force-push | `Bash(git push --force*)`, `Bash(git push --force-with-lease*)` |
| Never hard-reset onto a remote branch | `Bash(git reset --hard origin/*)` |
| Never make everything world-writable | `Bash(chmod -R 777*)`, `Bash(chmod 777 -R*)` |
| Never read my secrets | `Read(./.env)`, `Read(./.env.*)`, `Read(./secrets/**)` |

Two honest limits worth naming to the user if they ask.

Bash patterns match the command as written, so an equivalent command spelled differently gets through — the floor catches the obvious catastrophe, not a determined workaround. The real backstop is the permission mode, which is why the mode conversation matters more than the list length.

And some things in the starter list aren't bash commands at all. *Don't merge to a default branch in a repo I don't own* and *don't publish to a customer-facing surface without asking* are judgments, not patterns. They belong in the policy layer or the principles file, and the honest thing is to tell the user which of their rules are mechanically enforced and which are instructions the AI follows.

## Codex

Codex doesn't have a per-command deny list, and pretending otherwise produces a floor that isn't there. It constrains by sandbox and approval instead, in `~/.codex/config.toml` (user) or `.codex/config.toml` (project):

```toml
sandbox_mode = "workspace-write"   # read-only | workspace-write | danger-full-access
approval_policy = "on-request"     # untrusted | on-request | never
```

`sandbox_mode` bounds what's reachable; `approval_policy` decides when it stops to ask. Together they cover the same ground the deny list covers on Claude — from a different direction. `workspace-write` keeps writes inside the project (with `.git` and `.codex` protected) and is the sane default; the destructive-delete case is handled by not having reach outside the workspace at all, rather than by naming the command.

There's also a named-profile layer — `default_permissions = ":workspace"`, with custom `[permissions.<name>]` tables — worth reaching for when a user wants more than one posture. Note that `approval_policy` and `sandbox_mode` are deliberately ignored in project-local config, so the user-level file is where a real floor goes.

## Any other harness

Find the nearest enforced scope and use it. When the harness has no enforcement layer, say that plainly — the floor becomes an instruction the AI follows rather than a wall it can't cross, and the user deserves to know which one they have. Don't promise rules to a harness that has no rules.

## Going deeper

This is a floor, not a security posture. A user who wants per-project rules, managed settings that can't be overridden, secret-path denies, or a custom Codex permission profile can have all of it — but not during a first install, where it costs momentum and buys little. When someone shows interest, offer to put it on their tracker and move on.
