-- Count orders that need ProcessListeners fix
SELECT COUNT(*) as orders_to_fix
FROM "Order"
WHERE "ProcessListeners" = 0
  AND ("BGQuickBooksId" IS NULL OR "BGQuickBooksId" = '')
  AND "BGHasQuickBooksLog" = true;

-- Apply the fix
UPDATE "Order"
SET "ProcessListeners" = 2
WHERE "ProcessListeners" = 0
  AND ("BGQuickBooksId" IS NULL OR "BGQuickBooksId" = '')
  AND "BGHasQuickBooksLog" = true;
