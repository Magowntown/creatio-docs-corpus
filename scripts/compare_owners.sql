-- Compare a Supervisor order vs a synced order
SELECT
    "Number",
    "OwnerId",
    "BGHasQuickBooksLog",
    "BGHasInvoice",
    "ProcessListeners",
    "BGQuickBooksId"
FROM "Order"
WHERE "Number" IN ('ORD-16074', 'ORD-16091', 'ORD-16110', 'ORD-16107')
ORDER BY "Number";
