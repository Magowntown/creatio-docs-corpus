-- Check if BGQuickBooksId is empty string vs NULL
SELECT "Number",
       "BGQuickBooksId",
       CASE WHEN "BGQuickBooksId" IS NULL THEN 'IS NULL'
            WHEN "BGQuickBooksId" = '' THEN 'EMPTY STRING'
            ELSE 'HAS VALUE' END as status
FROM "Order"
WHERE "Number" IN ('ORD-16079', 'ORD-16107');
