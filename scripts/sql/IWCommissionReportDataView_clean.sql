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
