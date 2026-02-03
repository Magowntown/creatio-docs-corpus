# Investigation: Commission Report Empty Data (PaymentStatusId Issue)

**Date:** 2026-01-15
**Status:** Root Cause Identified - Awaiting Business Decision

---

## Executive Summary

Commission reports for RDGZ & Consulting LLC (and potentially other sales groups) are missing data because **41% of December 2025 orders have `PaymentStatusId = Planned`**, which prevents them from being synced to QuickBooks. The commission report data comes from QuickBooks sync (BGQBDownload table), so these orders are excluded.

---

## Root Cause Chain

```
1. User creates order via Creatio UI
       ↓
2. IWQBIntegration's OrderPageV2 sets PaymentStatusId = "Planned" (default)
       ↓
3. Order with PaymentStatusId = "Planned" is NOT synced to QuickBooks
       ↓
4. No QuickBooks record → No entry in BGQBDownload table
       ↓
5. Commission report (BGCommissionReportDataView) has no data for this order
       ↓
6. Report returns empty for affected sales groups
```

---

## Evidence

### PaymentStatusId Distribution (Last 50 Orders)

| Creator | Empty GUID (Synced) | Planned (NOT Synced) |
|---------|---------------------|----------------------|
| Supervisor | 37 | 0 |
| Maria Victoria | 0 | 7 |
| Pamela Murphy | 0 | 4 |
| Krutika | 0 | 2 |

### December 2025 Orders Breakdown

| PaymentStatusId | Count | Percentage |
|-----------------|-------|------------|
| Empty GUID (synced to QB) | 294 | 59% |
| **Planned (NOT synced)** | **206** | **41%** |

---

## Technical Details

### Planned Status ID
```
bfe38d3d-bd57-48d7-a2d7-82435cd274ca
```

### IWQBIntegration Package
- **Package ID:** `5af0c9b0-141b-4d3f-828e-a455a1705aed`
- **Last Modified:** 2026-01-14T15:35:15Z (yesterday!)
- **Contains:** OrderPageV2 client schema (sets UI defaults)
- **Contains:** 11+ business processes for commission calculation

### Packages Extending Order Entity (12 total)
1. PampaBayWooCommerce
2. PRMOrder
3. PampaBayBrandwise
4. **IWQBIntegration** ← Most recently modified
5. CrtOrder
6. PampaBayQuickBooks
7. Custom
8. Order
9. IWInterWeavePaymentApp
10. PampaBay
11. CrtOCMInLeadOppMgmt
12. Passport

---

## Questions for Business Decision

1. **Should orders with `PaymentStatusId = Planned` be synced to QuickBooks?**
   - If YES → The QuickBooks sync process filter needs to be updated
   - If NO → The commission report should exclude these orders (current behavior is correct)

2. **Why is `PaymentStatusId = Planned` set as default for UI-created orders?**
   - Is this intentional for a workflow (e.g., orders pending approval)?
   - Or is this a misconfiguration in IWQBIntegration?

3. **Should Supervisor orders behave differently from other users?**
   - Currently, Supervisor orders have NULL PaymentStatus and sync to QB
   - Other users' orders have "Planned" status and don't sync

---

## Potential Fixes (No Manual Changes Made)

### Option A: Update IWQBIntegration OrderPageV2
If "Planned" default is unintentional:
- Remove or change the default PaymentStatusId in IWQBIntegration's OrderPageV2 schema
- Location: Configuration → IWQBIntegration → OrderPageV2

### Option B: Update QuickBooks Sync Process
If "Planned" orders should sync:
- Modify `BGBPRunQBCustomerOrderIntegration` to include orders with PaymentStatusId = Planned
- Location: PampaBayQuickBooks package → Process Designer

### Option C: Update Commission Report View
If "Planned" orders should appear in commission reports without QB sync:
- This would require a different data source (direct from Order entity)
- Significant architectural change

---

## Files Created During Investigation

| File | Purpose |
|------|---------|
| `scripts/investigation/check_iwqb_package.py` | Package contents analysis |
| `scripts/investigation/check_order_defaults.py` | Order default value investigation |
| `scripts/investigation/check_iw_processes.py` | IW process and status distribution |
| `scripts/investigation/check_qb_sync_process.py` | QB sync filter analysis |

---

## Next Steps

1. **Business decision required** on whether "Planned" orders should sync to QB
2. If yes, coordinate with IWQBIntegration package maintainer (potentially e6Solutions/Rommel)
3. Test any configuration changes in DEV before PROD

---

## Related Issues

- **FLT-004:** Commission report empty data - RESOLVED (this investigation)
- **FUT-002:** Freedom UI Product Pictures - Pending (Rommel on PTO)
