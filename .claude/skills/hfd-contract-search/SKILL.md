---
name: hfd-contract-search
description: >-
  Find what provider contract HFD actually has on file and decide what it permits: can this provider be
  switched to BankLoan as-is, or does someone need to sign new paper first. Use when converting providers
  from RIC to BankLoan, when a parent adds locations, on ownership changes, on integration switches, or for
  any "does this provider need a new contract?" question, including auditing which locations in a parent tree
  are covered. Trigger on "contract search", "does this provider need a contract", "RIC to bank loan",
  "switch to bankloan", "is there a DSO agreement", "joinder", "DSO template", "what contract did they sign",
  "contract requirements SOP", or a list of providers to convert. Works with no database access - it reads
  SharePoint contract folders, the personal OneDrive contract folder, HubSpot for legal names, and Tableau for
  hierarchy. Do NOT trigger for pricing or program-code work (use hfd-pricing-change).
---

# HFD Contract Search

Answers one question per provider: **does the paper we already hold authorise what we want to do, or does someone have to sign something?**

The answer is never "look at the provider's current configuration." A provider's financial instrument in ELI, Tableau, or HubSpot's `ric_baas` describes how the account is *set up today*. It says nothing about which agreement was *signed*. Only the executed document is evidence.

## The two-axis test

Every HFD provider agreement encodes two independent facts. **Both must pass.** This is the whole skill.

**Axis 1 - INSTRUMENT.** What money product is authorised: bank loan, RIC, or both.

**Axis 2 - ENTITY SCOPE.** How many locations the signature binds: one entity, or an umbrella over a group.

A bank-loan agreement with single-practice scope authorises bank loan *for the signing entity only*. Its sibling locations are not covered and cannot be switched on the strength of it. This is the single most common wrong answer, and the one that costs the most when you get it wrong in either direction.

Read `references/contract-taxonomy.md` for the token lists on both axes, the naming variants across eras, and how to read a document whose filename carries no type. Do not work from memory here - the naming has drifted repeatedly and the reference is canonical.

## Procedure

1. **Resolve the signing entity, not the location.** Contracts are signed by legal entities. Group the input list by parent, then work per entity. A list of 76 locations is usually fewer than 20 real signature decisions, and that collapse is where all the leverage is.

2. **Resolve the Legal Name.** Contract folders are filed by Legal Name, and your input almost certainly has Practice Name. Neither Tableau datasource exposes `legalname` at all. Get it from HubSpot. See `references/lookup-paths.md`.

3. **Search every repository, and gather ALL candidate folders before judging any of them.** There is more than one contract store and more than one folder per entity. Never stop at the first name match - see the gotchas below.

4. **Classify each executed document on both axes**, using the filename where it carries a type and full-text search where it does not.

5. **Decide, per entity, then propagate to its locations.** An umbrella covers the children; single-practice scope does not.

6. **Report evidence, not just verdicts.** Every row carries the folder path and the filename it was decided from, so a human can check the reasoning in one click.

## Evidence repositories - check all of them

| Order | Where | Shape | Who can reach it |
|---|---|---|---|
| 1 | SharePoint > Legal > Shared Documents > **Provider and Merchant Contracts** | A-Z letter folders by Legal Name; each provider folder has `Contracts Executed` | Anyone with Legal site access |
| 2 | **A `Provider Contracts` folder on an individual's OneDrive** | Flat list by Legal Name. Legal's library lags, so recent contracts land here first | **Only the owner, plus whoever it is shared with** |
| 3 | HubSpot | Legal-name resolution and identity only. Holds no usable contract-instance data | Anyone with HubSpot access |

Exact paths, REST recipes, and field names are in `references/lookup-paths.md`.

**Checking only repository 1 produces mass false negatives.** In the RIC-low-cap run, 35 of 51 entities had an empty `Contracts Executed` in Legal; 28 of them had real executed bank-loan agreements sitting in repository 2. Stopping at Legal would have raised roughly 28 unnecessary contract requests.

### Repository 2 is not a shared system - resolve it per operator

Repository 2 is a **personal** OneDrive folder, not an org location. As of September 2026 the known copy belongs to **Ed Smith (esmith@gohfd.com)**, at `OneDrive > Provider Contracts`. Do not assume the path, the owner, or that you have access.

At the start of a run, establish which of these you are in:

1. **You own the folder.** Use it directly.
2. **It is shared with you.** It appears under OneDrive > Shared, or as a shortcut you have added to your own OneDrive. Either way you must resolve its real drive id - see `references/lookup-paths.md`.
3. **You cannot reach it.** Say so explicitly in the output. Run repositories 1 and 3, and mark everything they cannot settle as `VERIFY` with the reason "second contract repository not accessible to this operator". **Do not silently downgrade those rows to `NEEDS_NEW_CONTRACT`** - that is precisely the error that generates contract requests to providers who already signed.

Ask the operator early rather than guessing: *"Do you have access to a personal `Provider Contracts` OneDrive folder, or a share of one? Without it I can confirm far fewer providers."*

**This is a standing fragility worth naming when it bites.** A contract repository that lives on one person's personal drive is a single point of failure for the whole team, and any run by a different operator is systematically less complete. The durable fix is moving that content into the Legal library or a shared SharePoint site; until then, this skill's coverage varies by who runs it, and the output should say which repositories were actually searched.

## Decision outcomes

| Verdict | Meaning |
|---|---|
| `SWITCH_ONLY` | Bank-loan authorisation covers this location. Convert per the Converting an Account To Bank Loan SOP; no signature needed. |
| `NEEDS_NEW_CONTRACT` | No bank-loan authorisation covers this location. Needs a Bank Loan agreement, a DSO agreement, or a Joinder. |
| `CHILDREN_NEED_PAPER` | The entity itself is covered but its locations are not, because scope is single-practice. |
| `VERIFY` | Undetermined. **Never collapse this into "needs a contract."** |

`VERIFY` is a real outcome, not a failure. Filing lags, a contract may sit in a repository you cannot reach, and the SOP treats a HubSpot copy as equally valid. Reporting "not found, verify" is correct and useful; guessing "needs signature" manufactures work and annoys providers who already signed.

The full SOP branch logic - new locations, ownership changes, integration switches, EIN and PLLC non-rules - is in `references/decision-rules.md`.

## Gotchas that change answers

Each of these produced a wrong answer during the build of this skill, and each is cheap to defend against.

1. **Loose token matching invents contracts.** Matching on a name subset pulls in *other providers'* documents and classifies them as this provider's. Require the legal name to match, and flag anything weaker instead of accepting it.

2. **"Best name match wins" loses real contracts.** The same entity is often filed twice - once under Legal Name, once under DBA - and the better-matching folder is frequently the empty stub. Sono Bello's real bank-loan agreement sits under `B/Body Contour Centers, LLC dba Sono Bello` while `S/Sono Bello` is an empty shell. **Gather every candidate, fetch evidence from each separately, then prefer the one holding documents.**

3. **Multiple folders need opposite treatment.** Several folders for the *same* company (LPT Medical had three) means union the evidence. Several folders for *different* companies that share a name (three distinct "Dentistry by Design" entities) means flag and confirm - never merge. Decide which case you are in before combining anything.

4. **A near-name match is not a match.** "Preferred Dental PC" matched a folder called "Preferred Dental Care" holding no contract. Different provider.

5. **Empty folder is not evidence of absence.** See the repositories table above.

6. **A group can be covered without an umbrella.** Enamel Dentistry has no DSO agreement, but each location signed its own bank-loan agreement under its own entity. Check per-location folders before calling the children uncovered.

7. **Search does not index a personal OneDrive.** A search miss proves nothing about repository 2; enumerate it directly. Verified by control test. And if you had no access to repository 2 at all, say so in the output rather than reporting a confident-looking result built on one repository.

8. **Folder naming is `<Legal Name> dba <Practice Name>`.** Because the DBA is often present, Practice Name frequently matches too - so search on both, and treat a Practice-Name-only match as weaker evidence.

## Output

A decision table, one row per provider location, plus a by-entity view. Minimum columns:

`provider id | practice name | legal name | parent id | parent name | current instrument | DECISION | why | folder path (evidence) | contract file(s) found | folder match quality`

Group the by-entity view by signing entity - that is the list of contracts someone actually has to send, and it is always far shorter than the location list.

Always state the counts for each verdict, and always surface how many rows are `VERIFY` and why. A run that reports only the confident rows is hiding its own error bar.

**Record which repositories were actually searched, and by whom.** Coverage depends on the operator's access to repository 2, so a result is only interpretable alongside that fact. A reader who does not know repository 2 was skipped will read `VERIFY` as "no contract exists" - the exact misreading this skill is built to prevent.

## Reference Files

- `references/contract-taxonomy.md` - **Read before classifying any document.** Instrument and scope tokens, every naming variant by era, and how to type a document whose filename does not.
- `references/lookup-paths.md` - Exact repository paths, SharePoint REST and search recipes, HubSpot properties, Tableau datasource LUIDs and field captions.
- `references/decision-rules.md` - The full Contract Requirements SOP branch logic and the date boundaries.
