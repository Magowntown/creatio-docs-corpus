-- Get recent orders to see actual column values
SELECT "Number", "BGQuickBooksId", "BGNumberInvoice", "CreatedOn"
FROM "Order"
WHERE "CreatedOn" >= '2026-01-15'
ORDER BY "CreatedOn" DESC
LIMIT 30;
