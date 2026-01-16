#!/usr/bin/env python3
"""
Overnight Creatio Academy Crawl
===============================
Resumable crawler designed for long-running overnight operations.
Saves state after each page so it can be resumed if interrupted.

Usage:
    python3 overnight_crawl.py                    # Start/resume crawl
    python3 overnight_crawl.py --status           # Check progress
    python3 overnight_crawl.py --reset            # Start fresh
"""

import os
import sys
import json
import time
import argparse
from datetime import datetime
from pathlib import Path

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from scripts.crawlers.creatio_academy_crawler_v2 import (
    CreatioAcademyCrawlerV2,
    SECTIONS,
    BASE_URL,
    DOCS_VERSION,
    HAS_PLAYWRIGHT
)
from urllib.parse import urljoin

# Configuration
OUTPUT_DIR = Path("./creatio-docs-full")
STATE_FILE = OUTPUT_DIR / "crawl_state.json"
MAX_PAGES_TOTAL = 5000  # Safety limit

# All sections in priority order (most important first)
CRAWL_ORDER = [
    # Core development
    "dev-getting-started",
    "dev-back-end",
    "dev-front-end",
    "dev-integrations",

    # AI features
    "creatio-ai",

    # No-code
    "no-code-tools",
    "freedom-ui",
    "bpm-tools",
    "dashboards",

    # Products
    "sales",
    "marketing",
    "service",
    "studio",
    "financial",

    # Admin
    "admin",
    "admin-users",
    "admin-security",

    # Other
    "mobile",
    "marketplace",
    "releases",
    "glossary",
]


def load_state() -> dict:
    """Load crawl state from file."""
    if STATE_FILE.exists():
        with open(STATE_FILE) as f:
            return json.load(f)
    return {
        "started_at": datetime.now().isoformat(),
        "last_updated": None,
        "visited_urls": [],
        "failed_urls": [],
        "queue": [],
        "current_section": None,
        "sections_completed": [],
        "total_pages": 0,
        "total_images": 0,
        "total_code_examples": 0,
        "status": "not_started"
    }


def save_state(state: dict):
    """Save crawl state to file."""
    state["last_updated"] = datetime.now().isoformat()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)


def print_status(state: dict):
    """Print crawl status."""
    print("\n" + "=" * 60)
    print("CREATIO ACADEMY CRAWL STATUS")
    print("=" * 60)
    print(f"Status:          {state.get('status', 'unknown')}")
    print(f"Started:         {state.get('started_at', 'N/A')}")
    print(f"Last updated:    {state.get('last_updated', 'N/A')}")
    print(f"Pages crawled:   {state.get('total_pages', 0)}")
    print(f"Images saved:    {state.get('total_images', 0)}")
    print(f"Code examples:   {state.get('total_code_examples', 0)}")
    print(f"Failed URLs:     {len(state.get('failed_urls', []))}")
    print(f"Queue size:      {len(state.get('queue', []))}")
    print(f"Current section: {state.get('current_section', 'None')}")
    print(f"Sections done:   {len(state.get('sections_completed', []))}/{len(CRAWL_ORDER)}")

    completed = state.get('sections_completed', [])
    remaining = [s for s in CRAWL_ORDER if s not in completed]

    if completed:
        print(f"\nCompleted: {', '.join(completed[:5])}{'...' if len(completed) > 5 else ''}")
    if remaining:
        print(f"Remaining: {', '.join(remaining[:5])}{'...' if len(remaining) > 5 else ''}")

    print("=" * 60)

    # Check if complete
    if state.get('status') == 'complete':
        print("\n✅ CRAWL COMPLETE!")
        return True
    return False


def run_crawl():
    """Run the overnight crawl with state persistence."""
    from playwright.sync_api import sync_playwright

    # Load state
    state = load_state()

    if state["status"] == "complete":
        print("Crawl already complete. Use --reset to start fresh.")
        print_status(state)
        return True

    state["status"] = "running"
    save_state(state)

    # Initialize crawler
    crawler = CreatioAcademyCrawlerV2(output_dir=str(OUTPUT_DIR))
    crawler.visited_urls = set(state.get("visited_urls", []))

    print(f"\n🚀 Starting/resuming overnight crawl...")
    print(f"   Output: {OUTPUT_DIR}")
    print(f"   Previously visited: {len(crawler.visited_urls)} pages")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        )
        page = context.new_page()

        try:
            # Process sections in order
            for section_name in CRAWL_ORDER:
                if section_name in state.get("sections_completed", []):
                    continue

                if section_name not in SECTIONS:
                    continue

                state["current_section"] = section_name
                save_state(state)

                print(f"\n{'═' * 50}")
                print(f"SECTION: {section_name}")
                print(f"{'═' * 50}")

                # Build queue for this section
                start_url = urljoin(BASE_URL, SECTIONS[section_name])
                queue = [start_url] if start_url not in crawler.visited_urls else []

                # Load any existing queue items for this section
                queue.extend([u for u in state.get("queue", []) if u not in crawler.visited_urls])
                queue = list(set(queue))

                section_pages = 0
                max_per_section = 300  # Reasonable limit per section

                while queue and section_pages < max_per_section:
                    if state["total_pages"] >= MAX_PAGES_TOTAL:
                        print(f"⚠️ Reached max total pages ({MAX_PAGES_TOTAL})")
                        break

                    url = queue.pop(0)

                    if url in crawler.visited_urls:
                        continue

                    try:
                        # Crawl page
                        new_urls = crawler.crawl_page(page, url)

                        # Update state
                        state["visited_urls"] = list(crawler.visited_urls)
                        state["total_pages"] = crawler.pages_crawled
                        state["total_images"] = crawler.stats.get("images_downloaded", 0)
                        state["total_code_examples"] = crawler.stats.get("code_examples", 0)

                        # Add new URLs to queue (filter to same version)
                        for new_url in new_urls:
                            if new_url not in crawler.visited_urls and f"/docs/{DOCS_VERSION}" in new_url:
                                if new_url not in queue:
                                    queue.append(new_url)

                        state["queue"] = queue[:500]  # Keep queue manageable
                        save_state(state)

                        section_pages += 1

                        # Rate limiting
                        time.sleep(0.3)

                    except Exception as e:
                        print(f"  ✗ Error: {url} - {e}")
                        state["failed_urls"].append({"url": url, "error": str(e)})
                        save_state(state)

                # Mark section complete
                if section_name not in state.get("sections_completed", []):
                    state.setdefault("sections_completed", []).append(section_name)
                save_state(state)

                print(f"  ✓ Section complete: {section_pages} pages")

            # All sections done
            state["status"] = "complete"
            save_state(state)

        except KeyboardInterrupt:
            print("\n\n⏸️  Crawl paused. Run again to resume.")
            state["status"] = "paused"
            save_state(state)

        except Exception as e:
            print(f"\n\n❌ Error: {e}")
            state["status"] = "error"
            state["last_error"] = str(e)
            save_state(state)

        finally:
            browser.close()

    # Save final index
    crawler.save_index()

    # Print final status
    is_complete = print_status(state)

    return is_complete


def main():
    parser = argparse.ArgumentParser(description="Overnight Creatio Academy Crawl")
    parser.add_argument("--status", action="store_true", help="Check crawl status")
    parser.add_argument("--reset", action="store_true", help="Reset and start fresh")
    args = parser.parse_args()

    if args.status:
        state = load_state()
        print_status(state)
        return

    if args.reset:
        if STATE_FILE.exists():
            STATE_FILE.unlink()
            print("State reset. Starting fresh on next run.")
        return

    if not HAS_PLAYWRIGHT:
        print("Error: Playwright not installed")
        return

    # Run the crawl
    is_complete = run_crawl()

    if is_complete:
        print("\n" + "=" * 60)
        print("🎉 CRAWL COMPLETE!")
        print("=" * 60)
        print(f"\nOutput directory: {OUTPUT_DIR}")
        print("\nNext steps:")
        print("  1. Review the markdown files in creatio-docs-full/markdown/")
        print("  2. Check code examples in creatio-docs-full/code/")
        print("  3. Use the data for AI training")


if __name__ == "__main__":
    main()
