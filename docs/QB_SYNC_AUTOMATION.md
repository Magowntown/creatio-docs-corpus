# QuickBooks Sync Process Automation Guide

> **Target Process:** `BGBPGetQuickBooksCommissions`
> **Package:** `PampaBayQuickBooks`
> **Process UId:** `7b1ac959-1726-4340-bc66-210b31f5f365`

---

## Process Designer URL

**PROD:** https://pampabay.creatio.com/0/Nui/ViewModule.aspx?vm=SchemaDesigner#process/7b1ac959-1726-4340-bc66-210b31f5f365/

---

## Current State

```
[Start] → [Get QB Filter Dates - User Task] → [QB API Logic] → [End]
              ↑
              └── BLOCKS HERE waiting for manual date input
```

---

## Target State (After Automation)

```
[Start/Timer] → [Calculate Dates - Script Task] → [Conditional Gateway]
                                                         ↓
                        ┌────────────────────────────────┴────────────────────────────────┐
                        ↓                                                                  ↓
               [DatesAutoCalculated=true]                                    [DatesAutoCalculated=false]
                        ↓                                                                  ↓
               [Skip to QB API Logic]                                      [Get QB Filter Dates - User Task]
                        ↓                                                                  ↓
                        └────────────────────────────────┬────────────────────────────────┘
                                                         ↓
                                                [QB API Logic]
                                                         ↓
                                                      [End]
```

---

## Implementation Steps

### Step 1: Open Process Designer

1. Navigate to: https://pampabay.creatio.com/0/ClientApp/#/ProcessDesigner/7b1ac959-1726-4340-bc66-210b31f5f365
2. Click **Edit** to enable modifications
3. Note the current elements and their connections

### Step 2: Add Process Parameters

Add these new parameters (if not already existing):

| Parameter Name | Type | Direction | Default |
|----------------|------|-----------|---------|
| `DatesAutoCalculated` | Boolean | Input/Output | `true` |
| `CreatedStartDate` | DateTime | Input/Output | (empty) |
| `CreatedEndDate` | DateTime | Input/Output | (empty) |

**How to add:**
1. Click the process canvas background (deselect all elements)
2. In Properties panel, click **Parameters**
3. Click **Add** for each parameter
4. Set Name, Type, and Default Value

### Step 3: Add Script Task Element

1. From the element palette, drag a **Script Task** element onto the canvas
2. Place it **between Start and the existing "Get QB Filter Dates" user task**
3. Name it: `Calculate Sync Dates`

**Script Task Code:**

```csharp
// Calculate QuickBooks sync date range automatically
// Start Date = Last successful sync date (or 90 days ago if no records)
// End Date = Current date/time

using Terrasoft.Core.DB;
using System;

// Query for the most recent CreatedOn in BGCommissionReportQBDownload
var select = new Select(UserConnection)
    .Top(1)
    .Column("CreatedOn")
    .From("BGCommissionReportQBDownload")
    .OrderByDesc("CreatedOn") as Select;

DateTime startDate;
using (var dbExecutor = UserConnection.EnsureDBConnection()) {
    using (var reader = select.ExecuteReader(dbExecutor)) {
        if (reader.Read()) {
            startDate = reader.GetDateTime(0);
            // Add 1 second to avoid re-processing the last record
            startDate = startDate.AddSeconds(1);
        } else {
            // No existing records - start from 90 days ago
            startDate = DateTime.UtcNow.AddDays(-90);
        }
    }
}

DateTime endDate = DateTime.UtcNow;

// Set the process parameters
Set<DateTime>("CreatedStartDate", startDate);
Set<DateTime>("CreatedEndDate", endDate);
Set<bool>("DatesAutoCalculated", true);

// Log for debugging
var message = string.Format("Auto-calculated sync dates: {0} to {1}",
    startDate.ToString("yyyy-MM-dd HH:mm:ss"),
    endDate.ToString("yyyy-MM-dd HH:mm:ss"));
// Optional: Log to integration log or console

return true;
```

### Step 4: Add Conditional Gateway (Optional)

If you want to allow manual override:

1. Add an **Exclusive Gateway** element after the Script Task
2. Create two sequence flows:
   - **Auto path:** Condition `[#DatesAutoCalculated#] == true` → Goes directly to QB API logic
   - **Manual path:** Condition `[#DatesAutoCalculated#] == false` → Goes to "Get QB Filter Dates" user task

**Alternatively (Simpler):** Just remove the user task entirely and always use auto-calculated dates.

### Step 5: Connect the Elements

1. Delete the connection from Start to "Get QB Filter Dates"
2. Connect: `Start → Calculate Sync Dates → (Gateway or directly to QB API logic)`
3. If using gateway: Connect both paths to converge at the QB API logic element

### Step 6: Add Timer Start Event (Optional)

For automated scheduling:

1. Add a **Timer Start Event** element
2. Configure the timer:
   - **Cron expression:** `0 0 2 * * ?` (runs daily at 2:00 AM)
   - Or use the visual scheduler to set daily/weekly

3. Connect the Timer Start Event to the Script Task

### Step 7: Save and Publish

1. Click **Save**
2. Click **Publish** to compile the changes
3. Test by starting the process manually

---

## Testing the Automation

### Test 1: Manual Start (No Timer)

1. Go to Process Log
2. Start a new instance of "Get QuickBooks Commissions"
3. Verify it runs without requiring date input
4. Check BGCommissionReportQBDownload for new records

### Test 2: Verify Date Calculation

Check the process parameters after execution:
- `CreatedStartDate` should be slightly after the last sync date
- `CreatedEndDate` should be current date/time

### Test 3: Timer Execution (If Added)

1. Wait for the scheduled time
2. Verify process started automatically in Process Log
3. Verify new data synced

---

## Rollback Plan

If issues occur:

1. Open Process Designer
2. Revert to previous version (Creatio keeps version history)
3. Or: Remove the Script Task and reconnect Start directly to "Get QB Filter Dates"

---

## Verification SQL

After automated sync runs:

```sql
-- Check new records synced
SELECT COUNT(*), MAX("CreatedOn"), MIN("CreatedOn")
FROM "BGCommissionReportQBDownload"
WHERE "CreatedOn" > NOW() - INTERVAL '1 day';

-- Check date range of synced data
SELECT
    DATE_TRUNC('month', "BGTransactionDate") as month,
    COUNT(*) as records
FROM "BGCommissionReportQBDownload"
GROUP BY DATE_TRUNC('month', "BGTransactionDate")
ORDER BY month DESC
LIMIT 12;
```

---

## Files Related to This Change

| File | Purpose |
|------|---------|
| `docs/QB_SYNC_AUTOMATION.md` | This guide |
| `docs/ACTION_PLAN.md` | Overall action plan |
| `docs/CLAUDE_REFERENCE.md` | Process reference |

---

## Deployment Status

### Phase 1: Simplified Script ✅ DEPLOYED

**Deployed:** 2026-01-15
**Script:**
```csharp
DateTime startDate = DateTime.UtcNow.AddDays(-30);
DateTime endDate = DateTime.UtcNow;
Set<DateTime>("AutoStartDate", startDate);
Set<DateTime>("AutoEndDate", endDate);
return true;
```

**Verification Results:**
| Sync Date | Records | Notes |
|-----------|---------|-------|
| Jan 8, 2026 | 2 | Automated run with 30-day window |
| Jan 6, 2026 | 37 | Manual sync (initial catch-up) |

### Phase 2: Full ESQ Script (NEXT)

Replace the simplified script with database query to dynamically calculate start date:

```csharp
// Query last sync date from BGCommissionReportQBDownload
var esq = new EntitySchemaQuery(UserConnection.EntitySchemaManager, "BGCommissionReportQBDownload");
esq.AddColumn("CreatedOn").OrderByDesc();
esq.RowCount = 1;

DateTime startDate;
var collection = esq.GetEntityCollection(UserConnection);
if (collection.Count > 0) {
    startDate = collection[0].GetTypedColumnValue<DateTime>("CreatedOn").AddSeconds(1);
} else {
    startDate = DateTime.UtcNow.AddDays(-90);
}

DateTime endDate = DateTime.UtcNow;
Set<DateTime>("AutoStartDate", startDate);
Set<DateTime>("AutoEndDate", endDate);
return true;
```

**Note:** First attempt failed with "key not found" - may need `using Terrasoft.Core.Entities;` or different column access pattern.

---

## Change Log

| Date | Change | Author |
|------|--------|--------|
| 2026-01-15 | Initial automation guide created | Claude Code |
| 2026-01-15 | Phase 1 deployed and verified (2 records synced) | Claude Code |
