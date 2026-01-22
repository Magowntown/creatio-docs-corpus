-- Check orders that have correct flags but no QB sync
SELECT "Number", "StatusId", "BGHasQuickBooksLog", "BGHasInvoice", "BGQuickBooksId", "OwnerId"
FROM "Order"
WHERE "BGHasQuickBooksLog" = true
  AND ("BGQuickBooksId" IS NULL OR "BGQuickBooksId" = '')
  AND "CreatedOn" >= '2026-01-20'
ORDER BY "CreatedOn" DESC
LIMIT 15;
