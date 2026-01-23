# Report Testing Checklist

**Date:** 2026-01-22
**Environment:** PROD (pampabay.creatio.com)
**Handler:** v12 DEV-Style

---

## Quick Reference

| Report Type | Count | Expected Behavior |
|-------------|-------|-------------------|
| Looker Studio | 12 | Opens in new browser tab |
| Excel | 6 | Downloads .xlsx/.xlsm file |

---

## LOOKER STUDIO REPORTS (12)

These reports have a URL configured and should open in a new browser tab.

**Note:** Requires Google account permissions. If you see "Can't access report", BGlobal needs to share the Looker Studio dashboards with user accounts.

### Test Each Report:

| # | Report Name | Select | Click Generate | Expected | ✓ |
|---|-------------|--------|----------------|----------|---|
| 1 | Sales By Customer | ☐ | ☐ | Opens Looker in new tab | ☐ |
| 2 | Sales By Customer Type | ☐ | ☐ | Opens Looker in new tab | ☐ |
| 3 | Sales by Customer Year Comparison | ☐ | ☐ | Opens Looker in new tab | ☐ |
| 4 | Sales By Item | ☐ | ☐ | Opens Looker in new tab | ☐ |
| 5 | Sales By Item By Type Of Customer | ☐ | ☐ | Opens Looker in new tab | ☐ |
| 6 | Sales By Item Line | ☐ | ☐ | Opens Looker in new tab | ☐ |
| 7 | Sales By Item Theme | ☐ | ☐ | Opens Looker in new tab | ☐ |
| 8 | Sales By Line By Type Of Customer | ☐ | ☐ | Opens Looker in new tab | ☐ |
| 9 | Sales By Line With Ranking | ☐ | ☐ | Opens Looker in new tab | ☐ |
| 10 | Sales By Sales Group | ☐ | ☐ | Opens Looker in new tab | ☐ |
| 11 | Sales By Sales Rep | ☐ | ☐ | Opens Looker in new tab | ☐ |
| 12 | Sales Rep Monthly Report | ☐ | ☐ | Opens Looker in new tab | ☐ |

**Console log to look for:**
```
[v12] Report: <name> | Commission: false
[v12] Report metadata: <name> URL: YES
[v12] Opening Looker Studio in new tab: https://lookerstudio.google.com/...
```

---

## EXCEL REPORTS (6)

These reports download Excel files via UsrExcelReportService.

### Commission Reports (Show Year-Month + Sales Group filters)

| # | Report | Filters Visible? | Select Filters | Click Generate | Downloads? | ✓ |
|---|--------|------------------|----------------|----------------|------------|---|
| 1 | Commission | Year-Month + Sales Group | ☐ | ☐ | Excel file | ☐ |

**Steps for Commission:**
1. Select "Commission" from dropdown
2. ✓ Verify: Red warning label appears
3. ✓ Verify: Year-Month filter appears
4. ✓ Verify: Sales Group filter appears
5. Select a Year-Month (e.g., "2025-01" or "2024-12")
6. Optionally select a Sales Group
7. Click "Generate Report"
8. Wait for download (should start within 10-20 seconds)
9. Open Excel file and verify data

**Console log to look for:**
```
[v12] Report: Commission | Commission: true
[v12] Report metadata: Commission URL: NO
[v12] No Looker URL, using Excel service for: Commission
[v12] Found IntExcelReport: Rpt Commission -> 4ba4f203-7088-41dc-b86d-130c590b3594
[v12] UsrExcelReportService response: {success: true, key: "..."}
```

---

### Non-Commission Excel Reports (No filters shown)

| # | Report | Filters Hidden? | Click Generate | Downloads? | Notes | ✓ |
|---|--------|-----------------|----------------|------------|-------|---|
| 2 | Customers did not buy over a period of time | ☐ | ☐ | Excel file | Slow (>60s) | ☐ |
| 3 | Items by Customer | ☐ | ☐ | Excel file | Slow (>60s) | ☐ |
| 4 | Sales By Item | ☐ | ☐ | Excel file | Slow (>60s) | ☐ |
| 5 | Sales By Item By Type Of Customer | ☐ | ☐ | Excel file | Slow (>60s) | ☐ |
| 6 | Sales By Line | ☐ | ☐ | Excel file | Slow (>60s) | ☐ |

**Steps for Non-Commission Excel:**
1. Select report from dropdown
2. ✓ Verify: Commission filters are HIDDEN
3. ✓ Verify: Warning label is HIDDEN
4. Click "Generate Report"
5. Wait for "Generating Excel report..." message
6. Wait for download (may take 60+ seconds for large reports)
7. If timeout occurs, wait longer - report may still be generating

**Console log to look for:**
```
[v12] Report: <name> | Commission: false
[v12] Report metadata: <name> URL: NO
[v12] No Looker URL, using Excel service for: <name>
[v12] Found IntExcelReport: <template> -> <guid>
```

---

## Troubleshooting

### 502 Bad Gateway
- Server temporary issue
- Wait 30 seconds and try again
- If persists, may need app pool restart

### "Template not found"
- Check IntExcelReport table for matching template
- Template name must match report name or "Rpt <name>"

### Excel Opens with VBA Error
- Template may need updating
- Check for null DateTime values in data

### Looker "Can't access report"
- Google permissions issue
- BGlobal needs to share dashboards with user accounts

### Commission Filters Not Appearing
- Report name must contain "commission" (case insensitive)
- Check console for `[v12] Report: ... | Commission: true`

### Report Takes Too Long
- Normal for large datasets
- Reports without date filters query all historical data
- Consider adding date filter support in future

---

## Sign-Off

| Test | Passed | Tester | Date |
|------|--------|--------|------|
| Commission with filters | ☐ | | |
| Non-Commission Excel reports | ☐ | | |
| Looker Studio reports | ☐ | | |
| UI visibility correct | ☐ | | |

---

*Created: 2026-01-22*
