# Email Draft: QB Team Action Required

---

**To:** [QB Accounting Team]
**Subject:** ACTION REQUIRED: December 2025 Invoice Payments for Commission Reports

---

Hi Team,

We've identified why the Commission reports are showing **$0 sales for December 2025**.

## The Issue

December 2025 invoices haven't been marked as "paid" in QuickBooks yet. Our commission sync pulls payment data (ReceivePayment records) from QB, and without payments recorded, there's no data to sync.

**Scale:** 44 sales reps and 790 commission earners are affected. Top impacted:
- Office: 395 earners missing
- Jim: 124 earners missing
- Patricia Goncalves: 61 earners missing
- Carrie: 42 earners missing
- Carlos: 26 earners missing

**78% of December 2025 orders** show "Unpaid" payment status.

## Action Needed

1. **Process payments** for December 2025 invoices in QuickBooks
   - Review invoices from Dec 1-31, 2025
   - Record payments for completed/collected invoices

2. **After payments are recorded**, let us know and we'll run the commission sync to pull the data into Creatio

## Why This Matters

- Sales reps can't see their December 2025 commission
- Month-end reporting is incomplete
- January 2026 works correctly (because those payments were recorded)

## Timeline

Please prioritize December 2025 invoices when possible. Once payments are in QB, the commission data will sync automatically on the next scheduled run (or we can trigger it manually).

Let me know if you have questions about which invoices need attention.

Thanks,
[Your Name]

---

**Attachments:** See `docs/QB_TEAM_ACTION_REQUIRED.md` for detailed technical documentation including sample missing invoices.
