-- Check if our specific fixed orders now have BGQuickBooksId
SELECT "Number", "ProcessListeners", "BGQuickBooksId", "BGNumberInvoice"
FROM "Order"
WHERE "Number" IN ('ORD-16091', 'ORD-16094', 'ORD-16097', 'ORD-16107')
ORDER BY "Number";
