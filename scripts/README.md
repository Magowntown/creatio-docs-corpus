# Scripts Directory

> Automation scripts for testing, investigation, deployment, and documentation crawling.

## Directory Structure

```
scripts/
├── testing/          # API and report testing
├── investigation/    # Analysis and debugging (14 creatio_*.py scripts)
├── deployment/       # Deployment automation
├── crawlers/         # Documentation scrapers
├── diagnostics/      # Diagnostic utilities
├── tools/            # General tools
├── utilities/        # Helper scripts
├── fix/              # One-off fix scripts
├── deploy/           # Legacy deploy scripts
└── sql/              # SQL query scripts
```

## Key Scripts

### Investigation Scripts (Playwright-based)

| Script | Purpose |
|--------|---------|
| `investigation/creatio_api_schema.py` | REST API schema fetching |
| `investigation/creatio_apply_handler.py` | Apply handler changes |
| `investigation/creatio_browser_test.py` | Browser automation testing |
| `investigation/creatio_dom_extract.py` | DOM extraction for debugging |
| `investigation/creatio_extract_schema.py` | Schema extraction |
| `investigation/creatio_find_handlers.py` | Find handler definitions |
| `investigation/creatio_find_schema.py` | Schema search |
| `investigation/creatio_inspect.py` | Page inspection |
| `investigation/creatio_interaction_test.py` | UI interaction testing |
| `investigation/creatio_open_schema.py` | Open schema in designer |
| `investigation/creatio_report_button_fix.py` | Report button fixes |
| `investigation/creatio_source_code_test.py` | Source code validation |
| `investigation/creatio_ui_schema.py` | UI schema extraction |
| `investigation/review_report_flow.py` | Full report flow review |

### Testing Scripts

| Script | Purpose |
|--------|---------|
| `testing/test_report_service.py` | API baseline testing |
| `testing/test_items_by_customer.py` | Items by Customer report test |
| `testing/test_commission_dynamic_filters.py` | Commission filter testing |

### Crawlers

| Script | Purpose |
|--------|---------|
| `crawlers/creatio_academy_crawler.py` | V1 documentation crawler |
| `crawlers/creatio_academy_crawler_v2.py` | V2 improved crawler |

## Environment Setup

```bash
# Set credentials (required for most scripts)
export CREATIO_URL="https://pampabay.creatio.com"
export CREATIO_USERNAME="..."
export CREATIO_PASSWORD="..."

# Or load from .env
source ../.env
```

## Usage Examples

```bash
# Test report API
python3 testing/test_report_service.py

# Test specific report
CREATIO_REPORT_CODE=IW_Commission python3 testing/test_report_service.py

# Browser flow test
python3 investigation/review_report_flow.py --env dev

# Extract schema
python3 investigation/creatio_extract_schema.py
```

## Dependencies

- Python 3.9+
- Playwright (`pip install playwright && playwright install`)
- Requests library for API scripts

## Related Documentation

- `docs/reference/RESOURCE_INVENTORY.md` - Script inventory
- `CLAUDE.md` - Quick commands section
