-- First check how many need fixing
SELECT COUNT(*) as orders_to_fix
FROM "Order"
WHERE "BGHasQuickBooksLog" = false
  AND "BGQuickBooksId" IS NULL;

-- Then run the fix
UPDATE "Order"
SET "BGHasQuickBooksLog" = true, "BGHasInvoice" = true
WHERE "BGHasQuickBooksLog" = false
  AND "BGQuickBooksId" IS NULL;
