-- FLT-004 Root Cause Fix: Populate BGYearMonthId based on BGTransactionDate
--
-- Problem: BGYearMonthId is NULL for all rows in BGCommissionReportDataView
-- This causes INNER JOINs to exclude all data when filtering by Year-Month
--
-- Solution: Update the underlying table to populate BGYearMonthId
-- based on the BGTransactionDate field

-- First, check the current state
SELECT
    'Before Update' as Status,
    COUNT(*) as TotalRows,
    SUM(CASE WHEN BGYearMonthId IS NULL THEN 1 ELSE 0 END) as NullYearMonthRows,
    SUM(CASE WHEN BGYearMonthId IS NOT NULL THEN 1 ELSE 0 END) as PopulatedRows
FROM BGSalesItem;  -- or whatever the source table is

-- Check available BGYearMonth records
SELECT Id, Name
FROM BGYearMonth
ORDER BY Name DESC;

-- Preview what would be updated (run this first to verify)
SELECT TOP 100
    si.Id,
    si.BGTransactionDate,
    si.BGYearMonthId as CurrentYearMonthId,
    ym.Id as NewYearMonthId,
    ym.Name as YearMonthName
FROM BGSalesItem si
LEFT JOIN BGYearMonth ym ON ym.Name = FORMAT(si.BGTransactionDate, 'yyyy-MM')
WHERE si.BGYearMonthId IS NULL
  AND si.BGTransactionDate IS NOT NULL;

-- ============================================================
-- CAUTION: The UPDATE below will modify data!
-- Only run after verifying the preview above looks correct.
-- ============================================================

/*
-- Update BGYearMonthId based on transaction date
UPDATE si
SET si.BGYearMonthId = ym.Id
FROM BGSalesItem si
INNER JOIN BGYearMonth ym ON ym.Name = FORMAT(si.BGTransactionDate, 'yyyy-MM')
WHERE si.BGYearMonthId IS NULL
  AND si.BGTransactionDate IS NOT NULL;

-- Verify the update
SELECT
    'After Update' as Status,
    COUNT(*) as TotalRows,
    SUM(CASE WHEN BGYearMonthId IS NULL THEN 1 ELSE 0 END) as NullYearMonthRows,
    SUM(CASE WHEN BGYearMonthId IS NOT NULL THEN 1 ELSE 0 END) as PopulatedRows
FROM BGSalesItem;
*/

-- ============================================================
-- Alternative: Create missing BGYearMonth records first
-- ============================================================

/*
-- Find months that exist in data but not in BGYearMonth lookup
SELECT DISTINCT FORMAT(BGTransactionDate, 'yyyy-MM') as MissingMonth
FROM BGSalesItem
WHERE BGTransactionDate IS NOT NULL
  AND FORMAT(BGTransactionDate, 'yyyy-MM') NOT IN (SELECT Name FROM BGYearMonth);

-- Insert missing months (adjust columns as needed for your schema)
INSERT INTO BGYearMonth (Id, Name, CreatedOn, ModifiedOn)
SELECT
    NEWID(),
    FORMAT(BGTransactionDate, 'yyyy-MM'),
    GETUTCDATE(),
    GETUTCDATE()
FROM BGSalesItem
WHERE BGTransactionDate IS NOT NULL
GROUP BY FORMAT(BGTransactionDate, 'yyyy-MM')
HAVING FORMAT(BGTransactionDate, 'yyyy-MM') NOT IN (SELECT Name FROM BGYearMonth);
*/
