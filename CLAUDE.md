# CLAUDE.md - Creatio Reports Fix

> **Status:** 🔴 **SYNC-004:** QB Web Connector offline. **IW-001:** IW_Commission Excel columns misaligned.
> **Updated:** 2026-01-23 | **History:** `docs/SESSION_HISTORY.md`

---

## Issue Tracker

| ID | Issue | Status |
|----|-------|--------|
| **SYNC-004** | QB Web Connector offline (96.56.203.106:8080) | 🔴 **IT Action Required** |
| **SYNC-005** | 637 orders falsely marked "Processed" | 🔴 **Reset After QB Online** |
| **SYNC-003** | QB Customer Order Integration 20K limit | 🔴 **Batch Processing Required** |
| **CSP-001** | Looker Studio iframes blocked by Freedom UI CSP | 🔴 **Server Config Required** |
| **LOOKER-001** | Looker Studio Google permissions | 🔴 **BGlobal Action Required** |
| **RPT-004** | "Items by Customer" Row out of range | 🔴 **Template Issue** |
| **IW-001** | IW_Commission Excel columns misaligned | ⏳ Template alignment needed |
| **DEV-001** | PROD → DEV sync for IWQBIntegration | ⏳ In Progress |
| **DATA-001** | PaymentStatusId=Planned blocks QB sync | ⚠️ Business Decision Required |
| **DATA-005** | Patricia 97.8% commission missing | ⚠️ QB Payment Bottleneck |
| **DATA-003** | DEV commission data only through Oct 2025 | ⚠️ Needs QB Sync |
| **UI-002** | Non-Commission reports wrong filters | ✅ v18 attribute binding |
| **HANDLER-001** | Hybrid handler (Looker + Excel) | ✅ Deployed to PROD |
| **DL-004** | Commission download 404 | ✅ Deployed |
| **RPT-002** | "Rpt Sales By Line" GUID error | ✅ ESQ sanitization |
| **EARNERS-001** | Brandwise missing commission earners | ✅ 263 earners created |
| **DATA-002** | Dec 2025 invoices awaiting payment | ✅ Partial - sync pulled data |
| **SYNC-001** | QB sync process automation | ✅ Phase 1 deployed |

<details>
<summary>Resolved Issues (click to expand)</summary>

| ID | Issue | Resolution |
|----|-------|------------|
| DL-001 | "File wasn't available" | Fixed |
| DL-002 | `UsrURL` undefined | Fixed |
| DL-003 | Excel format/extension | Fixed |
| DL-005 | Excel VBA Type mismatch | Redirect approach |
| FLT-001 | Commission filters | Fixed |
| FLT-002 | IW_Commission filters | Partial (Sales Group only) |
| FLT-003 | Dynamic filters | Verified |
| FLT-004 | Commission empty data | View SQL fixed |
| UI-001 | DEV infinite loading | Hybrid.js handler |
| RPT-001 | Reports queryConfig | 13/13 configured |
| RPT-003 | BGYearMonth not found | View-specific mapping |
| SYNC-002 | UsrPage_ebkv9e8 QB sync | Debunked |
| PROC-001 | V4 Commission gateway | Dormant |
| FUT-002 | Freedom UI Product Pictures | On hold (Rommel PTO) |

</details>

---

## Active Blockers

### SYNC-004: QB Web Connector Offline

**Problem:** `96.56.203.106:8080` not responding. 157+ January 2026 orders cannot sync.
**Action:** IT team must bring QB Web Connector online.

### SYNC-003: 20K Record Limit

**Problem:** 81,803 records in `BGQuickBooksIntegrationLogDetail`, ESQ limit is 20,000.

**Batch Solution:**
```sql
-- Step 1: Move older pending to Re-Process (keep newest 15K)
WITH newest_pending AS (
    SELECT "Id" FROM "BGQuickBooksIntegrationLogDetail"
    WHERE "BGStatusId" = 'c97db3bc-634d-4c90-8432-ec7141c87640'
    ORDER BY "CreatedOn" DESC LIMIT 15000
)
UPDATE "BGQuickBooksIntegrationLogDetail"
SET "BGStatusId" = 'ff92e20c-da27-4255-96bc-57e32f0944f4'
WHERE "BGStatusId" = 'c97db3bc-634d-4c90-8432-ec7141c87640'
  AND "Id" NOT IN (SELECT "Id" FROM newest_pending);

-- Step 2: Run QB Customer Order Integration
-- Step 3: Rotate next 15K from Re-Process back to Pending
-- Repeat until complete
```

### SYNC-005: False "Processed" Orders

**Problem:** 637 orders marked "Processed" but have no BGQuickBooksId.
**Fix:** Reset after QB Web Connector online:
```sql
UPDATE "BGQuickBooksIntegrationLogDetail"
SET "BGStatusId" = 'c97db3bc-634d-4c90-8432-ec7141c87640', "BGErrorMessage" = ''
WHERE "BGStatusId" = 'e7428193-4cf1-4d1b-abae-00e93ab5e1c5'
  AND "BGRecordId" IN (SELECT "Id" FROM "Order" WHERE "BGQuickBooksId" IS NULL OR "BGQuickBooksId" = '');
```

### IW-001: IW_Commission Column Alignment

**Problem:** ESQ column order doesn't match Excel template headers.
**Status:** Template header order needed to align ESQ.

---

## Quick Reference

### Key Files

| Purpose | File |
|---------|------|
| **Frontend handler (PROD)** | `client-module/BGApp_eykaguu_UsrPage_ebkv9e8_v18_AttrBinding.js` |
| **Backend service** | `source-code/UsrExcelReportService_Updated.cs` |
| Handler (legacy) | `client-module/UsrPage_ebkv9e8_Updated.js` |

### Deployment URLs

| Component | URL |
|-----------|-----|
| Frontend | `https://dev-pampabay.creatio.com/0/ClientApp/#/ClientUnitSchemaDesigner/1d5dfc4d-732d-48d7-af21-9e3d70794734` |
| Backend | `https://dev-pampabay.creatio.com/0/ClientApp/#/SourceCodeSchemaDesigner/ed794ab8-8a59-4c7e-983c-cc039449d178` |

### Test Commands

```bash
# API tests
source .env && python3 scripts/testing/test_report_service.py
source .env && CREATIO_REPORT_CODE=IW_Commission python3 scripts/testing/test_report_service.py

# Browser test
python3 scripts/investigation/review_report_flow.py --env dev
```

### Status IDs (QB Integration Log)

| Status | GUID |
|--------|------|
| Pending | `c97db3bc-634d-4c90-8432-ec7141c87640` |
| Processed | `e7428193-4cf1-4d1b-abae-00e93ab5e1c5` |
| Error | `bdfc60c7-55fd-4cbd-9a2c-dca2def46d80` |
| Processing | `fc2a1755-cdb8-43ec-a637-cdbcb6ef4bef` |
| Re-Process | `ff92e20c-da27-4255-96bc-57e32f0944f4` |

---

## Documentation Index

| Topic | Document |
|-------|----------|
| **Session history** | `docs/SESSION_HISTORY.md` |
| **Team summary** | `docs/TEAM_SUMMARY_20260120.md` |
| **BGlobal email draft** | `docs/EMAIL_BGLOBAL_REPORT_ISSUES.md` |
| **Handler versions** | `docs/HANDLER_VERSION_HISTORY.md` |
| **Filter requirements** | `docs/REPORT_FILTER_MAPPING.md` |
| **QB Sync automation** | `docs/QB_SYNC_AUTOMATION.md` |
| **DATA-001 investigation** | `docs/INVESTIGATION_PAYMENT_STATUS.md` |
| **IW_Commission strategy** | `docs/IW_COMMISSION_STRATEGY.md` |
| **Technical reference** | `docs/CLAUDE_REFERENCE.md` |
| **Change history** | `docs/CLAUDE_HISTORY.md` |
| **Test results** | `docs/TEST_LOG.md` |

### Scripts

| Purpose | Script |
|---------|--------|
| API baseline | `scripts/testing/test_report_service.py` |
| Dynamic filters | `scripts/testing/test_commission_dynamic_filters.py` |
| Browser flow | `scripts/investigation/review_report_flow.py` |
| IWQBIntegration | `scripts/investigation/check_iwqb_package.py` |
| QB sync filters | `scripts/investigation/check_qb_sync_process.py` |

---

## Rules

- Credentials in `.env` only (never in logs/docs/commits)
- Log test results to `docs/TEST_LOG.md`
- Hidden iframe is canonical download approach
- Optimize for v8/Freedom UI-first

---

## Gates Status

```
✅ Gate A: API baseline (Commission + IW_Commission)
✅ Gate B: Runtime verification (reportDownloadFrame marker)
✅ Gate C: DL-001 browser download
✅ Gate C2: DL-003 macro extension (.xlsm serving)
✅ Gate D: Dynamic filter sweep (3 combos)
✅ Gate E: FLT-004 regression testing
🔄 Gate F: Hardening
🔄 Gate G: PROD upgrade checklist
```

---

## Data Pipeline (Commission Reports)

```
ORDER → QB SYNC → QB INVOICE → QB PAYMENT → COMMISSION REPORT
         ↑           ↑            ↑              ↑
     SYNC-004    SYNC-005    QB Accounting    Working
```

Most missing commission data is due to unpaid invoices in QuickBooks.
