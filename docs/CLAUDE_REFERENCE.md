# CLAUDE_REFERENCE.md - Technical Reference

> This file contains detailed technical reference. For current status, see `CLAUDE.md`.

---

## Platform Context

- **PROD:** Creatio v7 (Classic UI) - may have Classic-era patterns
- **DEV:** Creatio v8 (Freedom UI) - target for migration
- **Plan:** Upgrade PROD to v8, then align DEV packages into PROD

---

## Creatio Schema Types

| Type | Purpose | Designer URL |
|------|---------|--------------|
| Entity Schema | Database tables | `/EntitySchemaDesigner/{uid}` |
| Client Unit Schema | Frontend JS (Freedom UI) | `/ClientUnitSchemaDesigner/{uid}` |
| Source Code Schema | Backend C# services | `/SourceCodeSchemaDesigner/{uid}` |

### Project Schemas

| Schema | Type | UId |
|--------|------|-----|
| `UsrPage_ebkv9e8` | Client Unit | `1d5dfc4d-732d-48d7-af21-9e3d70794734` |
| `UsrExcelReportService` | Source Code | `ed794ab8-8a59-4c7e-983c-cc039449d178` |

---

## Freedom UI Handler Pattern

```javascript
define("UsrPage_ebkv9e8", [], function() {
    return {
        viewConfigDiff: [...],
        viewModelConfigDiff: [...],
        handlers: [
            {
                request: "usr.GenerateExcelReportRequest",
                handler: async (request, next) => {
                    const context = request.$context;
                    const report = await context.LookupAttribute_bsixu8a;
                    // ... logic ...
                    return next?.handle(request);
                }
            }
        ]
    };
});
```

### Lookup Attribute Mappings

| Attribute Name | Maps To | Returns |
|----------------|---------|---------|
| `LookupAttribute_bsixu8a` | BGPampaReport | `{ value: guid, displayValue: name }` |
| `LookupAttribute_yubshr1` | BGYearMonth | `{ value: guid, displayValue: "2025-10" }` |
| `LookupAttribute_nt0mer7` | BGSalesGroup | `{ value: guid, displayValue: name }` |

---

## API Patterns

### Authentication
```javascript
const getCookie = (name) => {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return "";
};
const bpmcsrf = getCookie("BPMCSRF");
```

### OData Query
```
GET /0/odata/EntityName?$filter=Column eq 'value'&$select=Id,Name
```

### REST Service Call
```javascript
fetch("/0/rest/ServiceName/MethodName", {
    method: "POST",
    headers: { "Content-Type": "application/json", "BPMCSRF": bpmcsrf },
    body: JSON.stringify({ ... })
});
```

---

## Working Download Code (Canonical)

```javascript
let iframe = document.getElementById('reportDownloadFrame');
if (!iframe) {
    iframe = document.createElement('iframe');
    iframe.id = 'reportDownloadFrame';
    iframe.style.display = 'none';
    iframe.setAttribute('aria-hidden', 'true');
    document.body.appendChild(iframe);
}
iframe.src = downloadUrl;
```

**Why this works:** No popup blocker, cookies sent automatically, Content-Disposition triggers download.

---

## Entity Relationships

```
UsrReportesPampa (UI dropdown)
    ├── Name (display)
    ├── UsrCode (stable, use for downloads)
    └──► IntExcelReport (template)
            ├── IntName
            ├── IntEntitySchemaName (data source)
            └── IntEsq (query JSON)
```

---

## Known-Good Test Values (DEV)

| Item | Value |
|------|-------|
| Commission IntExcelReport.Id | `4ba4f203-7088-41dc-b86d-130c590b3594` |
| IW_Commission IntExcelReport.Id | `07c77859-b7e5-43f3-97c6-14113f6a1f6f` |
| YearMonth (2025-08) | `aa1cdcc3-2666-439e-b702-4358b1b32c61` |
| SalesGroup (Pampa Bay - Online) | `83865e16-417e-4675-96d5-9c04c476d032` |

---

## Filter Column Paths

| Report | Entity | YearMonth Column | SalesGroup Column |
|--------|--------|------------------|-------------------|
| Commission | BGCommissionReportDataView | `BGYearMonth` | `BGSalesRep.BGSalesGroupLookup` |
| IW_Commission | IWPayments | `IWBGYearMonth` | `IWPaymentsInvoice.BGSalesGroup` |

---

## Deployment Steps

### Frontend Handler

1. Open: `https://dev-pampabay.creatio.com/0/ClientApp/#/ClientUnitSchemaDesigner/1d5dfc4d-732d-48d7-af21-9e3d70794734`
2. `Ctrl+A` → Paste `client-module/UsrPage_ebkv9e8_Updated.js`
3. `Ctrl+S` to save

### Backend Service

1. Open: `https://dev-pampabay.creatio.com/0/ClientApp/#/SourceCodeSchemaDesigner/ed794ab8-8a59-4c7e-983c-cc039449d178`
2. `Ctrl+A` → Paste `source-code/UsrExcelReportService_Updated.cs`
3. `Ctrl+S` → Actions → Publish

---

## DEV vs PROD Behavior

**PROD (pre-upgrade):**
- `POST /0/rest/IntExcelReportService/GetExportFiltersKey` returns key
- Download via `GET /0/rest/IntExcelReportService/GetExportFilteredData/{fileName}/{key}`
- Filtering is execution-context driven (BGExecutionId)

**DEV (v8):**
- `POST /0/rest/UsrExcelReportService/Generate` returns key
- Download via `GET /0/rest/UsrExcelReportService/GetReport/{key}/{reportName}`
- Filtering is FiltersConfig-driven

---

## Known Issues

### Playwright MCP Timeout
Browser automation times out after ~30 seconds. Use ChatGPT for long browser tests.

### Schema Designer Paste Issues
Use `Ctrl+A` → paste → `Ctrl+S`. Refresh if it fails.

---

## Issue Details

### DL-003B: FormatException Fix
`IntExcelReport.IntEntitySchemaName` can be a lookup. Reading with `GetTypedColumnValue<string>` throws FormatException.

**Fix:** Use ESQ joined lookup name (`IntEntitySchemaName.Name`) aliased as `IntEntitySchemaNameName`.

### FLT-004: Empty Commission Data
`BGYearMonthId` is NOT POPULATED in DEV. Lookup-based Year-Month filtering matches 0 rows.

**Workaround options:**
1. Service workaround: filter by `BGTransactionDate` date-range
2. Data fix: populate the Year-Month field

---

---

# Workflows

## TDD Cycle (Mandatory)

```
1. ISSUE → 2. TEST PLAN → 3. SOLUTION → 4. VERIFY → 5. LOG → 6. UPDATE DOCS
```

### Before ANY Code Change, Answer:
1. **What test proves this is broken?** (Run it, log the failure)
2. **What test proves this is fixed?** (Define it BEFORE coding)
3. **How will I verify?** (API script? Browser test? Manual?)
4. **Where will I log results?** (`docs/TEST_LOG.md`)

### Test Logging Format

```markdown
## Test Log: [YYYY-MM-DD] - [Issue ID] [Issue Name]

**Issue:** [Clear description]
**Goal:** [What success looks like]

**Test Plan:**
1. [Step]
2. [Step]

**Results:**
- [ ] Step 1: PASS/FAIL - [Evidence]
- [ ] Step 2: PASS/FAIL - [Evidence]

**Conclusion:** PASS/FAIL
**Next Action:** [What's next]
```

### Verification Methods

| What to Verify | Command/Method |
|----------------|----------------|
| API baseline | `python3 scripts/testing/test_report_service.py` |
| Handler deployed | Search for `reportDownloadFrame` in compiled JS |
| Browser download | `python3 scripts/investigation/review_report_flow.py --env dev` |
| Excel content | Open file, check Data sheet for filter values |
| Dynamic filters | `python3 scripts/testing/test_commission_dynamic_filters.py --env dev` |

---

## Multi-AI Collaboration

### AI Capabilities Matrix

| Task | Claude Code | ChatGPT | Gemini |
|------|-------------|---------|--------|
| Code editing | ✅ **Primary** | ❌ | ❌ |
| File operations | ✅ **Primary** | ❌ | ❌ |
| API testing | ✅ **Primary** | ❌ | ❌ |
| Long browser waits (30+ sec) | ❌ Timeout | ✅ **Primary** | ❌ |
| Screenshot capture | ⚠️ Limited | ✅ **Primary** | ❌ |
| Code review | ✅ Good | ✅ Good | ✅ **Best** |
| Debug analysis | ✅ Good | ✅ Good | ✅ **Best** |

### Roles

- **Claude Code:** edits files, deploys schema/service, runs test scripts, logs results
- **ChatGPT:** browser testing with long waits (60-90s), screenshot capture
- **Gemini:** code review, regression analysis, upgrade resilience check

### Handoff Checklist

Every handoff must include:
- Issue ID + environment (DEV/PROD)
- What changed (files modified)
- How it was verified (script output or browser evidence)
- Next action recommendation

---

## Test Prompts for Other AIs

### ChatGPT Browser Test
```
Test Creatio report download:
1. Login: https://dev-pampabay.creatio.com
2. Navigate: /Navigation/Navigation.aspx?schemaName=UsrPage_ebkv9e8
3. Select: Commission, 2025-10, Pampa Bay - Online
4. Click Report, wait 90s
5. Check ~/Downloads for .xlsm file

Report format:
- Login: PASS/FAIL
- Page loaded: PASS/FAIL
- Download completed: PASS/FAIL
- File downloaded: [filename or NONE]
```

### ChatGPT Handler Deployment (Gate B)
```
Deploy Creatio handler:
1. Login: https://dev-pampabay.creatio.com (Supervisor)
2. Open: /0/ClientApp/#/ClientUnitSchemaDesigner/1d5dfc4d-732d-48d7-af21-9e3d70794734
3. Ctrl+A → Delete → Paste code from client-module/UsrPage_ebkv9e8_Updated.js
4. Ctrl+S to save
5. Search for "reportDownloadFrame" to verify

Report: DEPLOYED/NOT_DEPLOYED
```

### Gemini Code Review
```
Review client-module/UsrPage_ebkv9e8_Updated.js for:
1. Error handling
2. Browser compatibility
3. OData injection risks
4. Race conditions
5. Edge cases
```

---

## Gate Definitions (Full)

| Gate | Description | Pass Criteria |
|------|-------------|---------------|
| A | API baseline | `test_report_service.py` passes for Commission + IW |
| B | Runtime verification | `reportDownloadFrame` marker found in compiled JS |
| C | DL-001 browser download | .xlsx downloads successfully |
| C2 | DL-003 durability | .xlsm served for macro-enabled files |
| D | Dynamic filter sweep | 3+ combos validated |
| E | Regression testing | Other reports work end-to-end |
| F | Hardening | Edge cases, error messages, double-click protection |
| G | PROD upgrade checklist | Deployment steps documented |

---

## DataService vs OData (Important Discovery - 2026-01-15)

**Finding:** OData queries may return empty results even with valid authentication, while DataService works correctly.

### When to Use DataService

Use DataService (`/0/DataService/json/SyncReply/SelectQuery`) instead of OData when:
- OData returns empty with no error
- Need reliable data access for investigation
- Querying custom BG/IW entities

### DataService Query Pattern

```bash
# Get CSRF token from cookies
CSRF=$(grep BPMCSRF /tmp/cookies_prod.txt | tail -1 | awk '{print $NF}')

# Query example
curl -s -b /tmp/cookies_prod.txt \
  "${CREATIO_PROD_URL}/0/DataService/json/SyncReply/SelectQuery" \
  -H "Content-Type: application/json" -H "BPMCSRF: $CSRF" \
  -d '{
    "rootSchemaName": "EntityName",
    "operationType": 0,
    "columns": {"items": {
      "Column1": {"expression": {"columnPath": "Column1"}},
      "Column2": {"expression": {"columnPath": "Column2"}}
    }},
    "allColumns": false,
    "rowCount": 10,
    "orderByItems": [{"orderType": 1, "columnPath": "CreatedOn"}]
  }'
```

### Useful DataService Queries

```bash
# Count records
-d '{"rootSchemaName": "EntityName", "operationType": 0,
  "columns": {"items": {"count": {"expression": {"expressionType": 1, "functionType": 2, "aggregationType": 1, "functionArgument": {"expressionType": 0, "columnPath": "Id"}}}}},
  "allColumns": false}'

# Get all columns (discover schema)
-d '{"rootSchemaName": "EntityName", "operationType": 0, "allColumns": true, "rowCount": 1}'
```

---

## QuickBooks Integration Process Reference

### Process: Get QuickBooks Commissions

- **Schema Name:** `BGBPGetQuickBooksCommissions`
- **Purpose:** Download payment data from QuickBooks Desktop to Creatio
- **Target Table:** `BGCommissionReportQBDownload`

### Process Flow

```
Start → "Get QB Filter Dates" (User Task) → QB API Call → Insert to BGCommissionReportQBDownload → End
           ↑
           └── BLOCKS HERE if no date input
```

### Known Issue (SYNC-001)

The process requires manual date input and will wait indefinitely at "Get QB Filter Dates" element.

**Query to find stuck processes:**
```bash
curl -s -b /tmp/cookies_prod.txt \
  "${CREATIO_PROD_URL}/0/DataService/json/SyncReply/SelectQuery" \
  -H "BPMCSRF: $CSRF" \
  -d '{
    "rootSchemaName": "SysProcessLog",
    "operationType": 0,
    "columns": {"items": {
      "Name": {"expression": {"columnPath": "Name"}},
      "StartDate": {"expression": {"columnPath": "StartDate"}},
      "Status": {"expression": {"columnPath": "Status.Name"}}
    }},
    "filters": {"filterType": 6, "isEnabled": true, "items": {
      "nameFilter": {"filterType": 1, "comparisonType": 11,
        "leftExpression": {"expressionType": 0, "columnPath": "Name"},
        "rightExpression": {"expressionType": 2, "parameter": {"dataValueType": 1, "value": "%QuickBooks%"}}
      }
    }},
    "rowCount": 20,
    "orderByItems": [{"orderType": 1, "columnPath": "StartDate"}]
  }'
```

**Query to check which element is stuck:**
```bash
curl -s -b /tmp/cookies_prod.txt \
  "${CREATIO_PROD_URL}/0/DataService/json/SyncReply/SelectQuery" \
  -H "BPMCSRF: $CSRF" \
  -d '{
    "rootSchemaName": "SysProcessElementLog",
    "operationType": 0,
    "columns": {"items": {
      "Caption": {"expression": {"columnPath": "Caption"}},
      "Status": {"expression": {"columnPath": "Status.Name"}}
    }},
    "filters": {"filterType": 6, "isEnabled": true, "items": {
      "processFilter": {"filterType": 1, "comparisonType": 3,
        "leftExpression": {"expressionType": 0, "columnPath": "SysProcess.Id"},
        "rightExpression": {"expressionType": 2, "parameter": {"dataValueType": 0, "value": "PROCESS_INSTANCE_ID"}}
      }
    }}
  }'
```

---

## Commission Report Data Flow

```
QuickBooks Desktop (external)
       ↓
BGBPGetQuickBooksCommissions (Creatio process)
       ↓
BGCommissionReportQBDownload (table - QB payment data)
       ↓
BGCommissionReportDataView (PostgreSQL view - JOINs 3 tables)
       ↓
UsrExcelReportService (C# - generates Excel)
       ↓
UsrPage_ebkv9e8 (JS - downloads via iframe)
       ↓
User's browser (receives .xlsm file)
```

### Key Tables for Commission Reports

| Table | Purpose | Last Updated (PROD) |
|-------|---------|---------------------|
| `BGCommissionReportQBDownload` | QB payment data | Jan 8, 2026 ✅ |
| `Order` | Sales orders | Active |
| `BGCommissionEarner` | Rep assignments | Active |
| `BGReportExecution` | Execution context | Active |

---

## December 2025 Data Gap Analysis (2026-01-15, Updated)

### Client Observation

> "Receiving Returns on the reports but not Sales"

### Complete Data Flow Investigation

**Full path traced:** Creatio Orders → QB Invoices → QB ReceivePayments → Commission Data

```
Creatio Orders → QB Invoices → [Awaiting Payment] → QB ReceivePayments → Commission Data
     ✅              ✅               ❌                    ❌                    ❌
  (EXISTS)       (SYNCED)        (NOT DONE)           (DOESN'T EXIST)        (MISSING)
```

### Key Findings

| Stage | Status | Evidence |
|-------|--------|----------|
| Dec 2025 Orders in Creatio | ✅ EXISTS | ORD-15159, ORD-15299, ORD-14800, ORD-14901, ORD-15110, etc. |
| Orders synced to QB (Invoices) | ✅ SYNCED | All have `BGQuickBooksId` populated |
| Invoices marked as Paid in QB | ❌ NOT DONE | No `ReceivePayment` records in QB |
| ReceivePayments synced back | ❌ NONE | Commission sync finds nothing to import |

### Commission Data (PROD)

| Month | Sales | Credit Memos (Returns) | Total |
|-------|-------|------------------------|-------|
| **Dec 2025** | **0** | **39** | **39** |
| Nov 2025 | 485 | 16 | 501 |
| Oct 2025 | ~400 | ~20 | ~420 |

### Root Cause (Confirmed)

**December 2025 invoices exist in QuickBooks but haven't been marked as "paid".**

The commission sync queries `ReceivePayment` records (created when invoices are paid), NOT `Invoice` records.

### Technical Analysis: BGQuickBooksService.cs

**GetQuickBooksReceivedPayments method (lines 2053-2112):**
```csharp
qSearch.QueryType = ObjsearchQueryTypes.qtReceivePaymentSearch;
// Queries QB for ReceivePayment records (NOT Invoices)
// ReceivePayments are created when invoices are PAID
```

**GetQuickBooksCreditMemos method (lines 2121-2181):**
```csharp
qSearch.QueryType = ObjsearchQueryTypes.qtCreditMemoSearch;
qSearch.SearchCriteria.PaidStatus = TPaidStatus.psPaid;
// Queries QB for Credit Memo records with PaidStatus = Paid
```

**Key Insight:** Commission sync pulls `ReceivePayment` records. An invoice must be marked as paid in QuickBooks for a ReceivePayment to exist.

### Verification Queries

**OData (recommended for large tables):**
```bash
# Total commission records
curl "${URL}/0/odata/BGCommissionReportQBDownload/\$count"

# Most recent synced records
curl "${URL}/0/odata/BGCommissionReportQBDownload?\$orderby=CreatedOn desc&\$top=10"

# December 2025 orders with QB sync status
curl "${URL}/0/odata/Order?\$filter=CreatedOn ge 2025-12-01T00:00:00Z and CreatedOn lt 2026-01-01T00:00:00Z&\$select=Number,BGQuickBooksId"
```

**Note:** DataService API may return incorrect results for large tables. Use OData for `BGCommissionReportQBDownload` (10,020+ records).

### Data Direction (Important)

```
Creatio Orders  ──────────────────►  QuickBooks Invoices  ──────────────────►  QB ReceivePayments
                (Order sync)                              (Manual in QB)
                                                                 │
                                                                 ▼
Commission Reports  ◄──────────────  BGCommissionReportQBDownload
                    (Commission sync)
```

### Action Required

**QuickBooks accounting team** needs to:
1. Process payments against December 2025 invoices
2. Mark invoices as "paid" to create ReceivePayment records
3. The next commission sync will automatically pull the data
