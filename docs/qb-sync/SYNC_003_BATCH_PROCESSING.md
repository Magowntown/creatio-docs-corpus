# SYNC-003: DEV Batch Processing Instructions

**Environment:** DEV (dev-pampabay.creatio.com)
**Issue:** 56,000+ pending records exceed 20K ESQ limit

---

## Prerequisites

1. Access to DEV PostgreSQL database (direct SQL access)
2. OR Creatio admin access to run business processes

---

## Option A: SQL Batch Processing (Recommended)

### Step 1: Check Current Counts

```sql
SELECT
    CASE "BGStatusId"
        WHEN 'c97db3bc-634d-4c90-8432-ec7141c87640' THEN 'Pending'
        WHEN 'e7428193-4cf1-4d1b-abae-00e93ab5e1c5' THEN 'Processed'
        WHEN 'bdfc60c7-55fd-4cbd-9a2c-dca2def46d80' THEN 'Error'
        WHEN 'fc2a1755-cdb8-43ec-a637-cdbcb6ef4bef' THEN 'Processing'
        WHEN 'ff92e20c-da27-4255-96bc-57e32f0944f4' THEN 'Re-Process'
        ELSE 'Unknown'
    END as status,
    COUNT(*) as count
FROM "BGQuickBooksIntegrationLogDetail"
GROUP BY "BGStatusId"
ORDER BY count DESC;
```

### Step 2: Move Older Pending to Re-Process (Keep Newest 15K)

```sql
-- Keep the newest 15,000 as Pending, move rest to Re-Process
WITH newest_pending AS (
    SELECT "Id"
    FROM "BGQuickBooksIntegrationLogDetail"
    WHERE "BGStatusId" = 'c97db3bc-634d-4c90-8432-ec7141c87640'  -- Pending
    ORDER BY "CreatedOn" DESC
    LIMIT 15000
)
UPDATE "BGQuickBooksIntegrationLogDetail"
SET "BGStatusId" = 'ff92e20c-da27-4255-96bc-57e32f0944f4'  -- Re-Process
WHERE "BGStatusId" = 'c97db3bc-634d-4c90-8432-ec7141c87640'  -- Pending
  AND "Id" NOT IN (SELECT "Id" FROM newest_pending);
```

### Step 3: Run QB Customer Order Integration

In Creatio DEV:
1. Go to System Designer → Business Processes
2. Find: "QB Customer Order Integration"
3. Click Run

### Step 4: Rotate Next Batch Back to Pending

```sql
-- Move next 15,000 from Re-Process back to Pending
WITH next_batch AS (
    SELECT "Id"
    FROM "BGQuickBooksIntegrationLogDetail"
    WHERE "BGStatusId" = 'ff92e20c-da27-4255-96bc-57e32f0944f4'  -- Re-Process
    ORDER BY "CreatedOn" DESC
    LIMIT 15000
)
UPDATE "BGQuickBooksIntegrationLogDetail"
SET "BGStatusId" = 'c97db3bc-634d-4c90-8432-ec7141c87640'  -- Pending
WHERE "Id" IN (SELECT "Id" FROM next_batch);
```

### Step 5: Repeat Steps 3-4

Repeat until all Re-Process records have been processed.

---

## Option B: Delete Old Pending Records (Quick Fix)

If the backlog isn't needed, you can delete older pending records:

```sql
-- WARNING: This deletes data permanently
-- Delete pending records older than 90 days
DELETE FROM "BGQuickBooksIntegrationLogDetail"
WHERE "BGStatusId" = 'c97db3bc-634d-4c90-8432-ec7141c87640'  -- Pending
  AND "CreatedOn" < NOW() - INTERVAL '90 days';
```

---

## Status Lookup Reference

| Status | GUID |
|--------|------|
| Pending | c97db3bc-634d-4c90-8432-ec7141c87640 |
| Processed | e7428193-4cf1-4d1b-abae-00e93ab5e1c5 |
| Error | bdfc60c7-55fd-4cbd-9a2c-dca2def46d80 |
| Processing | fc2a1755-cdb8-43ec-a637-cdbcb6ef4bef |
| Re-Process | ff92e20c-da27-4255-96bc-57e32f0944f4 |

---

## Expected Outcome

After batch processing:
- Pending count < 20,000
- QB Customer Order Integration runs successfully
- DEV commission data syncs for Nov 2025+
