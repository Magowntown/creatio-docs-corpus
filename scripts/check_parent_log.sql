-- Check parent log table columns
SELECT column_name
FROM information_schema.columns
WHERE table_name = 'BGQuickBooksIntegrationLog'
ORDER BY column_name;

-- Get a recent parent log entry for Customer Orders
SELECT "Id", "Name", "BGDate"
FROM "BGQuickBooksIntegrationLog"
ORDER BY "BGDate" DESC
LIMIT 5;
