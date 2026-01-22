-- DEMO: Compare working orders vs broken orders
-- This shows why Brandwise orders weren't syncing to QuickBooks

SELECT
    o."Number" as "Order",
    CASE WHEN o."OwnerId" = '410006e1-ca4e-4502-a9ec-e54d922d2c00'
         THEN 'Brandwise/Supervisor'
         ELSE 'Manual/User' END as "Source",
    o."BGHasQuickBooksLog" as "HasQBLog",
    o."ProcessListeners" as "ProcListeners",
    CASE WHEN l."Id" IS NOT NULL THEN 'YES' ELSE 'NO' END as "LogEntry",
    CASE WHEN o."BGQuickBooksId" IS NOT NULL AND o."BGQuickBooksId" != ''
         THEN 'SYNCED' ELSE 'NOT SYNCED' END as "QB Status",
    o."BGQuickBooksId" as "QB ID"
FROM "Order" o
LEFT JOIN "BGQuickBooksIntegrationLogDetail" l ON l."BGRecordId" = o."Id"
WHERE o."Number" IN (
    'ORD-16074',  -- Working order (manual)
    'ORD-16110',  -- Working order (manual)
    'ORD-16091',  -- Was broken (Brandwise) - now fixed
    'ORD-16107'   -- Was broken (Brandwise) - now fixed
)
ORDER BY o."Number";
