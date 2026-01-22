-- Get a recent parent log entry
SELECT "Id", "BGName", "CreatedOn"
FROM "BGQuickBooksIntegrationLog"
ORDER BY "CreatedOn" DESC
LIMIT 5;
