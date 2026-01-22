-- Find the Type for Customer Order
SELECT "Id", "Name"
FROM "BGQuickBooksIntegrationType"
ORDER BY "Name";

-- Find the Action for Add/Update
SELECT "Id", "Name"
FROM "BGQuickBooksIntegrationAction"
ORDER BY "Name";

-- Pending status ID (for new log entries)
SELECT "Id", "Name"
FROM "BGQuickBooksIntegrationStatus"
ORDER BY "Name";
