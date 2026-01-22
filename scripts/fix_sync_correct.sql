-- Count orders to fix (empty string OR null)
SELECT COUNT(*) as orders_to_fix
FROM "Order"
WHERE "BGHasQuickBooksLog" = false
  AND ("BGQuickBooksId" IS NULL OR "BGQuickBooksId" = '');

-- Fix them
UPDATE "Order"
SET "BGHasQuickBooksLog" = true, "BGHasInvoice" = true
WHERE "BGHasQuickBooksLog" = false
  AND ("BGQuickBooksId" IS NULL OR "BGQuickBooksId" = '');
