# Calendar: check availability, then send invites

Real invites to colleagues are outward-facing. Only send after the manager's
explicit go-ahead, and only at times you've **verified people are free**. Wrong
times (usually a timezone slip) is the most common failure — be deliberate.

## Time-zone math (do this consciously)

- HFD writes schedules in **Pacific**. In summer that's **PDT = UTC−7**; in winter
  **PST = UTC−8**. US **Central** in summer is **CDT = UTC−5**. So in summer
  **CT = PT + 2 hours**. Don't mechanically call it "PST" in July — the offset only
  works if you track the actual DST state.
- `find_available_time` often returns wall-clock labeled **UTC** (the organizer's
  mailbox zone). Convert to PT yourself: PT(summer) = UTC − 7. A wrong conversion
  here is exactly what produces "the times were all wrong."
- Keep every meeting inside the hire's working window (e.g., a Central hire working
  8–5 CT = 6 AM–3 PM PT).

## Checking availability (before proposing OR sending)

Tool: `outlook_find_available_time` (participants, afterDateTime/beforeDateTime in
UTC, durationMinutes, isOrganizerOptional). Read the returned `attendeeAvailability`.

- For a meeting the hire attends with a **peer** and *not* the manager (a
  meet-and-greet, a shadow), set **`isOrganizerOptional: true`** so you check the
  *peer's* free/busy independent of the manager's calendar. If you leave the
  manager as required organizer, their focus-holds can hide real openings and you'll
  get "OrganizerUnavailable" for meetings they aren't even in.
- The hire's own calendar usually isn't readable pre-start (personal email / not
  provisioned) — rely on their stated working window for their side.
- To confirm a *specific* slot, set the window to exactly that slot; a returned
  "free @100" both confirms availability and validates the email resolves.
- Re-verify at the **final** times right before sending — the manager may have
  shifted times, and calendars change.

## Sending invites

Tool: `create_or_update_event` (title, start, end, **timezone** IANA e.g.
`America/Los_Angeles`, attendees[], description, conference, recurrence). Notes:
- Pass RFC3339 with the correct offset (`2026-07-14T11:00:00-07:00`) **and**
  `timezone: America/Los_Angeles` — unambiguous for every attendee's zone.
- `conference: true` adds a Teams link — do this; the hire is likely remote.
- The event is organized by the **authed account** (the manager). You generally
  can't create on the hire's behalf pre-start, so the manager organizes the
  meet-and-greets. If the manager wants a specific one *off* their calendar
  (e.g., "have them meet X on their own"), don't auto-create it — leave it for the
  hire to book and say so.
- Recurring shadow with varied per-day times → one event per weekday pattern, e.g.
  `RRULE:FREQ=WEEKLY;BYDAY=MO,TH;COUNT=4`, `…BYDAY=TU;COUNT=2`, `…BYDAY=WE;COUNT=2`.
  Pick each day's time from real availability; a day whose morning is blocked (a
  team meeting, the committee) can take an afternoon slot — "daily" beats "same time."
- Give each invite a clear title and a description that tells both people what to
  cover and what to prepare.

## What the manager still has to do (report this)

- **Add the hire to recurring meetings the manager doesn't organize** (all-hands,
  another team's sync, the CS team meeting) — you can't add attendees to those.
- Meetings deliberately **left for the hire to self-book** (later-week intros, the
  governance committee) — confirm the "People to Meet" checklist covers them.
- Any page fixes you couldn't make because images are already in (see gotchas.md).

## Credentials (if asked to compile a team-password doc)

Team logins (e.g., PACER) may live in Teams — `chat_message_search` finds them.
Put them in an **access-restricted** location (OneDrive shared to the team only),
never a broad channel; recommend a password manager. **Do not echo secrets into
chat.** Note that the local file-create tool may target Google Drive, not OneDrive —
build the doc locally and hand it to the manager to place, rather than uploading a
team credential to a personal cloud.
