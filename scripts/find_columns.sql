-- Find QB-related columns in Order table
SELECT column_name
FROM information_schema.columns
WHERE table_name = 'Order'
  AND (column_name ILIKE '%quickbooks%' OR column_name ILIKE '%qb%' OR column_name ILIKE '%haslog%' OR column_name ILIKE '%invoice%')
ORDER BY column_name;
