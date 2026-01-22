-- Check if log entries now exist for our test orders
SELECT o."Number", l."Id" as LogId, l."BGStatusId"
FROM "Order" o
LEFT JOIN "BGQuickBooksIntegrationLogDetail" l ON l."BGRecordId" = o."Id"
WHERE o."Number" IN ('ORD-16091', 'ORD-16094', 'ORD-16097', 'ORD-16107')
ORDER BY o."Number";

-- Count pending log entries
SELECT COUNT(*) as pending_logs
FROM "BGQuickBooksIntegrationLogDetail"
WHERE "BGStatusId" = 'c97db3bc-634d-4c90-8432-ec7141c87640';
