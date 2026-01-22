-- Check error messages for failed syncs
SELECT
    o."Number",
    l."BGErrorMessage",
    l."ModifiedOn"
FROM "Order" o
JOIN "BGQuickBooksIntegrationLogDetail" l ON l."BGRecordId" = o."Id"
WHERE l."BGStatusId" = 'bdfc60c7-55fd-4cbd-9a2c-dca2def46d80'
  AND o."CreatedOn" >= '2026-01-20'
ORDER BY l."ModifiedOn" DESC
LIMIT 10;
