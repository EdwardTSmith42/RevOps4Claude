# Provider Hierarchy Reference

## Table: HFDProd_Finance.dbo.Providers

| Column | Type | Notes |
|--------|------|-------|
| ProviderId | int (PK) | Unique provider identifier |
| ProviderName | varchar | Provider display name |
| PracticeName | varchar | Practice/business name |
| ParentProvider | int (FK) | References ProviderId of parent. NULL if no parent. |
| IsParentProvider | bit | 1 = this provider is a parent account |
| FundingType | int | 10000=Cash Over Time, 10001=Cash Up Front, 10002=Hybrid Financing, NULL=unset |
| State | varchar | Two-letter state code |
| Zip | varchar | ZIP code (may have leading zeros, use LEFT(Zip,5) for 5-digit) |
| IsTest | bit | 1 = test provider, exclude from reporting |
| ProviderStatus | varchar | 'TST' = test, exclude from reporting |

## Table: HFDProd_Finance.dbo.ProviderRelationsReps

| Column | Type | Notes |
|--------|------|-------|
| ProviderId | int (FK) | Links to Providers.ProviderId |
| FirstName | varchar | Rep first name |
| LastName | varchar | Rep last name |

Used in LEFT JOIN for rep-based territory assignment. Concatenate as `RR.FirstName + ' ' + RR.LastName` for display.

## FundingType Classification

| Code | Name | Typical Classification |
|------|------|----------------------|
| 10000 | Cash Over Time | Special Markets |
| 10001 | Cash Up Front | Area Managers |
| 10002 | Hybrid Financing | Area Managers |
| NULL | (unset) | Area Managers (default) |

## Provider Classification Priority (Parent Account Groups)

When classifying providers into territory groups, the CASE logic follows first-match-wins in this priority:

1. **Special Markets** - specific ParentProvider IDs (hardcoded list)
2. **Excluded Accounts** - specific ParentProvider IDs (hardcoded list)
3. **Enterprise Management** - specific ParentProvider IDs (base set for formulas 1-2, extended set for formulas 3-4)
4. **Practice Name overrides** - specific ProviderId values matched by practice name (e.g., Bosley, Redemption Orthodontics)
5. **Rep-based exclusions** - dynamic filter using ProviderRelationsReps with parent ID and practice name exclusions
6. **FundingType fallback** - 10000 to Special Markets, 10001/10002 to Area Managers, NULL to Area Managers

## Territory Detail (Area Managers State Mapping)

When a provider falls into "Area Managers", the territory detail is determined by state:

| States | Territory |
|--------|-----------|
| AL, AR, KY, LA, MS, NC, SC, TN, VA, WV, DC | Southeast |
| CT, DE, MA, MD, ME, NH, NJ, NY, PA, RI, VT | Northeast |
| IA, IL, IN, MI, MN, MO, OH, WI | Midwest |
| TX (ZIP < 73301) | South Texas |
| TX (ZIP >= 73301), OK | South Central |
| GA | Georgia |
| FL | Florida |
| AZ, CO, KS, NM, NV, UT, ID, MT, ND, SD, WY | Desert Frontier |
| AK, CA, HI, NE, OR, WA | West |
| (no match) | Area Managers Invalid Address Information |

The TX ZIP split uses `TRY_CAST(LEFT(P.Zip, 5) AS INT)` to safely parse the numeric portion.

## Four Output Columns

The provider classification produces 4 columns on DimProvider:

| Column | Logic |
|--------|-------|
| ProviderParentAccountGroup | BaseGroup, unless Area Managers with invalid address, then TerritoryDetail |
| ProviderParentAccountGroupDetail | TerritoryDetail when Area Managers, otherwise BaseGroup |
| ProviderParentAccountGroupEnterprise | EnterpriseGroup, unless Area Managers with invalid address, then TerritoryDetail |
| ProviderParentAccountGroupEnterpriseDetail | TerritoryDetail when Area Managers, otherwise EnterpriseGroup |

The "group" and "detail" columns match when the value is anything other than a valid Area Managers territory (Special Markets = Special Markets, Excluded Accounts = Excluded Accounts, Area Managers Invalid Address Information = Area Managers Invalid Address Information). They differ only for valid Area Managers territories where group shows "Area Managers" and detail shows the specific territory.
