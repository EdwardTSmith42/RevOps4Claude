# Decision rules - the Contract Requirements SOP, as branch logic

Source: HFD Procedure Manual > Revenue Manual > Revenue Operations > Onboarding > **Contract Requirements**
(ClickUp doc `h5m23-40053`, page `h5m23-44593`), plus **Converting an Account To Bank Loan** (page `h5m23-25193`).

The goal of all of it is to minimise risk to HFD. When a case is genuinely unclear, Legal or Compliance (Terri Persinger) decides - not the operator, and not this skill.

## Branch A - converting an existing provider to bank loan

The question this skill exists for.

```
Does bank-loan authorisation cover THIS location?

 ├─ This provider's own folder holds a bank-loan or combined agreement
 │     └─ SWITCH_ONLY
 │
 ├─ No, but a parent or sibling entity holds one
 │     ├─ scope is DSO / umbrella, signed on or after April 2024  -> SWITCH_ONLY
 │     ├─ scope is single-practice or multi-practice not naming
 │     │  this location                                            -> NEEDS_NEW_CONTRACT
 │     └─ signed before April 2024                                 -> NEEDS_NEW_CONTRACT or Joinder
 │
 ├─ Only RIC paper found anywhere in the entity                     -> NEEDS_NEW_CONTRACT
 │
 └─ Nothing found, or the document's type cannot be established     -> VERIFY
```

After a `SWITCH_ONLY` decision, the conversion itself follows the Converting an Account To Bank Loan SOP:

1. Configure the account from the account-to-copy (Company ID field). It defaults to RIC.
2. If the parent is set to bank loan, the Provider Settings tab needs no change - but check the account anyway.
3. If the parent is not bank loan, set Provider Settings to `BankLoanDefault`.
4. **V3 accounts: do not touch Provider Settings.** That tab drives workflow, and full integrations do not land on the platform during originations.
5. Raise a ticket for Charles Anderson or Fred Wong to change the financial instrument and risk pipeline, then post it in the "Finance Offer Configs" Teams chat. Risk pipelines vary - see the Risk Pipelines Per Flow doc.
6. ONEderful only: record the transition date in the Affordable Care onboarding sheet.

Note the distinction: **parent set to bank loan is a configuration fact and does not mean a bank-loan contract was signed.** Step 2 is about config inheritance, not authorisation. Never let it substitute for contract evidence.

## Branch B - a parent adding new locations

- Contract signed **on or after April 2024 using the DSO_Management template** -> onboard with no new contract, indefinitely, however long after the original. Legal has confirmed non-DSOs may use the DSO form with no risk to HFD.
- Contract signed **before April 2024** -> each location needs its own contract, or a **Joinder Agreement** covering multiple locations.
- A location that signs a DSO agreement creates the umbrella for its siblings. The signer need not be the parent.

## Branch C - things that do NOT require a new contract

- **Duplicate EINs.** Multiple locations may share one EIN. Per Legal: the EIN identifies employer tax accounts and has no bearing on contracts. HFD does not require an EIN from providers; due diligence requires an active corporate entity in good standing.
- **PLLC or any other entity type.** A PLLC is just a flavour of LLC. HFD Legal requires one agreement per corporate entity - not several per entity, and not a different count by entity type.

## Branch D - ownership changes (sometimes)

- If an umbrella agreement is in place (DSO_Management, or any partner agreement), **no ownership-change form is needed**. EIN, point of contact and banking details can be updated within the same corporate structure.
- A new contract or assignment IS needed for non-umbrella agreements, or where the executing entity does not control the new entity - it cannot bind a company it does not own. Aspen acquiring ClearChoice and Lovet is the worked example. Use the assignment-transfer form.

## Branch E - integration switches

Any move between integrations (Easy Apply, Wonderful, Rectangle Health, and so on) requires all three:

1. A new contract, because pricing changes.
2. A Termination request to Legal for the old account, via the ClickUp intake form.
3. Revenue share moves from old partner to new partner - approved, though Legal is still finalising the general policy.

## Branch F - escalated legal review

Accounts that look concerning - suspicious website, mixed verticals and specialties - go to escalated legal review via the ClickUp form, **not** email.

**Do not stop onboarding for these.** Legal monitors them more closely and reaches out if there is a problem. Flagging is not blocking.

## What counts as a valid contract

- For a standalone provider with no parent, a **RIC or a BAAS contract** satisfies the general onboarding requirement. For a *bank-loan conversion* specifically, only bank-loan or combined paper qualifies.
- A contract found in **HubSpot is equally valid** as one in the Legal folder. Filing to Legal runs daily but can take up to a week.

That last point is why `VERIFY` exists as a verdict. Absence of a filed document is not evidence that nothing was signed.
