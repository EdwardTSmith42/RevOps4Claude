# Technical Details — HFDV3 Monitoring & Architecture

## Table of Contents

1. [Database Schema](#database-schema)
2. [Row Counts and Reduction](#row-counts)
3. [Custom SQL Queries (3-Year Rolling)](#custom-sql)
4. [Join Model](#join-model)
5. [Virtual Connection Table Inventory](#vconn-tables)
6. [Calculated Field Inventory](#calculated-fields)
7. [Monitor Config Reference](#monitor-config)
8. [Key LUIDs and Identifiers](#luids)

---

## Database Schema {#database-schema}

All tables are in the `Analytics` database on `PRPTBI01`.

### FactApplication (dw.FactApplication) — 55 columns

```
ApplicationId (int), ApplicationUniqueKey (varchar 64),
ApplicationApplicantKey (varchar 64), ApplicationProviderKey (varchar 12),
ApplicationOfferKey (varchar 128), ApplicationRiskModel (varchar 128),
ApplicationRiskModelVersion (char 10), ApplicationScorebreakModel (varchar 128),
ApplicationScorebreakModelVersion (char 10), ApplicationStatus (varchar 16),
ApplicationPatientId (varchar 64), ApplicationTreatmentAmount (decimal),
ApplicationProcAmount (decimal), ApplicationCreatedOn (datetime),
ApplicationSubmittedOn (datetime), ApplicationAgreementSignedOn (datetime),
ApplicationTentProcedureDate (datetime), ApplicationConfProcedureDate (datetime),
ApplicationActivatedOn (datetime), ApplicationLocale (varchar 16),
ApplicationSessionIdentifier (varchar 64), ApplicationScore (numeric),
ApplicationScoreGrade (varchar 12), ApplicationFICO (int),
ApplicationCreditScore (int), ApplicationCreditScoreType (varchar 32),
ApplicationRanToCompletion (bit), ApplicationDisposition (varchar 32),
ApplicationIPAddress (varchar 32), ApplicationLatitude (numeric),
ApplicationLongitude (numeric), ApplicationDeviceFingerprint (varchar 64),
ApplicationApplicantIsOnOFAC (bit), ApplicationPRSFirstName (varchar 64),
ApplicationPRSLastName (varchar 64), ApplicationFinancialInstrument (varchar 64),
ApplicationSource (varchar 64), ApplicationOriginationTechnology (varchar 16),
ApplicationLifecycleStage (varchar 12), ApplicationProgramCode (nvarchar 255),
ApplicationRowHash (int), ApplicationLastUpdate (datetime),
ApplicationAnnualIncome (numeric), ApplicationMonthlyStatedIncome (numeric),
ApplicationEmployer (varchar 75), ApplicationPosition (varchar 40),
ApplicationWorkPhone (varchar 21), ApplicationYearsThere (int),
ApplicationEmployType (varchar 15), ApplicationGrossPay (money),
ApplicationOtherIncome (money), ApplicationFiledBankruptcy (int),
ApplicationDischargedOn (date), ApplicationSegment (nvarchar 50),
ApplicationPrimaryErrorDescription (nvarchar 200),
ApplicationCriticalMessage (nvarchar max)
```

### FactContract (dw.FactContract) — 43 columns

```
ContractId (int), ContractProviderKey (varchar 12),
ContractUniqueKey (varchar 64), ContractApplicationKey (varchar 64),
ContractApplicantKey (varchar 64), ContractOfferKey (varchar 64),
ContractFinanceOwnerKey (int), ContractPaymentFrequency (varchar 32),
ContractDownPayment (decimal), ContractTotalDownPayment (decimal),
ContractValue (decimal), ContractProcAmount (decimal),
ContractBalance (decimal), ContractOpeningBalance (decimal),
ContractPrincipalBalance (decimal), ContractTotalAmountOwed (decimal),
ContractMonthlyAmountOwed (decimal), ContractPayments (decimal),
ContractStatus (varchar 32), ContractStatusOn (datetime),
ContractFirstPaymentOn (datetime), ContractFirstPaymentCollected (bit),
ContractOptOutAutoDraft (bit), ContractWriteOffDate (date),
ContractWriteOffAmount (decimal), ContractDeliquentDate (date),
ContractAgingBucket (varchar 32), ContractOnHold (bit),
ContractDetailStatus (varchar 32), ContractInterestRate (decimal),
ContractAdvanceRate (decimal), ContractProgramCode (varchar 32),
ContractProgramGroup (varchar 32), ContractPromoCode (varchar 32),
ContractThirdPartyFeeRate (decimal), ContractTotalFeeRate (decimal),
ContractFirstPaymentAmount (decimal), ContractNumberOfPayments (int),
ContractNextPaymentDate (date), ContractDocStampTaxAmount (decimal),
ContractTerm (int), ContractCreated (datetime),
ContractOriginationTechnology (varchar 16)
```

### FactOffer (dw.FactOffer) — 10 columns

```
OfferId (int), OfferHistoryUniqueKey (varchar 64),
OfferUniqueKey (varchar 64), OfferApplicationUniqueKey (varchar 64),
OfferRequestCreditGrade (varchar 6), OfferRequestServiceCost (decimal),
OfferRequestProgramCode (varchar 64), OfferRequestRegion (varchar 2),
OfferIssuedDate (datetime), OfferProgramCodeCurrent (varchar 50)
```

### DimProvider (dw.DimProvider) — 46 columns

```
Id (int), ProviderUniqueKey (varchar 12), ProviderPartnerKey (int),
ProviderName (varchar 128), ProviderPracticeName (varchar 128),
ProviderParentKey (varchar 64), ProviderAddressKey (varchar 64),
ProviderPracticeType (varchar 64), ProviderStatus (varchar 32),
ProviderCompanyId (varchar 128), ProviderCustomerChannel (varchar 32),
ProviderMonthlyPaymentFee (decimal), ProviderMinAmountAllowed (decimal),
ProviderMaxAmountAllowed (decimal), ProviderMaxTermMonths (int),
ProviderDecisionMaker (varchar 64), ProviderDecisionMakerEmail (varchar 128),
ProviderCreatedOn (datetime), ProviderActivatedOn (datetime),
ProviderTrainedOn (datetime), ProviderRelationsRep (varchar 128),
ProviderSalesRep1 (varchar 128), ProviderFundingType (varchar 32),
ProviderNetworkPartnerUniqueKey_Temporary (varchar 32),
ProviderWebsite (varchar 256), ProviderIsActive (bit),
ProviderIsParent (bit), ProviderFinancialInstrument (varchar 50),
ProviderPublicKey (varchar 64), ProviderUtm_Source (varchar 255),
ProviderUtm_Medium (varchar 255), ProviderUtm_Campaign (varchar 255),
ProviderRegionalDirectorOperations (varchar 255),
ProviderEnablePreQual (bit), ProviderRowHash (int),
ProviderLastUpdate (date), ProviderSalesTerritories (varchar 50),
ProviderWorkflow (varchar 100), ProviderPrequalLink (nvarchar 1000),
PMOName (nvarchar 255), PMOEmail (nvarchar 255),
InvisalignDID (nvarchar 50), InvisalignLID (nvarchar 50),
ProviderParentAccountGroup (varchar 50),
ProviderParentAccountGroupDetail (varchar 50),
ProviderParentAccountGroupEnterprise (varchar 50),
ProviderParentAccountGroupEnterpriseDetail (varchar 50),
ProviderForecastSegment (varchar 50)
```

### DimPerson (dw.DimPerson) — 11 columns

```
PersonId (int), PersonUniqueKey (varchar 64),
PersonAddressKey (varchar 64), PersonHashedNationalId (varchar 32),
PersonType (varchar 32), PersonFirstName (varchar 128),
PersonLastName (varchar 128), PersonDOB (date),
PersonMobile (varchar 64), PersonEmail (varchar 256),
PersonAgeInYears (int)
```

**PII fields to exclude:** PersonHashedNationalId, PersonFirstName, PersonLastName,
PersonDOB, PersonMobile, PersonEmail.

### DimAddress (dw.DimAddress) — 11 columns

```
AddressId (int), AddressUniqueKey (varchar 64),
AddressStreet1 (varchar 256), AddressStreet2 (varchar 256),
AddressCity (varchar 128), AddressPostalCode (varchar 10),
AddressCountry (varchar 128), AddressRegion (varchar 64),
AddressLatitude (numeric), AddressLongitude (numeric),
AddressRowHash (int), AddressLastUpdate (date)
```

**PII fields to exclude:** AddressStreet1, AddressStreet2.

### DimDate (dbo.DimDate) — 56 columns

Standard date dimension. Calendar and fiscal year attributes, holidays, weekday flags.

### FactSAOPurchase (dw.FactSAOPurchase)

12 fields: SAO Purchase Release Date, SAO Purchase Partner, SAO Purchase Type,
SAO Program Code, SAO Purchase Contract Unique Key, SAO Purchase Funding Release Date,
SAO Purchase Unique Key, SAO Purchase Financial Owner, SAO Merchant Discount Rate,
SAO Purchase Transaction Date, SAO Current, SAO Purchase Amount.

---

## Row Counts {#row-counts}

Measured June 2026:

| Table | Total Rows | 3-Year Filtered | Reduction |
|-------|-----------|----------------|-----------|
| FactApplication | 9,430,371 | 3,685,256 | 61% |
| FactContract | ~1,750,000 | 721,861 | 59% |
| FactOffer | ~22,600,000 | ~21,900,000 | 3% |
| DimPerson | ~9,800,000 | 3,685,254 | 62% |
| DimAddress | ~9,800,000 | ~3,685,254 | 62% |
| DimProvider | 28,156 | 28,156 | 0% |
| DimDate | ~11,000 | ~11,000 | 0% |
| FactSAOPurchase | 767,527 | 767,527 | 0% |
| DimOfferFast | 984,843 | — | EXCLUDED |
| sdr_leads | 11,910 | — | EXCLUDED |

FactOffer statistics:
- Avg offers per application: 7
- Max offers per application: 3,246
- Distinct program codes: 508
- Distinct regions: 59
- Distinct credit grades: 18
- Monthly aggregation: ~114K unique combos (99.5% compression)

---

## Custom SQL Queries {#custom-sql}

### FactApplication (3-year rolling)

```sql
SELECT *
FROM dw.FactApplication
WHERE ApplicationCreatedOn >= DATEADD(YEAR, -3, GETDATE())
```

### FactContract (3-year rolling)

```sql
SELECT *
FROM dw.FactContract
WHERE ContractCreated >= DATEADD(YEAR, -3, GETDATE())
```

### DimPerson (filtered, PII-safe)

```sql
SELECT DISTINCT
    p.PersonId, p.PersonUniqueKey, p.PersonAddressKey,
    p.PersonType, p.PersonAgeInYears
FROM dw.DimPerson p
INNER JOIN dw.FactApplication a
    ON a.ApplicationApplicantKey = p.PersonUniqueKey
WHERE a.ApplicationCreatedOn >= DATEADD(YEAR, -3, GETDATE())
```

### DimAddress (filtered, PII-safe)

```sql
SELECT DISTINCT
    addr.AddressId, addr.AddressUniqueKey,
    addr.AddressCity, addr.AddressPostalCode,
    addr.AddressCountry, addr.AddressRegion,
    addr.AddressLatitude, addr.AddressLongitude
FROM dw.DimAddress addr
INNER JOIN dw.DimPerson p
    ON p.PersonAddressKey = addr.AddressUniqueKey
INNER JOIN dw.FactApplication a
    ON a.ApplicationApplicantKey = p.PersonUniqueKey
WHERE a.ApplicationCreatedOn >= DATEADD(YEAR, -3, GETDATE())
```

### Monitor Metric Query (Treatment Volume)

```sql
SELECT CAST(SUM(c.ContractValue) AS DECIMAL(18,2))
FROM dw.FactContract c
INNER JOIN dw.DimProvider p ON c.ContractProviderKey = p.ProviderUniqueKey
WHERE p.ProviderCustomerChannel != 'Online'
  AND p.ProviderStatus != 'TST'
  AND c.ContractCreated >= DATEADD(YEAR, -3, GETDATE())
```

As of June 2026, this returns ~$1.92B.

---

## Join Model {#join-model}

```
FactApplication (center)
├── ApplicationApplicantKey = PersonUniqueKey → DimPerson
│   └── PersonAddressKey = AddressUniqueKey → DimAddress
├── ApplicationProviderKey = ProviderUniqueKey → DimProvider
│   └── ProviderAddressKey = AddressUniqueKey → DimAddress (provider addr)
├── ApplicationCreatedOn = Date → DimDate
├── ApplicationUniqueKey = OfferApplicationUniqueKey → FactOffer (SEPARATE DS)
│   └── OfferRequestProgramCode → DimOffer joins
└── ApplicationUniqueKey = ContractApplicationKey → FactContract
        └── ContractUniqueKey = SAOPurchaseContractUniqueKey → FactSAOPurchase
```

---

## Virtual Connection Table Inventory {#vconn-tables}

The HFDV3Base virtual connection has 14 tables (Ed confirmed via screenshot).
The Tableau metadata API only returns 9-10 via field groups:

| Group | Table(s) | Fields | Calculated |
|-------|----------|--------|------------|
| 0 | DimOffer | 28 | 0 |
| 1 | DimProvider | 192 | 87 |
| 2 | DimPerson + FactApplication | 77 | 0 |
| 3 | FactContract | 43 | 0 |
| 4 | (cross-table calcs) | 39 | 39 |
| 5 | FactSAOPurchase | 12 | 0 |
| 6 | DimOfferFast + FactOffer | 35 | 0 |
| 7 | sdr_leads | 9 | 0 |
| 8 | ProgramCodes | 2 | 0 |
| 9 | Forecast/Goals | 15 | 0 |

---

## Calculated Field Inventory {#calculated-fields}

### DimProvider LOD Calcs (87 calculated fields)

These are FIXED-level LOD calculations, most at `[Provider Unique Key]` level with
"(AM)" variants at `[Provider Parent Account Group Detail]` level.

**Provider-level metrics:**
- `cnt_Current Apps` — `{ FIXED [Provider Unique Key] : COUNTD(IF [flag_Is Current Period]...) }`
- `cnt_Prior Apps` — same pattern for prior period
- `cnt_Lifetime Apps` — `{ FIXED [Provider Unique Key] : COUNTD([Application Unique Key]) }`
- `val_Current Contract Value` — `{ FIXED [...] : SUM(IF [flag_Is Current Period]...) }`
- `val_Prior Contract Value` — same for prior period
- `val_Lifetime Contract Value` — `{ FIXED [...] : SUM([Contract Value]) }`
- `avg_Current/Prior/Lifetime Credit Score` — AVG patterns

**Growth and pacing:**
- `pct_App Growth Rate` — current vs prior period apps
- `pct_Value Growth Rate` — current vs prior period value
- `pct_Daily App Run Rate` — current apps / days elapsed MTD
- `val_Daily Run Rate` — current value / days elapsed MTD
- `cnt_Projected Apps` — current + (run rate × days remaining)
- `val_Projected Contract Value` — same for value
- `pct_Pacing vs Prior` — projected vs prior

**Capability analysis:**
- `avg_Best Month Ever` — `{ FIXED [...] : MAX({ FIXED [...], DATETRUNC('month',...) : COUNTD(...) }) }`
- `pct_Capability` — current metric / best month ever
- `Capability Status` — "At Capacity" / "Room to Grow" / "Underperforming"

**Selector calcs (driven by p_Metric View parameter):**
- `sel_Growth Rate`, `sel_Current Metric`, `sel_Best Month Ever`, etc.
- All use `CASE [p_Metric View] WHEN "Applications" THEN ... WHEN "Activations" THEN ...`

**Provider classification:**
- `Provider Funding Type Description` — maps codes to labels
- `flag_Is DSO` — has parent key
- `Enrollment Type` — LOD check for ALIGN program
- `flag_Has Contact Info` — decision maker email present
- `flag_Volume Down Value Up` — growth/decline pattern

### Date/Period Calcs (39 calculated fields)

All driven by the `p_Analysis Period` parameter:

- `flag_Is Current Period`, `flag_Is Prior Period` — date range membership
- `dt_Current Period Start/End`, `dt_Prior Period Start/End` — boundaries
- `dt_Days Elapsed MTD`, `dt_Days Remaining`, `dt_Days in Month`
- `dt_Current/Prior Period Length`
- `pct_progress` — days elapsed / total days
- `rank_Growth`, `rank_Decline`, `rank_New Provider` — provider rankings
- `flag_Is Top 10 Decliner`, `flag_Is Top 10 New Provider`
- `clr_Growth Status` — color coding
- `Current Period Dates`, `Prior Period Dates` — display labels

### Parameters (5)

- `p_View Level` — LIST: "Provider Summary" / others
- `p_Metric View` — LIST: "Applications" / "Activations" / "Credit Grade" / etc.
- `p_Custom Start Date` — DATE (default: 2026-01-10)
- `p_Custom End Date` — DATE (default: 2026-04-01)
- `p_Analysis Period` — LIST: "MTD vs Prior MTD" / others

---

## Monitor Config Reference {#monitor-config}

The current `config.yaml` structure:

```yaml
tableau:
  server: "https://10az.online.tableau.com"
  site: "healthcarefinancedirect"
  api_version: "3.24"

sql_server:
  server: "PRPTBI01"
  database: "Analytics"
  driver: "{ODBC Driver 18 for SQL Server}"
  trust_server_certificate: true

metric_pairs:
  - name: "HFD Treatment Volume vs SQL Source of Truth"
    source_a:
      source_type: "tableau"
      datasource_luid: "9cffc20f-2e85-475e-a24d-2687cc566ace"
      # SUM(ContractValue) excluding Online/TST
    source_b:
      source_type: "sql"
      query: "SELECT CAST(SUM(...)) ... WHERE ... DATEADD(YEAR, -3, GETDATE())"
    refresh_targets:
      - type: "datasource"
        id: "9cffc20f-2e85-475e-a24d-2687cc566ace"

bridge_servers:
  - name: "PRPTBI01"
    datasource_ids:
      - "9cffc20f-2e85-475e-a24d-2687cc566ace"
    remediation:
      service_name: "Tableau Bridge worker(esmith@OFFICE)"
      bridge_log_dir: "\\\\PRPTBI01\\C$\\Users\\esmith\\Documents\\My Tableau Bridge Repository\\Logs"
```

---

## Key LUIDs and Identifiers {#luids}

| Resource | LUID | Notes |
|----------|------|-------|
| Ed's Treatment Volume DS | `9cffc20f-2e85-475e-a24d-2687cc566ace` | Active, monitored |
| v.HfdV3 published DS | `583b19c2-c2ac-4aa4-a207-4714da9a0262` | Being retired |
| HFDV3Base virtual connection | `4ab51096-dda8-4c67-bd23-75815bd25d92` | Being retired |
| Enterprise Origination Scorecard | `ca75c2ed-edf8-4d88-9c3e-5c7906095688` | Test workbook |
| Bridge server | PRPTBI01 | Windows, ODBC 18 |
| Bridge service | `Tableau Bridge worker(esmith@OFFICE)` | For restart |
