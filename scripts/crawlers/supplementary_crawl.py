#!/usr/bin/env python3
"""
Supplementary Creatio Crawl
===========================
Crawls additional resources not captured in the main overnight crawl:
1. Remaining queued URLs from main crawl
2. Skipped sections (mobile, marketplace, releases, glossary)
3. Community forums
4. Using Firecrawl for faster extraction where possible
"""

import os
import sys
import json
import time
from datetime import datetime
from pathlib import Path
from urllib.parse import urljoin, urlparse

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from scripts.crawlers.creatio_academy_crawler_v2 import (
    CreatioAcademyCrawlerV2,
    SECTIONS,
    BASE_URL,
    DOCS_VERSION,
    HAS_PLAYWRIGHT
)

# Configuration
OUTPUT_DIR = Path("./creatio-docs-supplementary")
STATE_FILE = OUTPUT_DIR / "crawl_state.json"
MAIN_STATE_FILE = Path("./creatio-docs-full/crawl_state.json")

# Additional URLs to crawl
ADDITIONAL_SECTIONS = {
    "mobile": "/docs/8.x/user/mobile_app",
    "marketplace": "/docs/8.x/user/marketplace",
    "releases": "/docs/8.x/user/release_notes",
    "glossary": "/docs/8.x/user/glossary",
}

COMMUNITY_URLS = [
    "https://community.creatio.com/questions",
    "https://community.creatio.com/articles",
    "https://community.creatio.com/ideas",
]

def load_main_state() -> dict:
    """Load state from main crawl to get queued URLs."""
    if MAIN_STATE_FILE.exists():
        with open(MAIN_STATE_FILE) as f:
            return json.load(f)
    return {}

def load_state() -> dict:
    """Load supplementary crawl state."""
    if STATE_FILE.exists():
        with open(STATE_FILE) as f:
            return json.load(f)
    return {
        "started_at": datetime.now().isoformat(),
        "last_updated": None,
        "visited_urls": [],
        "failed_urls": [],
        "queue": [],
        "total_pages": 0,
        "status": "not_started"
    }

def save_state(state: dict):
    """Save crawl state."""
    state["last_updated"] = datetime.now().isoformat()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)

def print_status(state: dict):
    """Print crawl status."""
    print("\n" + "=" * 60)
    print("SUPPLEMENTARY CRAWL STATUS")
    print("=" * 60)
    print(f"Status:          {state.get('status', 'unknown')}")
    print(f"Pages crawled:   {state.get('total_pages', 0)}")
    print(f"Failed URLs:     {len(state.get('failed_urls', []))}")
    print(f"Queue size:      {len(state.get('queue', []))}")
    print("=" * 60)

    if state.get('status') == 'complete':
        print("\n✅ SUPPLEMENTARY CRAWL COMPLETE!")
        return True
    return False

def run_crawl(max_pages: int = 1000):
    """Run supplementary crawl."""
    from playwright.sync_api import sync_playwright

    state = load_state()
    main_state = load_main_state()

    if state["status"] == "complete":
        print("Supplementary crawl already complete.")
        print_status(state)
        return True

    # Build initial queue
    if not state["queue"] and state["status"] == "not_started":
        # Add remaining URLs from main crawl
        queue = main_state.get("queue", [])
        print(f"Adding {len(queue)} URLs from main crawl queue")

        # Add skipped sections
        for section_name, path in ADDITIONAL_SECTIONS.items():
            url = urljoin(BASE_URL, path)
            if url not in queue:
                queue.append(url)
                print(f"Adding section: {section_name}")

        state["queue"] = queue
        state["status"] = "running"
        save_state(state)

    # Get already visited from main crawl
    main_visited = set(main_state.get("visited_urls", []))

    # Initialize crawler
    crawler = CreatioAcademyCrawlerV2(output_dir=str(OUTPUT_DIR))
    crawler.visited_urls = set(state.get("visited_urls", [])) | main_visited

    print(f"\n🚀 Starting supplementary crawl...")
    print(f"   Output: {OUTPUT_DIR}")
    print(f"   Queue: {len(state['queue'])} URLs")
    print(f"   Already visited: {len(crawler.visited_urls)} URLs")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        )
        page = context.new_page()

        try:
            pages_crawled = 0
            queue = state["queue"]

            while queue and pages_crawled < max_pages:
                url = queue.pop(0)

                if url in crawler.visited_urls:
                    continue

                # Only crawl academy.creatio.com for now
                if "academy.creatio.com" not in url:
                    continue

                try:
                    new_urls = crawler.crawl_page(page, url)

                    state["visited_urls"] = list(crawler.visited_urls)
                    state["total_pages"] = crawler.pages_crawled

                    # Add new URLs
                    for new_url in new_urls:
                        if new_url not in crawler.visited_urls and new_url not in queue:
                            if "academy.creatio.com" in new_url:
                                queue.append(new_url)

                    state["queue"] = queue[:500]
                    save_state(state)

                    pages_crawled += 1
                    time.sleep(0.3)

                except Exception as e:
                    print(f"  ✗ Error: {url} - {e}")
                    state["failed_urls"].append({"url": url, "error": str(e)})
                    save_state(state)

            if not queue or pages_crawled >= max_pages:
                state["status"] = "complete"
                save_state(state)

        except KeyboardInterrupt:
            print("\n⏸️ Crawl paused.")
            state["status"] = "paused"
            save_state(state)

        finally:
            browser.close()

    crawler.save_index()
    return print_status(state)

def run_firecrawl_batch(urls: list, max_urls: int = 100):
    """Use Firecrawl for batch extraction."""
    try:
        from firecrawl import FirecrawlApp
        from dotenv import load_dotenv
        load_dotenv()

        api_key = os.getenv("FIRECRAWL_API_KEY")
        if not api_key:
            print("No Firecrawl API key found")
            return []

        fc = FirecrawlApp(api_key=api_key)
        results = []

        for i, url in enumerate(urls[:max_urls]):
            try:
                print(f"[{i+1}/{min(len(urls), max_urls)}] Firecrawl: {url[:60]}...")
                doc = fc.scrape_url(url, params={
                    'formats': ['markdown'],
                    'onlyMainContent': True
                })
                if doc and doc.get('markdown'):
                    results.append({
                        'url': url,
                        'markdown': doc['markdown'],
                        'title': doc.get('metadata', {}).get('title', '')
                    })
                time.sleep(0.5)  # Rate limit
            except Exception as e:
                print(f"  Error: {e}")

        return results

    except ImportError:
        print("Firecrawl not installed")
        return []

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Supplementary Creatio Crawl")
    parser.add_argument("--status", action="store_true", help="Check status")
    parser.add_argument("--max-pages", type=int, default=1000, help="Max pages to crawl")
    parser.add_argument("--firecrawl", action="store_true", help="Use Firecrawl for remaining queue")
    args = parser.parse_args()

    if args.status:
        state = load_state()
        print_status(state)
    elif args.firecrawl:
        main_state = load_main_state()
        queue = main_state.get("queue", [])
        print(f"Using Firecrawl for {len(queue)} URLs...")
        results = run_firecrawl_batch(queue)
        print(f"Extracted {len(results)} pages via Firecrawl")

        # Save results
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        with open(OUTPUT_DIR / "firecrawl_results.json", "w") as f:
            json.dump(results, f, indent=2)
    else:
        if not HAS_PLAYWRIGHT:
            print("Playwright not installed")
            sys.exit(1)
        run_crawl(max_pages=args.max_pages)
