# Tool-Wrapper Skills — bank the tool knowledge a session just earned

Loaded by os-skillify when generating a wrapper skill for an external tool (CLI, MCP server, SaaS API, desktop app). The ambient offer behavior — *when* to propose banking tool knowledge — lives in `../../_shared/references/proactive-prompting.md` (the instant-offer exception); this file is the *contents* standard: what makes a wrapper genuinely useful rather than a doc-dump.

A recurring, high-value thing to skillify: the user works with an external tool — a CLI, an MCP server, a SaaS API, a desktop app — and the session spends real effort learning to drive it. Docs get fetched, auth gets untangled, tool names get discovered, a working invocation finally lands. That knowledge is a sunk cost, and without capture it evaporates when the session ends; the next session pays it all again. When you notice a session has just earned tool knowledge the hard way, offer to bank it as a small wrapper skill (or extend the existing wrapper for that tool). This is an instant offer — the re-discovery cost is obvious the first time, so it doesn't wait for the usual repeated-pattern threshold.

What makes a wrapper genuinely useful rather than a doc-dump — capture the *working subset*, verified locally:

- **The calls the user actually makes.** A tool may expose a hundred operations; the wrapper documents the handful this user really uses (read these things, post/update those things) with working invocations. Inventorying the full API surface every session is exactly the waste the wrapper exists to end.
- **Which auth method actually works here** — not the three the docs describe, the one that's proven on this machine.
- **The transport that won** — API vs curl vs MCP vs CLI, and why, if a competitor was tried and lost.
- **Where credentials live** — a *pointer* (.env file, harness credential store, wherever the user keeps them), never the secret itself.
- **The permission ledger** — what the user has said is fine to do freely versus what needs a per-action ask. This is user-decided, learned once, and honored thereafter.
- **Small scripts or step-patterns for common jobs** — a little runnable script or a numbered pattern the agent follows beats prose when the job recurs.
- **A last-verified date** — so a future session knows how much to trust it, and re-verifies quietly when it's gone stale rather than failing loudly.

And one line in every wrapper it generates: *when you hit friction this skill didn't cover, ask the user whether to fold what you just learned back into the skill or its linked files.* Wrappers that don't self-update decay into the doc-dumps they were meant to replace.

The bar throughout: verified-locally beats copied-from-docs. A wrapper of unverified doc-paste is worse than no wrapper — it costs the same re-discovery *plus* the debugging of stale instructions.

