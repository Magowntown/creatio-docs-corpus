-- Check actual values of the flag
SELECT "Number", "BGHasQuickBooksLog", pg_typeof("BGHasQuickBooksLog") as datatype
FROM "Order"
WHERE "Number" IN ('ORD-16079', 'ORD-16107')
LIMIT 5;
