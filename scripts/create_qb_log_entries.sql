-- Count orders that need log entries
SELECT COUNT(*) as orders_needing_logs
FROM "Order" o
WHERE o."BGHasQuickBooksLog" = true
  AND (o."BGQuickBooksId" IS NULL OR o."BGQuickBooksId" = '')
  AND NOT EXISTS (
    SELECT 1 FROM "BGQuickBooksIntegrationLogDetail" l
    WHERE l."BGRecordId" = o."Id"
  );

-- First, we need to know the correct TypeId and ActionId values
-- Check existing log entries for reference
SELECT DISTINCT "BGTypeId", "BGActionId", "BGStatusId"
FROM "BGQuickBooksIntegrationLogDetail"
LIMIT 10;
