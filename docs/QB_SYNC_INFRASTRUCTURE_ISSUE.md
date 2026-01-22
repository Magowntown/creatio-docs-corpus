# QB Sync Infrastructure Issue - Action Required

**Date:** 2026-01-20
**Priority:** HIGH
**Status:** QB Web Connector Offline

---

## Executive Summary

QuickBooks sync from Creatio is failing due to QB Web Connector connectivity issues. **637 orders from Aug 2023 - Jan 2026** are marked as "Processed" but never actually synced to QuickBooks.

---

## Current Situation

### Sync Results (January 2026)

| Status | Orders |
|--------|--------|
| Successfully synced to QB | 336 |
| Failed - Connection Timeout | 57 |
| Stuck in Processing | 100 |
| Config Issues (Discount/Customer) | 2 |

### False "Processed" Orders (Historical)

| Metric | Value |
|--------|-------|
| Orders marked Processed with no QB ID | **637** |
| Date range | Aug 14, 2023 → Jan 16, 2026 |
| Root cause | Sync marks "Processed" even on connection failure |

---

## Connectivity Test Results

**QB Web Connector:** `96.56.203.106:8080`

| Test | Result |
|------|--------|
| Ping | ❌ 100% packet loss |
| Port 8080 | ❌ Connection timeout |
| HTTP request | ❌ No response |

**Last successful sync:** Jan 20, 2026 at 8:43 PM (ORD-16065)
**Connection failed after:** 11:28 PM

---

## QB Configuration in Creatio

### QuickBooks Online (OAuth2)
- **Realm ID:** 4620816365280622260
- **Client ID:** ABpTGWCEBBYm4Xeqz3fDCjfaWIWwvhxzSdzPbXw2G233GbNAcV
- **Last token update:** May 2023 (likely expired)

### QuickBooks Desktop (Web Connector)
- **Server:** 96.56.203.106:8080
- **Status:** OFFLINE

---

## Error Breakdown (59 Total Errors)

| Error Type | Count | Fix Required |
|------------|-------|--------------|
| Connection Timeout | 57 | QB Web Connector must be online |
| Missing Discount Account | 1 | Create "Discount" account in QB Chart of Accounts |
| Customer Not Found | 1 | Verify customer exists in QB |

---

## Action Items

### Immediate (QB/IT Team)

1. **Check QB Web Connector service** on server `96.56.203.106`
   - Is the service running?
   - Check Windows Services for "QuickBooks Web Connector"

2. **Verify network connectivity**
   - Port 8080 must be accessible from Creatio servers
   - Check firewall rules

3. **Restart Web Connector** if needed

### After QB Web Connector is Online

4. **Reset 637 false-processed orders** (SQL to be run):
```sql
UPDATE "BGQuickBooksIntegrationLogDetail"
SET "BGStatusId" = 'c97db3bc-634d-4c90-8432-ec7141c87640',  -- Pending
    "BGErrorMessage" = ''
WHERE "BGStatusId" = 'e7428193-4cf1-4d1b-abae-00e93ab5e1c5'  -- Processed
  AND "BGRecordId" IN (
      SELECT "Id" FROM "Order"
      WHERE "BGQuickBooksId" IS NULL OR "BGQuickBooksId" = ''
  );
```

5. **Run "QB Customer Order Integration"** to process the backlog

### Long-term Fix (e6Solutions)

6. **Fix sync code** to NOT mark orders as "Processed" when connection fails
   - Location: `BGQuickBooksLogDetail.ProcessCustomerOrders()`
   - Issue: Catches connection exception but still marks as Processed
   - Should: Mark as Error with retry capability

### QB Configuration Fixes

7. **Create "Discount" account** in QB Chart of Accounts
   - Required for orders with percentage discounts

8. **Verify missing customer** exists in QB
   - Check order with Customer Issue error

---

## Orders to Verify in QuickBooks

These 10 orders were successfully synced on Jan 19-20:

| Order # | Invoice # | QB Invoice ID |
|---------|-----------|---------------|
| ORD-16076 | 62046 | 42BF65-1768878026 |
| ORD-16078 | 62051 | 42C0A8-1768879067 |
| ORD-16080 | 62053 | 42BFF9-1768878500 |
| ORD-16085 | 62059 | 42BFC8-1768878356 |
| ORD-16086 | 62060 | 42BFD2-1768878397 |
| ORD-16089 | 62064 | 42C06C-1768878885 |
| ORD-16093 | 62076 | 42C20C-1768937103 |
| ORD-16101 | 62074 | 42C1F3-1768937051 |
| ORD-16110 | 62075 | 42C215-1768937155 |

---

## Impact on Commission Reports

Orders not synced to QuickBooks will NOT appear in Commission reports because:
1. Commission data comes from QB ReceivePayment records
2. No QB Invoice = No payment can be recorded = No commission data

**Estimated impact:** 637+ orders missing from historical commission reports

---

## QB Connection Configuration (from Creatio SysSettings)

### QB Desktop (Production) - OFFLINE

| Setting | Value |
|---------|-------|
| `BGQuickBooksLocalUrl` | `http://96.56.203.106` |
| `BGQuickBooksLocalPort` | (empty - defaults to 99, but 8080 in errors) |
| `BGQuickBooksLocalUser` | `qbconnect` |
| `BGQuickBooksLocalTimeout` | (empty - defaults to 90 sec) |

**Status:** ❌ Server not responding

### QB Online (Sandbox) - NOT PRODUCTION

| Setting | Value |
|---------|-------|
| `BGQuickBooksBaseUrl` | `https://sandbox-quickbooks.api.intuit.com` |
| `BGQuickBooksRealmId` | `4620816365305265500` |
| `BGQuickBooksClientId` | `ABNXZf2JipNOTv...` |
| Access/Refresh Tokens | Present (may be expired) |

**Status:** ⚠️ Configured for SANDBOX, not production data

### Why We Can't Switch to QB Online

1. QB Online is pointing to **sandbox** (test) environment
2. Production data is in QB Desktop
3. Switching would require:
   - Change URL to `quickbooks.api.intuit.com`
   - New OAuth tokens for production
   - Verify production RealmId
   - Developer + QB admin involvement

---

## What Was Done From Creatio Side

| Action | Result |
|--------|--------|
| Fixed BGHasQuickBooksLog flag | 626 orders |
| Fixed ProcessListeners flag | 626 orders |
| Created QB log entries | 658 orders |
| Ran QB Customer Order Integration | 336 orders synced |
| Reset QB Busy error (ORD-15956) | Ready for retry |
| Identified all error types | Documented |
| Verified new orders have correct flags | ✅ Working |

**We have done everything possible from Creatio.** Remaining blockers require IT/QB team action.

---

## Contact Information

**QB Web Connector Server:** 96.56.203.106
**Creatio Environment:** PROD (pampabay.creatio.com)

---

*Document created: 2026-01-20*
*Updated: 2026-01-20 (late) - Added connection config details*
*For e6Solutions meeting*
