# Email Draft: Danlyn - Reports Page Update

**Status:** DRAFT - send after backend deployment
**Date:** 2026-01-29
**To:** Danlyn (Pampa Bay)

---

**Subject:** Reports Page Update - Good Progress + Need Your Input on Final Touches

---

Hi Danlyn,

Hope you're doing well! I wanted to give you an update on the Reports page and explain what we've been working through over the past few weeks.

### What Was Actually Going On

When Creatio pushed their automatic platform update from version 7 (Classic UI) to version 8 (Freedom UI), it wasn't just a visual refresh—it was a fundamental architectural change to how the frontend framework operates. The custom Reports page and packages that BGlobal originally built were designed specifically for version 7's patterns and APIs.

Think of it like this: v7 used a specific framework (ExtJS-based with "mixins" and classic schema inheritance) to connect filters, buttons, and data sources. Version 8 replaced that entire framework with something called "Freedom UI" which uses a completely different binding model and component structure. The code patterns BGlobal wrote simply don't translate—they had to be rewritten from the ground up.

**Important clarification:** Our IWQBIntegration package was initially suspected as a potential conflict, but after investigation, we confirmed it was not the root cause. The issue was purely the v7→v8 framework incompatibility with BGlobal's `BGlobalLookerStudio` and `BGApp_eykaguu` packages that power the Reports page.

**Why reverting wasn't an option:** The v8 update is platform-wide and already integrated with QuickBooks sync, order processing, and invoicing. Rolling back just the Reports page would break data source bindings and potentially corrupt those integrations.

### Where We Are Now

**Working:**
- Commission reports (with Year/Month and Sales Group lookup filters)
- Items by Customer report (with Customer lookup and date range filters)
- Looker Studio reports display correctly via the embedded iframe component
- Excel file generation and downloads for most report types

**Still needs fine-tuning:**
- "Customers did not buy" report — we just resolved an issue where the backend was attempting to query the full `BGSalesByCustomerView` (millions of rows) without date filters, causing an OutOfMemoryException. The fix adds proper ESQ filtering before data retrieval.
- A few other Excel reports may need their filter configurations validated against the actual view columns

### Where I Need Your Help

1. **Filter accuracy check:** Once we deploy these final backend changes, I'd like you or your team to test each report and confirm the filters displayed match your actual business requirements. For example:
   - Does "Items by Customer" need all three date ranges (Created, Shipping, Delivery) or just one?
   - Does "Customers did not buy" need a Customer filter, or is date range + status sufficient?
   - Are there any reports where certain filters should be hidden or required?

2. **Looker Studio access:** The Looker Studio dashboards render correctly within Creatio's iframe, but we don't have Google account credentials to access the actual dashboard configurations. If there are issues with those reports (missing data, incorrect filter parameters being passed, etc.), we'll need either your team or BGlobal to troubleshoot from the Looker Studio side—we can only control what URL parameters Creatio sends to the iframe.

### Next Steps

I'll be deploying the backend service updates (`UsrExcelReportService`) shortly. After that, I'll reach out to coordinate a quick testing session so we can validate the full report suite together.

Let me know if you have any questions or if there's a specific report you want prioritized!

Best,
[Your Name]

---

## Notes for Follow-up

After sending this email:
1. Deploy backend changes to PROD
2. Test "Customers did not buy" report with date filters
3. Schedule testing session with Danlyn
4. Document any filter adjustments requested
