-- BGCustomerDidNotBuyView - Original BGlobal V7 Definition
-- Extracted from: PampaBay_2026-01-28_16.45.47.zip
-- Script: BGPostgreSql_CustomerDidNotBuyView
-- Pattern: Type A (Execution-Based)
--
-- PURPOSE: Finds customers (Accounts) who have NOT placed orders within a specified date range
-- but MAY have placed orders before that date range.
--
-- KEY DESIGN DECISIONS:
-- 1. Uses JOIN "BGReportExecution" ON true (Cartesian product) for execution-based filtering
-- 2. Date filters come from BGReportExecution record (BGCreatedFrom, BGCreatedTo)
-- 3. NOT EXISTS clause finds customers without orders in the date range
-- 4. Only outputs Account ID - Name/Address/City must come via ESQ relationship columns
-- 5. Timezone adjustment: (o."CreatedOn" - '05:00:00'::interval) for EST
--
-- GUID REFERENCES:
-- 2b9201fc-3891-4ba3-abde-1bb9ce195ecc = OrderStatus "Cancelled" (excluded)
-- 154d3407-9d8c-49c2-84cd-e85afeb8d55a = BGOrderType "Customer"
-- 03a75490-53e6-df11-971b-001d60e938c6 = AccountType "Customer"
-- ee1c85c3-cfcb-df11-9b2a-001d60e938c6 = CommunicationType "Email"

DROP VIEW IF EXISTS "BGCustomerDidNotBuyView";
CREATE VIEW "BGCustomerDidNotBuyView" AS
SELECT
    a."Id",
    a."CreatedOn",
    a."CreatedById",
    a."ModifiedOn",
    a."ModifiedById",
    a."ProcessListeners",
    a."Id" AS "BGAccountId",

    -- Subquery: Get most recent order ID (before the date range)
    (
        SELECT o1."Id"
        FROM "Order" o1
        WHERE o1."AccountId" = a."Id"
            AND o1."StatusId" != '2b9201fc-3891-4ba3-abde-1bb9ce195ecc'  -- Not Cancelled
            AND o1."BGOrderTypeId" = '154d3407-9d8c-49c2-84cd-e85afeb8d55a'  -- Customer orders
        ORDER BY o1."CreatedOn" DESC
        LIMIT 1
    ) AS "BGLastOrderId",

    -- Subquery: Get email from AccountCommunication
    (
        SELECT ac."Number"
        FROM "AccountCommunication" AS ac
        WHERE ac."AccountId" = a."Id"
            AND ac."CommunicationTypeId" = 'ee1c85c3-cfcb-df11-9b2a-001d60e938c6'  -- Email type
        ORDER BY ac."CreatedOn" DESC
        LIMIT 1
    ) AS "BGEmail",

    -- Subquery: Count orders BEFORE the date range (previous order history)
    (
        SELECT COUNT(*)
        FROM "Order" AS o2
        WHERE o2."AccountId" = a."Id"
            AND o2."StatusId" != '2b9201fc-3891-4ba3-abde-1bb9ce195ecc'  -- Not Cancelled
            AND o2."BGOrderTypeId" = '154d3407-9d8c-49c2-84cd-e85afeb8d55a'  -- Customer orders
            AND (
                ((re."BGCreatedFrom" IS NULL AND re."BGCreatedTo" IS NULL)
                    OR (re."BGCreatedFrom" IS NOT NULL AND (o2."CreatedOn" - '05:00:00'::interval)::date < re."BGCreatedFrom"::date))
                OR
                ((re."BGCreatedFrom" IS NULL AND re."BGCreatedTo" IS NOT NULL)
                    AND (o2."CreatedOn" - '05:00:00'::interval)::date < re."BGCreatedTo"::date)
            )
    ) AS "BGPreviousOrderCount",

    -- Human-readable filter description
    (
        'Created Date: '::text || COALESCE(to_char(re."BGCreatedFrom", 'mm/dd/yyyy'::text), ''::text)
        || ' to '::text || COALESCE(to_char(re."BGCreatedTo", 'mm/dd/yyyy'), ''::text)
    ) AS "BGFilters",

    -- Execution ID for filtering (Type A pattern)
    re."Id" AS "BGExecutionId"

FROM "Account" AS a
JOIN "BGReportExecution" AS re ON true  -- Cartesian product! All accounts × all executions

WHERE
    -- Only Customer account type
    a."TypeId" = '03a75490-53e6-df11-971b-001d60e938c6'
    AND
    -- NOT EXISTS: No orders in the specified date range
    NOT EXISTS (
        SELECT 1
        FROM "Order" AS o
        WHERE o."AccountId" = a."Id"
            AND o."BGOrderTypeId" = '154d3407-9d8c-49c2-84cd-e85afeb8d55a'  -- Customer orders
            AND o."StatusId" != '2b9201fc-3891-4ba3-abde-1bb9ce195ecc'  -- Not Cancelled
            -- Date range filter from BGReportExecution
            AND (re."BGCreatedFrom" IS NULL OR (o."CreatedOn" - '05:00:00'::interval)::date >= re."BGCreatedFrom"::date)
            AND (re."BGCreatedTo" IS NULL OR (o."CreatedOn" - '05:00:00'::interval)::date <= re."BGCreatedTo"::date)
    );

-- USAGE:
-- 1. Create BGReportExecution record with BGCreatedFrom/BGCreatedTo dates
-- 2. Query view with: WHERE "BGExecutionId" = '<execution_guid>'
-- 3. Use ESQ relationship columns for Account details:
--    - BGAccount.Name (customer name)
--    - BGAccount.Address
--    - BGAccount.City.Name
--    - BGAccount.Region.Name
--    - BGAccount.Zip
--    - BGAccount.Phone
