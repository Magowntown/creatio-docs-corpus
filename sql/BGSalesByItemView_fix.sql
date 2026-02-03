-- BGSalesByItemView SQL Fix
-- Purpose: Add BGProductDescription column for "Items by Customer" DESCRIPCION fix
-- Date: 2026-01-29
--
-- CHANGE: Added p."Description" AS "BGProductDescription" to SELECT clause
-- The Product table is ALREADY JOINED, so this is a simple column addition.
--
-- Apply to: PROD (pampabay.creatio.com)
-- Package: PampaBay
-- Schema: BGSalesByItemView (UId: d38b4d04-7c79-4b4a-8611-306f86d1e5c9)

DROP VIEW IF EXISTS "BGSalesByItemView";

CREATE VIEW "BGSalesByItemView" AS
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
  op."TotalAmount" AS "BGAmount",
  p."Name" AS "BGItem",                    -- Product Name (existing)
  p."Description" AS "BGProductDescription", -- NEW: Product Description for DESCRIPCION column
  op."Quantity" AS "BGQuantity",
  ac."Name" AS "BGCustomer",
  os."Name" AS "BGStatus",
  sg."BGSalesGroupName" AS "BGSalesGroup",
  e."Name" AS "BGSalesRep"
FROM
    (
      (
        (
          (
            (
              "Order" o
              JOIN "Account" ac ON (
                (o."AccountId" = ac."Id")
              )
            )
            JOIN "OrderStatus" os ON (
              (o."StatusId" = os."Id")
            )
          )
          JOIN "BGSalesGroup" sg ON (
            (o."BGSalesGroupId" = sg."Id")
          )
        )
        JOIN "Employee" e ON (
          (
            sg."Id" = e."BGSalesGroupLookupId"
          )
        )
      )
      JOIN "OrderProduct" op ON (
        (op."OrderId" = o."Id")
      )
    )
    JOIN "Product" p ON (
      (p."Id" = op."ProductId")
    )
WHERE
    (
      o."BGOrderTypeId" = '154d3407-9d8c-49c2-84cd-e85afeb8d55a' :: uuid
    )
    AND (sg.* IS NOT NULL)
    AND os."Id" IN (
      '29fa66e3-ef69-4feb-a5af-ec1de125a614',  -- Status 1
      '40de86ee-274d-4098-9b92-9ebdcf83d4fc',  -- Status 2
      '8ab0f830-908b-40d7-80a3-7f49ef70ce70'   -- Status 3
    );

-- VERIFICATION QUERY (run after applying):
-- SELECT "BGItem", "BGProductDescription", "BGCustomer"
-- FROM "BGSalesByItemView"
-- LIMIT 5;
