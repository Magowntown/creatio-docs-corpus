-- BGSalesByItemView Employee JOIN Fix
-- Problem: JOIN Employee e ON (sg."Id" = e."BGSalesGroupLookupId") joins ALL employees in sales group
-- Fix: JOIN Employee e ON (o."BGSalesRepLookupId" = e."Id") joins specific sales rep on order
-- Impact: Eliminates 26x duplicate rows per order line
-- Date: 2026-01-29

CREATE OR REPLACE VIEW "BGSalesByItemView" AS SELECT o."Id", o."CreatedOn", o."CreatedById", o."ModifiedOn", o."ModifiedById", o."ProcessListeners", o."Number" AS "BGNumber", o."BGPONumber", o."BGShipDate", o."BGDeliveryDate", op."Price" AS "BGPrice", op."TotalAmount" AS "BGAmount", p."Name" AS "BGItem", p."Description" AS "BGProductDescription", op."Quantity" AS "BGQuantity", ac."Name" AS "BGCustomer", os."Name" AS "BGStatus", sg."BGSalesGroupName" AS "BGSalesGroup", e."Name" AS "BGSalesRep" FROM ((((("Order" o JOIN "Account" ac ON ((o."AccountId" = ac."Id"))) JOIN "OrderStatus" os ON ((o."StatusId" = os."Id"))) JOIN "BGSalesGroup" sg ON ((o."BGSalesGroupId" = sg."Id"))) LEFT JOIN "Employee" e ON ((o."BGSalesRepLookupId" = e."Id"))) JOIN "OrderProduct" op ON ((op."OrderId" = o."Id"))) JOIN "Product" p ON ((p."Id" = op."ProductId")) WHERE o."BGOrderTypeId" = '154d3407-9d8c-49c2-84cd-e85afeb8d55a'::uuid AND sg.* IS NOT NULL AND os."Id" IN ('29fa66e3-ef69-4feb-a5af-ec1de125a614','40de86ee-274d-4098-9b92-9ebdcf83d4fc','8ab0f830-908b-40d7-80a3-7f49ef70ce70');
