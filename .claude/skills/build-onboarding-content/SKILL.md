---
name: build-onboarding-content
description: >-
  Build a new-hire onboarding plan for HFD in Confluence — matching the house
  template, personalized to the role, with a day-by-day Week-1 schedule, a
  scaffolded Weeks 2–3 training plan, scavenger hunts, a plain-English role
  reference library, and (on approval) the actual calendar invites. Use this
  WHENEVER someone is onboarding a new employee or contractor: "make an
  onboarding plan/page/doc", "onboard <name>", "welcome page for the new hire",
  "ramp plan", "first-week schedule", "training plan", "new-hire scavenger
  hunt", or when copying/adapting an existing onboarding page for a new person
  or role. Also use for pieces of the job — just the Week-1 calendar, just a
  scavenger hunt, just the who-to-meet plan. Trigger even if they don't say the
  word "Confluence" or "template" — HFD onboarding lives on Confluence and
  follows one house standard, and this skill encodes it plus the traps
  (images-last, surgical edits, real availability checks).
metadata:
  type: project
---

# Build onboarding content (HFD)

You are helping a manager stand up a new hire's onboarding. The deliverable is a
set of **Confluence pages** in the house style, plus **calendar invites** once
the manager approves. This skill encodes what the house standard looks like,
where the source material lives, how to personalize it, and the specific traps
that will bite you if you don't know them.

Read the four reference files when you reach the step that needs them:
- `references/page-template.md` — the exact section-by-section page anatomy + HTML+ snippets.
- `references/role-packs.md` — role-specific content (the Provider Due Diligence pack is worked in full; use it as the model for any role).
- `references/calendar-invites.md` — availability-checking and invite-sending playbook (timezones, tools, recurrence).
- `references/gotchas.md` — the failure modes. **Read this before your first page edit.**

## Where HFD onboarding lives (canonical facts)

- **Space:** the personal Confluence space keyed `~5fc7eb89f2df6c0076e3282b`
  (display name "Suzanne Zubris"), numeric **spaceId `2344845349`**. Every
  onboarding plan is created here as a page; deep-dive companions are child pages.
- **Exemplars to copy the standard from** (cloudId `healthcarefinancedirect.atlassian.net`):
  - Same-role match matters most — find a prior hire in the **same or closest role** and mirror it.
  - Provider Due Diligence Specialist: Lindsey Blackwell `4178477057`, Tatiana Cleveland `4211146753`.
  - Integration/analytics roles: Matthew Carnes `4178378753` (the fullest **jargon table** + the scavenger-hunt model), Himanshu Jain `4533977091`.
- **Tools:** Confluence via the Atlassian MCP (`getConfluencePage`, `createConfluencePage`,
  `updateConfluencePage`); SharePoint/Outlook via the M365 connector; calendar
  invites via a create-event tool (see `references/calendar-invites.md`).

## The process

Work in five phases. Do not skip the study phase — the whole point is that the
result reads like the manager's own prior onboarding pages, not a generic AI draft.

### 1. Study (be a student first)

- Fetch 2–3 exemplar pages (the same-role one + Matt's for jargon). If a page is
  too large for one tool result, have a subagent extract it so the bulk stays out
  of your context.
- For a specialized role, read the **real work artifacts** so the content is
  grounded, not invented. For due diligence that means the actual checklist and a
  completed report (see `references/role-packs.md`). Grounding is what makes the
  scavenger hunts and reference library genuinely useful.
- Read the new hire's **resume/cover letter** if provided (often dropped in
  `~/Downloads`) so you can personalize the welcome and calibrate depth.

### 2. Design & confirm (pace the manager)

Propose the shape, then ask only the **genuinely blocking** questions — a handful,
not twenty. The ones that actually gate the work:
- **Start date** (the spine of the Week-1 calendar).
- **The hire's work email** (to check availability and send invites).
- **The hire's time zone / working hours** (adjust the schedule and add a
  cross-timezone "who to contact & when" guide; see below).
- **Who manages/trains them** and who runs any daily training — org state drifts
  (people go on leave, change roles), so confirm rather than assume from an old page.
- **Booking mode** — almost always: build the page first, manager reviews/edits,
  then you send invites. Real invites to colleagues are outward-facing; get a clear
  go-ahead before sending.

### 3. Build (incrementally, surgically)

- Create the main page, then add sections. **Every edit after the first must
  fetch the live page and change only the target region** — never regenerate the
  whole body from your own copy, or you will clobber the manager's manual edits
  and (fatally) their uploaded images. See `references/gotchas.md`.
- Put the big companions on **child pages** and link them from the main page:
  a **role Reference Library** (plain-English "what is X" explainers), a
  **Business Scavenger Hunt** (learn the product by doing), and a **role-specific
  Scavenger Hunt** (the deep craft, grounded in real artifacts).
- Follow `references/page-template.md` for the exact sections and HTML+ syntax.

### 4. Review

Run a read-only pass (a subagent is good for this) across all pages for: stale
names/roles, times that don't add up, PT/CT mismatches, missing links, and gaps a
brand-new hire would hit (who to escalate to, how to get test credentials/tool
access). Fix via **surgical** edits only. Flag anything you can't safely fix
(e.g., after images are in) for the manager to do manually.

### 5. Invites (only on the manager's explicit "send"/"publish")

Follow `references/calendar-invites.md`. In short: pull the **final times from the
page** (the manager may have corrected them), **re-verify each attendee is
actually free at those exact times**, then send with a Teams link. Report what you
sent and what the manager still needs to do (add the hire to recurring meetings
they don't own; any meetings deliberately left for the hire to self-book).

## Personalization & time zones

- Weave one or two specifics from the resume into the welcome ("you're set up to
  crush this because…"). Keep it warm and true, never fawning.
- If the hire is in a **different time zone** from HQ, keep meeting times in the
  house convention but show **both** zones on every time, and add a
  **"Working Across Time Zones — who to reach & when"** table ordered by who comes
  online earliest for them. Use *confirmed* working hours where you have them and
  say so; don't fabricate precise hours for people you haven't checked.

## Scaffolded training (Weeks 2–3)

Model the core training as **gradual release — "I do → we do → you do"**: shadow →
supervised reps → run it solo with the trainer watching → solo. Map each day to one
part of the real process, end with a **competency checklist** the trainer signs
off, and if there's a standing daily shadow, book it (see calendar reference).

## Voice & principles

- Write in the **manager's first-person voice** — warm, direct, ADHD-aware (one
  clear "start here" per day; a daily comment habit; a specific follow-up ask
  attached to each meeting). No AI attribution anywhere.
- Reward-the-comments promise: include a tiered comment reward on the hunts; leave
  the actual rewards for the manager to set.
- **When in doubt on anything outward-facing (sending invites, publishing), ask.**

## Optional: harden this skill

This skill was written from a single real build. To pressure-test it, the
skill-creator flow can run it against a couple of fresh onboarding prompts and
diff the output — offer that if the manager wants to improve it further.
