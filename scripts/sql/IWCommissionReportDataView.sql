-- IWCommissionReportDataView
-- Package: IWQBIntegration
-- Purpose: Resolves lookups for IW_Commission report (QuickBooks payments)
-- Filter: Direct on IWPaymentDue (date) + IWSalesGroupId (GUID)
--
-- Created: 2026-01-13
-- Related: FLT-002 - IW_Commission report implementation
--
-- Usage:
--   1. Run this SQL in pgAdmin against DEV database
--   2. Register entity schema in IWQBIntegration package
--   3. Configure IntExcelReport to use this view

CREATE OR REPLACE VIEW public."IWCommissionReportDataView" AS
SELECT
    iw."Id",
    iw."IWPaymentDue" AS "IWTransactionDate",
    iw."IWAmount",
    iw."IWCommissionAmount",
    iw."IWQBInvoiceNumber",
    iw."IWDescription",
    iw."IWMemo",
    iw."IWSalesGroupId",
    sg."BGName" AS "IWSalesGroupName",
    iw."IWAccountId",
    acct."Name" AS "IWAccountName",
    iw."IWPaymentsInvoiceId",
    ord."Number" AS "IWOrderNumber",
    iw."IWOwnerId",
    iw."CreatedOn",
    iw."ModifiedOn"
FROM "IWPayments" iw
LEFT JOIN "BGSalesGroup" sg ON iw."IWSalesGroupId" = sg."Id"
LEFT JOIN "Account" acct ON iw."IWAccountId" = acct."Id"
LEFT JOIN "Order" ord ON iw."IWPaymentsInvoiceId" = ord."Id";

-- Verify the view
-- SELECT * FROM "IWCommissionReportDataView";

-- After creating view, run this to link IW_Commission report:
-- UPDATE "IntExcelReport"
-- SET "IntEntitySchemaNameId" = (
--     SELECT "UId" FROM "SysSchema"
--     WHERE "Name" = 'IWCommissionReportDataView'
--     LIMIT 1
-- )
-- WHERE "Id" = '07c77859-b7e5-43f3-97c6-14113f6a1f6f';
