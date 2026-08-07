---
name: hfd-hiring-deck
description: Build or update HFD's hiring intro deck for a specific open role. Use when the user asks to create a hiring presentation, candidate deck, or interview intro deck for a new HFD role (e.g. "make a hiring deck for the X role", "copy the deck for Y role", "update the hiring presentation"). Also use when modifying any slide in an existing HFD hiring deck — the skill encodes which slides are evergreen vs role-specific and what to swap when the role changes.
---

# HFD Hiring Deck

Edward's hiring intro deck. Twenty slides that walk a candidate from "what is HFD" → "what's this team" → "what is this specific role". The skill captures which slides are evergreen, which must be re-thought per role, and the specific traps to avoid when porting the deck to a new role.

## When to use this skill

- Asked to **build a new hiring deck** for a specific role
- Asked to **copy the deck to a new role** (Senior Growth Analyst → Provider Due Diligence Specialist, etc.)
- Asked to **update slides in a hiring deck** — even just one — because the per-role context matters
- Reviewing a hiring deck for tone/audience fit

If the user says "make a hiring deck for [role]", load this skill before doing anything else. It saves a full revision cycle.

## Deck structure — what each slide does

The deck lives at `C:\Users\esmith\temp\Hiring Presentation - Senior Growth Analyst\` (the path the user opens it from). The original Beautiful.ai export of slides 1–11 is mostly **images** baked into the slide — they must be rebuilt as native pptx shapes when edited. Slides 13–20 are native.

| Slide | Title | Status per role | What to do |
|---|---|---|---|
| 1 | Who we are | Evergreen | Don't touch |
| 2 | Our EPIC Values | Evergreen | Don't touch |
| 3 | Our purpose | Evergreen | Don't touch |
| 4 | Our vision | Evergreen | Don't touch |
| 5 | Our mission | Evergreen | Don't touch |
| 6 | Provider stats (Invisalign, etc.) | Evergreen | Don't touch |
| 7 | How we do it | Evergreen | Don't touch |
| 8 | HFD At Its Core | Evergreen | Don't touch |
| 9 | Cash Up Front | Semi-evergreen | Keep — describes HFD's business |
| 10 | Cash Over Time | Semi-evergreen | Keep — describes HFD's business |
| 11 | Integrated Pay Over Time | Semi-evergreen | Keep — describes HFD's business |
| 12 | Funds Flow | Semi-evergreen | Keep — describes HFD's business |
| **13** | **Section divider: "[Department] at HFD"** | **Role-specific** | Update department name (Analytics/Operations/etc.) |
| **14** | **About Me** | **Role-specific tone** | Update Edward's intro framing — analyst flavor for analyst roles, ops flavor for ops roles |
| **15** | **Department Structure (org chart)** | **Role-specific** | Highlight THIS ROLE; mark other open roles as HIRING |
| **16** | **Supporting Revenue Growth** | **Role-specific** | Rewrite all four bullets in the candidate's language |
| **17** | **This Role Requires** | **Role-specific** | Rebuild from the JD — six pillars, plus left-panel framing |
| **18** | **Tools we use diagram** | **Role-specific** | Replace the tool set with what THIS role will actually touch |
| **19** | **A Day in this role** | **Role-specific** | Six tiles, sprint-cadence callout, tools band, "why this role matters" |
| 20 | Questions? | Evergreen | Don't touch |

## Role-specific rebuild checklist — read before touching slides 13–19

When porting the deck to a new role, run through every cell of this checklist BEFORE marking the work done. The default failure mode is leaving analyst-flavored content in non-analyst decks (or vice versa).

### Slide 13 — section divider
- [ ] Title matches the candidate's department, not the previous role's department.
- Analyst-track roles → "Revenue Analytics at HFD"
- Ops/RevOps roles → "Revenue Operations at HFD"

### Slide 14 — About Me
- [ ] Edward's identity line matches the candidate's frame of reference.
- Analyst-track candidate: "Data Scientist turned RevOps Leader And Analytics"
- Ops-track candidate: "RevOps Leader" (drop "Data Scientist turned" framing — it signals the wrong center of gravity to a non-analyst)
- Keep the personal lines (health journey, psychological-safety mission). Those are evergreen.

### Slide 15 — Org chart
- [ ] THIS ROLE is highlighted (accent-teal box) and placed in the correct reporting line.
- [ ] All currently-open roles show a `HIRING` tag — don't lose other openings just because you're focused on this one.
- [ ] Manager names current: **Hema** (Analytics Manager), **Tenae** (RevOps Manager). Edward is Director above both.
- [ ] Gustavo is **RevOps Team Lead** under Tenae. **Dimira, Cale, Candice, Tia** are RevOps Associates labeled "Reports to Gustavo" (offset to show nesting).
- [ ] **Matt Carnes** (Integrated Channel Analyst) reports **direct to Edward**, not to Hema.
- [ ] **Frederic** (Senior Financial Analyst) and **Lakshmi** (Operations Analyst) report to Hema.
- [ ] Direct-to-Edward column: Matt Carnes, Laura (Senior HubSpot Admin), Ashley (Senior Marketing Ops), Dulce (Pricing Associate), Dream (Technical PM).
- Reporting line for THIS ROLE — ask the user if unsure:
  - Analyst / data / growth roles → under Hema
  - Provider Due Diligence Specialist → direct to Tenae (peer to Gustavo, not under him)
  - Other RevOps ops roles → ask

### Slide 16 — Supporting Revenue Growth
- [ ] Every one of the four arrow bullets reframed for THIS candidate. **Common trap:** partial text-replace that leaves one bullet with analyst language ("actionable analytics", "deep dives", "Tableau heavy") in a non-analyst deck.
- Sales-team line: keep the count (~10 field reps, 2 AEs, 1 SDR) but reframe what they hand off:
  - Analyst role: "leads we measure and report on"
  - PDD role: "providers that land on your desk first"
  - Account exec role: ask
- Tableau / SQL line: only keep heavy-tool framing for roles that will actually use them daily. For non-analyst roles, soften to "you can dip in for trends."
- Tickets / projects line: HubSpot Ticketing + ClickUp is true for everyone — adapt the request type (reactive analytics requests vs reactive due-diligence requests vs etc.)
- "Actionable analytics vs deep dives" line: only keep verbatim for analytics roles. Rewrite for any other role.

### Slide 17 — This Role Requires
- [ ] Six pillars rebuilt straight from the JD's "you will" + "who you are" sections.
- [ ] Left dark panel headline reframed in the candidate's language ("You are the gatekeeper of quality" for PDD; "This role is the bridge between data and decisions" for analyst).
- [ ] Bottom callout is a memorable quote from the JD — what kind of person thrives here.
- [ ] Subtitle reads "From the [Role Title] job description" — make sure the role name matches.

### Slide 18 — Tools diagram
- [ ] **REBUILD the tool set for the role.** Don't leave the inherited tools from the previous role. This is the slide I most reliably miss.
- Tool sets by role family:
  - **Analyst / Growth** — SQL Server, Tableau, HubSpot, ClickUp, Python, PostHog, Datadog, Clay
  - **Provider Due Diligence** — HubSpot, State + Federal license databases, Excel, ClickUp, DocuSign, NPI Registry, NPPES, Secretary of State portals
  - **Marketing Ops** — HubSpot, Marketo / Customer.io, Tableau, Clay, KickBox, Sendoso
  - **Pricing** — HubSpot, Excel, SQL Server, Tableau, internal pricing models
- The original slide 18 has an analyst-heavy diagram (Spark Post, Clay, LogRocket, PostHog, KickBox, Sendoso, Aloware, FiveNine). For non-analyst roles this whole diagram needs to be **replaced**, not nudged.

### Slide 19 — A Day in this role
- [ ] Six tiles, each one a real activity from the JD.
- [ ] Subtitle ("Mornings on X. Afternoons on Y.") tailored to the role.
- [ ] **Sprint cadence tile present:** "We run on 2-week sprints" with committed points and the daily HubSpot rollup. **Avoid the word "burndown"** — it's tech jargon. Say "a live SharePoint dashboard" instead for non-tech roles.
- [ ] Tools band at the bottom matches slide 18.
- [ ] "Why this role matters" line pulled from the JD's "why this role matters" section if present, else written from the role's impact.

## Funding model terminology (slides 9–11) — keep these correct

When the user asks me to rebuild the funding slides, get these right:

| Channel | Slide title | What HFD calls it | Funding type | What it actually is |
|---|---|---|---|---|
| 1 | Cash Up Front | **Sale of Purchase (SAO)** | 10001 | Provider funded through HFD's Sale-of-Purchase program. **NOT "Sale of Account."** |
| 2 | Cash Over Time | **On balance sheet servicing** | 10000 | Loan HFD funds + services directly on our balance sheet. |
| 3 | Integrated Pay Over Time | **Lender aggregators inside the HFD platform** | n/a | Externally funded credit offers wired into HFD's flow. **Do not call them "partners" and do not mention the partner table** — call them lender aggregators. |

Section labels on slide 11: "Powered by Lender Aggregators", "What Aggregators Get", "Example Lender Aggregators".

## Org chart cheat sheet (canonical, as of 2026)

```
Edward Smith — Director of Analytics & RevOps
├── Hema — Analytics Manager
│   ├── Frederic — Senior Financial Analyst
│   ├── Lakshmi — Operations Analyst
│   └── (HIRING or THIS ROLE) — Senior Growth Strategy Analyst
├── Tenae — RevOps Manager
│   ├── (HIRING or THIS ROLE) — Provider Due Diligence Specialist (specialist IC, peer to Gustavo)
│   └── Gustavo — RevOps Team Lead
│       ├── Dimira — RevOps Associate (Reports to Gustavo)
│       ├── Cale — RevOps Associate (Reports to Gustavo)
│       ├── Candice — RevOps Associate (Reports to Gustavo)
│       └── Tia — RevOps Associate (Reports to Gustavo)
└── Direct to Edward
    ├── Matt Carnes — Integrated Channel Analyst
    ├── Laura — Senior HubSpot Admin
    ├── Ashley — Senior Marketing Ops
    ├── Dulce — Pricing Associate
    └── Dream — Technical PM
```

Names that are nicknames or have changed:
- "Bel" is **Tia** — always use Tia
- "Rina" is no longer on the team — replaced by Matt Carnes
- Always ask Edward where a new role reports if not obvious from the role family table above

## Visual system

The deck uses a fixed palette. Don't invent new colors.

| Variable | Hex | Usage |
|---|---|---|
| HFD_BLUE | `0145F1` | Primary accent — managers, accent bars, badges |
| HFD_DARK | `0A1A40` | Dark panels, director box, hero callouts |
| HFD_LIGHT_BG | `F5F7FB` | Card backgrounds |
| HFD_ICE | `E3ECFE` | Soft-accent boxes — IC nodes, partner chips |
| ACCENT_TEAL | `1CB0A8` | "THIS ROLE" highlight, "How it works" step numbers |
| WHITE | `FFFFFF` | Body backgrounds, text on dark panels |
| DARK_TEXT | `101628` | Body text |
| GREY | `555E6E` | Caption / secondary text |

Fonts: **Poppins** for headers and body. (Poppins.zip ships in the deck folder; the user has it installed.)

Slide canvas: 12,192,000 × 6,858,000 EMU (13.33in × 7.5in, widescreen).

**Never use emoji** as iconography — Poppins doesn't include emoji glyphs and they render as `□` placeholders in PowerPoint and PDF. Use numbered circles (`01`, `02`, ...) or small text badges instead.

## Build pattern

The PDD deck was built by copying the Senior Growth deck and editing six slides. Use the same pattern:

1. Copy the most recent role's deck as the starting point: `shutil.copy("Senior Growth Strategy Analyst at HFD.pptx", "<New Role> at HFD.pptx")`.
2. Open with python-pptx.
3. For each role-specific slide, `clear_shapes(slide)` then build fresh shapes (or surgically edit native text where applicable — slides 14, 16, 13 can be text-edited; 15, 17, 18, 19 should be cleared + rebuilt).
4. Save.
5. Convert to PDF with `soffice --headless --convert-to pdf` and render slides 13–19 to JPG with `pdftoppm -jpeg -r 110`.
6. Read every rendered slide before declaring success. **Look specifically for inherited language** from the previous role.

Reusable helpers (color constants, `add_round_rect`, `add_text`, `add_circle_number`, `clear_shapes`, `set_solid_bg`) live in `build.py` in the project folder. Import them rather than redefining.

## Common pitfalls (the ones I've actually hit)

1. **Partial text replacement on slide 16** — three of four bullets get reframed and the fourth keeps the previous role's flavor. Fix: rebuild slide 16 from scratch rather than text-replacing, OR verify each bullet visually after rendering.
2. **Forgetting slide 18 entirely** — the tools diagram is the most-skipped slide because it's not in the "obvious" rewrite path (15/17/19). Add it to the checklist explicitly.
3. **Leaving analyst-track About Me** — slide 14's title and bullets need to be re-pointed for non-analyst roles.
4. **Using emoji for icons** — they don't render. Use numbered badges (`01`/`02`/...) in circles.
5. **Calling Bel "Bel"** — always Tia.
6. **Putting Matt Carnes under Hema** — he reports directly to Edward.
7. **Calling channel 1 "Sale of Account"** — it's "Sale of Purchase."
8. **Mentioning "the partner table" on slide 11** — call them lender aggregators, no partner-table reference.
9. **Saying "burndown"** to non-tech candidates on slide 19 — call it a live SharePoint dashboard.
10. **Stale logos / providers on slides 9–11** — when the warehouse is reachable, pull current SAO providers (fundingtype 10001), on-balance-sheet providers (fundingtype 10000), and lender aggregators from the partner table for fresh examples.

## Verification loop

Before saving the deck to the user's folder:

1. Render every role-specific slide (13–19) to JPG.
2. Read each image and ask: "If I were a candidate for THIS role, would every word on this slide make sense to me?"
3. Specifically scan for: tools the candidate won't use, jargon from the previous role family, the name "Bel", references to "Sale of Account" or "the partner table", emoji placeholder squares.
4. Fix anything that doesn't pass the candidate-eye test before handing back.

## Saving + handoff

Save to the user's connected folder:
`C:\Users\esmith\temp\Hiring Presentation - Senior Growth Analyst\<Role Title> at HFD.pptx`

Use `mcp__cowork__present_files` so the user gets a clickable card.
