# Overnight Creatio Academy Crawl - Ralph Loop

## Objective
Crawl the entire Creatio Academy documentation to build an AI training corpus for a "Creatio Expert" AI agent.

## Your Task Each Iteration

1. **Check crawl status**:
   ```bash
   python3 scripts/crawlers/overnight_crawl.py --status
   ```

2. **If status is "complete"**:
   - Output: `<promise>CRAWL COMPLETE</promise>`
   - Report final statistics

3. **If status is "not_started", "paused", or "running"**:
   - Continue the crawl:
   ```bash
   python3 scripts/crawlers/overnight_crawl.py
   ```

4. **If status is "error"**:
   - Check the error in `creatio-docs-full/crawl_state.json`
   - Try to fix and resume
   - If unfixable after 3 attempts, report and stop

## Success Criteria
- All 20+ documentation sections crawled
- At least 500 pages collected
- No critical errors blocking progress

## Important
- The crawl auto-saves progress after each page
- If interrupted, it resumes from where it left off
- Be patient - this is a long-running operation
- Check progress every few minutes

## Completion Promise
When the crawl status shows "complete", output:
```
<promise>CRAWL COMPLETE</promise>
```
