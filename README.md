# Creatio Report Fix Project

> **AI Agents / New Sessions:** Start with `CLAUDE.md` for current status, then use `docs/AI_NAVIGATION.md` for scenario-based lookup.
>
> **Quick Status (2026-02-05):**
> - ✅ Reports COMPLETE - Handed to BGlobal/Rommel
> - 🔴 IWQBIntegration BLOCKED - Missing IWInterWeavePaymentApp in PROD
> - 🟡 QB Go-Live Ready - Pending confirmation

---

## 📍 Navigation Hub

### Entry Points

| Document | Purpose | When to Use |
|----------|---------|-------------|
| **`CLAUDE.md`** | Current status, active issues, quick deploy | **START HERE** for any session |
| `docs/AI_NAVIGATION.md` | Scenario → Document mapping | Finding docs by task |
| `docs/DOCUMENT_INDEX.md` | Complete 113+ document listing | Full documentation inventory |
| `docs/SHARED_UNDERSTANDING.md` | Consolidated system knowledge | Deep understanding needed |
| `docs/reference/RESOURCE_INVENTORY.md` | All available resources (17GB) | Finding files, code, examples |

### Quick Task Lookup

| Task | Start With |
|------|------------|
| **Freedom UI Development** | `docs/reference/CREATIO_SDK_REFERENCE.md` → `FreedomUIProjectTemplate_v5/` |
| **Report Fix** | `docs/reference/MASTER_CATALOG.md` → `docs/reference/HANDLER_VERSION_HISTORY.md` |
| **IWQBIntegration Import** | `docs/investigation/IWQBINTEGRATION_TEAM_INSTRUCTIONS.md` |
| **Commission Process** | `docs/investigation/COMMISSION_CALCULATION_INVESTIGATION.md` |
| **QB Sync Issues** | `docs/qb-sync/QB_SYNC_AUTOMATION.md` |
| **Platform Architecture** | `docs/reference/CREATIO_ARCHITECTURE_DEEP_DIVE.md` |
| **Code Examples** | `creatio-docs-full/code/` (1,496 directories) |

---

## 📁 Directory Structure

```
creatio-report-fix/
│
├── 📄 CLAUDE.md                    # ⭐ MAIN ENTRY POINT - Current status, issues
├── 📄 README.md                    # This navigation hub
├── 📄 package.json                 # Node dependencies (@creatio-devkit/common)
│
├── 📁 docs/                        # Project documentation (113+ documents)
│   ├── AI_NAVIGATION.md            # Scenario → Document mapping
│   ├── DOCUMENT_INDEX.md           # Complete document listing
│   ├── SHARED_UNDERSTANDING.md     # Consolidated knowledge
│   ├── investigation/              # Technical analysis (30+ docs)
│   ├── reference/                  # System knowledge (20+ docs)
│   ├── logs/                       # Session logs
│   ├── issues/                     # Issue-specific docs
│   ├── qb-sync/                    # QB integration
│   ├── deployment/                 # Deployment guides
│   └── communication/              # Emails, summaries
│
├── 📁 FreedomUIProjectTemplate_v5/ # ⭐ Angular 17 Freedom UI template (UNZIPPED)
│   ├── src/app/app.module.ts       # @CrtModule pattern example
│   ├── src/app/view-elements/      # Create components here
│   ├── webpack.config.js           # Module Federation config
│   └── package.json                # Angular 17 + SDK dependencies
│
├── 📁 creatio-docs-full/           # ⭐ Creatio Academy (5,000 pages)
│   ├── markdown/                   # Documentation (5,000 files)
│   ├── code/                       # Code examples (1,496 directories)
│   ├── html/                       # Original HTML
│   └── images/                     # Screenshots
│
├── 📁 client-module/               # Frontend handlers (99 versions)
│   └── BGApp_eykaguu_UsrPage_ebkv9e8_v54_FlatObject.js  # Current PROD
│
├── 📁 source-code/                 # Backend services (C#)
│   └── UsrExcelReportService_Updated.cs                 # Current PROD
│
├── 📁 scripts/                     # Automation scripts (90+)
│   ├── testing/                    # API and report tests
│   ├── investigation/              # Analysis scripts (14 creatio_*.py)
│   ├── deployment/                 # Deployment automation
│   └── crawlers/                   # Documentation scrapers
│
├── 📁 sql/                         # SQL view definitions (12 files)
│   ├── VwBGSalesByItemView_*.sql   # Sales By Item views
│   ├── BGCommissionReportDataView.sql
│   └── BGCustomerDidNotBuyView_ORIGINAL.sql
│
├── 📁 vba/                         # Excel macro fixes
│   └── PMPSalesbySalesRep_FIXED_v2.bas  # Infinite loop fix
│
├── 📁 investigation/               # Package analysis
│   └── IWQBIntegration/            # 4.4MB extracted package data
│
├── 📁 node_modules/                # NPM packages
│   ├── @creatio-devkit/common/     # ⭐ SDK v0.832.0
│   └── @creatio/base/              # Base types v0.832.0
│
└── 📁 creatio-docs-*/              # Additional doc crawls (12 variants)
```

---

## 🔧 Key Resources

### TypeScript SDK

| Resource | Location | Content |
|----------|----------|---------|
| SDK Reference | `docs/reference/CREATIO_SDK_REFERENCE.md` | Complete API guide |
| Type Definitions | `node_modules/@creatio-devkit/common/index.d.ts` | 99KB TypeScript types |
| Changelog | `node_modules/@creatio-devkit/common/CHANGELOG.md` | Version history |
| Project Template | `FreedomUIProjectTemplate_v5/` | Angular 17 starter |

### Code Examples (from Academy)

```bash
# Find remote module examples
find creatio-docs-full/code -path "*remote-module*" -name "*.js"

# Find validator examples
find creatio-docs-full/code -path "*validator*" -name "*.js"

# Find all Freedom UI examples
find creatio-docs-full/code -path "*freedom*" -name "*.js"
```

### D1 Development Guides (Windows)

Accessible via WSL at `/mnt/c/Creatio/D1_mkpdev-interweave/`:
- `CREATIO_DEVELOPMENT_COMPLETE_REFERENCE_GUIDE.md` (17KB)
- `CREATIO_SAFE_DEVELOPMENT_PRACTICES_GUIDE.md` (9KB)
- `CREATIO_QUICK_REFERENCE_ARCHITECTURE.md` (9KB)
- `CREATIO_OPTIMAL_PROMPTS_COLLECTION.md` (13KB)

---

## 🚀 Quick Commands

### Testing

```bash
# Load credentials
source .env

# Test report API
python3 scripts/testing/test_report_service.py

# Test specific report
CREATIO_REPORT_CODE=IW_Commission python3 scripts/testing/test_report_service.py

# Browser flow test
python3 scripts/investigation/review_report_flow.py --env dev
```

### Freedom UI Development

```bash
# Install SDK
npm install @creatio-devkit/common

# Use template (replace placeholders)
cd FreedomUIProjectTemplate_v5
# Replace <%projectName%> and <%vendorPrefix%> in all files
npm install
npm run build
# Copy dist/*.js to Creatio package File Content
```

---

## 📊 Project Status Summary

| Area | Status | Documentation |
|------|--------|---------------|
| **Reports** | ✅ Complete | Handed to BGlobal/Rommel |
| **IWQBIntegration** | 🔴 Blocked | `docs/investigation/IWQBINTEGRATION_TEAM_INSTRUCTIONS.md` |
| **QB Go-Live** | 🟡 Ready | Monitor stability |
| **Commission Process** | 📋 Documented | `docs/investigation/COMMISSION_CALCULATION_INVESTIGATION.md` |

---

## 📚 For AI Agents / New Sessions

### Recommended Reading Order

1. **`CLAUDE.md`** - Current status, active tasks, gotchas
2. **`docs/AI_NAVIGATION.md`** - Find documents by scenario
3. **Task-specific document** - Based on what you need to do
4. **`docs/reference/RESOURCE_INVENTORY.md`** - If you need to find resources

### Key Gotchas (from CLAUDE.md)

- WCF date format required: `/Date(milliseconds)/` not ISO 8601
- Customer filter MUST be LOOKUP, not text
- Only ONE data source per Freedom UI page
- V3 commission process has 26x cascade bug - keep disabled
- Template uses `<%projectName%>` and `<%vendorPrefix%>` placeholders

---

## 🔗 Environment

| Env | URL | Purpose |
|-----|-----|---------|
| PROD | pampabay.creatio.com | Production |
| DEV | dev-pampabay.creatio.com | Development |
| DEV (MKP) | mkpdev-interweave.creatio.com | Package development |

---

## 📦 Dependencies

```json
{
  "@creatio-devkit/common": "^0.832.0",
  "@creatio/base": "^0.832.0",
  "puppeteer": "^24.35.0"
}
```

---

*Last Updated: 2026-02-05*
