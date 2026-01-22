# Source Code - Backend Services

> **Last Updated:** 2026-01-20
> **Currently Deployed:** `UsrExcelReportService_Updated.cs`

## Quick Reference

| Status | File | Purpose |
|--------|------|---------|
| ✅ **DEPLOYED** | `UsrExcelReportService_Updated.cs` | Main Excel report service (92KB) |
| ⚠️ Legacy | All other files | Historical versions, do not deploy |

## Deployment Information

**Schema UID:** `ed794ab8-8a59-4c7e-983c-cc039449d178`
**Package:** BGApp_eykaguu
**URL:** `https://pampabay.creatio.com/0/ClientApp/#/SourceCodeSchemaDesigner/ed794ab8-8a59-4c7e-983c-cc039449d178`

## Service Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/0/rest/UsrExcelReportService/Generate` | POST | Generate Excel report, returns key |
| `/0/rest/UsrExcelReportService/GetReport/{key}/{name}` | GET | Download generated report |

## Generate Request Format

```json
{
    "ReportId": "guid-of-IntExcelReport",
    "YearMonthId": "guid-or-empty-guid",
    "SalesRepId": "guid-or-empty-guid"
}
```

## Why This Service Exists

`IntExcelReportService` (Creatio's built-in service) has a known bug:
- `Generate` returns a key
- `GetReport/{key}` returns **404**
- Root cause: Library doesn't store file bytes in `SessionData`

`UsrExcelReportService` fixes this by:
1. Properly storing bytes in `userConnection.SessionData[key]`
2. Retrieving and serving bytes in `GetReport`

## File History

| Date | File | Notes |
|------|------|-------|
| 2026-01-20 | `UsrExcelReportService_Updated.cs` | **CURRENT** - Full featured |
| 2026-01-13 | `UsrExcelReportService_Simple.cs` | Simplified version |
| 2026-01-13 | `UsrExcelReportService_Standalone.cs` | Standalone attempt |
| Earlier | Other `_v2`, `_Fixed`, etc. | Historical iterations |

## Do Not Deploy

- `BGIntExcelReportService2_updated.cs` - Attempted to modify built-in service
- `UsrExcelReportService_WithFilters.cs` - Has filter issues
- Any file not listed as "DEPLOYED" above
