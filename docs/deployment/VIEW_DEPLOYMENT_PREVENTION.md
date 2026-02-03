# PostgreSQL View Deployment - Prevention Guide

**Created:** 2026-01-15
**Purpose:** Prevent future incidents where PostgreSQL views are missing in production

---

## Root Cause Analysis

### What Happened (2026-01-15)

The Commission report in PROD failed with:
```
PostgresException: 42P01: relation "public.BGCommissionReportDataView" does not exist
```

**Root cause:** The PostgreSQL view was never created in PROD. Only the Creatio entity schema (metadata) existed.

### Why It Happened

1. **Creatio entity schemas ≠ PostgreSQL views**
   - Entity schemas are metadata definitions stored in Creatio's configuration
   - They tell Creatio "this entity exists and has these columns"
   - They do NOT automatically create the underlying database object

2. **Views must be created manually via SQL**
   - When an entity schema references a view, the view must be created separately
   - No automatic sync exists between Creatio entity schemas and PostgreSQL views

3. **Missing verification step**
   - The deployment plan said "VERIFY SQL VIEW" but didn't explicitly check if the view existed
   - Assumption was made that the view would exist because the entity schema existed

---

## Critical Distinction

| Creatio Entity Schema | PostgreSQL View |
|-----------------------|-----------------|
| Configuration metadata | Actual database object |
| Stored in `SysSchema` table | Created via `CREATE VIEW` SQL |
| Defines columns/types for Creatio | Defines the actual SQL query |
| Does NOT create database object | MUST be created separately |
| Visible in Workspace Explorer | Visible in pgAdmin/database tools |

### How to Check

**Entity Schema (Creatio):**
```
Workspace Explorer → [Package] → Entities → [Entity Name]
```

**PostgreSQL View (Database):**
```sql
SELECT pg_get_viewdef('"ViewName"'::regclass, true);
```

If the view doesn't exist, you'll get:
```
ERROR: relation "ViewName" does not exist
```

---

## Pre-Deployment Checklist

### For Any View-Based Entity

Before deploying to any environment, verify BOTH:

- [ ] **Entity schema exists** in Creatio (Workspace Explorer)
- [ ] **PostgreSQL view exists** in database (`pg_get_viewdef`)
- [ ] **View SQL is correct** (matches expected query)
- [ ] **View returns data** (`SELECT * FROM "ViewName" LIMIT 5`)

### Verification Commands

```sql
-- 1. Check if view exists and get its definition
SELECT pg_get_viewdef('"BGCommissionReportDataView"'::regclass, true);

-- 2. Check if view returns data
SELECT * FROM public."BGCommissionReportDataView" LIMIT 5;

-- 3. Check row count (may be slow for large views)
SELECT COUNT(*) FROM public."BGCommissionReportDataView";
```

---

## View Inventory

### Current Views Requiring Manual SQL Deployment

| View Name | Package | SQL File | Notes |
|-----------|---------|----------|-------|
| `BGCommissionReportDataView` | IWQBIntegration | `scripts/sql/BGCommissionReportDataView_fix_PROD.sql` | Commission report data |
| `IWCommissionReportDataView` | IWQBIntegration | (pending) | IW_Commission report data |

### Required Columns for All Views

All views MUST include these BaseEntity columns:
```sql
"Id"                  -- UUID primary key
"CreatedOn"           -- Timestamp
"CreatedById"         -- UUID
"ModifiedOn"          -- Timestamp
"ModifiedById"        -- UUID
"ProcessListeners"    -- Integer (usually 0)
```

Without these columns, Creatio cannot treat the view as a proper entity.

---

## Deployment Process (Updated)

### Step 1: Deploy Entity Schema to Creatio
```
1. Open Workspace Explorer
2. Navigate to target package
3. Add/Update entity schema
4. Save and Compile
```

### Step 2: Deploy PostgreSQL View (CRITICAL - NEW EMPHASIS)
```sql
-- ALWAYS verify view exists BEFORE testing
SELECT pg_get_viewdef('"ViewName"'::regclass, true);

-- If error "relation does not exist", CREATE the view:
CREATE OR REPLACE VIEW public."ViewName" AS
  ... (full SQL) ...

-- Verify creation:
SELECT * FROM public."ViewName" LIMIT 5;
```

### Step 3: Test End-to-End
```
1. Generate report via UI
2. Verify data appears in report
3. Check filters work correctly
```

---

## Monitoring Recommendations

### Manual Check (Before Each Deployment)

Run this query to verify all expected views exist:
```sql
SELECT viewname
FROM pg_views
WHERE schemaname = 'public'
AND viewname IN (
  'BGCommissionReportDataView',
  'IWCommissionReportDataView'
  -- Add other views as needed
);
```

### Expected Results
- Row count should match number of views
- Missing views indicate deployment incomplete

### After Major Updates

After any Creatio upgrade or package deployment:
1. Re-run view existence check
2. Verify view definitions match expected SQL
3. Test report generation

---

## Recovery Procedure

If a view is missing:

1. **Get the SQL definition** from:
   - `scripts/sql/` directory in this repo
   - Previous environment (DEV/UAT)
   - Database backups

2. **Create the view:**
   ```sql
   CREATE OR REPLACE VIEW public."ViewName" AS
     ... (SQL from file) ...
   ```

3. **Verify:**
   ```sql
   SELECT * FROM public."ViewName" LIMIT 5;
   ```

4. **Compile Creatio** (may be necessary):
   - Configuration → Compile all

5. **Test the feature** that uses the view

---

## Lessons Learned

1. **Never assume views exist** - Always verify with `pg_get_viewdef`
2. **Entity schemas are metadata only** - They don't create database objects
3. **Document all views** - Keep SQL files in source control
4. **Test after deployment** - Don't just deploy, verify end-to-end

---

## Related Files

| Purpose | Location |
|---------|----------|
| BGCommissionReportDataView SQL | `scripts/sql/BGCommissionReportDataView_fix_PROD.sql` |
| IWCommissionReportDataView SQL | (pending creation) |
| Deployment plan | `docs/PROD_DEPLOYMENT_PLAN.md` |
| Test log | `docs/TEST_LOG.md` |

---

## Sign-Off Checklist Template

Use this for every view deployment:

| Item | DEV | PROD | Date |
|------|-----|------|------|
| Entity schema deployed | ☐ | ☐ | |
| **PostgreSQL view created** | ☐ | ☐ | |
| View returns data | ☐ | ☐ | |
| Report generation tested | ☐ | ☐ | |
| Filters tested | ☐ | ☐ | |

---

*This document created after 2026-01-15 PROD incident where Commission report failed due to missing PostgreSQL view.*
