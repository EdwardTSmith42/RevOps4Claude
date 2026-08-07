# Evidence lanes

The four-lane taxonomy for collecting evidence during a bug investigation. Used by `evidence`, `pr-interrogate`, and `recurring-hunt` modes.

## The four lanes

- **Support lane** — exact transcript snippets and key user actions from your support-system (whatever you use: shared inbox, helpdesk, in-app chat, tracker comments). Pulled before code-side investigation so user-reported behavior anchors the rest.
- **Runtime lane** — server / app / tool-call logs in bounded time windows. Use UTC timestamps and explicit windows around the incident.
- **Error lane** — issues / events from your error-monitoring system (Sentry is the assumed default; adapt to your tool) correlated with concrete timestamps and entities. Pull issue links, timestamps, counts, and error signatures. Apply `user-attribution-rule.md` for user-count wording.
- **Replay lane** — when a session-replay tool is in play, prefer extracting the action timeline as text over long video playback. The action timeline is text the agent can reason over; video isn't.

## Lane-by-lane evidence checklist

### Support lane

- Conversation IDs, screenshots, timestamps (UTC).
- User / org / project identifiers.
- Direct quotes of what the user said and tried.
- Key user actions in order.

### Runtime lane

- Server logs in bounded time window.
- App / client logs (especially around the moment of failure).
- Tool-call traces (when the system makes external calls).
- Database / state queries to verify entity state.

### Error lane

- Error-monitoring issue links + signatures.
- Event counts and `userCount` (label as "attributed users" unless tracking is confirmed — see `user-attribution-rule.md`).
- First-seen / last-seen timestamps.
- Both relevant environments (production + staging/dev when comparison helps).
- Resolved + unresolved when needed.

### Replay lane

- Replay identifier: site ID + recording ID + replay URL.
- Session context: user hash, country/device/browser, timestamp.
- **"See all <n> actions" extraction first** — text-based action timeline. Video playback only when text isn't enough.
- Error/friction signals: errors, rage-clicks, dead clicks, loops, navigational U-turns.
- Screenshots: player view, actions list, key moment(s).

## Lane sequencing

Run lanes in parallel where possible (each lane is independent). Combine via UTC timeline correlation: line up timestamps across lanes to confirm whether evidence patterns reinforce each other or contradict.

**Production-only queries first** when querying error/runtime data:
- Production has more data — denser signal, visible trends.
- Dev/staging may have untested code throwing errors for unrelated reasons that contaminate the signature.

## Lane status

Every lane gets a status. See `lane-status-vocabulary.md`.

## Used by

- `evidence` mode — the core taxonomy for the full investigation flow
- `pr-interrogate` mode — uses error and runtime lanes for production correlation
- `recurring-hunt` mode — uses Local Investigation when fixing isn't safe this pass

## Malleability note

**Canonical:** the four-lane split (support / runtime / error / replay). Each lane represents an independent evidence source with distinct collection patterns; collapsing them loses the parallel-collection efficiency.

**Adaptable:** which lane is primary depends on the bug. UI-handoff bugs lean replay; multi-system data bugs lean runtime; user-reported bugs always start with support.

