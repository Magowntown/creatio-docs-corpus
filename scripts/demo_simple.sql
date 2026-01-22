-- Simple comparison of working vs broken orders
SELECT
    o."Number",
    o."BGHasQuickBooksLog",
    o."ProcessListeners",
    o."BGQuickBooksId"
FROM "Order" o
WHERE o."Number" IN ('ORD-16074', 'ORD-16110', 'ORD-16091', 'ORD-16107')
ORDER BY o."Number";
