# Commission Fix - Quick Reference Guide

**For:** Administrators and developers maintaining the commission system
**Last Updated:** 2026-01-19

---

## TL;DR - What to Do

### If Commission Report Shows Empty Data

1. **Check earners exist:**
   ```bash
   python3 scripts/utilities/final_gap_analysis.py
   ```

2. **If earners missing:** Run earner creation script (see below)

3. **If earners exist but report empty:** Check if orders have `BGNumberInvoice`
   - If not, run "Get QuickBooks Commissions" process in Creatio

---

## Key URLs

| Purpose | URL |
|---------|-----|
| PROD | `https://pampabay.creatio.com` |
| DEV | `https://dev-pampabay.creatio.com` |
| pgAdmin | (local installation) |

---

## Common Tasks

### 1. Verify Commission Data Integrity

```bash
cd /home/magown/creatio-report-fix
python3 scripts/utilities/final_gap_analysis.py
```

**Expected Output:**
- Manual QB Download records: 249+
- Auto-created earners: 30+ per day
- Total view records: 34,000+

### 2. Check BGIsNote Schema

```bash
python3 scripts/utilities/find_bgisnote.py
```

**Expected:** `BGIsNote=False (type: bool)` - NOT integer

### 3. Populate QB Download Records (If Needed)

```bash
# Edit script to update date filter if needed
python3 scripts/utilities/populate_qb_download_v2.py
```

### 4. Verify View State

```bash
python3 scripts/utilities/get_current_view.py
```

---

## SQL Quick Reference

### Check View Record Count

```sql
SELECT COUNT(*) FROM public."BGCommissionReportDataView";
```

### Check BGIsNote Type

```sql
SELECT "BGIsNote", pg_typeof("BGIsNote")
FROM public."BGCommissionReportDataView"
LIMIT 1;
-- Expected: false, boolean
```

### Check Commission Earners

```sql
SELECT COUNT(*) FROM public."BGCommissionEarner"
WHERE "CreatedOn" >= CURRENT_DATE;
```

### Check QB Download Records

```sql
SELECT COUNT(*) FROM public."BGCommissionReportQBDownload"
WHERE "BGQuickBooksId" LIKE 'MANUAL-%';
```

---

## Entity Relationships

```
Order
├── BGCommissionEarner (1:many)
│   ├── BGOrderId → Order.Id
│   ├── BGSalesRepId → Employee.Id
│   └── BGCommissionRate (decimal)
│
└── BGCommissionReportQBDownload (via BGNumberInvoice)
    ├── BGCleanInvoiceNumber = Order.BGNumberInvoice
    ├── BGOrderId → Order.Id
    └── BGSalesRepId → Employee.Id

BGCommissionReportDataView (READ-ONLY)
├── Source 1: BGCommissionReportQBDownload (BGIsNote=FALSE)
└── Source 2: BGCommissionReportNotes (BGIsNote=TRUE)
```

---

## Troubleshooting

### Error: "cannot change data type of view column"

**Solution:** Use DROP + CREATE in transaction:
```sql
BEGIN;
DROP VIEW IF EXISTS public."BGCommissionReportDataView";
CREATE VIEW public."BGCommissionReportDataView" AS ...;
COMMIT;
```

### Error: "cannot insert into view"

**Solution:** Insert into source tables:
- Regular commissions: `BGCommissionReportQBDownload`
- Manual notes: `BGCommissionReportNotes`

### Error: FK constraint on BGCustomerId

**Solution:** Omit `BGCustomerId` field from inserts (nullable)

### Records not appearing in view

**Cause:** Order.BGNumberInvoice doesn't match

**Solution:** Run "Get QuickBooks Commissions" process

---

## File Locations

| File | Purpose |
|------|---------|
| `scripts/sql/BGCommissionReportDataView_BGIsNote_fix.sql` | View schema fix |
| `scripts/utilities/populate_qb_download_v2.py` | QB download population |
| `scripts/utilities/final_gap_analysis.py` | Data integrity check |
| `scripts/utilities/find_bgisnote.py` | BGIsNote location |
| `docs/COMMISSION_FIX_COMPLETE.md` | Full documentation |
| `docs/ACTION_LOG.md` | What was done |

---

## Process Dependencies

```
Order Created
    ↓
[Add Commission Earners] → BGCommissionEarner created
    ↓
[QB Sync] → Order.BGNumberInvoice populated
    ↓
[Get QuickBooks Commissions] → BGCommissionReportQBDownload created
    ↓
BGCommissionReportDataView → Shows in report
```

---

## Contacts

| Role | Action |
|------|--------|
| DB Admin | Apply SQL fixes in pgAdmin |
| Creatio Admin | Run business processes |
| QB Team | Mark invoices as paid |

---

## Daily Health Check

Run this to verify system health:

```bash
cd /home/magown/creatio-report-fix
python3 scripts/utilities/final_gap_analysis.py | grep -E "(✅|❌|⚠️|Total|Created)"
```

**Healthy Output:**
```
• Auto-earner creation: ✅ WORKING
Total view records: 34,XXX
```
