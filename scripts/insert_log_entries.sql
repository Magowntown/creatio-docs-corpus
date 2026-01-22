-- Insert log entries for orders missing them
-- Uses: Type=Customer Order, Action=Insert, Status=Pending
INSERT INTO "BGQuickBooksIntegrationLogDetail" (
    "Id",
    "BGQuickBooksIntegrationLogId",
    "BGTypeId",
    "BGActionId",
    "BGStatusId",
    "BGRecordId",
    "BGName",
    "BGDate",
    "CreatedOn",
    "ModifiedOn",
    "CreatedById",
    "ModifiedById",
    "ProcessListeners"
)
SELECT
    gen_random_uuid(),
    'a8f4bc9b-9c81-4613-a96b-7de3a6ea3bb5',  -- Today's log
    '14535998-d4c0-45ac-bbac-8c0185bfcc1a',  -- Customer Order
    'facb63c3-3599-4cb5-b86d-179b0636a3cb',  -- Insert
    'c97db3bc-634d-4c90-8432-ec7141c87640',  -- Pending
    o."Id",
    o."Number",
    NOW(),
    NOW(),
    NOW(),
    '410006e1-ca4e-4502-a9ec-e54d922d2c00',  -- Supervisor
    '410006e1-ca4e-4502-a9ec-e54d922d2c00',  -- Supervisor
    0
FROM "Order" o
WHERE o."BGHasQuickBooksLog" = true
  AND (o."BGQuickBooksId" IS NULL OR o."BGQuickBooksId" = '')
  AND NOT EXISTS (
    SELECT 1 FROM "BGQuickBooksIntegrationLogDetail" l
    WHERE l."BGRecordId" = o."Id"
  );
