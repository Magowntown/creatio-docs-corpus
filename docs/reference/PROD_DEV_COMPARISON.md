# PROD vs DEV Code Comparison

**Date:** 2026-01-21
**Purpose:** Compare report components between PROD and DEV before consolidation

---

## Components to Compare

### 1. Backend Service: UsrExcelReportService

| Environment | URL |
|-------------|-----|
| **PROD** | `https://pampabay.creatio.com/0/ClientApp/#/SourceCodeSchemaDesigner/ed794ab8-8a59-4c7e-983c-cc039449d178` |
| **DEV** | `https://dev-pampabay.creatio.com/0/ClientApp/#/SourceCodeSchemaDesigner/ed794ab8-8a59-4c7e-983c-cc039449d178` |

**What to compare:**
- [ ] Total line count
- [ ] `GenerateWithDateFilter` method exists
- [ ] `GenerateIWCommissionWithDateFilter` method exists
- [ ] `SanitizeEsqJson` method exists (RPT-002 fix)
- [ ] IW_Commission handling in Generate method

**Local reference:** `source-code/UsrExcelReportService_Updated.cs`

---

### 2. Frontend Handler: UsrPage_ebkv9e8

| Environment | URL |
|-------------|-----|
| **PROD** | `https://pampabay.creatio.com/0/ClientApp/#/ClientUnitSchemaDesigner/561d9dd4-8bf2-4f63-a781-54ac48a74972` |
| **DEV** | `https://dev-pampabay.creatio.com/0/ClientApp/#/ClientUnitSchemaDesigner/561d9dd4-8bf2-4f63-a781-54ac48a74972` |

**What to compare:**
- [ ] Handler type (Hybrid vs old version)
- [ ] `usr.GenerateReportRequest` handler exists
- [ ] Looker Studio URL detection
- [ ] IntExcelReport lookup logic
- [ ] Commission filter visibility toggle

**Local reference:** `client-module/BGApp_eykaguu_UsrPage_ebkv9e8_Hybrid_v2.js`

---

### 3. SQL Views

**Query to check view existence:**
```sql
-- Run in both PROD and DEV pgAdmin
SELECT viewname FROM pg_views
WHERE schemaname = 'public'
AND viewname IN ('BGCommissionReportDataView', 'IWCommissionReportDataView');
```

**Query to get view definitions:**
```sql
-- BGCommissionReportDataView
SELECT pg_get_viewdef('"BGCommissionReportDataView"'::regclass, true);

-- IWCommissionReportDataView
SELECT pg_get_viewdef('"IWCommissionReportDataView"'::regclass, true);
```

**Expected:**
| View | PROD | DEV |
|------|------|-----|
| BGCommissionReportDataView | ✅ Should exist | ✅ Should exist |
| IWCommissionReportDataView | ❓ Check | ✅ Just created |

---

### 4. Entity Schemas

**Query to check entity schemas:**
```sql
SELECT s."Name", s."Caption", p."Name" as "Package", s."ModifiedOn"
FROM "SysSchema" s
JOIN "SysPackage" p ON s."SysPackageId" = p."Id"
WHERE s."Name" IN ('BGCommissionReportDataView', 'IWCommissionReportDataView')
ORDER BY s."Name";
```

---

### 5. IntExcelReport Configurations

**Query to compare configurations:**
```sql
SELECT
    r."IntName",
    r."IntSheetName",
    s."Name" as "EntitySchemaName",
    LENGTH(r."IntEsq") as "EsqLength",
    r."ModifiedOn"
FROM "IntExcelReport" r
LEFT JOIN "SysSchema" s ON r."IntEntitySchemaNameId" = s."Id"
WHERE r."IntName" IN ('Rpt Commission', 'Commission', 'IW_Commission')
ORDER BY r."IntName";
```

---

## Comparison Checklist

### PROD State (extract these)

- [ ] **UsrExcelReportService.cs** - Copy full code from PROD designer
- [ ] **UsrPage_ebkv9e8.js** - Copy full code from PROD designer
- [ ] **BGCommissionReportDataView SQL** - Run pg_get_viewdef query
- [ ] **IntExcelReport configs** - Run comparison query

### DEV State (verify these)

- [ ] **UsrExcelReportService.cs** - Should match local repo
- [ ] **UsrPage_ebkv9e8.js** - Should match local repo
- [ ] **IWCommissionReportDataView SQL** - Just created
- [ ] **IntExcelReport IW_Commission** - Just configured

---

## Quick Extraction Commands

### From PROD (run in browser console on PROD)

```javascript
// Get report configurations
fetch('/0/odata/IntExcelReport?$select=Id,IntName,IntSheetName,IntEsq&$filter=contains(IntName,\'Commission\')').then(r=>r.json()).then(console.log)
```

### From DEV (run in browser console on DEV)

```javascript
// Get report configurations
fetch('/0/odata/IntExcelReport?$select=Id,IntName,IntSheetName,IntEsq&$filter=contains(IntName,\'Commission\')').then(r=>r.json()).then(console.log)
```

---

## Expected Differences

| Component | Expected in PROD | Expected in DEV |
|-----------|------------------|-----------------|
| UsrExcelReportService | Full version with IW support | Same |
| UsrPage_ebkv9e8 | Hybrid handler | Same |
| BGCommissionReportDataView | ✅ Exists | ✅ Exists |
| IWCommissionReportDataView | ❓ May not exist | ✅ Just created |
| IntExcelReport Commission | ✅ Configured | ✅ Configured |
| IntExcelReport IW_Commission | ❓ May not be configured | ✅ Just configured |

---

## Next Steps After Comparison

1. **If PROD has newer code:** Copy PROD → DEV
2. **If DEV has newer code:** Verify and keep DEV version
3. **If IWCommissionReportDataView missing in PROD:** Will deploy from DEV later
4. **Document all differences** before making changes

