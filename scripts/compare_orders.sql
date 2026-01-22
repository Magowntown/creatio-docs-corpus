-- Compare a synced order vs unsynced order
SELECT "Number", "BGQuickBooksId", "StatusId", "OwnerId", "CreatedOn"
FROM "Order"
WHERE "Number" IN ('ORD-16074', 'ORD-16079', 'ORD-16110', 'ORD-16107')
ORDER BY "Number";
