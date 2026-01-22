# Creatio Report Fix Project

> **AI Agents:** Start with `CLAUDE.md` for complete status, issues, and session history.
>
> **Quick Status (2026-01-20):**
> - ✅ Commission Excel reports working
> - ❌ Looker Studio blocked (CSP + Google permissions)
> - ❌ Other Excel reports have template issues
> - 📧 Email sent to BGlobal for resolution

## Current State

| Component | Status | Blocker |
|-----------|--------|---------|
| Commission (Excel) | ✅ Working | Data accuracy (QB payments) |
| Looker Studio reports | ❌ Blocked | CSP + Google permissions |
| Other Excel reports | ❌ Blocked | IntExcelReport template config |

## Deployed Components

| Component | File | Schema UID |
|-----------|------|------------|
| **Frontend Handler** | `client-module/BGApp_eykaguu_UsrPage_ebkv9e8_Hybrid_v2.js` | `561d9dd4-8bf2-4f63-a781-54ac48a74972` |
| **Backend Service** | `source-code/UsrExcelReportService_Updated.cs` | `ed794ab8-8a59-4c7e-983c-cc039449d178` |

## Key Documentation

| Document | Purpose |
|----------|---------|
| `CLAUDE.md` | **START HERE** - Full status, issues, session logs |
| `docs/EMAIL_BGLOBAL_REPORT_ISSUES.md` | Email to BGlobal about blocking issues |
| `docs/TEST_LOG.md` | Test results and verification |
| `client-module/README.md` | Handler file index |
| `source-code/README.md` | Service file index |

## Environment

| Env | URL | Creatio Version |
|-----|-----|-----------------|
| PROD | pampabay.creatio.com | v8 (Freedom UI) |
| DEV | dev-pampabay.creatio.com | v8 (Freedom UI) |

## Current Architecture

```
User selects report → Clicks "Generate"
         ↓
    Has Looker URL?
    ├─ YES → window.open() in new tab
    │        ⚠️ Blocked by Google permissions
    └─ NO  → UsrExcelReportService
              ↓
              Resolve report name → IntExcelReport ID
              ↓
              Generate Excel → Download via iframe
              ✅ Working for Commission
              ❌ Template errors for others
```

## Known Issues (2026-01-20)

### CSP-001: Looker Studio Iframes Blocked
- Freedom UI (v8) blocks external iframes via Content Security Policy
- Original system used iframes, now broken after v7→v8 migration

### LOOKER-001: Google Permissions Required
- Workaround (new tab) requires Google account access to dashboards
- BGlobal needs to configure sharing permissions

### RPT-004: Excel Template Errors
- Reports without Looker URLs fall back to Excel
- IntExcelReport configurations have issues ("Row out of range", etc.)

### DATA-002: Commission Data Gap
- Dec 2025 / Jan 2026 data ~93% missing
- Root cause: QuickBooks invoices not marked as paid
- Not a technical issue - requires QB accounting action

## Awaiting BGlobal Response

1. CSP configuration to whitelist Looker Studio
2. Google permissions for Looker Studio dashboards
3. IntExcelReport template review
4. QuickBooks payment processing for Commission data

## Directory Structure

```
creatio-report-fix/
├── CLAUDE.md                 # Main status & documentation
├── README.md                 # This file
├── .env                      # Credentials (not in git)
├── client-module/            # Frontend handlers (JS)
│   ├── README.md             # Handler file index
│   └── BGApp_eykaguu_*.js    # Handler versions
├── source-code/              # Backend services (C#)
│   ├── README.md             # Service file index
│   └── UsrExcelReportService_*.cs
├── docs/                     # Documentation
│   ├── TEST_LOG.md           # Test results
│   ├── EMAIL_BGLOBAL_*.md    # Communications
│   └── *.md                  # Various analysis docs
├── scripts/                  # Utility scripts
│   ├── testing/              # Test scripts
│   ├── investigation/        # Analysis scripts
│   └── deployment/           # Deploy scripts
└── creatio-docs-*/           # Crawled Creatio documentation
```

## For New AI Sessions

1. Read `CLAUDE.md` - Contains full context and issue tracking
2. Check `docs/TEST_LOG.md` - Recent test results
3. Review `client-module/README.md` - Which handler is deployed
4. Review `source-code/README.md` - Which service is deployed

## Credentials

Stored in `.env` (not committed):
```
CREATIO_URL=https://pampabay.creatio.com
CREATIO_USERNAME=***
CREATIO_PASSWORD=***
```

## Quick Commands

```bash
# Load credentials
source .env

# Test API
python3 scripts/testing/test_report_service.py
```
