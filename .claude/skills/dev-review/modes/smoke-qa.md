# Mode: smoke-qa

Part of the `dev-review` skill. Selected when the user wants diff-aware UI smoke testing on a web app branch — phrasings like "Smoke-test this branch," "QA the changed routes," "Run the diff-aware UI smoke," "Visit affected pages."

## Job

Diff-aware route inference + browser-use validation. Identify routes likely affected by the changed files, visit them with an isolated browser session, capture title / URL / body-text preview / interactive-element snapshot / screenshot. Produce a smoke-QA report with evidence per route.

## Scope adaptation

Per `../references/scope-adapter.md`, `smoke-qa` works on:
- **Branch** (default): diff against `origin/develop` or named base; visit routes from changed files.
- **Commit / commit-range:** diff for that scope; visit routes inferred from those changes.
- **PR:** PR diff; visit routes for changed files.

For very large diffs (many routes), apply sub-agent fanout: one subagent per route cluster (e.g., authenticated vs unauthenticated, by feature area). Each subagent does its slice's smoke; parent reconciles into the report.

## Run

### 1. Choose the target

- Use user-provided `base-url` when given (e.g., `http://localhost:3000` for local dev, `https://staging.example.com` for staging).
- Otherwise auto-probe common local ports: 3000, 8080, 5173, 4321.
- For staging/production with auth: use `browser-use` skill's shared real-browser profile to inherit logged-in state.

### 2. Identify the diff

```bash
# Choose git base: origin/develop > origin/main > tracked branch > merge-base
BASE=origin/develop  # or as detected
git diff --name-only $BASE...HEAD                          # committed changes
git diff --name-only --cached                              # staged
git diff --name-only                                        # unstaged
```

Union all three. These are the files to map to routes.

### 3. Infer affected routes

Heuristics by framework:

- **Next.js `pages/` directory:** file path `pages/foo/bar.tsx` → route `/foo/bar`.
- **Next.js `app/` directory:** file path `app/foo/page.tsx` → route `/foo`.
- **React Router projects (config-driven routing):** find the router config file (commonly `<root>/src/Router*.tsx`, `routes.tsx`, or framework equivalent); parse `<Route path="..." element={<X />}>` patterns; map page components back to paths. Adapt the config-file path to whatever your repo uses.
- **Other frameworks:** add framework-specific heuristics or fall back to user-provided `--paths`.

Output: list of unique routes likely affected by the diff.

### 4. Visit routes via browser-use skill

For each route, use the `browser-use` skill (don't write a custom bash wrapper):

```
For each route in inferred-routes:
  - Navigate to <base-url>/<route>
  - Wait for stable state (DOM ready + first contentful paint)
  - Capture: page title, final URL (after redirects), body-text preview (first 500 chars), interactive elements snapshot (visible buttons / links / forms), screenshot
  - Note errors: 4xx / 5xx response codes, JS console errors, blank pages, timeout
```

Use a clear session name: `check-smoke-qa-<branch-slug>`. Use isolated profile if the diff might mutate auth state; use shared profile if you need authenticated routes and the change shouldn't leak.

### 5. Capture evidence per route

For each visited route, record:
- Route path
- Final URL (post-redirect)
- HTTP status (if available)
- Page title
- Body-text preview (first ~500 chars)
- Interactive-element snapshot (buttons / links / inputs visible)
- Screenshot path
- Any error/friction signals (console errors, rage-click candidates if applicable, navigational U-turns)

### 6. Produce report

Use `../templates/smoke-qa-report.md`. Output to `.local/check-smoke-qa/<timestamp>/report.md` with screenshots saved alongside. Do NOT commit these to the repo.

## Limitations

- **Route inference is heuristic, not full framework routing.** False positives (route inferred but not actually affected) and false negatives (route affected but not inferred) are both possible.
- **Smoke/regression oriented, not a replacement for deep scripted E2E.**
- **`browser-use` doesn't expose console/network logs as rich gstack-style data.** This skill focuses on route coverage, redirect detection, screenshots, and empty-page signals.
- **`--shared-auth` (when used) intentionally leaves the shared real-browser session open** so it doesn't disrupt normal `browser-use` workflows.

## Hard rules

- **Use the `browser-use` skill, not custom browser wrappers.** Don't write bash wrappers around browser-use.
- **Keep reports narrow and evidence-based.** Don't over-claim what wasn't observed.
- **If the user asks for deeper workflow automation than smoke can support, say so and switch to `browser-use` directly** instead of stretching this mode.
- **Default to isolated session.** Use shared session only when authenticated routes are needed.

## Mode-specific references

- `../references/scope-adapter.md` (scope decisions; fanout for large diffs)
- `../templates/smoke-qa-report.md`

Cross-skill:
- `browser-use` (invoked for actual browser ops)

## Output

See `../templates/smoke-qa-report.md`. Sections:

- **Scope** (branch / base; routes inferred; routes visited)
- **Per-route evidence** (path / status / title / body preview / interactive elements / screenshot path / errors)
- **Summary** (passed / blocked / errored / inferred-not-visited)
- **Follow-ups** (routes that need manual verification; invoke `dev-scope-deferral` for any that should be addressed later)

## Design Rationale

Mode-specific notes:

- **Use the existing `browser-use` skill, not a bash wrapper.** Browser-use handles real-browser auth and session management cleanly; wrapping it loses that.
- **Diff-aware route inference is what makes this mode worth running.** Without it, the user provides routes manually; with it, the smoke run scales to "review what actually changed."
- **Routing-config parsing is the generalization point.** Repos vary; the pattern (parse routing config to map files → URLs) is what holds, not any one path.
- **"Smoke/regression oriented, not a replacement for E2E"** — explicit scope fence. Don't try to run full E2E from this mode.
- **Reports stay local in `.local/check-smoke-qa/`** — sandbox-safe; not committed.

