-- =============================================================================
-- ALL VIEWS: Add Product Description Column
-- =============================================================================
-- Date: 2026-01-29
-- Purpose: Add BGProductDescription to all product-related views for consistency
-- Pattern: p."Description" AS "BGProductDescription"
--
-- Views that need this fix (have Product JOIN but missing Description):
-- 1. BGSalesByItemView - DONE (applied 2026-01-29)
-- 2. BGSalesByItemByTypeOfCustomerView - NEEDS FIX
-- 3. BGSalesByItemThemeView - NEEDS FIX
-- 4. BGSalesByLineByTypeOfCustomerView - NEEDS FIX (may already have BGDescription)
--
-- Views that ALREADY have Product Description:
-- - BGSalesByItemLineView (has p."Description" AS "BGDescription")
-- - BGSalesByLineWithRankingView (has P."BGDescription" AS "BGProductDescription")
-- =============================================================================


-- =============================================================================
-- 1. BGSalesByItemView - ALREADY APPLIED
-- =============================================================================
-- Status: ✅ DONE - User applied via Creatio Configuration
-- Column added: p."Description" AS "BGProductDescription"


-- =============================================================================
-- 2. BGSalesByItemByTypeOfCustomerView - NEEDS FIX
-- =============================================================================
-- This view is identical to BGSalesByItemView but includes BGCustomerType
-- Add: p."Description" AS "BGProductDescription" after p."Name" AS "BGItem"

DROP VIEW IF EXISTS "BGSalesByItemByTypeOfCustomerView";

CREATE VIEW "BGSalesByItemByTypeOfCustomerView" AS
SELECT
  o."Id",
  o."CreatedOn",
  o."CreatedById",
  o."ModifiedOn",
  o."ModifiedById",
  o."ProcessListeners",
  o."Number" AS "BGNumber",
  o."BGPONumber",
  o."BGShipDate",
  (CASE WHEN (o."BGDeliveryDate" <> null)
    THEN o."BGDeliveryDate"
    ELSE o."Date"
  END) AS "BGDeliveryDate",
  op."Price" AS "BGPrice",
  op."Amount" AS "BGAmount",
  p."Name" AS "BGItem",
  p."Description" AS "BGProductDescription",  -- NEW: Added for consistency
  op."Quantity" AS "BGQuantity",
  ac."Name" AS "BGCustomer",
  os."Name" AS "BGStatus",
  sg."BGSalesGroupName" AS "BGSalesGroup",
  e."Name" AS "BGSalesRep",
  ct."Name" AS "BGCustomerType"
FROM
    (((((("Order" o
      JOIN "Account" ac ON (o."AccountId" = ac."Id"))
      JOIN "OrderStatus" os ON (o."StatusId" = os."Id"))
      JOIN "BGSalesGroup" sg ON (o."BGSalesGroupId" = sg."Id"))
      JOIN "Employee" e ON (sg."Id" = e."BGSalesGroupLookupId"))
      JOIN "OrderProduct" op ON (op."OrderId" = o."Id"))
      JOIN "Product" p ON (p."Id" = op."ProductId"))
      JOIN "BGCustomerTypeLookup" ct ON (ct."Id" = ac."BGCustomerTypeId")
WHERE
    o."BGOrderTypeId" = '154d3407-9d8c-49c2-84cd-e85afeb8d55a'::uuid
    AND sg.* IS NOT NULL
    AND os."Id" IN (
      '29fa66e3-ef69-4feb-a5af-ec1de125a614',
      '40de86ee-274d-4098-9b92-9ebdcf83d4fc',
      '8ab0f830-908b-40d7-80a3-7f49ef70ce70'
    );


-- =============================================================================
-- 3. BGSalesByItemThemeView - NEEDS FIX
-- =============================================================================
-- This view groups by product theme
-- Add: p."Description" AS "BGProductDescription" after p."Name" AS "BGItem"

DROP VIEW IF EXISTS "BGSalesByItemThemeView";

CREATE VIEW "BGSalesByItemThemeView" AS
SELECT
  o."Id",
  o."CreatedOn",
  o."CreatedById",
  o."ModifiedOn",
  o."ModifiedById",
  o."ProcessListeners",
  o."Number" AS "BGNumber",
  o."BGPONumber",
  o."BGShipDate",
  o."BGDeliveryDate",
  op."Price" AS "BGPrice",
  op."Amount" AS "BGAmount",
  p."Name" AS "BGItem",
  p."Description" AS "BGProductDescription",  -- NEW: Added for consistency
  op."Quantity" AS "BGQuantity",
  ac."Name" AS "BGCustomer",
  os."Name" AS "BGStatus",
  sg."BGSalesGroupName" AS "BGSalesGroup",
  e."Name" AS "BGSalesRep",
  pt."Name" AS "BGTheme"
FROM
    ((((((("Order" o
      JOIN "Account" ac ON (o."AccountId" = ac."Id"))
      JOIN "OrderStatus" os ON (o."StatusId" = os."Id"))
      JOIN "BGSalesGroup" sg ON (o."BGSalesGroupId" = sg."Id"))
      JOIN "Employee" e ON (sg."Id" = e."BGSalesGroupLookupId"))
      JOIN "OrderProduct" op ON (op."OrderId" = o."Id"))
      JOIN "Product" p ON (p."Id" = op."ProductId"))
      JOIN "BGProductThemeLookup" pt ON (pt."Id" = p."BGProductThemeId"))
WHERE
    o."BGOrderTypeId" = '154d3407-9d8c-49c2-84cd-e85afeb8d55a'::uuid
    AND sg.* IS NOT NULL
    AND os."Id" IN (
      '29fa66e3-ef69-4feb-a5af-ec1de125a614',
      '40de86ee-274d-4098-9b92-9ebdcf83d4fc',
      '8ab0f830-908b-40d7-80a3-7f49ef70ce70'
    );


-- =============================================================================
-- 4. BGSalesByLineByTypeOfCustomerView - NEEDS FIX
-- =============================================================================
-- This view has Line grouping + CustomerType
-- Add: p."Description" AS "BGProductDescription" after p."Name" AS "BGItem"

DROP VIEW IF EXISTS "BGSalesByLineByTypeOfCustomerView";

CREATE VIEW "BGSalesByLineByTypeOfCustomerView" AS
SELECT
  o."Id",
  o."CreatedOn",
  o."CreatedById",
  o."ModifiedOn",
  o."ModifiedById",
  o."ProcessListeners",
  o."Number" AS "BGNumber",
  o."BGPONumber",
  o."BGShipDate",
  (CASE WHEN (o."BGDeliveryDate" <> null)
    THEN o."BGDeliveryDate"
    ELSE o."Date"
  END) AS "BGDeliveryDate",
  op."Price" AS "BGPrice",
  op."Amount" AS "BGAmount",
  p."Name" AS "BGItem",
  p."Description" AS "BGProductDescription",  -- NEW: Added for consistency
  op."Quantity" AS "BGQuantity",
  ac."Name" AS "BGCustomer",
  os."Name" AS "BGStatus",
  sg."BGSalesGroupName" AS "BGSalesGroup",
  e."Name" AS "BGSalesRep",
  ct."Name" AS "BGCustomerType",
  lp."Name" AS "BGLine"
FROM
    (((((((("Order" o
      JOIN "Account" ac ON (o."AccountId" = ac."Id"))
      JOIN "OrderStatus" os ON (o."StatusId" = os."Id"))
      JOIN "BGSalesGroup" sg ON (o."BGSalesGroupId" = sg."Id"))
      JOIN "Employee" e ON (sg."Id" = e."BGSalesGroupLookupId"))
      JOIN "OrderProduct" op ON (op."OrderId" = o."Id"))
      JOIN "Product" p ON (p."Id" = op."ProductId"))
      JOIN "BGCustomerTypeLookup" ct ON (ct."Id" = ac."BGCustomerTypeId"))
      JOIN "BGLineProduct" lp ON (lp."Id" = p."BGLineId"))
WHERE
    o."BGOrderTypeId" = '154d3407-9d8c-49c2-84cd-e85afeb8d55a'::uuid
    AND sg.* IS NOT NULL
    AND os."Id" IN (
      '29fa66e3-ef69-4feb-a5af-ec1de125a614',
      '40de86ee-274d-4098-9b92-9ebdcf83d4fc',
      '8ab0f830-908b-40d7-80a3-7f49ef70ce70'
    );


-- =============================================================================
-- VERIFICATION QUERIES
-- =============================================================================

-- Verify BGSalesByItemView has new column:
-- SELECT "BGItem", "BGProductDescription", "BGCustomer" FROM "BGSalesByItemView" LIMIT 5;

-- Verify BGSalesByItemByTypeOfCustomerView has new column:
-- SELECT "BGItem", "BGProductDescription", "BGCustomerType" FROM "BGSalesByItemByTypeOfCustomerView" LIMIT 5;

-- Verify BGSalesByItemThemeView has new column:
-- SELECT "BGItem", "BGProductDescription", "BGTheme" FROM "BGSalesByItemThemeView" LIMIT 5;

-- Verify BGSalesByLineByTypeOfCustomerView has new column:
-- SELECT "BGItem", "BGProductDescription", "BGLine" FROM "BGSalesByLineByTypeOfCustomerView" LIMIT 5;


-- =============================================================================
-- SUMMARY
-- =============================================================================
-- Views Fixed: 4 total
-- 1. BGSalesByItemView - Applied via Creatio UI
-- 2. BGSalesByItemByTypeOfCustomerView - Apply via this script
-- 3. BGSalesByItemThemeView - Apply via this script
-- 4. BGSalesByLineByTypeOfCustomerView - Apply via this script
--
-- Views Already Have Description:
-- - BGSalesByItemLineView (BGDescription)
-- - BGSalesByLineWithRankingView (BGProductDescription)
--
-- No Changes Needed:
-- - BGSalesByCustomerView (no product data)
-- - BGSalesByCustomerYearComparisonView (no product data)
-- - BGSalesBySalesGroupView (no product data)
-- - BGSalesRepMonthlyReportView (no product data)
-- =============================================================================
