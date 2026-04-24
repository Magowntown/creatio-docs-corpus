# Session Log — 2026-03-30: Pampa Bay PROD Investigation (Products, Payments, Orders)

## Summary
Read-only diagnostic of three Pampa Bay Creatio↔QB integration issues via PROD OData API, driven by Danlyn Milito's email chain.

## Issues Investigated

### Issue 1: Product Data Displacement (487 items affected)
**Root cause:** Sync mapped wrong Creatio fields to QB.

**Correct mapping confirmed by Danlyn (color-coded screenshot of CER1725WG):**
| Creatio OData Field | Creatio UI Label | QB Field |
|---|---|---|
| `BGDescription` | Description (Item Details) | QB Purchase + Sales Description |
| `Price` | Price (Item Cost section) | QB Cost |
| `BGWholesalePrice` | Wholesale Price (Prices Detail) | QB Sales Price |

**Common mistake:** `BGMSRP` is NOT the Sales Price field — it's the retail MSRP. `BGWholesalePrice` is correct.

**Scale:** 12,308 total products, 3,359 QB-linked, 487 on Danlyn's affected list.

**Post-3/16 verification:** Only CER2869WG was created by integration after the fix date. Awaiting Danlyn's QB check (expected: Desc="Square Snack Bowl", Cost=$0.96, SalesPrice=$7.00).

**KIC-MAD4018G was ruled out** — created independently in QB and Creatio, not by the integration.

### Issue 2: Auth.net Payment Flow Dead Since 3/17
**Finding:** `IWTransactions` entity in PROD has only 6 records. Newest is TR-00008 from 2026-03-17. No Auth.net transactions created in 13+ days.

**Example:** ORD-17745 (PO 38651, $144.00) — Auth.net Trans ID 1215403578921 settled 3/25 but `IWAuthNetTransactionId` is blank in Creatio, QB Invoice #64254 shows Payments Applied = $0.00.

**QB→Creatio `IWPayments` are still flowing** (latest from 3/28). Only the Auth.net→Creatio direction is broken.

**Key entities discovered:**
- `IWTransactions` — Auth.net transaction records (AUTH.NET tab in Order UI)
- `IWPayments` — Payment records (Payments section in sidebar)
- Order fields: `IWAuthNetTransactionId`, `IWAuthNetTransactionAmount`

### Issue 3: Order Export Filtering
Extended filtering switched on 3/30 (today). Monitoring needed.

## Resolution Timeline (from Dmytro)
- Products: fix mapping tonight (3/30)
- Auth.net payments: load to Creatio tomorrow or Wednesday (3/31 or 4/1)
- Creatio→QB payment push: after Auth.net load
- Full automated sync: by Monday 4/6

## OData Queries Run (PROD: pampabay.creatio.com)
- `Product?$filter=Code eq 'MAS2971WH'` — verified Price=4.33, BGWholesalePrice=22.00, BGCurrentCost=44.00, BGMSRP=55.00
- `Product?$filter=Code eq 'WOW1819WH'` — verified Price=2.50, BGWholesalePrice=16.00
- `Product?$filter=Code eq 'CER1725WG'` — mapped UI to OData: Price=1.28, BGWholesalePrice=7.00, BGDescription="Snack Bowl"
- `Product?$filter=Code eq 'KIC-MAD4018G'` — confirmed no BGQuickBooksId, CreatedOn=3/26
- `Product?$filter=Code eq 'CER2869WG'` — only post-3/16 item with QB link
- `Product/$count` — 12,308 total; with BGQuickBooksId filter — 3,359
- `Order?$filter=Number eq 'ORD-17745'` — full record, confirmed IWAuthNetTransactionId empty
- `IWTransactions?$top=10&$orderby=CreatedOn desc` — only 6 records, newest 3/17
- `IWPayments?$top=10&$orderby=CreatedOn desc` — QB payments flowing, latest 3/28
- `$metadata` — discovered IWTransactions and IWPayments entity names

## Files Created/Modified
- `/home/magown/creatio-hub/docs-corpus/.env` — updated PROD password
- This session log

## Emails Drafted
- To Dmytro: product mapping corrections, Auth.net flow status, CER2869WG test request
- To Danlyn: product mapping confirmation request, payment status update, CER2869WG verification ask
