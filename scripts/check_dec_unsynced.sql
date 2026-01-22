-- Check the 35 unsynced December orders - are they canceled?
SELECT "Number", "StatusId", "BGHasQuickBooksLog", "CreatedOn"
FROM "Order"
WHERE "CreatedOn" >= '2025-12-01' AND "CreatedOn" < '2026-01-01'
  AND ("BGQuickBooksId" IS NULL OR "BGQuickBooksId" = '')
ORDER BY "CreatedOn" DESC
LIMIT 20;
