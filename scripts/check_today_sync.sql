-- Check today's orders and their sync status
SELECT
    "Number",
    "BGHasQuickBooksLog",
    "ProcessListeners",
    CASE WHEN "BGQuickBooksId" IS NOT NULL AND "BGQuickBooksId" != ''
         THEN 'YES' ELSE 'NO' END as "Synced",
    "BGQuickBooksId",
    "BGNumberInvoice",
    "CreatedOn"
FROM "Order"
WHERE "CreatedOn" >= '2026-01-20'
ORDER BY "CreatedOn" DESC
LIMIT 25;
