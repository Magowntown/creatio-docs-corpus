# e6Solutions Meeting Notes - January 20, 2026

## Agenda

1. Brandwise Integration Issues (Critical)
2. v8/Freedom UI Migration Status
3. Looker Studio / CSP Issues
4. QuickBooks Sync Process Overview

---

## 1. CRITICAL: Brandwise Integration Issues

### Problem Discovered

Orders imported from Brandwise are **not syncing to QuickBooks**, causing missing Commission report data.

### Root Causes (3 Issues)

| Issue | Expected Value | Brandwise Value | Impact |
|-------|---------------|-----------------|--------|
| `BGHasQuickBooksLog` | `true` | `false` | Order skipped by sync process |
| `ProcessListeners` | `> 0` | `0` | No business process triggered |
| QB Log Entry | Created automatically | **Not created** | Sync process has nothing to process |

### Data Impact

- **658 orders** were stuck (not syncing to QuickBooks)
- December 2025 & January 2026 Commission reports showed missing data
- Client reported missing sales data for specific reps (e.g., Patricia Goncalves)

### Temporary Fixes Applied Today

1. SQL: Set `BGHasQuickBooksLog = true` on 626 orders
2. SQL: Set `ProcessListeners = 2` on affected orders
3. SQL: Inserted 658 records into `BGQuickBooksIntegrationLogDetail` with Pending status
4. Ran QB Customer Order Integration process (currently running)

### PERMANENT FIX NEEDED

The **Brandwise integration code** needs to be modified to:

```csharp
// When creating orders, set these fields:
entity.SetColumnValue("BGHasQuickBooksLog", true);
entity.SetColumnValue("BGHasInvoice", true);
entity.SetColumnValue("ProcessListeners", 2);  // Or trigger via proper mechanism

// AND create a log entry in BGQuickBooksIntegrationLogDetail:
// - BGTypeId = '14535998-d4c0-45ac-bbac-8c0185bfcc1a' (Customer Order)
// - BGActionId = 'facb63c3-3599-4cb5-b86d-179b0636a3cb' (Insert)
// - BGStatusId = 'c97db3bc-634d-4c90-8432-ec7141c87640' (Pending)
// - BGRecordId = Order.Id
```

### Questions for e6Solutions

1. Where is the Brandwise integration code located? (Package name?)
2. Was this working before the v8 migration?
3. Can you implement the fix, or do we need to engage another party?

---

## 2. v8/Freedom UI Migration Status

### Current State

- Migration started but **not fully complete**
- Some components broken due to v7 → v8 changes

### Known Migration Issues

| Issue | Description | Status |
|-------|-------------|--------|
| CSP Blocking Iframes | Looker Studio embeds blocked by Content Security Policy | Needs CSP config |
| Looker Studio Access | Users get "Can't access report" errors | Needs Google permissions |
| IntExcelReport Templates | Some throw "Row out of range" errors | Needs template review |

### Questions for e6Solutions

1. What is the migration timeline/status?
2. Were the report templates tested after migration?
3. Who is responsible for CSP configuration?

---

## 3. Looker Studio / Reports Issues

### Looker Studio URLs in System

| Report | URL |
|--------|-----|
| Sales By Customer | `https://lookerstudio.google.com/embed/u/0/reporting/3b2a38a0-981e-4552-b607-1855bc65e335/page/pf9CD` |
| Sales By Sales Group | `https://lookerstudio.google.com/embed/u/0/reporting/50e808d8-196d-4f12-a7e5-a2b203571f84/page/p_8mvpobcd3c` |
| Sales By Customer Type | `https://lookerstudio.google.com/embed/reporting/adac9cc3-9b6b-456a-ae85-4017c6ca4a27/page/p_8mvpobcd3c` |

### Issues

1. **CSP blocks iframe embeds** - Freedom UI has strict Content Security Policy
2. **Google permissions** - Users can't access reports even via direct URL
3. **Unknown ownership** - Who owns/manages these Google dashboards?

### Questions for e6Solutions

1. Do you know who created/owns these Looker Studio dashboards?
2. Were these working in the original v7 setup via iframes?
3. Is there a plan to address CSP configuration?

---

## 4. QuickBooks Sync Process Overview

### How It Should Work

```
Order Created
    ↓
BGHasQuickBooksLog = true + ProcessListeners > 0
    ↓
Log entry created in BGQuickBooksIntegrationLogDetail (Status: Pending)
    ↓
"QB Customer Order Integration" process runs
    ↓
Process reads Pending log entries
    ↓
Creates/updates Invoice in QuickBooks
    ↓
Order.BGQuickBooksId populated
    ↓
Log entry status → Processed
```

### Current Problem

Brandwise orders skip steps 2-3, so the sync process never sees them.

### Key Tables

| Table | Purpose |
|-------|---------|
| `Order` | Source orders |
| `BGQuickBooksIntegrationLog` | Parent log (daily batch) |
| `BGQuickBooksIntegrationLogDetail` | Individual order sync records |

### Key Fields on Order

| Field | Purpose |
|-------|---------|
| `BGHasQuickBooksLog` | Flag to enable QB sync |
| `BGHasInvoice` | Flag for invoice generation |
| `ProcessListeners` | Enables business process triggers |
| `BGQuickBooksId` | QuickBooks invoice ID (populated after sync) |
| `BGNumberInvoice` | Invoice number from QB |

---

## 5. Action Items

### For e6Solutions

- [ ] Locate Brandwise integration code
- [ ] Implement permanent fix for order creation
- [ ] Clarify v8 migration status and timeline
- [ ] Identify Looker Studio dashboard ownership

### For InterWeave

- [ ] Monitor today's QB sync (658 orders processing)
- [ ] Verify Commission report data after sync completes
- [ ] Follow up with BGlobal on Looker Studio ownership
- [ ] Consider scheduled job to catch orders with missing flags

---

## 6. Documentation Created

All investigation and fixes documented in:

- `/home/magown/creatio-report-fix/CLAUDE.md` - Main status doc
- `/home/magown/creatio-report-fix/QB_SYNC_ISSUE_ANALYSIS.md` - Root cause analysis
- `/home/magown/creatio-report-fix/docs/CLIENT_COMMISSION_UPDATE_20260120.md` - Client summary

---

## Contact

**BGlobal Response:** Uriel Nusenbaum confirmed they weren't part of v8 migration. Provided CSP documentation link. Awaiting response on Looker Studio ownership.
