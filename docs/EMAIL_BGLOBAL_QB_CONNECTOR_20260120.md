# Email to BGlobal - QB Web Connector Critical Issue

**To:** Uriel Nusenbaum (BGlobal)
**From:** Andrew Magown
**Date:** January 20, 2026
**Subject:** RE: QB Web Connector - Critical Blocker for Commission Reports

---

Hi Uriel,

Thank you for confirming the QB Web Connector is unreachable from your end as well. This helps us understand the scope of the issue.

I want to provide a comprehensive summary of our investigation today, because **the QB Web Connector being offline is the critical blocker** preventing Commission reports from working correctly.

---

## The Core Problem: QB Web Connector is Offline

**Server:** `96.56.203.106:8080`
**Status:** Completely unreachable

| Test | Result |
|------|--------|
| Ping from our location | ❌ 100% packet loss |
| Telnet from BGlobal (your test) | ❌ Failed |
| Creatio sync attempts | ❌ Connection timeout errors |

**Last successful sync from Creatio:** January 20, 2026 at 8:43 PM
**Connection failed after:** 11:28 PM

---

## Impact of QB Web Connector Being Offline

### Immediate Impact
- **57 orders** failed to sync today due to connection timeouts
- **100 orders** stuck in "Processing" status (connection dropped mid-sync)
- **No new orders can sync** to QuickBooks until this is resolved

### Historical Impact (Bug Discovery)
We discovered that **637 orders from August 2023 to January 2026** were marked as "Processed" in Creatio but **never actually synced to QuickBooks**. The sync code marks orders as successful even when the connection fails - this is a bug that should be addressed.

### Commission Report Impact
- Patricia Goncalves has **1,250 commission earners** but only **27 appear in reports** (2.2%)
- Orders not in QuickBooks = No invoices = No payments recorded = No commission data
- **Estimated 637+ orders missing from historical commission reports**

---

## What We Fixed Today (Creatio Side)

We completed all possible fixes from within Creatio:

| Action | Result |
|--------|--------|
| Fixed BGHasQuickBooksLog flag | 626 orders |
| Fixed ProcessListeners flag | 626 orders |
| Created missing QB log entries | 658 orders |
| Successfully synced orders (before outage) | 336 orders |
| Reset retriable errors | Ready for retry |
| Verified new orders have correct flags | ✅ Working |

**We have exhausted all options from the Creatio side.** The remaining blocker is the QB Web Connector infrastructure.

---

## QB Connection Configuration

From Creatio's SysSettings:

### QB Desktop (Production) - OFFLINE
| Setting | Value |
|---------|-------|
| `BGQuickBooksLocalUrl` | `http://96.56.203.106` |
| `BGQuickBooksLocalPort` | (empty - defaults to 99) |
| `BGQuickBooksLocalUser` | `qbconnect` |

### QB Online - NOT VIABLE
| Setting | Value |
|---------|-------|
| `BGQuickBooksBaseUrl` | `https://sandbox-quickbooks.api.intuit.com` |

The QB Online connection is configured for **sandbox** (test environment), not production. We cannot use it as a fallback.

---

## Clarification on Your Telnet Test

You mentioned trying a telnet test that failed. Could you confirm what server/port you tested? We need to specifically verify connectivity to the **QB Web Connector at `96.56.203.106:8080`** - this is the endpoint Creatio uses to sync orders to QuickBooks Desktop.

---

## Questions for BGlobal

1. **Who manages the QB Web Connector server at 96.56.203.106?**
   - Is this a BGlobal server, Pampa Bay's server, or hosted elsewhere?
   - Who has access to restart the QuickBooks Web Connector Windows service?

2. **IP Restrictions:** You mentioned it might have IP permissions.
   - What IPs are whitelisted?
   - Does Creatio's PROD environment (pampabay.creatio.com) have the correct outbound IPs whitelisted?

3. **Is the server itself online?**
   - Can someone physically or via RDP check if the Windows server is running?
   - Is QuickBooks Desktop running on that server?
   - Is the QB Web Connector service started?

4. **Sync code bug:** The code that marks orders "Processed" even on connection failure - is this something BGlobal can fix, or should e6Solutions handle it?

---

## Requested Actions

| Priority | Action | Owner |
|----------|--------|-------|
| 🔴 **CRITICAL** | Restore QB Web Connector at 96.56.203.106:8080 | IT/Server Admin |
| 🔴 **HIGH** | Verify IP whitelist includes Creatio PROD | IT/BGlobal |
| 🟡 **MEDIUM** | Fix sync bug (marks Processed on failure) | BGlobal/e6Solutions |
| 🟢 **After online** | We will reset 637 false-processed orders | Us |

---

## Looker Studio Access

For Looker Studio dashboard access, please add these users:
- [USER EMAIL 1]
- [USER EMAIL 2]
- [ADD MORE AS NEEDED]

---

## Summary

The Commission report system is architecturally sound - we've verified data flows correctly when infrastructure is working. **The single critical blocker is the QB Web Connector being offline.** Until it's restored:
- No new orders can sync to QuickBooks
- No new invoice/payment data can flow to Commission reports
- 637 historical orders remain unsynced

Please let us know who can help restore the QB Web Connector service, or if there's additional information needed to diagnose the connectivity issue.

Thank you,
Andrew

---

**Attachments available upon request:**
- `docs/QB_SYNC_INFRASTRUCTURE_ISSUE.md` - Full technical details
- `docs/COMMISSION_DATA_PIPELINE_ANALYSIS.md` - Complete data flow analysis
- `docs/TEAM_SUMMARY_20260120.md` - Non-technical summary
