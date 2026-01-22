-- December 2025 order sync status
SELECT
    COUNT(*) as total_dec_orders,
    SUM(CASE WHEN "BGQuickBooksId" IS NOT NULL AND "BGQuickBooksId" != '' THEN 1 ELSE 0 END) as with_qb_id,
    SUM(CASE WHEN "BGQuickBooksId" IS NULL OR "BGQuickBooksId" = '' THEN 1 ELSE 0 END) as without_qb_id,
    SUM(CASE WHEN "BGNumberInvoice" IS NOT NULL AND "BGNumberInvoice" != '' THEN 1 ELSE 0 END) as with_invoice
FROM "Order"
WHERE "CreatedOn" >= '2025-12-01' AND "CreatedOn" < '2026-01-01';
