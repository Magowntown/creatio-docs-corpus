SELECT "Number", "BGHasQuickBooksLog", "BGHasInvoice", "BGQuickBooksId"
FROM "Order"
WHERE "Number" IN ('ORD-16074', 'ORD-16079', 'ORD-16107', 'ORD-16110')
ORDER BY "Number";
