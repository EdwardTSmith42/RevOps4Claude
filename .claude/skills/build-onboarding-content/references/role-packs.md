# Role packs

The house template (page-template.md) is role-agnostic. What makes an onboarding
genuinely useful is the **role-specific pack**: the jargon, the reference-library
topics, the scavenger-hunt spine, and — crucially — the **real work artifacts** it
points at. Below is the Provider Due Diligence pack, worked in full, followed by a
recipe for building a pack for any other role.

## Provider Due Diligence Specialist (worked example)

**What the job is:** the gate that decides which providers HFD can safely fund.
KYB (Know Your **Business**) on each provider before the bank partner (Hatch) will
fund them. Weak DD is what caused the Hatch compliance escalation, so the role is
mission-critical.

**Real artifacts to read (SharePoint) — ground everything in these:**
- Master checklist: **Compliance → BSA AML → Provider DD Testing** ("Provider DD
  Checklist"). Sections: Provider info · Ownership verification (intake name vs
  LexisNexis) · KYB/background (LexisNexis SmartLinx + Small Business Credit Score)
  · Expected activity · OFAC/sanctions · Licensing/incorporation · Exceptions ·
  Internal review (log in **Themis**) · **Approval Blockers (hard stops)**.
- Completed reports: **RevOps → Due Diligence (Greenbrier)** → per-provider folders
  → a Middesk/Cobalt-style "Business Record" PDF (SOS good-standing, TIN/IRS match,
  NPI, watchlist/OFAC, bankruptcies, UCC liens, litigations, criminal, address/web
  verification, each line tagged SUCCESS/WARNING/FAILURE). Use one as the worked
  case in the scavenger hunt — but point to it in SharePoint, don't paste a named
  person's records onto the wiki.
- Restricted industries: "BSA NAICS Restricted" list.
- Signed contracts (not the DD research): the manager's OneDrive "Provider
  Contracts" folder.

**Reference Library topics** (one `<details>` each): NPI/NPPES · Secretary of State
& "good standing" · TIN/EIN & IRS match · KYB vs KYC vs CIP · Beneficial ownership
/ BOI ≥25% (definition only — confirm whether the team actually performs a BO
*check* before making it a task) · OFAC & the SDN list · adverse media · PACER &
federal court records · **bankruptcies & the chapters (7 liquidation / 11 business
reorg / 13 individual reorg)** · UCC liens (open vs closed, secured party, lapse) ·
litigation & judgments · criminal records (fraud/financial-crime are the hard stops)
· LexisNexis SmartLinx & Small Business Credit Score · watchlist/PEP · NAICS/SIC &
BSA/AML restricted industries · Themis · how to read the Business Record · the hard
stops. Plus a quick acronym glossary.

**Business Scavenger Hunt spine:** provider journey (enroll→activate→originate→fund
and where DD sits) · submit test applications (get test SSNs/cards + a safe test
provider from the RevOps lead) · find your way around Ops/ELI, the Legal contracts
folder, HubSpot DD queue + Tableau dashboard · understand RIC vs BaaS and why the
role matters.

**DD Scavenger Hunt spine:** (A) read the real Business Record and find each result
· (B) make the judgment calls — which findings are hard stops vs document-and-proceed
· (C) run the tools yourself (NPPES, state SOS, OFAC scan, PACER orientation,
NAICS check) · (D) capstone: complete a full mock packet and walk a trainer through it.

**Trainers/attendees:** the DD teammates (peers in the same role) run the daily
shadow; Compliance covers the compliance role + the bank partner; the manager owns
priorities/escalation. **Confirm current org state** — who trains what shifts often.

**Governance:** the Due Diligence Approval Committee (functions as the credit
committee) approves providers; knowing its cadence helps the hire time when packets
must be ready.

## Recipe: build a pack for a new role

1. **Find the closest prior onboarding page** and read it for the jargon and the
   scavenger-hunt style.
2. **Find the role's real process doc + a real output** (an SOP, a checklist, a
   completed deliverable). SharePoint search on the role's key nouns finds these;
   the process doc becomes the training spine and the output becomes the scavenger
   hunt's worked case. Ground the reference library in the terms that actually
   appear in those artifacts — that's what makes it real instead of generic.
3. **List the "what is X?" terms** a newcomer to that role hits in the artifacts →
   those become Reference Library entries (what it is / why it matters here / where
   to check).
4. **Verify with the manager** which steps the team *actually* performs — SOPs are
   sometimes target-state, not live. Don't turn an aspirational step into a task.
5. Reuse the house template for everything else.
