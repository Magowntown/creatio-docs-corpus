# IWQBIntegration - Next Steps & Improvements

**Date:** 2026-01-30
**Based On:** Consolidated investigation findings from 6 parallel agent analyses

---

## Immediate Next Steps (Before PROD Import)

### Priority 1: Verification Queries (Run in PROD)

Execute these SQL queries in PROD to verify environment readiness:

```sql
-- 1. Check Order.SalesTax column exists
SELECT column_name, data_type
FROM information_schema.columns
WHERE table_name = 'Order' AND column_name LIKE '%SalesTax%';

-- 2. Check OrderProduct.TaxStatus column exists
SELECT column_name, data_type
FROM information_schema.columns
WHERE table_name = 'OrderProduct' AND column_name LIKE '%TaxStatus%';

-- 3. List existing IW columns in Order (detect pre-existing IWQBIntegration)
SELECT column_name
FROM information_schema.columns
WHERE table_name = 'Order' AND column_name LIKE 'IW%'
ORDER BY column_name;

-- 4. Check commission process versions currently active
SELECT "Name", "IsActualVersion", "Enabled"
FROM "SysSchema"
WHERE "Name" LIKE 'IWCalculateCommission%'
ORDER BY "Name";

-- 5. Check tax process versions currently active
SELECT "Name", "IsActualVersion", "Enabled"
FROM "SysSchema"
WHERE "Name" LIKE '%TaxStatusByOrderSalesTax%'
ORDER BY "Name";

-- 6. Verify dependency packages exist
SELECT "Name", "Version", "ModifiedOn"
FROM "SysPackage"
WHERE "Name" IN ('PampaBayQuickBooks', 'PampaBay', 'IWInterWeavePaymentApp')
ORDER BY "Name";
```

### Priority 2: Configuration Decisions Required

| Decision | Options | Recommended | Reason |
|----------|---------|-------------|--------|
| Commission Version | V1, V2, V3, V4 | **V2** | Standard commission, no Order cascade |
| Tax Process | V1, V2 | **V2** | Enhanced version |
| System Setting: IWEnableCommissionV3 | true/false | **false** | Prevents 26x cascade |
| System Setting: IWEnableCommissionV4 | true/false | **false** | Use V2 first, evaluate V4 later |
| System Setting: IWEnableAutoPaymentProcessing | true/false | **Verify with finance** | Business decision |

### Priority 3: Backup Procedure

```bash
# 1. Create PROD database backup
pg_dump -Fc pampabay > pampabay_prod_pre_iwqb_20260130.backup

# 2. Export current IWQBIntegration from PROD (if exists)
# Configuration → Packages → IWQBIntegration → Export

# 3. Document current record counts
psql -c "SELECT 'Order' as entity, COUNT(*) FROM \"Order\"
         UNION ALL SELECT 'OrderProduct', COUNT(*) FROM \"OrderProduct\"
         UNION ALL SELECT 'Invoice', COUNT(*) FROM \"Invoice\"
         UNION ALL SELECT 'IWPayments', COUNT(*) FROM \"IWPayments\";"
```

---

## Suggested Investigation Continuations

### 1. DEV vs PROD Package Version Comparison
**Purpose:** Identify all differences between DEV and PROD IWQBIntegration versions
**Method:** Export PROD package, compare schemas using diff tool
**Estimated Effort:** 30 minutes with agent assistance

### 2. Commission Calculation Logic Analysis
**Purpose:** Understand exact business rules in V1-V4 commission processes
**Method:** Deep dive into process script tasks and formula definitions
**Risk:** V4 may have custom business rules that override standard commission
**Estimated Effort:** 1 hour

### 3. QuickBooks Field Mapping Audit
**Purpose:** Document all QB sync field mappings (Creatio ↔ QuickBooks)
**Method:** Analyze BGQuickBooksIntegrationMapping or similar sync configuration
**Value:** Ensures sync works correctly after import
**Estimated Effort:** 45 minutes

### 4. Invoice Race Condition Resolution
**Purpose:** Redesign invoice update processes to eliminate race condition
**Method:** Merge 3 processes into 1 atomic operation OR add transaction locking
**Risk:** Current design can corrupt IWCreditedTotal values
**Estimated Effort:** 2-4 hours (significant refactoring)

### 5. PCI Compliance Audit
**Purpose:** Verify credit card data handling meets PCI-DSS requirements
**Method:** Review encryption, access controls, audit logging for IWOrderCreditCardNumber, IWOrderCVMValue, etc.
**Risk:** Compliance violation if improperly stored
**Estimated Effort:** 1 hour for initial assessment

---

## Suggested Improvements to IWQBIntegration Package

### Improvement 1: Add Column Filters to V3 StartSignal4

**Problem:** V3 triggers commission recalculation on ANY Order field change
**Current:** StartSignal4 has no filter → 26x duplicate calculations

**Fix:**
```json
{
    "StartSignal4": {
        "EntitySchemaName": "Order",
        "EntityChangeType": "Updated",
        "ColumnUIds": [
            "Amount",
            "CommissionEarnerId",
            "BGSalesGroupId"
        ]
    }
}
```

**Benefit:** Only triggers on commission-affecting changes

### Improvement 2: Consolidate Invoice Update Processes

**Problem:** 3 processes write to same Invoice fields without coordination
**Risk:** Race condition, lost updates, incorrect balances

**Fix:** Create single `IWUpdateInvoiceOnPaymentChange` process:
```
1. Calculate PaymentAmount (sum of linked payments)
2. Calculate IWCreditedTotal (sum of credits)
3. Set IWInvoiceCheckbox based on both values
4. Write all fields in single transaction
```

**Benefit:** Eliminates race condition, ensures consistent calculations

### Improvement 3: Add Process Version Control System Setting

**Problem:** Unclear which commission version should be active
**Risk:** Multiple versions enabled = duplicate calculations

**Fix:** Add `IWActiveCommissionVersion` system setting:
```sql
INSERT INTO "SysSettings" ("Code", "ValueTypeName", "Value")
VALUES ('IWActiveCommissionVersion', 'ShortText', 'V2');
```

Then add check in each process:
```csharp
var activeVersion = SysSettings.GetValue<string>("IWActiveCommissionVersion");
if (activeVersion != "V3") return; // Skip if not this version
```

**Benefit:** Single point of control for commission version

### Improvement 4: Add Audit Logging for PCI Fields

**Problem:** Credit card data stored without audit trail
**Risk:** PCI-DSS compliance violation

**Fix:** Add EventsProcess that logs access to sensitive fields:
```csharp
public void OnOrderSaved(Entity order) {
    var sensitiveFields = new[] {
        "IWOrderCreditCardNumber",
        "IWOrderCVMValue",
        "IWOrderBankAccountNumber"
    };

    foreach (var field in sensitiveFields) {
        if (order.GetChangedColumnValues().Any(c => c.Name == field)) {
            AuditLogger.Log(
                entity: "Order",
                recordId: order.Id,
                field: field,
                action: "Modified",
                user: UserConnection.CurrentUser.Id
            );
        }
    }
}
```

**Benefit:** Audit trail for compliance, easier investigation of unauthorized access

### Improvement 5: Add Health Check Dashboard

**Problem:** No visibility into commission calculation status
**Risk:** Errors go unnoticed until finance discovers discrepancies

**Fix:** Create dashboard showing:
- Commission process execution success/failure rates
- Invoice balance discrepancies (PaymentAmount vs actual payments)
- QB sync status by entity type
- Process execution timing (detect cascade issues)

**Benefit:** Proactive monitoring, earlier error detection

---

## Risk Mitigation Strategy

### If Problems Occur After Import

**Scenario 1: Commission Duplication**
```sql
-- Disable all commission processes immediately
UPDATE "SysSchema"
SET "Enabled" = false
WHERE "Name" LIKE 'IWCalculateCommission%';

-- Flush caches
-- Configuration → Actions → Flush caches
```

**Scenario 2: Tax Status Not Setting**
```sql
-- Check process is enabled
SELECT "Name", "Enabled" FROM "SysSchema"
WHERE "Name" LIKE '%TaxStatusByOrderSalesTax%';

-- If both disabled, enable V2
UPDATE "SysSchema"
SET "Enabled" = true
WHERE "Name" = 'IWSetOrderandProductTaxStatusByOrderSalesTaxV2';
```

**Scenario 3: Invoice Balances Incorrect**
```sql
-- Recalculate all invoice balances
UPDATE "Invoice" inv
SET "PaymentAmount" = (
    SELECT COALESCE(SUM(p."Amount"), 0)
    FROM "IWPayments" p
    WHERE p."InvoiceId" = inv."Id"
);
```

**Scenario 4: Form Layout Broken**
- Open Form Designer
- Rearrange overlapping fields
- Save and compile

---

## Timeline Recommendation

| Phase | Duration | Activities |
|-------|----------|------------|
| Pre-Import | 1 day | Run verification queries, make configuration decisions, create backup |
| Import | 30 min | Import package, compile |
| Configuration | 1 hour | Disable duplicate processes, set system settings |
| Testing | 2-4 hours | Execute test checklist from IWQBINTEGRATION_PROD_IMPORT_CHECKLIST.md |
| Monitoring | 1 week | Watch for commission duplicates, invoice discrepancies |
| Stabilization | Ongoing | Address issues as they arise |

---

## Documents Reference

| Document | Purpose |
|----------|---------|
| `IWQBINTEGRATION_CONFLICT_ASSESSMENT.md` | Full risk analysis |
| `IWQBINTEGRATION_PROD_IMPORT_CHECKLIST.md` | Step-by-step import procedure |
| `IWQBINTEGRATION_DEEP_DIVE_ANALYSIS.md` | Detailed risk investigation |
| `IWQBINTEGRATION_CONSOLIDATED_FINDINGS.md` | All parallel investigation results |
| `IWQBINTEGRATION_INVESTIGATION_LOG.md` | Timeline and methodology |

---

*Next steps document prepared: 2026-01-30*
