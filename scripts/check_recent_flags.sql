-- Check if TODAY's orders have correct BGHasQuickBooksLog flag
SELECT
    "Number",
    "BGHasQuickBooksLog",
    "BGHasInvoice",
    "CreatedOn"
FROM "Order"
WHERE "CreatedOn" >= '2026-01-20'
ORDER BY "CreatedOn" DESC
LIMIT 20;
