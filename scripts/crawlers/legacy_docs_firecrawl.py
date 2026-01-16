#!/usr/bin/env python3
"""
Creatio Legacy Documentation Crawler (v7.x)
============================================
Crawls old-academy.creatio.com using Firecrawl API.

Usage:
    python3 legacy_docs_firecrawl.py [--output-dir OUTPUT] [--section SECTION]
    python3 legacy_docs_firecrawl.py --all  # Crawl all sections
"""

import os
import sys
import json
import time
import hashlib
import argparse
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
from urllib.parse import urljoin, urlparse

# Load environment
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

try:
    from firecrawl import FirecrawlApp
    HAS_FIRECRAWL = True
except ImportError:
    HAS_FIRECRAWL = False
    print("Error: firecrawl-py not installed. Install with: pip install firecrawl-py")
    sys.exit(1)

# Configuration
BASE_URL = "https://old-academy.creatio.com"
OUTPUT_DIR = Path("./creatio-docs-v7")

# All legacy documentation sections
LEGACY_SECTIONS = {
    # Products - User Documentation
    "marketing": "/documents/marketing/last",
    "sales-team": "/documents/sales-team/last",
    "sales-commerce": "/documents/sales-commerce/last",
    "sales-enterprise": "/documents/sales-enterprise/last",
    "service-customer-center": "/documents/customer-center/last",
    "service-enterprise": "/documents/service-enterprise/last",
    "portal": "/documents/portal/last",
    "studio": "/documents/studio/last",
    "mobile": "/documents/mobile/last",

    # Developer Documentation
    "development-sdk": "/documents/technic-sdk/last",
    "marketplace-apps": "/documents/technic-sdkmp/last",
    "bpms": "/documents/technic-bpms/last",

    # Financial Services
    "financial-lending": "/documents/lending/last",
    "financial-journey": "/documents/customer-journey/last",
    "financial-sales": "/documents/bank-sales/last",

    # Specialized
    "field-module": "/documents/field-module/last",
    "pharma": "/documents/pharma/last",

    # Telephony Connectors
    "telephony-asterisk": "/documents/asterisk-connector/last",
    "telephony-avaya": "/documents/connector-avaya/last",
    "telephony-oktell": "/documents/connector-oktell/last",
    "telephony-cisco": "/documents/cisco-finesse-connector/last",
    "telephony-tapi": "/documents/tapi-connector/last",

    # Release Notes
    "release-notes": "/documents/creatio-release-notes-7-17-0",

    # Getting Started & Training
    "getting-started": "/getting-started",
    "video-courses": "/video-courses",
}

class LegacyDocsCrawler:
    def __init__(self, output_dir: Path, api_key: str = None):
        self.output_dir = output_dir
        self.api_key = api_key or os.environ.get("FIRECRAWL_API_KEY")

        if not self.api_key:
            raise ValueError("FIRECRAWL_API_KEY not found in environment")

        self.app = FirecrawlApp(api_key=self.api_key)
        self.stats = {
            "total_pages": 0,
            "successful": 0,
            "failed": 0,
            "sections_completed": [],
            "start_time": datetime.now().isoformat(),
        }

        # Create output directories
        self.output_dir.mkdir(parents=True, exist_ok=True)
        (self.output_dir / "markdown").mkdir(exist_ok=True)
        (self.output_dir / "html").mkdir(exist_ok=True)
        (self.output_dir / "metadata").mkdir(exist_ok=True)

    def generate_id(self, url: str) -> str:
        """Generate unique ID from URL"""
        return hashlib.md5(url.encode()).hexdigest()[:16]

    def save_page(self, url: str, data: dict, section: str):
        """Save crawled page data"""
        page_id = self.generate_id(url)

        # Save markdown
        if data.get("markdown"):
            md_path = self.output_dir / "markdown" / f"{section}_{page_id}.md"
            with open(md_path, "w", encoding="utf-8") as f:
                # Add frontmatter
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
        metadata = {
            "url": url,
            "title": data.get("title"),
            "section": section,
            "crawled_at": datetime.now().isoformat(),
            "links": data.get("links", []),
            "word_count": len(data.get("markdown", "").split()) if data.get("markdown") else 0,
        }
        with open(meta_path, "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=2)

        return page_id

    def crawl_section(self, section_name: str, section_path: str, max_pages: int = 500):
        """Crawl a single documentation section"""
        url = urljoin(BASE_URL, section_path)
        print(f"\n{'='*60}")
        print(f"Crawling section: {section_name}")
        print(f"URL: {url}")
        print(f"Max pages: {max_pages}")
        print(f"{'='*60}")

        try:
            # Use Firecrawl v2 crawl method
            result = self.app.crawl(
                url,
                limit=max_pages,
                scrape_options={
                    "formats": ["markdown", "html"],
                },
                poll_interval=5,
            )

            # Handle different response formats
            pages = []
            if isinstance(result, dict):
                pages = result.get("data", [])
            elif isinstance(result, list):
                pages = result
            elif hasattr(result, 'data'):
                pages = result.data if result.data else []

            if pages:
                print(f"  Found {len(pages)} pages")

                for page in pages:
                    # Handle both dict and object responses
                    if isinstance(page, dict):
                        markdown = page.get("markdown")
                        html = page.get("html")
                        page_url = page.get("url", url)
                        title = page.get("title", "Untitled")
                    else:
                        markdown = getattr(page, 'markdown', None)
                        html = getattr(page, 'html', None)
                        page_url = getattr(page, 'url', url)
                        title = getattr(page, 'title', 'Untitled')

                    if markdown or html:
                        page_data = {
                            "markdown": markdown,
                            "html": html,
                            "title": title,
                            "url": page_url,
                        }
                        page_id = self.save_page(page_url, page_data, section_name)
                        self.stats["successful"] += 1
                        self.stats["total_pages"] += 1
                        print(f"  ✓ Saved: {title[:50]}")
                    else:
                        self.stats["failed"] += 1
                        print(f"  ✗ No content: {page_url}")

                self.stats["sections_completed"].append(section_name)
                return len(pages)
            else:
                print(f"  No data returned for {section_name}")
                return 0

        except Exception as e:
            print(f"  Error crawling {section_name}: {e}")
            import traceback
            traceback.print_exc()
            self.stats["failed"] += 1
            return 0

    def crawl_single_page(self, url: str, section: str = "single"):
        """Crawl a single page using scrape mode"""
        print(f"\nScraping: {url}")

        try:
            result = self.app.scrape(
                url,
                formats=["markdown", "html"],
            )

            # Handle different response formats
            if result:
                if isinstance(result, dict):
                    page_data = result
                else:
                    page_data = {
                        "markdown": getattr(result, 'markdown', None),
                        "html": getattr(result, 'html', None),
                        "title": getattr(result, 'title', 'Untitled'),
                    }

                page_id = self.save_page(url, page_data, section)
                self.stats["successful"] += 1
                self.stats["total_pages"] += 1
                print(f"  ✓ Saved: {page_data.get('title', 'Untitled')}")
                return True
            return False

        except Exception as e:
            print(f"  Error: {e}")
            import traceback
            traceback.print_exc()
            self.stats["failed"] += 1
            return False

    def crawl_all(self, max_pages_per_section: int = 200):
        """Crawl all documentation sections"""
        print(f"\n{'#'*60}")
        print(f"STARTING FULL LEGACY DOCS CRAWL")
        print(f"Sections: {len(LEGACY_SECTIONS)}")
        print(f"Max pages per section: {max_pages_per_section}")
        print(f"Output: {self.output_dir}")
        print(f"{'#'*60}")

        for section_name, section_path in LEGACY_SECTIONS.items():
            self.crawl_section(section_name, section_path, max_pages_per_section)
            # Brief pause between sections to avoid rate limiting
            time.sleep(2)

        self.save_stats()
        self.print_summary()

    def save_stats(self):
        """Save crawl statistics"""
        self.stats["end_time"] = datetime.now().isoformat()
        stats_path = self.output_dir / "crawl_stats.json"
        with open(stats_path, "w") as f:
            json.dump(self.stats, f, indent=2)

    def print_summary(self):
        """Print crawl summary"""
        print(f"\n{'='*60}")
        print("CRAWL COMPLETE")
        print(f"{'='*60}")
        print(f"Total pages crawled: {self.stats['total_pages']}")
        print(f"Successful: {self.stats['successful']}")
        print(f"Failed: {self.stats['failed']}")
        print(f"Sections completed: {len(self.stats['sections_completed'])}")
        print(f"Output directory: {self.output_dir}")

        # Count files
        md_count = len(list((self.output_dir / "markdown").glob("*.md")))
        html_count = len(list((self.output_dir / "html").glob("*.html")))
        print(f"Markdown files: {md_count}")
        print(f"HTML files: {html_count}")


def main():
    parser = argparse.ArgumentParser(description="Crawl Creatio Legacy Documentation (v7.x)")
    parser.add_argument("--output-dir", type=str, default="./creatio-docs-v7",
                        help="Output directory for crawled content")
    parser.add_argument("--section", type=str, choices=list(LEGACY_SECTIONS.keys()),
                        help="Crawl specific section only")
    parser.add_argument("--all", action="store_true", help="Crawl all sections")
    parser.add_argument("--max-pages", type=int, default=200,
                        help="Maximum pages per section")
    parser.add_argument("--url", type=str, help="Crawl single URL")
    parser.add_argument("--list-sections", action="store_true",
                        help="List all available sections")

    args = parser.parse_args()

    if args.list_sections:
        print("Available sections:")
        for name, path in LEGACY_SECTIONS.items():
            print(f"  {name}: {BASE_URL}{path}")
        return

    output_dir = Path(args.output_dir)

    try:
        crawler = LegacyDocsCrawler(output_dir)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)

    if args.url:
        crawler.crawl_single_page(args.url)
    elif args.section:
        crawler.crawl_section(args.section, LEGACY_SECTIONS[args.section], args.max_pages)
    elif args.all:
        crawler.crawl_all(args.max_pages)
    else:
        print("Specify --all, --section, or --url")
        parser.print_help()

    crawler.save_stats()
    crawler.print_summary()


if __name__ == "__main__":
    main()
