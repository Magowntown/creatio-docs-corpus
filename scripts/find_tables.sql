-- Find QB-related lookup tables
SELECT table_name
FROM information_schema.tables
WHERE table_name ILIKE '%quickbooks%'
   OR table_name ILIKE '%bgtype%'
   OR table_name ILIKE '%bgaction%'
   OR table_name ILIKE '%bgstatus%'
ORDER BY table_name;
