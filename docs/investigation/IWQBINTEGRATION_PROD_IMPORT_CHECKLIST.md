# IWQBIntegration PROD Import Checklist

**Date:** 2026-01-30
**Package:** IWQBIntegration v8.3.2.4199
**Target:** PROD Environment (pampabay.creatio.com)

---

## Pre-Import Verification

### Phase 1: Dependency Check

- [ ] **1.1** Verify PampaBayQuickBooks package exists in PROD
  ```
  Configuration → Packages → Search "PampaBayQuickBooks"
  ```

- [ ] **1.2** Verify PampaBay package exists in PROD
  ```
  Configuration → Packages → Search "PampaBay"
  ```

- [ ] **1.3** Verify IWInterWeavePaymentApp package exists in PROD
  ```
  Configuration → Packages → Search "IWInterWeavePaymentApp"
  ```

- [ ] **1.4** Document current package versions
  | Package | PROD Version | DEV Version |
  |---------|--------------|-------------|
  | PampaBayQuickBooks | _______ | _______ |
  | PampaBay | _______ | _______ |
  | IWInterWeavePaymentApp | _______ | _______ |
  | IWQBIntegration | _______ | 8.3.2.4199 |

### Phase 2: Process Audit (CRITICAL)

#### Commission Process Versions

- [ ] **2.1** Query PROD to identify active commission processes
  ```sql
  SELECT "Name", "IsActualVersion", "Enabled", "ModifiedOn"
  FROM "SysSchema"
  WHERE "Name" LIKE 'IWCalculateCommission%'
  ORDER BY "Name";
  ```

- [ ] **2.2** Document which version is currently active in PROD
  | Process | Is Active | Enabled | Notes |
  |---------|-----------|---------|-------|
  | IWCalculateCommissiononPayment (Base) | ☐ | ☐ | |
  | IWCalculateCommissiononPaymentV2 | ☐ | ☐ | |
  | IWCalculateCommissiononPaymentIWQBIntegrationV3 | ☐ | ☐ | Triggers on Order! |
  | IWCalculateCommissiononPaymentCustomV4 | ☐ | ☐ | |

- [ ] **2.3** DECISION: Which commission version should be active post-import?
  - [ ] V1 (Base)
  - [ ] V2
  - [ ] V3 (QB Integration - includes Order trigger)
  - [ ] V4 (Custom)

#### Tax Status Process Versions

- [ ] **2.4** Query PROD for tax status processes
  ```sql
  SELECT "Name", "IsActualVersion", "Enabled", "ModifiedOn"
  FROM "SysSchema"
  WHERE "Name" LIKE '%OrderProductTaxStatus%' OR "Name" LIKE '%TaxStatusByOrderSalesTax%'
  ORDER BY "Name";
  ```

- [ ] **2.5** Document tax process status
  | Process | Is Active | Enabled | Notes |
  |---------|-----------|---------|-------|
  | BGSetOrderProductTaxStatusByOrderSalesTax | ☐ | ☐ | V1 |
  | IWSetOrderandProductTaxStatusByOrderSalesTaxV2 | ☐ | ☐ | V2 |

- [ ] **2.6** DECISION: Which tax process should be active?
  - [ ] V1 only
  - [ ] V2 only
  - [ ] Both (not recommended)

#### Invoice Processes

- [ ] **2.7** Query PROD for invoice processes
  ```sql
  SELECT "Name", "IsActualVersion", "Enabled", "ModifiedOn"
  FROM "SysSchema"
  WHERE "Name" LIKE 'IWUpdate%Invoice%' OR "Name" LIKE 'IWAccountCheck%'
  ORDER BY "Name";
  ```

- [ ] **2.8** Document invoice process ownership
  | Field | Authoritative Process | Backup Process |
  |-------|----------------------|----------------|
  | Invoice.PaymentAmount | _________________ | N/A |
  | Invoice.IWCreditedTotal | _________________ | _________________ |
  | Invoice.IWInvoiceCheckbox | _________________ | _________________ |

### Phase 3: Schema Verification

- [ ] **3.1** Verify Order.SalesTax column exists in PROD
  ```sql
  SELECT column_name, data_type
  FROM information_schema.columns
  WHERE table_name = 'Order' AND column_name LIKE '%SalesTax%';
  ```

- [ ] **3.2** Verify Order.BGSalesGroupId column exists (for cascade)
  ```sql
  SELECT column_name, data_type
  FROM information_schema.columns
  WHERE table_name = 'Order' AND column_name LIKE '%SalesGroup%';
  ```

- [ ] **3.3** Verify OrderProduct.TaxStatus column exists
  ```sql
  SELECT column_name, data_type
  FROM information_schema.columns
  WHERE table_name = 'OrderProduct' AND column_name LIKE '%TaxStatus%';
  ```

- [ ] **3.4** Check for conflicting IW columns already in PROD Order
  ```sql
  SELECT column_name
  FROM information_schema.columns
  WHERE table_name = 'Order' AND column_name LIKE 'IWOrder%'
  ORDER BY column_name;
  ```
  Expected: Should be empty OR match DEV exactly

### Phase 4: Entity Extension Conflict Check

- [ ] **4.1** Check if BGApp_eykaguu extends any of these entities
  ```sql
  SELECT s."Name" AS "SchemaName", p."Name" AS "PackageName"
  FROM "SysSchema" s
  JOIN "SysPackage" p ON s."SysPackageId" = p."Id"
  WHERE p."Name" = 'BGApp_eykaguu'
    AND s."Name" IN ('Account', 'Activity', 'Contact', 'Invoice',
                     'InvoiceProduct', 'Opportunity', 'Order',
                     'OrderProduct', 'Product', 'BGSalesGroup');
  ```

- [ ] **4.2** Check if Custom package extends any of these entities
  ```sql
  SELECT s."Name" AS "SchemaName", p."Name" AS "PackageName"
  FROM "SysSchema" s
  JOIN "SysPackage" p ON s."SysPackageId" = p."Id"
  WHERE p."Name" = 'Custom'
    AND s."Name" IN ('Account', 'Activity', 'Contact', 'Invoice',
                     'InvoiceProduct', 'Opportunity', 'Order',
                     'OrderProduct', 'Product', 'BGSalesGroup');
  ```

- [ ] **4.3** Document conflicts found
  | Entity | Also Extended By | Resolution |
  |--------|------------------|------------|
  | | | |

### Phase 5: Backup

- [ ] **5.1** Create PROD database backup
  - Backup name: `pampabay_prod_pre_iwqb_YYYYMMDD`
  - Backup location: _______________________

- [ ] **5.2** Export current IWQBIntegration from PROD (if exists)
  ```
  Configuration → IWQBIntegration → Export package
  ```
  - File saved to: _______________________

- [ ] **5.3** Document current PROD state
  - Total Orders: _______
  - Total OrderProducts: _______
  - Total Invoices: _______
  - Total Payments: _______

---

## Import Procedure

### Phase 6: Import Package

- [ ] **6.1** Navigate to Configuration
  ```
  https://pampabay.creatio.com/0/ClientApp/#/WorkspaceExplorer/
  ```

- [ ] **6.2** Import IWQBIntegration package
  - Click "Install from file"
  - Select: `IWQBIntegration_2026-01-30_08.33.58.zip`
  - Wait for import completion

- [ ] **6.3** Review import log for errors
  - Errors found: ☐ Yes ☐ No
  - If yes, document: _______________________

### Phase 7: Process Configuration (CRITICAL)

- [ ] **7.1** Disable duplicate commission processes
  ```
  Process Designer → Find process → Set "Active" = false
  ```

  Disable these (keep only ONE active):
  - [ ] IWCalculateCommissiononPayment (if not chosen)
  - [ ] IWCalculateCommissiononPaymentV2 (if not chosen)
  - [ ] IWCalculateCommissiononPaymentIWQBIntegrationV3 (if not chosen)
  - [ ] IWCalculateCommissiononPaymentCustomV4 (if not chosen)

- [ ] **7.2** Disable duplicate tax process
  - [ ] BGSetOrderProductTaxStatusByOrderSalesTax (if V2 is chosen)
  - [ ] IWSetOrderandProductTaxStatusByOrderSalesTaxV2 (if V1 is chosen)

- [ ] **7.3** Verify only authoritative invoice processes are active
  - For IWCreditedTotal: Keep only _______________________
  - For IWInvoiceCheckbox: Keep only _______________________

### Phase 8: Compile

- [ ] **8.1** Compile IWQBIntegration package
  ```
  Configuration → IWQBIntegration → Compile
  ```

- [ ] **8.2** Compile all (if needed)
  ```
  Configuration → Actions → Compile all
  ```

- [ ] **8.3** Compilation successful: ☐ Yes ☐ No
  - If no, errors: _______________________

---

## Post-Import Testing

### Phase 9: Order/OrderProduct Tests

- [ ] **9.1** Create new test Order
  - Order Number: _______
  - Sales Tax field set: ☐ Yes ☐ No
  - Expected: Tax status process should trigger

- [ ] **9.2** Verify OrderProduct.TaxStatus was set
  ```sql
  SELECT op."Id", op."Name", op."TaxStatus"
  FROM "OrderProduct" op
  WHERE op."OrderId" = '<test order id>';
  ```
  - TaxStatus populated: ☐ Yes ☐ No

- [ ] **9.3** Modify existing Order
  - If V3 commission is active, verify NO unexpected commission recalculation
  - Commission unchanged: ☐ Yes ☐ No (expected: Yes, unless V3 is intentional)

- [ ] **9.4** Add Product to Order
  - Verify TaxStatus is set on new OrderProduct: ☐ Yes ☐ No

### Phase 10: Payment/Commission Tests

- [ ] **10.1** Create test Payment record
  - Payment ID: _______
  - Associated Order: _______

- [ ] **10.2** Verify commission calculated (only ONCE)
  ```sql
  SELECT "Id", "IWCommissionAmount", "ModifiedOn"
  FROM "IWPayments"  -- or relevant commission table
  WHERE "Id" = '<test payment id>';
  ```
  - Commission calculated: ☐ Yes ☐ No
  - Only one calculation (no duplicates): ☐ Yes ☐ No

- [ ] **10.3** Modify Payment
  - Commission recalculated correctly: ☐ Yes ☐ No

- [ ] **10.4** Delete Payment
  - Related records updated correctly: ☐ Yes ☐ No

### Phase 11: Invoice Tests

- [ ] **11.1** Verify Invoice fields update on Payment changes
  | Field | Updated Correctly |
  |-------|-------------------|
  | PaymentAmount | ☐ Yes ☐ No |
  | IWCreditedTotal | ☐ Yes ☐ No |
  | IWInvoiceCheckbox | ☐ Yes ☐ No |

- [ ] **11.2** No race condition errors in logs
  ```sql
  SELECT * FROM "SysProcessLog"
  WHERE "StartDate" > NOW() - INTERVAL '1 hour'
    AND "ErrorDescription" IS NOT NULL
  ORDER BY "StartDate" DESC;
  ```
  - Errors found: ☐ Yes ☐ No

### Phase 12: Commission Report Test

- [ ] **12.1** Generate Commission report
  - Navigate to Reports page
  - Select Commission report
  - Set YearMonth filter
  - Click Generate

- [ ] **12.2** Report downloads successfully: ☐ Yes ☐ No

- [ ] **12.3** Report data is correct: ☐ Yes ☐ No

### Phase 13: Regression Tests

- [ ] **13.1** Existing Orders still display correctly: ☐ Yes ☐ No

- [ ] **13.2** Order form page loads without errors: ☐ Yes ☐ No

- [ ] **13.3** Invoice form page loads without errors: ☐ Yes ☐ No

- [ ] **13.4** Payment form page loads without errors: ☐ Yes ☐ No

- [ ] **13.5** No JavaScript console errors on key pages: ☐ Yes ☐ No

---

## Rollback Procedure (If Needed)

### Emergency Rollback Steps

1. **Restore database backup**
   ```
   pg_restore -d pampabay pampabay_prod_pre_iwqb_YYYYMMDD.backup
   ```

2. **Or disable problematic processes**
   ```sql
   UPDATE "SysSchema"
   SET "Enabled" = false
   WHERE "Name" IN (
     'IWCalculateCommissiononPayment',
     'IWCalculateCommissiononPaymentV2',
     'IWCalculateCommissiononPaymentIWQBIntegrationV3',
     'IWCalculateCommissiononPaymentCustomV4',
     'BGSetOrderProductTaxStatusByOrderSalesTax',
     'IWSetOrderandProductTaxStatusByOrderSalesTaxV2'
   );
   ```

3. **Flush Creatio caches**
   - Restart application pool
   - Or: Configuration → Actions → Flush caches

---

## Sign-Off

| Step | Completed | Date | Verified By |
|------|-----------|------|-------------|
| Pre-Import Verification | ☐ | | |
| Backup Created | ☐ | | |
| Package Imported | ☐ | | |
| Processes Configured | ☐ | | |
| Compilation Success | ☐ | | |
| Order Tests Pass | ☐ | | |
| Payment Tests Pass | ☐ | | |
| Invoice Tests Pass | ☐ | | |
| Commission Report Works | ☐ | | |
| Regression Tests Pass | ☐ | | |

**Final Approval:** _________________________ Date: _____________

---

*Checklist prepared: 2026-01-30*
