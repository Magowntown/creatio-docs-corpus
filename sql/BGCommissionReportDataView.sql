-- BGCommissionReportDataView SQL View Definition
-- Retrieved from PROD (pampabay.creatio.com) on 2026-01-23
-- Package: PampaBayQuickBooks (f63b797a-cff7-4fdc-9c73-000676e1d209)
-- Schema UId: e60e7a82-955e-4ea9-ae1a-203dd28a0e64

DROP VIEW IF EXISTS "BGCommissionReportDataView";

CREATE OR REPLACE VIEW "BGCommissionReportDataView" AS
    SELECT
      so."Id",
      so."CreatedById",
      so."CreatedOn",
      so."ModifiedById",
      so."ModifiedOn",
      so."ProcessListeners",
      CASE WHEN (
        qb."BGTransactionTypeId" = 'c26d3478-7ac1-49e9-97f9-1c0809552f1f' :: uuid
      ) THEN sum(qb."BGAmount") ELSE CASE WHEN (so."BGShippingCharge" IS NULL) THEN sum(qb."BGAmount") ELSE CASE WHEN (
        sum(qb."BGAmount") = (so."Amount" - so."BGTaxAmount")
      ) THEN (
        sum(qb."BGAmount") - so."BGShippingCharge"
      ) ELSE CASE WHEN (
        (so."Amount" - so."BGTaxAmount") = (0):: numeric
      ) THEN 0.0 ELSE (
        sum(qb."BGAmount") -sum(COALESCE(cm."BGAmount", 0)) - round(
          (
            (
              (sum(qb."BGAmount")-sum(COALESCE(cm."BGAmount", 0))) / (so."Amount" - so."BGTaxAmount")
            ) * so."BGShippingCharge"
          ),
          2
        )
      ) END END END END AS "BGAmount",
      (
        CASE WHEN (qb."BGTransactionTypeId" = 'c26d3478-7ac1-49e9-97f9-1c0809552f1f' :: uuid)
        THEN
            sum(qb."BGAmount")
        ELSE
          CASE WHEN (so."BGShippingCharge" IS NULL)
          THEN
                sum(qb."BGAmount")
          ELSE
            CASE WHEN (
                sum(qb."BGAmount") = (so."Amount" - so."BGTaxAmount")
            ) THEN (
                  sum(qb."BGAmount") - so."BGShippingCharge"
            ) ELSE
                  CASE WHEN ( (so."Amount" - so."BGTaxAmount") = (0):: numeric)
                      THEN
                              0.0
                      ELSE
                          ( sum(qb."BGAmount")-sum(COALESCE(cm."BGAmount", 0)) - round((((sum(qb."BGAmount")-sum(COALESCE(cm."BGAmount", 0))) / (so."Amount" - so."BGTaxAmount")) * so."BGShippingCharge"), 2)
                        )
                      END
                  END
              END
          END * (ce."BGCommissionRate" / 100.00)
      ) AS "BGCommission",
      ce."BGCommissionRate" AS "BGCommissionRatePercentage",
      qb."BGDescription",
      qb."BGInvoiceNumber",
      so."Id" AS "BGOrderId",
      so."BGPONumber",
      ce."BGSalesRepId",
      so."BGInvoiceDate" AS "BGTransactionDate",
      qb."BGTransactionTypeId",
      0 AS "BGIsNote",
      re."Id" AS "BGExecutionId",
      re."BGYearMonthId"
    FROM
      (
        (
          (
            (
              (
                (
                  "BGCommissionReportQBDownload" qb
                  JOIN "Order" so ON (
                    (
                      (so."BGNumberInvoice" IS NOT NULL)
                      AND (
                        (qb."BGCleanInvoiceNumber"):: text <> '' :: text
                      )
                      AND (
                        (so."BGNumberInvoice"):: text = (qb."BGCleanInvoiceNumber"):: text
                      )
                    )
                  )
                )
                JOIN "BGCommissionEarner" ce ON (
                  (ce."BGOrderId" = so."Id")
                )
              )
              LEFT JOIN "Contact" cont ON (
                (cont."Id" = ce."BGSalesRepId")
              )
            )
            JOIN "Employee" rep ON (
              (rep."Id" = ce."BGSalesRepId")
            )
          )
          JOIN "BGReportExecution" re ON (
            (
              (re."BGReportName"):: text = 'Commission' :: text
            )
          )
        )
        LEFT JOIN "BGYearMonth" ym ON (
          (ym."Id" = re."BGYearMonthId")
        )
        LEFT JOIN (SELECT SUM("BGAmount") as "BGAmount","BGInvoiceNumber" FROM "BGCommissionReportQBDownload" GROUP BY "BGInvoiceNumber") cm ON (
          ((qb."BGInvoiceNumber")||'-CM' = (cm."BGInvoiceNumber"))
        )
      )
    WHERE
      (
        (
          (re."BGSalesGroupId" IS NULL)
          OR (
            re."BGSalesGroupId" = rep."BGSalesGroupLookupId"
          )
        )
          AND (
              (ym."Id" IS NULL)
              OR
               (
                EXTRACT('month' FROM qb."BGTransactionDate") = EXTRACT('month' FROM ((ym."BGDateTime") + '1 day' :: interval))
                AND
                EXTRACT('year' FROM qb."BGTransactionDate")= EXTRACT('year' FROM ((ym."BGDateTime") + '1 day' :: interval))
              )
          )
      )
    GROUP BY
      qb."BGTransactionTypeId",
      qb."BGInvoiceNumber",
      qb."BGDescription",
      qb."BGPONumber",
      so."Id",
      so."CreatedById",
      so."CreatedOn",
      so."ModifiedById",
      so."ModifiedOn",
      so."ProcessListeners",
      so."BGShippingCharge",
      so."BGInvoiceDate",
      so."Amount",
      so."BGTaxAmount",
      ce."Id",
      ce."BGCommissionRate",
      ce."BGSalesRepId",
      re."Id",
      re."BGYearMonthId"
    UNION ALL
    -- Manual commission notes (BGIsNote=1)
    SELECT
      crn."Id",
      crn."CreatedById",
      crn."CreatedOn",
      crn."ModifiedById",
      crn."ModifiedOn",
      crn."ProcessListeners",
      crn."BGAmount",
      crn."BGAmount" AS "BGCommission",
      100 AS "BGCommissionRatePercentage",
      crn."Name" AS "BGDescription",
      '' :: character varying AS "BGInvoiceNumber",
      NULL :: uuid AS "BGOrderId",
      '' :: character varying AS "BGPONumber",
      crn."BGSalesRepId",
      crn."BGDate" AS "BGTransactionDate",
      NULL :: uuid AS "BGTransactionTypeId",
      1 AS "BGIsNote",
      re."Id" AS "BGExecutionId",
      re."BGYearMonthId"
    FROM
      (
        (
          (
            "BGCommissionReportNotes" crn
            LEFT JOIN "Employee" emp ON (
              (emp."Id" = crn."BGSalesRepId")
            )
          )
          JOIN "BGReportExecution" re ON (
            (
              (re."BGReportName"):: text = 'Commission' :: text
            )
          )
        )
        LEFT JOIN "BGYearMonth" ym ON (
          (ym."Id" = re."BGYearMonthId")
        )
      )
    WHERE
      (
        (
          (re."BGSalesGroupId" IS NULL)
          OR (
            re."BGSalesGroupId" = emp."BGSalesGroupLookupId"
          )
        )
        AND (
          (ym."Id" IS NULL)
          OR (
            (ym."BGDateTime"):: date <= crn."BGDate"
          )
        )
        AND (
          (ym."Id" IS NULL)
          OR (
            (
              ym."BGDateTime" + '1 mon' :: interval
            ) >= crn."BGDate"
          )
        )
      );

-- Source Tables:
-- 1. BGCommissionReportQBDownload - QuickBooks transaction data
-- 2. Order - Creatio orders (joined on BGNumberInvoice)
-- 3. BGCommissionEarner - Sales rep commission assignments
-- 4. Employee - Sales group filtering
-- 5. BGReportExecution - Report execution context (filters)
-- 6. BGYearMonth - Period filtering
-- 7. BGCommissionReportNotes - Manual commission adjustments (UNION ALL)

-- Business Logic:
-- - BGAmount calculation excludes shipping charges (proportionally allocated)
-- - Credit memos (TransactionTypeId c26d3478-7ac1-49e9-97f9-1c0809552f1f) handled differently
-- - BGIsNote=0 for QB data, BGIsNote=1 for manual notes
-- - Filtering by BGSalesGroupId and BGYearMonth from BGReportExecution
