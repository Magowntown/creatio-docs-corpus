-- Find columns in QB log table
SELECT column_name
FROM information_schema.columns
WHERE table_name = 'BGQuickBooksIntegrationLogDetail'
ORDER BY column_name;
