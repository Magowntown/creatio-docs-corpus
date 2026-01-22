-- Check how many January orders now have QB sync
SELECT
    COUNT(*) as total_jan_orders,
    SUM(CASE WHEN "BGQuickBooksId" IS NOT NULL AND "BGQuickBooksId" != '' THEN 1 ELSE 0 END) as with_qb_id,
    SUM(CASE WHEN "BGQuickBooksId" IS NULL OR "BGQuickBooksId" = '' THEN 1 ELSE 0 END) as without_qb_id
FROM "Order"
WHERE "CreatedOn" >= '2026-01-01';
