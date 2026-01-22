-- Check if orders have QB log entries
SELECT o."Number", l."Id" as LogId, l."BGStatusId", l."BGActionId"
FROM "Order" o
LEFT JOIN "BGQuickBooksIntegrationLogDetail" l ON l."BGOrderId" = o."Id"
WHERE o."Number" IN ('ORD-16091', 'ORD-16094', 'ORD-16097', 'ORD-16107')
ORDER BY o."Number";
