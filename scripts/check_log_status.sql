-- Check log entry status for today's orders
SELECT
    o."Number",
    l."BGStatusId",
    s."Name" as "Status",
    o."BGQuickBooksId"
FROM "Order" o
LEFT JOIN "BGQuickBooksIntegrationLogDetail" l ON l."BGRecordId" = o."Id"
LEFT JOIN "BGQuickBooksLogStatus" s ON s."Id" = l."BGStatusId"
WHERE o."CreatedOn" >= '2026-01-20'
ORDER BY o."CreatedOn" DESC
LIMIT 20;
