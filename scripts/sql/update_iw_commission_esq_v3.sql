-- IW_Commission ESQ Fix v3
-- Purpose: Fix column order to match Excel template
-- Issue: ESQ had 8 columns, template expects 13 - causing misalignment
--
-- Template expected column order:
-- 1. Sales Rep (IWSalesRep)
-- 2. Sales Group (IWSalesGroup)
-- 3. Account (IWAccount)
-- 4. PO Number (IWPONumber)
-- 5. Invoice Date (IWInvoiceDate)
-- 6. Amount (IWAmount)
-- 7. Commission (IWCommissionAmount)
-- 8. Commission Rate (IWCommissionRatePercentage)
-- 9. Transaction Date (IWTransactionDate)
-- 10. Transaction Type (IWTransactionType)
-- 11. Is Note (IWIsNote)
-- 12. Description (IWDescription)
-- 13. Year-Month (IWYearMonth)
--
-- Date: 2026-01-21

UPDATE "IntExcelReport"
SET "IntEsq" = '{
  "rootSchemaName": "IWCommissionReportDataView",
  "operationType": 0,
  "filters": {
    "filterType": 6,
    "rootSchemaName": "IWCommissionReportDataView",
    "items": {}
  },
  "columns": {
    "className": "Terrasoft.QueryColumns",
    "items": {
      "Sales Rep": {
        "className": "Terrasoft.EntityQueryColumn",
        "caption": "Sales Rep",
        "orderDirection": 0,
        "orderPosition": 0,
        "isVisible": true,
        "expression": {
          "className": "Terrasoft.ColumnExpression",
          "expressionType": 0,
          "columnPath": "IWSalesRep"
        }
      },
      "Sales Group": {
        "className": "Terrasoft.EntityQueryColumn",
        "caption": "Sales Group",
        "orderDirection": 0,
        "orderPosition": 1,
        "isVisible": true,
        "expression": {
          "className": "Terrasoft.ColumnExpression",
          "expressionType": 0,
          "columnPath": "IWSalesGroup"
        }
      },
      "Account": {
        "className": "Terrasoft.EntityQueryColumn",
        "caption": "Account",
        "orderDirection": 0,
        "orderPosition": 2,
        "isVisible": true,
        "expression": {
          "className": "Terrasoft.ColumnExpression",
          "expressionType": 0,
          "columnPath": "IWAccount"
        }
      },
      "PO Number": {
        "className": "Terrasoft.EntityQueryColumn",
        "caption": "PO Number",
        "orderDirection": 0,
        "orderPosition": 3,
        "isVisible": true,
        "expression": {
          "className": "Terrasoft.ColumnExpression",
          "expressionType": 0,
          "columnPath": "IWPONumber"
        }
      },
      "Invoice Date": {
        "className": "Terrasoft.EntityQueryColumn",
        "caption": "Invoice Date",
        "orderDirection": 0,
        "orderPosition": 4,
        "isVisible": true,
        "expression": {
          "className": "Terrasoft.ColumnExpression",
          "expressionType": 0,
          "columnPath": "IWInvoiceDate"
        }
      },
      "Amount": {
        "className": "Terrasoft.EntityQueryColumn",
        "caption": "Amount",
        "orderDirection": 0,
        "orderPosition": 5,
        "isVisible": true,
        "expression": {
          "className": "Terrasoft.ColumnExpression",
          "expressionType": 0,
          "columnPath": "IWAmount"
        }
      },
      "Commission": {
        "className": "Terrasoft.EntityQueryColumn",
        "caption": "Commission",
        "orderDirection": 0,
        "orderPosition": 6,
        "isVisible": true,
        "expression": {
          "className": "Terrasoft.ColumnExpression",
          "expressionType": 0,
          "columnPath": "IWCommissionAmount"
        }
      },
      "Commission Rate": {
        "className": "Terrasoft.EntityQueryColumn",
        "caption": "Commission Rate",
        "orderDirection": 0,
        "orderPosition": 7,
        "isVisible": true,
        "expression": {
          "className": "Terrasoft.ColumnExpression",
          "expressionType": 0,
          "columnPath": "IWCommissionRatePercentage"
        }
      },
      "Transaction Date": {
        "className": "Terrasoft.EntityQueryColumn",
        "caption": "Transaction Date",
        "orderDirection": 0,
        "orderPosition": 8,
        "isVisible": true,
        "expression": {
          "className": "Terrasoft.ColumnExpression",
          "expressionType": 0,
          "columnPath": "IWTransactionDate"
        }
      },
      "Transaction Type": {
        "className": "Terrasoft.EntityQueryColumn",
        "caption": "Transaction Type",
        "orderDirection": 0,
        "orderPosition": 9,
        "isVisible": true,
        "expression": {
          "className": "Terrasoft.ColumnExpression",
          "expressionType": 0,
          "columnPath": "IWTransactionType"
        }
      },
      "Is Note": {
        "className": "Terrasoft.EntityQueryColumn",
        "caption": "Is Note",
        "orderDirection": 0,
        "orderPosition": 10,
        "isVisible": true,
        "expression": {
          "className": "Terrasoft.ColumnExpression",
          "expressionType": 0,
          "columnPath": "IWIsNote"
        }
      },
      "Description": {
        "className": "Terrasoft.EntityQueryColumn",
        "caption": "Description",
        "orderDirection": 0,
        "orderPosition": 11,
        "isVisible": true,
        "expression": {
          "className": "Terrasoft.ColumnExpression",
          "expressionType": 0,
          "columnPath": "IWDescription"
        }
      },
      "Year-Month": {
        "className": "Terrasoft.EntityQueryColumn",
        "caption": "Year-Month",
        "orderDirection": 0,
        "orderPosition": 12,
        "isVisible": true,
        "expression": {
          "className": "Terrasoft.ColumnExpression",
          "expressionType": 0,
          "columnPath": "IWYearMonth"
        }
      }
    }
  },
  "isDistinct": false,
  "rowCount": -1,
  "rowsOffset": -1,
  "isPageable": false,
  "allColumns": false,
  "useLocalization": true,
  "useRecordDeactivation": false,
  "serverESQCacheParameters": {
    "cacheLevel": 0,
    "cacheGroup": "",
    "cacheItemName": ""
  },
  "queryOptimize": false,
  "useMetrics": false,
  "adminUnitRoleSources": 0,
  "querySource": 0,
  "ignoreDisplayValues": false,
  "isHierarchical": false
}'
WHERE "IntName" = 'IW_Commission';

-- Verify the update
SELECT "IntName", "IntEsq" FROM "IntExcelReport" WHERE "IntName" = 'IW_Commission';
