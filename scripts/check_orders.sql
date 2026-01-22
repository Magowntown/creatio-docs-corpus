-- Check unsynced orders
SELECT "Number", "BGQuickBooksId", "BGNumberInvoice", "StatusId", "CreatedOn"
FROM "Order"
WHERE "BGQuickBooksId" IS NULL
  AND "CreatedOn" >= '2026-01-01'
ORDER BY "CreatedOn" DESC
LIMIT 20;
