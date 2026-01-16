#!/usr/bin/env python3
"""
Creatio Authenticated Hybrid Crawler
=====================================
Uses Playwright for authentication + URL discovery
Uses Firecrawl for high-quality content extraction

Usage:
    python3 authenticated_hybrid_crawl.py --target elearning
    python3 authenticated_hybrid_crawl.py --all
"""

import os
import sys
import json
import time
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Set, List, Optional, Dict
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
    print("Error: playwright not installed")
    sys.exit(1)

try:
    from firecrawl import FirecrawlApp
    HAS_FIRECRAWL = True
except ImportError:
    HAS_FIRECRAWL = False
    print("Warning: firecrawl not installed - using Playwright-only mode")

# Configuration
ACADEMY_URL = "https://academy.creatio.com"
COMMUNITY_URL = "https://community.creatio.com"
OUTPUT_DIR = Path("./creatio-docs-authenticated-hybrid")

# Credentials
EMAIL = "amagown@interweave.biz"
PASSWORD = "k1AOF6my!"

# Firecrawl API
FIRECRAWL_API_KEY = os.environ.get("FIRECRAWL_API_KEY", "")

# Crawl targets with deeper link patterns
TARGETS = {
    "elearning": {
        "start_urls": [
            f"{ACADEMY_URL}/e-learning",
            f"{ACADEMY_URL}/e-learning?page=1",
            f"{ACADEMY_URL}/e-learning?page=2",
        ],
        "link_patterns": ["/e-learning/"],
        "max_pages": 300,
    },
    "training": {
        "start_urls": [f"{ACADEMY_URL}/training"],
        "link_patterns": ["/training/"],
        "max_pages": 100,
    },
    "certification": {
        "start_urls": [f"{ACADEMY_URL}/certification"],
        "link_patterns": ["/certification/", "/self-assessment-test/"],
        "max_pages": 50,
    },
    "community": {
        "start_urls": [
            COMMUNITY_URL,
            f"{COMMUNITY_URL}/articles",
            f"{COMMUNITY_URL}/questions",
        ],
        "link_patterns": ["/articles/", "/questions/", "/ideas/", "community.creatio.com"],
        "max_pages": 500,
    },
}


class AuthenticatedHybridCrawler:
    def __init__(self, output_dir: Path, use_firecrawl: bool = True):
        self.output_dir = output_dir
        self.use_firecrawl = use_firecrawl and HAS_FIRECRAWL and FIRECRAWL_API_KEY
        self.visited_urls: Set[str] = set()
        self.discovered_urls: Set[str] = set()
        self.cookies: List[Dict] = []

        self.stats = {
            "total_pages": 0,
            "successful": 0,
            "failed": 0,
            "targets": [],
            "mode": "hybrid" if self.use_firecrawl else "playwright-only",
            "start_time": datetime.now().isoformat(),
        }

        # Create directories
        self.output_dir.mkdir(parents=True, exist_ok=True)
        (self.output_dir / "markdown").mkdir(exist_ok=True)
        (self.output_dir / "html").mkdir(exist_ok=True)
        (self.output_dir / "metadata").mkdir(exist_ok=True)

        self.browser = None
        self.context = None
        self.page = None

        if self.use_firecrawl:
            self.firecrawl = FirecrawlApp(api_key=FIRECRAWL_API_KEY)
            print(f"Mode: Hybrid (Playwright + Firecrawl)")
        else:
            self.firecrawl = None
            print(f"Mode: Playwright-only")

    def generate_id(self, url: str) -> str:
        return hashlib.md5(url.encode()).hexdigest()[:16]

    def normalize_url(self, url: str) -> str:
        parsed = urlparse(url)
        return f"{parsed.scheme}://{parsed.netloc}{parsed.path}".rstrip('/')

    def dismiss_cookie_dialog(self):
        """Dismiss cookie consent dialog if present"""
        try:
            cookie_selectors = [
                '#CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll',
                '#CybotCookiebotDialogBodyButtonAccept',
                'button[id*="accept"]',
            ]
            for selector in cookie_selectors:
                if self.page.locator(selector).count() > 0:
                    self.page.click(selector, timeout=5000)
                    print("  Dismissed cookie dialog")
                    time.sleep(1)
                    return True
        except:
            pass
        return False

    def login_academy(self) -> bool:
        """Login to academy.creatio.com via profile.creatio.com SSO"""
        print("=== Logging in to Academy ===")
        login_url = f"{ACADEMY_URL}/user/login"

        self.page.goto(login_url, wait_until="networkidle", timeout=30000)
        time.sleep(2)
        print(f"  Redirected to: {self.page.url}")

        self.dismiss_cookie_dialog()

        try:
            # Fill email
            for selector in ['input[name="name"]', '#edit-name']:
                if self.page.locator(selector).count() > 0:
                    self.page.fill(selector, EMAIL)
                    print(f"  Filled email using: {selector}")
                    break

            # Fill password
            for selector in ['input[name="pass"]', '#edit-pass']:
                if self.page.locator(selector).count() > 0:
                    self.page.fill(selector, PASSWORD)
                    print(f"  Filled password using: {selector}")
                    break

            # Submit
            for selector in ['input[type="submit"]', 'button[type="submit"]']:
                if self.page.locator(selector).count() > 0:
                    self.page.click(selector)
                    print(f"  Clicked submit using: {selector}")
                    break

            time.sleep(5)

            if "profile.creatio.com/user/login" not in self.page.url and "academy.creatio.com" in self.page.url:
                print(f"  ✓ Login successful! Current URL: {self.page.url}")
                # Capture cookies for Firecrawl
                self.cookies = self.context.cookies()
                return True
            else:
                print(f"  ✗ Login may have failed. URL: {self.page.url}")
                return False

        except Exception as e:
            print(f"  ✗ Login error: {e}")
            return False

    def login_community(self) -> bool:
        """Login to community.creatio.com via SSO"""
        print("=== Logging in to Community ===")
        login_url = f"{COMMUNITY_URL}/user/login"

        try:
            self.page.goto(login_url, wait_until="networkidle", timeout=30000)
            time.sleep(2)
            print(f"  Redirected to: {self.page.url}")

            if "community.creatio.com" in self.page.url and "/user/login" not in self.page.url:
                print(f"  ✓ Already authenticated via SSO!")
                return True

            self.dismiss_cookie_dialog()

            # Fill form if needed
            for selector in ['input[name="name"]', '#edit-name']:
                try:
                    if self.page.locator(selector).count() > 0 and self.page.locator(selector).first.is_visible():
                        self.page.fill(selector, EMAIL, timeout=10000)
                        break
                except:
                    continue

            for selector in ['input[name="pass"]', '#edit-pass']:
                try:
                    if self.page.locator(selector).count() > 0 and self.page.locator(selector).first.is_visible():
                        self.page.fill(selector, PASSWORD, timeout=10000)
                        break
                except:
                    continue

            for selector in ['input[type="submit"]', 'button[type="submit"]']:
                try:
                    if self.page.locator(selector).count() > 0:
                        self.page.click(selector, timeout=10000)
                        break
                except:
                    continue

            time.sleep(5)

            if "community.creatio.com" in self.page.url and "/user/login" not in self.page.url:
                print(f"  ✓ Community login successful!")
                return True

            return False

        except Exception as e:
            print(f"  ✗ Community login error: {e}")
            return False

    def discover_urls_playwright(self, start_urls: List[str], patterns: List[str], max_depth: int = 3) -> Set[str]:
        """Use Playwright to discover all URLs matching patterns"""
        print(f"  Discovering URLs with Playwright (depth={max_depth})...")

        all_urls = set()
        to_visit = list(start_urls)
        visited = set()
        depth = 0

        while to_visit and depth < max_depth:
            next_batch = []
            for url in to_visit:
                normalized = self.normalize_url(url)
                if normalized in visited:
                    continue
                visited.add(normalized)

                try:
                    self.page.goto(url, wait_until="networkidle", timeout=20000)
                    time.sleep(0.5)

                    # Get all links
                    links = self.page.eval_on_selector_all(
                        'a[href]',
                        'elements => elements.map(el => el.href)'
                    )

                    for link in links:
                        if any(pattern in link for pattern in patterns):
                            # Skip assets
                            if any(ext in link.lower() for ext in ['.png', '.jpg', '.jpeg', '.gif', '.svg', '.pdf', '.zip', '.css', '.js']):
                                continue
                            link_normalized = self.normalize_url(link)
                            if link_normalized not in all_urls:
                                all_urls.add(link_normalized)
                                next_batch.append(link)

                except Exception as e:
                    print(f"    Error discovering {url[:50]}: {e}")

            to_visit = next_batch[:100]  # Limit per depth
            depth += 1
            print(f"    Depth {depth}: {len(all_urls)} URLs found")

        return all_urls

    def scrape_with_firecrawl(self, url: str) -> Optional[dict]:
        """Use Firecrawl to extract content with better markdown"""
        try:
            result = self.firecrawl.scrape(
                url,
                formats=['markdown', 'html'],
                only_main_content=True,
            )

            if result and result.get('markdown'):
                return {
                    "url": url,
                    "title": result.get('metadata', {}).get('title', 'Untitled'),
                    "markdown": result.get('markdown', ''),
                    "html": result.get('html', ''),
                }
        except Exception as e:
            print(f"    Firecrawl error for {url[:50]}: {e}")
        return None

    def scrape_with_playwright(self, url: str) -> Optional[dict]:
        """Fallback: use Playwright for content extraction"""
        try:
            from bs4 import BeautifulSoup
            import html2text

            self.page.goto(url, wait_until="networkidle", timeout=20000)
            time.sleep(0.5)

            html = self.page.content()
            title = self.page.title()

            soup = BeautifulSoup(html, 'html.parser')
            for tag in soup.find_all(['nav', 'footer', 'header', 'script', 'style', 'aside']):
                tag.decompose()

            main = soup.find('main') or soup.find('article') or soup.find(class_='content') or soup.body
            content_html = str(main) if main else str(soup)

            h = html2text.HTML2Text()
            h.ignore_links = False
            h.body_width = 0
            markdown = h.handle(content_html)

            return {
                "url": url,
                "title": title,
                "markdown": markdown,
                "html": html,
            }
        except Exception as e:
            print(f"    Playwright scrape error for {url[:50]}: {e}")
        return None

    def save_page(self, data: dict, target: str):
        """Save page content"""
        url = data.get("url", "")
        page_id = self.generate_id(url)

        if data.get("markdown"):
            md_path = self.output_dir / "markdown" / f"{target}_{page_id}.md"
            with open(md_path, "w", encoding="utf-8") as f:
                f.write(f"---\n")
                f.write(f"url: {url}\n")
                f.write(f"title: {data.get('title', 'Untitled')}\n")
                f.write(f"target: {target}\n")
                f.write(f"crawled: {datetime.now().isoformat()}\n")
                f.write(f"---\n\n")
                f.write(data["markdown"])

        if data.get("html"):
            html_path = self.output_dir / "html" / f"{target}_{page_id}.html"
            with open(html_path, "w", encoding="utf-8") as f:
                f.write(data["html"])

        meta_path = self.output_dir / "metadata" / f"{target}_{page_id}.json"
        with open(meta_path, "w", encoding="utf-8") as f:
            json.dump({
                "url": url,
                "title": data.get("title"),
                "target": target,
                "crawled_at": datetime.now().isoformat(),
            }, f, indent=2)

        return page_id

    def crawl_target(self, target_name: str):
        """Crawl a specific target using hybrid approach"""
        if target_name not in TARGETS:
            print(f"Unknown target: {target_name}")
            return

        config = TARGETS[target_name]
        start_urls = config["start_urls"]
        patterns = config["link_patterns"]
        max_pages = config["max_pages"]

        print(f"\n{'='*60}")
        print(f"Crawling: {target_name}")
        print(f"Start URLs: {len(start_urls)}")
        print(f"Max pages: {max_pages}")
        print(f"{'='*60}")

        # Phase 1: URL Discovery with Playwright
        urls_to_scrape = self.discover_urls_playwright(start_urls, patterns, max_depth=3)
        urls_to_scrape = list(urls_to_scrape)[:max_pages]
        print(f"  Found {len(urls_to_scrape)} URLs to scrape")

        # Phase 2: Content extraction
        pages_scraped = 0
        for i, url in enumerate(urls_to_scrape):
            if url in self.visited_urls:
                continue
            self.visited_urls.add(url)

            print(f"  [{i+1}/{len(urls_to_scrape)}] {url[:70]}...")

            # Try Firecrawl first, fallback to Playwright
            data = None
            if self.use_firecrawl:
                data = self.scrape_with_firecrawl(url)

            if not data:
                data = self.scrape_with_playwright(url)

            if data and data.get("markdown"):
                self.save_page(data, target_name)
                self.stats["successful"] += 1
                self.stats["total_pages"] += 1
                pages_scraped += 1
                print(f"    ✓ Saved: {data.get('title', 'Untitled')[:50]}")
            else:
                self.stats["failed"] += 1
                print(f"    ✗ No content")

            time.sleep(0.3)  # Rate limiting

        self.stats["targets"].append(target_name)
        print(f"\n  Completed {target_name}: {pages_scraped} pages")

    def crawl_all(self):
        """Crawl all targets"""
        print(f"\n{'#'*60}")
        print("AUTHENTICATED HYBRID CRAWL - ALL TARGETS")
        print(f"Output: {self.output_dir}")
        print(f"Mode: {self.stats['mode']}")
        print(f"{'#'*60}")

        with sync_playwright() as p:
            self.browser = p.chromium.launch(headless=True)
            self.context = self.browser.new_context()
            self.page = self.context.new_page()

            # Login to Academy
            if not self.login_academy():
                print("Academy login failed, continuing anyway...")

            # Crawl Academy targets
            for target in ["elearning", "training", "certification"]:
                self.crawl_target(target)

            # Login to Community (may already be authenticated via SSO)
            if not self.login_community():
                print("Community login failed, continuing anyway...")

            self.crawl_target("community")

            self.browser.close()

        self.save_stats()
        self.print_summary()

    def crawl_single(self, target_name: str):
        """Crawl a single target"""
        with sync_playwright() as p:
            self.browser = p.chromium.launch(headless=True)
            self.context = self.browser.new_context()
            self.page = self.context.new_page()

            if target_name in ["elearning", "training", "certification"]:
                self.login_academy()
            elif target_name == "community":
                self.login_community()

            self.crawl_target(target_name)
            self.browser.close()

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
        print(f"Mode: {self.stats['mode']}")
        print(f"Total pages: {self.stats['total_pages']}")
        print(f"Successful: {self.stats['successful']}")
        print(f"Failed: {self.stats['failed']}")
        print(f"Targets: {', '.join(self.stats['targets'])}")

        md_count = len(list((self.output_dir / "markdown").glob("*.md")))
        print(f"Markdown files: {md_count}")


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Creatio Authenticated Hybrid Crawler")
    parser.add_argument("--target", choices=list(TARGETS.keys()), help="Crawl specific target")
    parser.add_argument("--all", action="store_true", help="Crawl all targets")
    parser.add_argument("--output-dir", default="./creatio-docs-authenticated-hybrid", help="Output directory")
    parser.add_argument("--no-firecrawl", action="store_true", help="Disable Firecrawl, use Playwright only")
    parser.add_argument("--list-targets", action="store_true", help="List available targets")

    args = parser.parse_args()

    if args.list_targets:
        print("Available targets:")
        for name, config in TARGETS.items():
            print(f"  {name}: {config['start_urls'][0]}")
        return

    use_firecrawl = not args.no_firecrawl
    crawler = AuthenticatedHybridCrawler(Path(args.output_dir), use_firecrawl=use_firecrawl)

    if args.all:
        crawler.crawl_all()
    elif args.target:
        crawler.crawl_single(args.target)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
