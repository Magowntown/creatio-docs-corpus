#!/usr/bin/env python3
"""
Creatio Legacy Documentation Crawler (v7.x) - Hybrid Approach
==============================================================
Uses Playwright for URL discovery and Firecrawl for content extraction.

Usage:
    python3 legacy_docs_hybrid.py --all
    python3 legacy_docs_hybrid.py --section development-sdk
"""

import os
import sys
import json
import time
import hashlib
import argparse
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Set, Optional
from urllib.parse import urljoin, urlparse
from concurrent.futures import ThreadPoolExecutor, as_completed

# Load environment
try:
    with open('.env') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, val = line.split('=', 1)
                os.environ[key] = val
except:
    pass

try:
    from playwright.sync_api import sync_playwright
    HAS_PLAYWRIGHT = True
except ImportError:
    HAS_PLAYWRIGHT = False
    print("Warning: playwright not installed")

try:
    from firecrawl import FirecrawlApp
    HAS_FIRECRAWL = True
except ImportError:
    HAS_FIRECRAWL = False
    print("Warning: firecrawl-py not installed")

try:
    from bs4 import BeautifulSoup
    import html2text
    HAS_BS4 = True
except ImportError:
    HAS_BS4 = False

# Configuration
BASE_URL = "https://old-academy.creatio.com"
OUTPUT_DIR = Path("./creatio-docs-v7")

# Documentation sections - Developer docs use specific version, User docs use /last/
LEGACY_SECTIONS = {
    # Developer Documentation (v7.16 specific)
    "development-sdk": "/documents/technic-sdk/7-16/creatio-development-guide",
    "marketplace-apps": "/documents/technic-sdkmp/7-16/marketplace-apps-development",
    "bpms": "/documents/technic-bpms/7-16/bpm-tools",
    # User Documentation (use /last/ for better link discovery)
    "marketing": "/documents/marketing/last/marketing-creatio",
    "sales-team": "/documents/sales-team/last/sales-creatio-team",
    "sales-enterprise": "/documents/sales-enterprise/last/sales-creatio-enterprise",
    "service-enterprise": "/documents/service-enterprise/last/service-creatio-enterprise",
    "studio": "/documents/studio/last/studio-creatio",
    "mobile": "/documents/mobile/last/mobile-creatio",
}

class LegacyHybridCrawler:
    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
        self.api_key = os.environ.get("FIRECRAWL_API_KEY")
        self.firecrawl = FirecrawlApp(api_key=self.api_key) if self.api_key else None
        self.visited_urls: Set[str] = set()
        self.stats = {
            "total_pages": 0,
            "successful": 0,
            "failed": 0,
            "sections": [],
            "start_time": datetime.now().isoformat(),
        }

        # Create directories
        self.output_dir.mkdir(parents=True, exist_ok=True)
        (self.output_dir / "markdown").mkdir(exist_ok=True)
        (self.output_dir / "html").mkdir(exist_ok=True)
        (self.output_dir / "metadata").mkdir(exist_ok=True)

    def generate_id(self, url: str) -> str:
        return hashlib.md5(url.encode()).hexdigest()[:16]

    def normalize_url(self, url: str) -> str:
        """Normalize URL for deduplication"""
        parsed = urlparse(url)
        return f"{parsed.scheme}://{parsed.netloc}{parsed.path}".rstrip('/')

    def discover_urls_playwright(self, start_url: str, max_depth: int = 3) -> List[str]:
        """Use Playwright to discover URLs by navigating the site"""
        print(f"  Discovering URLs with Playwright from: {start_url}")
        urls = set()
        to_visit = [(start_url, 0)]
        visited = set()

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            while to_visit and len(urls) < 500:
                current_url, depth = to_visit.pop(0)
                normalized = self.normalize_url(current_url)

                if normalized in visited or depth > max_depth:
                    continue

                visited.add(normalized)

                try:
                    page.goto(current_url, wait_until="networkidle", timeout=30000)
                    time.sleep(1)  # Let JS render

                    # Find all links
                    links = page.eval_on_selector_all(
                        'a[href]',
                        'elements => elements.map(el => el.href)'
                    )

                    for link in links:
                        if link and BASE_URL in link and '/documents/' in link:
                            # Skip image and asset URLs
                            if any(ext in link.lower() for ext in ['.png', '.jpg', '.jpeg', '.gif', '.svg', '.pdf', '.zip', '.css', '.js']):
                                continue
                            link_normalized = self.normalize_url(link)
                            if link_normalized not in visited:
                                urls.add(link)
                                if depth < max_depth:
                                    to_visit.append((link, depth + 1))

                    urls.add(current_url)
                    print(f"    Found {len(urls)} URLs (depth {depth})")

                except Exception as e:
                    print(f"    Error navigating {current_url}: {e}")

            browser.close()

        return list(urls)

    def scrape_with_firecrawl(self, url: str) -> Optional[dict]:
        """Scrape a single URL with Firecrawl"""
        try:
            result = self.firecrawl.scrape(url, formats=["markdown", "html"])
            return {
                "url": url,
                "markdown": getattr(result, 'markdown', None),
                "html": getattr(result, 'html', None),
                "title": getattr(result, 'title', 'Untitled'),
            }
        except Exception as e:
            print(f"    Firecrawl error for {url}: {e}")
            return None

    def scrape_with_playwright(self, url: str) -> Optional[dict]:
        """Fallback: scrape with Playwright if Firecrawl fails"""
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()
                page.goto(url, wait_until="networkidle", timeout=30000)
                time.sleep(2)

                title = page.title()
                html = page.content()

                # Convert HTML to markdown
                markdown = ""
                if HAS_BS4:
                    soup = BeautifulSoup(html, 'html.parser')
                    # Remove nav, footer, etc
                    for tag in soup.find_all(['nav', 'footer', 'header', 'script', 'style']):
                        tag.decompose()

                    h = html2text.HTML2Text()
                    h.ignore_links = False
                    h.ignore_images = False
                    markdown = h.handle(str(soup))

                browser.close()
                return {
                    "url": url,
                    "markdown": markdown,
                    "html": html,
                    "title": title,
                }
        except Exception as e:
            print(f"    Playwright error for {url}: {e}")
            return None

    def save_page(self, data: dict, section: str):
        """Save page content"""
        url = data.get("url", "")
        page_id = self.generate_id(url)

        # Save markdown
        if data.get("markdown"):
            md_path = self.output_dir / "markdown" / f"{section}_{page_id}.md"
            with open(md_path, "w", encoding="utf-8") as f:
                f.write(f"---\n")
                f.write(f"url: {url}\n")
                f.write(f"title: {data.get('title', 'Untitled')}\n")
                f.write(f"section: {section}\n")
                f.write(f"crawled: {datetime.now().isoformat()}\n")
                f.write(f"---\n\n")
                f.write(data["markdown"])

        # Save HTML
        if data.get("html"):
            html_path = self.output_dir / "html" / f"{section}_{page_id}.html"
            with open(html_path, "w", encoding="utf-8") as f:
                f.write(data["html"])

        # Save metadata
        meta_path = self.output_dir / "metadata" / f"{section}_{page_id}.json"
        with open(meta_path, "w", encoding="utf-8") as f:
            json.dump({
                "url": url,
                "title": data.get("title"),
                "section": section,
                "crawled_at": datetime.now().isoformat(),
            }, f, indent=2)

        return page_id

    def crawl_section(self, section_name: str, section_path: str, max_pages: int = 100):
        """Crawl a documentation section"""
        start_url = urljoin(BASE_URL, section_path)
        print(f"\n{'='*60}")
        print(f"Crawling: {section_name}")
        print(f"Start URL: {start_url}")
        print(f"{'='*60}")

        # Discover URLs
        if HAS_PLAYWRIGHT:
            urls = self.discover_urls_playwright(start_url, max_depth=3)
        else:
            urls = [start_url]

        print(f"  Total URLs discovered: {len(urls)}")
        urls = urls[:max_pages]

        # Scrape each URL
        for i, url in enumerate(urls):
            normalized = self.normalize_url(url)
            if normalized in self.visited_urls:
                continue

            self.visited_urls.add(normalized)
            print(f"  [{i+1}/{len(urls)}] Scraping: {url[:80]}...")

            # Try Firecrawl first, fallback to Playwright
            data = None
            if self.firecrawl:
                data = self.scrape_with_firecrawl(url)

            if not data and HAS_PLAYWRIGHT:
                data = self.scrape_with_playwright(url)

            if data and (data.get("markdown") or data.get("html")):
                self.save_page(data, section_name)
                self.stats["successful"] += 1
                self.stats["total_pages"] += 1
                print(f"    ✓ Saved: {data.get('title', 'Untitled')[:50]}")
            else:
                self.stats["failed"] += 1
                print(f"    ✗ Failed")

            # Rate limiting
            time.sleep(1)

        self.stats["sections"].append(section_name)

    def crawl_all(self, max_pages_per_section: int = 100):
        """Crawl all sections"""
        print(f"\n{'#'*60}")
        print("STARTING FULL LEGACY DOCS CRAWL")
        print(f"Sections: {len(LEGACY_SECTIONS)}")
        print(f"Output: {self.output_dir}")
        print(f"{'#'*60}")

        for name, path in LEGACY_SECTIONS.items():
            self.crawl_section(name, path, max_pages_per_section)

        self.save_stats()
        self.print_summary()

    def save_stats(self):
        self.stats["end_time"] = datetime.now().isoformat()
        with open(self.output_dir / "crawl_stats.json", "w") as f:
            json.dump(self.stats, f, indent=2)

    def print_summary(self):
        print(f"\n{'='*60}")
        print("CRAWL COMPLETE")
        print(f"{'='*60}")
        print(f"Total pages: {self.stats['total_pages']}")
        print(f"Successful: {self.stats['successful']}")
        print(f"Failed: {self.stats['failed']}")
        print(f"Sections: {len(self.stats['sections'])}")

        md_count = len(list((self.output_dir / "markdown").glob("*.md")))
        print(f"Markdown files: {md_count}")


def main():
    parser = argparse.ArgumentParser(description="Crawl Creatio Legacy Docs (Hybrid)")
    parser.add_argument("--output-dir", type=str, default="./creatio-docs-v7")
    parser.add_argument("--section", type=str, choices=list(LEGACY_SECTIONS.keys()))
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--max-pages", type=int, default=100)
    parser.add_argument("--list-sections", action="store_true")

    args = parser.parse_args()

    if args.list_sections:
        for name, path in LEGACY_SECTIONS.items():
            print(f"  {name}: {BASE_URL}{path}")
        return

    crawler = LegacyHybridCrawler(Path(args.output_dir))

    if args.section:
        crawler.crawl_section(args.section, LEGACY_SECTIONS[args.section], args.max_pages)
    elif args.all:
        crawler.crawl_all(args.max_pages)
    else:
        parser.print_help()

    crawler.save_stats()
    crawler.print_summary()


if __name__ == "__main__":
    main()
