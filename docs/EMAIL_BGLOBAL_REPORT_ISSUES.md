# Email to BGlobal: Creatio Reports Issues (v7 to v8 Migration)

---

**To:** BGlobal Support/Development Team
**From:** [Your Name]
**Subject:** Reports Page Issues Following Creatio 7 to 8 (Freedom UI) Migration - Action Required

---

Hi BGlobal Team,

We've been troubleshooting issues with the Reports page in our Creatio PROD environment following the migration from Creatio 7 (Classic UI) to Creatio 8 (Freedom UI). I wanted to summarize our findings and request your assistance on several items.

## Summary of Issues

### 1. Looker Studio Iframes Blocked by Content Security Policy (CSP)

**Problem:** The original Reports page design embedded Looker Studio dashboards in iframes. After the Creatio 8 migration, these iframes are now blocked by the browser with the following errors:

```
Refused to frame 'https://bglobalsolutions.com/' because it violates Content Security Policy
X-Frame-Options set to 'sameorigin'
```

**Root Cause:** Freedom UI (Creatio 8) has stricter default CSP policies that prevent embedding external domains in iframes.

**Impact:** Reports that rely on Looker Studio (Sales By Customer, Sales By Sales Group, Sales By Customer Type, etc.) cannot be displayed inline.

---

### 2. Looker Studio Direct Access - Google Permissions Issue

**Attempted Workaround:** We modified the handler to open Looker Studio reports in a new browser tab instead of an iframe (bypassing CSP restrictions).

**Result:** Users receive a Google authentication error:

```
Can't access report
Your current account [user@email.com] can't access this report, or the report doesn't exist.
```

**Root Cause:** The URLs stored in `UsrReportesPampa.UsrURL` are embed-format URLs designed for authenticated iframe contexts. When accessed directly, Google doesn't recognize the user's permissions.

**Question for BGlobal:**
- Which Google account(s) should have access to these Looker Studio dashboards?
- Can the reports be shared with specific users or made "Anyone with link can view"?
- Should the URLs in `UsrReportesPampa` be updated to regular viewing URLs instead of embed URLs?

---

### 3. Reports Without Looker Studio URLs

Several reports in `UsrReportesPampa` have no Looker Studio URL configured (`UsrURL` is empty):

| Report Name | UsrCode | UsrURL |
|-------------|---------|--------|
| Commission | Commission | (empty) |
| Sales By Item By Type Of Customer | SalesByItemByTypeOfCustomer | (empty) |
| Customers did not buy over a period of time | CustomersDidNotBuyOverAPeriodOfTime | (empty) |
| Sales By Item | SalesByItem | (empty) |

**Question for BGlobal:**
- Were these reports intentionally excluded from Looker Studio?
- Should they have Looker Studio dashboards, or are they Excel-only reports?
- Are the corresponding `IntExcelReport` templates configured correctly for these reports?

---

### 4. IntExcelReportService / Excel Template Issues

When attempting to use Excel downloads as a fallback, we encountered several errors:

| Report | Error |
|--------|-------|
| Items by Customer | `ArgumentException: Row out of range` at `LoadEsqToSheet` |
| Various reports | `FormatException: Excel template with Id [GUID] not found` |
| Various reports | `Unknown error` with null response |

**Root Cause:** The `IntExcelReport` configurations (ESQ queries, template ranges, entity mappings) appear to have issues or may not be fully configured.

**Question for BGlobal:**
- Were the Excel report templates (`IntExcelReport`) tested after the v8 migration?
- Can you provide documentation on how these reports were originally intended to work?

---

### 5. Commission Report - Missing Records for Recent Months

**Problem:** Commission reports are generating successfully, but showing significantly fewer records than expected for December 2025 and January 2026.

**Investigation Findings:**

| Month | Expected Records | Actual Records | Gap |
|-------|-----------------|----------------|-----|
| December 2025 | ~500+ | ~39 | ~93% missing |
| January 2026 | ~400+ | Partial | Significant gap |

**Root Cause Identified:** The Commission report data flows through QuickBooks sync:

```
Creatio Orders → QB Invoices → [Payment Processing] → QB ReceivePayments → Commission Data
     ✅              ✅               ❌                      ❌                  ❌
  (EXISTS)       (SYNCED)      (NOT PROCESSED)         (NOT CREATED)        (MISSING)
```

- December 2025 orders **exist** in Creatio
- Orders were **synced to QuickBooks** as invoices (all have `BGQuickBooksId`)
- Invoices have **NOT been marked as "paid"** in QuickBooks
- Commission sync pulls from `ReceivePayment` records (created when invoices are paid)
- Since no payments are recorded, no commission data is synced back

**Evidence:**
- Credit Memos (Returns) ARE syncing correctly for December 2025 (39 records)
- Sales data is missing because it comes from ReceivePayments, not Invoices
- Specific sales reps (e.g., Patricia Goncalves) showing $0 commission for December despite having 63 commission earner records

**Question for BGlobal / QuickBooks Team:**
- Is there a backlog in processing invoice payments in QuickBooks for December 2025?
- Is the QuickBooks → Creatio sync process ("Get QuickBooks Commissions") running correctly?
- Are there any known issues with the payment processing workflow?

**Impact:** Sales representatives cannot see accurate commission data for the past 2 months, affecting compensation visibility and reporting accuracy.

---

## Current Workaround Status

| Report Type | Status | Notes |
|-------------|--------|-------|
| Commission (Excel) | ⚠️ Partial | Downloads work, but **missing ~93% of Dec 2025 / Jan 2026 data** due to QB payment backlog |
| Reports with Looker Studio URLs | ❌ Blocked | CSP blocks iframes; direct access requires Google permissions |
| Reports without URLs (Excel fallback) | ❌ Errors | Template configuration issues ("Row out of range", etc.) |

---

## Requested Actions from BGlobal

1. **CSP Configuration:** Is it possible to whitelist `lookerstudio.google.com` and `bglobalsolutions.com` in Creatio's Content Security Policy settings for Freedom UI?

2. **Looker Studio Permissions:** Please advise on how to grant user access to the Looker Studio dashboards, or update sharing settings to allow broader access.

3. **URL Format:** Should the `UsrReportesPampa.UsrURL` values be updated from embed format to direct viewing format?

4. **Excel Templates:** Please review the `IntExcelReport` configurations for reports that don't have Looker Studio URLs to ensure they work as a fallback.

5. **Original Design Documentation:** Any documentation on the intended Reports page architecture would be helpful for troubleshooting.

6. **QuickBooks Payment Processing:** Please investigate why December 2025 and January 2026 invoices have not been processed as paid in QuickBooks. This is blocking commission data from syncing to Creatio.

7. **Commission Sync Process:** Confirm the "Get QuickBooks Commissions" process is running correctly and review any errors in the sync logs.

---

## Environment Details

- **Environment:** PROD (pampabay.creatio.com)
- **Creatio Version:** 8.x (Freedom UI)
- **Previous Version:** 7.x (Classic UI)
- **Affected Package:** BGlobalLookerStudio, BGApp_eykaguu

---

Please let us know the best path forward. We can schedule a call to discuss if that would be helpful.

Thank you,
[Your Name]
[Your Contact Information]

---

*Attachments (if needed):*
- Screenshot of CSP error in browser console
- Screenshot of Looker Studio "Can't access report" message
- List of reports with/without Looker Studio URLs
