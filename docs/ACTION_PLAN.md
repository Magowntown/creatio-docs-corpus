# ACTION_PLAN.md - Next Steps & Priority Queue

> **Last Updated:** 2026-01-15
> **Status:** SYNC-001 requires immediate manual action

---

## Priority Queue

### P0 - Immediate (COMPLETED ✅)

#### SYNC-001: QuickBooks Date Input - RESOLVED

**Status:** ✅ COMPLETED on 2026-01-15

**Result:**
- Manual date entry completed (2024-07-01 to 2026-01-15)
- **8,428 records synced** to BGCommissionReportQBDownload
- Max CreatedOn: Jan 8, 2026 2:41:43 PM

**Next:** Automate the process (see P1 below)

---

### P1 - Current Priority

#### Automate QB Sync Process - PHASE 1 COMPLETE ✅

**Status:** Simplified automation deployed and verified working

**What was done:**
1. ✅ Added process parameters: `AutoStartDate`, `AutoEndDate`
2. ✅ Added Script Task with 30-day window calculation
3. ✅ Mapped parameters to "Get QB Filter Dates" user task
4. ✅ Verified: Process runs with auto-filled dates

**Verification (2026-01-15):**
| Sync Date | Records | Source |
|-----------|---------|--------|
| Jan 8, 2026 | 2 | Automated run (30-day window) |
| Jan 6, 2026 | 37 | Manual sync |

**Current Script (Deployed):**
```csharp
DateTime startDate = DateTime.UtcNow.AddDays(-30);
DateTime endDate = DateTime.UtcNow;
Set<DateTime>("AutoStartDate", startDate);
Set<DateTime>("AutoEndDate", endDate);
return true;
```

---

#### Upgrade to Full ESQ Script - NEXT

**What:** Replace 30-day window with dynamic query from last sync date.

**Why:** Current script uses fixed 30-day window. Should query `MAX(CreatedOn)` from `BGCommissionReportQBDownload` to avoid gaps or redundant syncs.

**Process Designer URL:** https://pampabay.creatio.com/0/Nui/ViewModule.aspx?vm=SchemaDesigner#process/7b1ac959-1726-4340-bc66-210b31f5f365/

**Full Guide:** `docs/QB_SYNC_AUTOMATION.md`

---

#### Verify Commission Report Works

**What:** Test that Commission reports return data for Dec 2025/Jan 2026.

**Test Cases:**
| Year-Month | Sales Group | Expected |
|------------|-------------|----------|
| 2025-12 | RDGZ & Consulting LLC | >0 data rows |
| 2026-01 | (any) | >0 data rows |
| 2024-12 | RDGZ & Consulting LLC | ~55 rows (regression) |

---

### P2 - Business Decision Required

#### DATA-001: PaymentStatusId=Planned Blocking Orders

**What:** 41% of December 2025 orders have `PaymentStatusId = Planned`, preventing QB sync.

**Questions for Business:**
1. Should orders with status "Planned" sync to QuickBooks?
2. Is "Planned" intentional for a workflow (e.g., pending approval)?
3. Should different users have different default behavior?

**Options:**
| Option | Description | Effort |
|--------|-------------|--------|
| A | Remove "Planned" default from OrderPageV2 | Low |
| B | Update QB sync to include "Planned" orders | Medium |
| C | Change report to pull from Order directly | High |

**Reference:** `docs/INVESTIGATION_PAYMENT_STATUS.md`

---

### P3 - Long-Term Improvements

#### Automate QB Sync Dates

**What:** Modify `BGBPGetQuickBooksCommissions` to auto-calculate dates.

**Current Behavior:** Requires manual date entry, blocks indefinitely if not filled.

**Proposed Behavior:**
- Start Date = MAX(CreatedOn) from BGCommissionReportQBDownload
- End Date = Current date
- Remove or make optional the "Get QB Filter Dates" user task
- Schedule to run on timer (daily or weekly)

---

#### V4 Process Gateway Error

**What:** `IWCalculateCommissiononPaymentCustomV4` has gateway condition error.

**Error:** `Unable to compute expression "[#Parameter:xxx#]<0"`

**Impact:** Affects IW pipeline, not BG Commission reports.

**Priority:** Lower - separate from main Commission report issue.

---

## Related Issues Status

| ID | Issue | Status | Priority |
|----|-------|--------|----------|
| **SYNC-001** | QB sync completed, automating | ✅ Resolved / 🔄 Automating | P1 |
| DATA-001 | PaymentStatusId=Planned blocks sync | ⚠️ Business Decision | P2 |
| V4 Gateway | IW process condition error | ⏸️ Low Priority | P3 |
| FUT-002 | Freedom UI Product Pictures | 📋 Rommel on PTO | P3 |

---

## Files Updated This Session

| File | Purpose |
|------|---------|
| `CLAUDE.md` | Added SYNC-001, session log, updated status |
| `docs/TEST_LOG.md` | Full investigation documentation |
| `docs/CLAUDE_REFERENCE.md` | DataService queries, QB process flow |
| `docs/CLAUDE_HISTORY.md` | Change log entries |
| `docs/ACTION_PLAN.md` | This file - priority queue |
| `docs/QB_SYNC_AUTOMATION.md` | **NEW** - Process automation guide |

---

## Quick Reference

### PROD Authentication
```bash
source .env && curl -s -c /tmp/cookies_prod.txt \
  "${CREATIO_PROD_URL}/ServiceModel/AuthService.svc/Login" \
  -H "Content-Type: application/json" \
  -d "{\"UserName\":\"${CREATIO_PROD_USERNAME}\",\"UserPassword\":\"${CREATIO_PROD_PASSWORD}\"}"
```

### DataService Query Template
```bash
CSRF=$(grep BPMCSRF /tmp/cookies_prod.txt | tail -1 | awk '{print $NF}')
curl -s -b /tmp/cookies_prod.txt \
  "${CREATIO_PROD_URL}/0/DataService/json/SyncReply/SelectQuery" \
  -H "Content-Type: application/json" -H "BPMCSRF: $CSRF" \
  -d '{"rootSchemaName": "EntityName", "operationType": 0, "allColumns": true, "rowCount": 5}'
```

### Commission Report Test
```bash
source .env && CREATIO_URL=$CREATIO_PROD_URL CREATIO_USERNAME=$CREATIO_PROD_USERNAME \
  CREATIO_PASSWORD=$CREATIO_PROD_PASSWORD CREATIO_YEAR_MONTH_NAME=2025-12 \
  CREATIO_SALES_GROUP_ID=edfefb79-77b6-43fe-932b-c012d9a2fc9d \
  python3 scripts/testing/test_report_service.py
```
