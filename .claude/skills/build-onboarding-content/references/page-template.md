# Page anatomy — the HFD onboarding house standard

Every onboarding plan follows this spine. Keep the emoji headers and the warm,
first-person-from-the-manager voice. Times use the house PST convention (add the
hire's zone in parentheses if they're elsewhere). Reproduce these sections in order.

## Main page

1. **`## 👋 Hi, <Name>!`** — welcome, one-line role statement, a personalized line
   from their background, and who their manager is. Follow with an info panel:
   `📸 Manager — before publishing: drag the Welcome banner, EPIC graphic, and Org
   Chart images from <exemplar>'s page` (media can't be copied via API).
2. **Quick Links & Tools** — Technical Support Portal, Teams/Outlook, SharePoint
   ("HFD Hub"), Confluence, ClickUp, HubSpot, the **Legal Folder** (contracts +
   DD), and any role tool (e.g., Themis for compliance). Bold the ones they'll live in.
3. **People Stuff – Wellness** — Paylocity (Company ID 163665), Employee Navigator,
   Anthem/Kaiser/Sunlife, EAP (guidanceresources.com), Calm, AWC watercoolers.
4. **`## 🧭 HFD Purpose, Mission, Values`** — EPIC graphic placeholder + the EPIC
   line: **E**xcellence · **P**assionate · **I**nnovative · **C**ollaboration.
5. **`## 🎯 How to make the BEST of your first 2 weeks`** — be a sponge / invest in
   relationships / don't be afraid to ask. Add a role-specific line (for risk roles:
   "when in doubt, escalate — never guess").
6. **`## 👥 Who's Who — Org Chart`** — image placeholder.
7. **`## 🤝 Meet your team`** — a small table of the **actual team only** (manager +
   direct teammates). Everyone else belongs in "People to Meet," not here — don't
   group the whole department as "your team."
8. **`## 🌱 Week 1 (dates)`** — a `data-layout="wide"` 5-column Mon–Fri table.
   Each cell: bolded time (both zones if cross-tz), the meeting, one line of
   context, and a **`👉 follow-up`** ask ("comment one thing that surprised you").
   Mark role-critical meetings with ⭐. Include a daily check-in and a "how's it
   going" prompt. Leave HR/IT/BAI setup as "via <HR contact>" if not yet scheduled.
9. **`## ✅ Week 1 Tasks`** (right under the Week-1 grid) — a task-list checklist,
   plus a **`## 🤝 People to Meet`** task-list: prioritized, with a panel noting
   "spread these over your first 3–4 weeks, don't cram week 1"; mark already-booked
   ones ✓. Include a short "who to escalate to / who to ask for X" box.
10. **`## 🌱 Weeks 2 & 3`** — the scaffolded training (see below).
11. **`## 🕐 Working Across Time Zones`** (if the hire is remote in another zone) —
    a contacts table (person · go to them for… · online PT · online CT) ordered by
    who's online earliest for the hire, an "early-morning tip," and any governance
    body's meeting cadence.
12. **`## 📚 Deep-Dive Resources`** — links to the child pages (Reference Library,
    Business Scavenger Hunt, role Scavenger Hunt).
13. **`## 📖 JARGON! Read me, Read me!`** — the shared 3-column jargon table
    (Term · Description · Used in a sentence). Copy from Matt's page `4178378753`;
    role-specific terms go in the Reference Library instead.
14. **Framework break** — e.g., "Understanding RICs and BaaS" as a two-column
    layout; tie it to why the role matters.
15. **`## 💬 Microsoft Teams Tips`** and any closing.

## Weeks 2–3 scaffold (gradual release)

Intro the "I do → we do → you do" model. A daily-rhythm panel (daily check-in →
morning shadow → midday do-together → afternoon Q&A + read the matching Reference
Library entry). Two week tables mapping each day to one part of the real process;
Week 2 is "we do," Week 3 tapers to solo + a **Competency Checklist** (task-list)
the trainer signs off. If there's a standing daily shadow, state its booked times
and book it (calendar reference).

## Child pages (created with `parentId` = the main page id)

- **Reference Library** — collapsible `<details>` entries, one per concept, each
  answering *what it is · why it matters for this role · where you check it*.
  ADHD-friendly: short, plain, no jargon-without-a-gloss.
- **Business Scavenger Hunt** — learn the product/business by doing (submit test
  applications, find a provider in the ops portal, a contract in Legal, a report in
  Tableau/SSRS). "Comment your answer" per item.
- **Role Scavenger Hunt** — the deep craft, grounded in a **real** artifact: read
  a real report → make the judgment calls → run the tools → complete a mock packet.
  Point to sensitive source docs in SharePoint rather than pasting PII onto the wiki.
- Both hunts: cross-link each other + the Library, and include a **tiered
  comment-reward promise** (leave the actual rewards for the manager).

## Snippets

Reward promise:
```html
<div data-type="panel-success"><p>🎁 <strong>Comment rewards:</strong> 25 comments → …;
100 → …; 150 → … <em>(Manager: set the actual rewards.)</em></p></div>
```
Reference-library entry:
```html
<details><summary><strong>What is an NPI?</strong></summary>
<p>A 10-digit ID for a healthcare provider…</p>
<p><strong>Why it matters for DD:</strong> …</p>
<p><strong>Where you check it:</strong> …</p></details>
```
