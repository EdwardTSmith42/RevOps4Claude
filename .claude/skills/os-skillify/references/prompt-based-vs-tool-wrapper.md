# Prompt-based vs. tool-wrapper skills

Legacy prompts split into two broad categories that convert differently. Identifying which category a source falls into early in `from-prompt` mode (or which category an existing skill falls into in `enhance` mode) saves effort and prevents `DEFER` decisions getting made implicitly.

## The two categories

### Prompt-based skills

The source is **mostly text**: rationales, taxonomies, classification rules, output contracts, craft moves, domain knowledge. The skill works by giving the agent good thinking — no external scripts or runtime integrations are required.

**Examples from the v0.1 bug-investigation pilot:**

- `bug-fix-expert.md` — orchestrator picker; pure prompt; converted directly (`SHIP NOW`).
- `bug-investigation-standard.md` — investigation workflow; pure prompt; converted directly.
- `latent-bug-scout.md` — defect-family taxonomy + signals catalog; pure prompt; converted directly.
- `mutation-scout.md` — mutation thinking framing; pure prompt; converted directly.
- `interrogate.md` — PR interrogation workflow; pure prompt; converted directly.
- `fresh-eyes.md` — meta-review workflow; pure prompt; converted directly.
- `scope-deferral-investigation-drop.md` — deferral discipline; mostly prompt with one filesystem path; converted with light path adaptation.

### Tool-wrapper skills

The source is **mostly orchestration glue around something external**: bash scripts, custom CLI tools, MCP integrations, runtime auth flows, sandboxed filesystem mechanics.

**Examples from the v0.1 pilot:**

- `root-cause-bug-ops.md` — orchestration wrapper for Codex case-management scripts; the scripts don't exist in Claude Code → `DEFER + SALVAGE`.
- `blast-radius-investigator.md` — wrapper around a custom Python scanner script → `DEFER + SALVAGE`.
- `hotjar-replay-investigator.md` — wraps `browser_use_hotjar_shared.sh` → `DEFER` (when ported, use `browser-use` skill or Chrome MCP).
- `sentry-report-coordinator.md` — wraps `run_sentry_report.sh` → `DEFER + SALVAGE` (when ported, use Sentry MCP).
- `cursor-branch-debug-loop.md` — wraps Cursor CLI with auth probing → `DEFER` (Claude has its own challenger paradigms).
- `duck-hunt.md` — partially tool-wrapper (custom heartbeat scheduling) but mostly prompt → adapted to delegate scheduling to `/loop` while preserving the prompt-based per-cycle behavior.

## How to identify

When you read a source, count the proportion of:

- *Prompt content* — text describing what the agent should think, decide, output, avoid. Includes taxonomies, classification rules, rationales, craft moves, output contracts.
- *Glue content* — bash command examples, CLI invocations, env-var setup, file-path config, custom script paths.

Heuristics:

- **>80% prompt content, <20% glue** — clearly prompt-based. Convert directly. Adapt path config if needed; otherwise `SHIP NOW`.
- **<50% prompt content, >50% glue** — clearly tool-wrapper. Apply tool-wrapper conversion path (below).
- **In between** — check whether the glue is the *job* or the *delivery mechanism*. Glue that orchestrates external scripts the agent can't reproduce → tool-wrapper. Glue that's just bash command examples the agent could equally well call directly → prompt-based with a practical-commands section.

Specific signals that flag tool-wrapper:

- Hard-coded paths to custom scripts in the source's directory: `~/.agents/skills/<name>/scripts/...`, legacy or harness-specific equivalents such as `~/.codex/skills/` and `~/.claude/skills/`, or `${SOMETHING_HOME}/scripts/...`.
- Auth probes: `printenv X_API_KEY`, custom CLI auth checks (e.g., `agent -p ... "Reply with exactly OK."`).
- Custom file-system conventions: `lanes.json`, `hypotheses.jsonl`, `case-schema.yaml`.
- RRULE / cron-style scheduling encoded directly in the prompt.
- MCP-server-name references (e.g., Sentry MCP `mcp__...__search_issues`).

## Conversion path: prompt-based skills

Standard `from-prompt` workflow applies straightforwardly:

1. **Setup** — workspace + destination decided.
2. **Phase 1 (Classify)** — most chunks are craft moves / domain knowledge / output shape. Few scaffolding candidates beyond classic patterns (tip bribery, persona cosplay).
3. **Phase 2 (Rationale)** — usually fast. The source's rationale is often stated explicitly because there's no orchestration distracting from it.
4. **Phase 3 (Plan)** — disposition is usually `SHIP NOW` (standalone) or `MERGE` (with siblings into a category skill).
5. **Phase 4 (Build)** — straightforward template-driven build.
6. **Phase 5 (Verify)** — craft preservation easy to check by reading.
7. **Phase 6 (Log)** — full entry per template.

Common issues:

- Hard-coded paths (`/Users/<you>/.codex/private/...`) need adaptation to portable, purpose-appropriate equivalents. Skill locations default to `.agents/skills/`; harness-specific data/config locations stay clearly labeled or become environment-driven.
- Codex sibling skill cross-references (`$delivery-ops`, `$bug-investigation-standard`) need re-pointing to converted equivalents (or kept as inert pointers documented in the decision log).

## Conversion path: tool-wrapper skills

Tool-wrappers usually warrant `DEFER + SALVAGE`:

1. **Setup** — same as prompt-based.
2. **Phase 1 (Classify)** — separate *prompt content* from *glue content*. The glue is mostly drop. The prompt content is salvageable.
3. **Phase 2 (Rationale)** — focus on the prompt content's rationale. The orchestration's rationale is usually obvious (*we use script X because it does Y faster than the agent could*).
4. **Phase 3 (Plan)** — disposition is usually `DEFER + SALVAGE`. The orchestration role waits; the prompt content moves to shared references in the cluster being built.
5. **Phase 4 (Build)** — for the salvage portion only. Add to shared references with attribution (note the source skill).
6. **Phase 5 (Verify)** — verify the salvaged rules are preserved; verify the deferred-skill decision-log entry captures the deferral context.
7. **Phase 6 (Log)** — `DEFER + SALVAGE` entry. Two destinations to document: the deferred-skill record (what's not converted yet) and the salvaged-content destinations (where rules live now).

Common patterns to salvage:

- *Epistemic rules* — e.g., *"never claim 0 affected users without confirmed tracking."* These are AGENTS.md-level user preferences that survive in shared references.
- *Noise filters* — domain-specific filters (e.g., Stream Lab signature filter); preserve verbatim with origin notes.
- *Output contracts* — formatting rules that apply across the cluster.
- *War-story-derived patterns* — *"mixed-group issue IDs include unrelated production events; scope filtering to env + signature/message instead."*

When the deferred-skill's tool dependency becomes available (a script gets ported, an MCP launches), come back and run a fresh `from-prompt` round on the original source — the salvaged rules can then re-integrate cleanly.

## When to revisit (`enhance` mode)

In `enhance` mode, periodically re-check tool-wrapper deferrals:

- Has the dependency become available? (Script ported? MCP launched? Sibling skill landed?)
- Has Claude Code grown a native pattern that supersedes the original tool? (e.g., the `browser-use` skill makes most custom Hotjar / Chrome / Brave wrappers unnecessary — a deferred Hotjar skill might convert as a thin wrapper around `browser-use` without porting the original bash script.)

Re-running `from-prompt` on the deferred source with the dependency now available may move the disposition from `DEFER` to `SHIP NOW` or `ADAPT`.

## Used by

- `from-prompt` — Setup + Phase 3 (disposition selection).
- `enhance` — Phase 1 (Survey, identifying skill types) + Phase 3 (Decisions on whether to revisit deferrals).
- `disposition-vocabulary.md` cross-references this doc for `DEFER` and `DEFER + SALVAGE` signal recognition.

## Source

Distilled from the v0.1 bug-investigation pilot. The pilot hit a 6-of-14 ratio of tool-wrapper skills warranting `DEFER + SALVAGE` — a higher proportion than expected. Future cluster conversions should triage prompt-based vs. tool-wrapper early to set realistic scope.
