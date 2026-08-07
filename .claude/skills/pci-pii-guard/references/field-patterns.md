# Sensitive Field Name Patterns

Use this reference to identify sensitive fields by name pattern — even when the
field name is abbreviated, prefixed, or unconventionally named.

---

## PII Patterns

### SSN / Government ID
Exact or containing: `ssn`, `social_security`, `social_sec`, `tax_id`, `taxid`,
`itin`, `ein`, `sin` (Canadian), `national_id`, `govt_id`, `gov_id`, `id_number`

### Date of Birth
Exact or containing: `dob`, `date_of_birth`, `birth_date`, `birthdate`,
`born_on`, `birth_day`, `birthday`

### Name (flag when full name is exposed)
Combinations of: `first_name` + `last_name`, `full_name`, `legal_name`,
`borrower_name`, `patient_name`, `applicant_name`, `customer_name`
> Single name components (first_name alone) are lower risk but flag in aggregate

### Address
Street-level fields: `address`, `address_line`, `street`, `street_address`,
`addr1`, `addr2`, `mailing_address`, `physical_address`, `residence`
> City, state, zip alone are low risk; flag when combined with street

### Contact
`phone`, `phone_number`, `mobile`, `cell`, `fax`, `email`, `email_address`
> These are context-dependent — flag but don't always block

### Financial Identity
`bank_name` + account fields together, `employer_id`, `payroll_id`

---

## PCI Patterns

### Card Numbers (PAN)
`card_number`, `cc_number`, `cc_num`, `credit_card`, `debit_card`,
`card_no`, `pan`, `primary_account_number`, `card_digits`

### Card Security
`cvv`, `cvc`, `cvc2`, `cvv2`, `card_code`, `security_code`, `pin`
> NEVER display, mask, or hash — always fully redact as `[REDACTED - PCI]`

### Card Metadata
`expiry`, `expiration`, `exp_date`, `card_expiry`, `valid_thru`, `valid_through`,
`expiry_month`, `expiry_year`, `card_holder`, `cardholder_name`

### Bank / Account
`account_number`, `acct_number`, `acct_no`, `acct_num`, `bank_account`,
`checking_account`, `savings_account`, `routing_number`, `routing_no`,
`aba_routing`, `aba`, `iban`, `swift`, `bic`, `sort_code`

---

## Compound Risk Signals

These fields are individually low-risk but become high-risk when queried together.
Flag and warn the user when you see two or more of these in the same SELECT or API call:

- `first_name` + `last_name` + (`address` OR `dob` OR `ssn`)
- `email` + `dob`
- `zip_code` + `dob` + `gender` (classic re-identification triad)
- Any name field + any government ID field

---

## Common False Positives (Generally Safe)

These sound sensitive but are usually surrogate keys or non-sensitive:
- `account_id`, `account_key`, `acct_id` — surrogate IDs, not account numbers
- `contact_id`, `borrower_id`, `loan_id`, `patient_id` — preferred surrogate keys
- `state` (alone) — geographic, not sensitive
- `zip` (alone) — generally safe unless combined
- `card_type` (`Visa`, `Mastercard`) — not sensitive
- `last4`, `card_last4`, `account_last4` — already masked, safe to display
