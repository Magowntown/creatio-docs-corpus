-- ============================================================================
-- RESET PAYMENTSTATUSID FROM 'PLANNED' TO NULL (EMPTY GUID)
-- ============================================================================
-- Run this in pgAdmin connected to PROD database
-- ============================================================================

-- Planned Status ID: bfe38d3d-bd57-48d7-a2d7-82435cd274ca
-- Empty GUID: 00000000-0000-0000-0000-000000000000

-- ============================================================================
-- STEP 1: Check how many orders are affected (READ ONLY)
-- ============================================================================

SELECT COUNT(*) as affected_count
FROM "Order"
WHERE "PaymentStatusId" = 'bfe38d3d-bd57-48d7-a2d7-82435cd274ca';

-- ============================================================================
-- STEP 2: Preview sample of orders to be updated (READ ONLY)
-- ============================================================================

SELECT "Id", "Number", "CreatedOn", "PaymentStatusId"
FROM "Order"
WHERE "PaymentStatusId" = 'bfe38d3d-bd57-48d7-a2d7-82435cd274ca'
ORDER BY "CreatedOn" DESC
LIMIT 20;

-- ============================================================================
-- STEP 3: Execute the UPDATE (⚠️ THIS MODIFIES DATA)
-- ============================================================================

-- Start a transaction for safety
BEGIN;

-- Update PaymentStatusId from 'Planned' to NULL (empty GUID)
UPDATE "Order"
SET "PaymentStatusId" = '00000000-0000-0000-0000-000000000000',
    "ModifiedOn" = NOW(),
    "ModifiedById" = '410006e1-ca4e-4502-a9ec-e54d922d2c00'  -- Supervisor
WHERE "PaymentStatusId" = 'bfe38d3d-bd57-48d7-a2d7-82435cd274ca';

-- Check how many were updated
-- Should show the same count as Step 1

-- If everything looks good, COMMIT the transaction:
COMMIT;

-- If something went wrong, ROLLBACK instead:
-- ROLLBACK;

-- ============================================================================
-- STEP 4: Verify the update (READ ONLY)
-- ============================================================================

-- Should return 0 if all orders were updated
SELECT COUNT(*) as remaining_planned
FROM "Order"
WHERE "PaymentStatusId" = 'bfe38d3d-bd57-48d7-a2d7-82435cd274ca';

-- ============================================================================
-- ADDITIONAL: Remove default from IWQBIntegration schema
-- ============================================================================
-- The OrderPageV2 schema in IWQBIntegration is setting PaymentStatusId = Planned
-- as default. This needs to be removed in the Configuration UI:
--
-- 1. Navigate to:
--    https://pampabay.creatio.com/0/ClientApp/#/ClientUnitSchemaDesigner/6c9e5e8b-9d0b-41b4-b24d-bec395eb68bf
--
-- 2. Look for PaymentStatus default value in:
--    - attributes section
--    - methods.init() or methods.onEntityInitialized()
--    - diff with defValue
--
-- 3. Remove or comment out the default value
-- 4. Save and Compile
-- ============================================================================
