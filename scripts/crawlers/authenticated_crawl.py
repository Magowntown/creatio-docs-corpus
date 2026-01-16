#!/usr/bin/env python3
"""
Creatio Authenticated Content Crawler
======================================
Crawls e-learning, training, certification, and community content
using authenticated Playwright session.

Usage:
    python3 authenticated_crawl.py --target elearning
    python3 authenticated_crawl.py --target community
    python3 authenticated_crawl.py --all
"""

import os
import sys
import json
import time
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Set, List, Optional
from urllib.parse import urljoin, urlparse

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
    from bs4 import BeautifulSoup
    import html2text
    HAS_BS4 = True
except ImportError:
    HAS_BS4 = False
    print("Warning: bs4/html2text not installed - markdown conversion limited")

# Configuration
ACADEMY_URL = "https://academy.creatio.com"
COMMUNITY_URL = "https://community.creatio.com"
OUTPUT_DIR = Path("./creatio-docs-authenticated")

# Credentials
EMAIL = "amagown@interweave.biz"
PASSWORD = "k1AOF6my!"

# Crawl targets
TARGETS = {
    "elearning": {
        "start_url": f"{ACADEMY_URL}/e-learning",
        "link_patterns": ["/e-learning/"],
        "max_pages": 200,
    },
    "training": {
        "start_url": f"{ACADEMY_URL}/training",
        "link_patterns": ["/training/"],
        "max_pages": 50,
    },
    "certification": {
        "start_url": f"{ACADEMY_URL}/certification",
        "link_patterns": ["/certification/"],
        "max_pages": 30,
    },
    "community": {
        "start_url": COMMUNITY_URL,
        "link_patterns": ["/articles/", "/questions/", "/ideas/", "community.creatio.com"],
        "max_pages": 300,
    },
}


class AuthenticatedCrawler:
    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
        self.visited_urls: Set[str] = set()
        self.stats = {
            "total_pages": 0,
            "successful": 0,
            "failed": 0,
            "targets": [],
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

    def generate_id(self, url: str) -> str:
        return hashlib.md5(url.encode()).hexdigest()[:16]

    def normalize_url(self, url: str) -> str:
        parsed = urlparse(url)
        # Strip fragment and query for deduplication
        return f"{parsed.scheme}://{parsed.netloc}{parsed.path}".rstrip('/')

    def dismiss_cookie_dialog(self):
        """Dismiss cookie consent dialog if present"""
        try:
            # Try common cookie consent button selectors
            cookie_selectors = [
                '#CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll',
                '#CybotCookiebotDialogBodyButtonAccept',
                'button[id*="accept"]',
                'button[id*="Allow"]',
                '.cookie-accept',
                '[data-cookiebanner="accept_button"]',
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

    def login_academy(self):
        """Login to academy.creatio.com via profile.creatio.com SSO"""
        print("=== Logging in to Academy ===")
        login_url = f"{ACADEMY_URL}/user/login"

        # Note: This redirects to profile.creatio.com for centralized auth
        self.page.goto(login_url, wait_until="networkidle", timeout=30000)
        time.sleep(2)
        print(f"  Redirected to: {self.page.url}")

        # Dismiss cookie dialog first
        self.dismiss_cookie_dialog()

        # Fill login form
        try:
            # Try different selectors for email/username field
            email_selectors = ['input[name="name"]', 'input[name="email"]', 'input[type="email"]', '#edit-name']
            for selector in email_selectors:
                if self.page.locator(selector).count() > 0:
                    self.page.fill(selector, EMAIL)
                    print(f"  Filled email using: {selector}")
                    break

            # Password field
            pass_selectors = ['input[name="pass"]', 'input[type="password"]', '#edit-pass']
            for selector in pass_selectors:
                if self.page.locator(selector).count() > 0:
                    self.page.fill(selector, PASSWORD)
                    print(f"  Filled password using: {selector}")
                    break

            # Submit
            submit_selectors = ['input[type="submit"]', 'button[type="submit"]', '#edit-submit']
            for selector in submit_selectors:
                if self.page.locator(selector).count() > 0:
                    self.page.click(selector)
                    print(f"  Clicked submit using: {selector}")
                    break

            time.sleep(5)

            # Check if login succeeded
            # After successful login, URL is academy.creatio.com/?login=XXXXXXX (token)
            # vs login page which is profile.creatio.com/user/login
            if "profile.creatio.com/user/login" not in self.page.url and "academy.creatio.com" in self.page.url:
                print(f"  ✓ Login successful! Current URL: {self.page.url}")
                return True
            else:
                print(f"  ✗ Login may have failed. URL: {self.page.url}")
                return False

        except Exception as e:
            print(f"  ✗ Login error: {e}")
            return False

    def login_community(self):
        """Login to community.creatio.com via profile.creatio.com SSO"""
        print("=== Logging in to Community ===")
        login_url = f"{COMMUNITY_URL}/user/login"

        try:
            # Note: This redirects to profile.creatio.com for centralized auth
            self.page.goto(login_url, wait_until="networkidle", timeout=30000)
            time.sleep(2)
            print(f"  Redirected to: {self.page.url}")

            # If already logged in via Academy SSO, may skip to community directly
            if "community.creatio.com" in self.page.url and "/user/login" not in self.page.url:
                print(f"  ✓ Already authenticated via SSO!")
                return True

            # Dismiss cookie dialog
            self.dismiss_cookie_dialog()

            # Fill login form with individual selectors
            email_filled = False
            for selector in ['input[name="name"]', '#edit-name', 'input[type="email"]']:
                try:
                    if self.page.locator(selector).count() > 0 and self.page.locator(selector).first.is_visible():
                        self.page.fill(selector, EMAIL, timeout=10000)
                        email_filled = True
                        print(f"  Filled email using: {selector}")
                        break
                except:
                    continue

            pass_filled = False
            for selector in ['input[name="pass"]', '#edit-pass', 'input[type="password"]']:
                try:
                    if self.page.locator(selector).count() > 0 and self.page.locator(selector).first.is_visible():
                        self.page.fill(selector, PASSWORD, timeout=10000)
                        pass_filled = True
                        print(f"  Filled password using: {selector}")
                        break
                except:
                    continue

            if email_filled and pass_filled:
                for selector in ['input[type="submit"]', 'button[type="submit"]', '#edit-submit']:
                    try:
                        if self.page.locator(selector).count() > 0:
                            self.page.click(selector, timeout=10000)
                            print(f"  Clicked submit using: {selector}")
                            break
                    except:
                        continue

                time.sleep(5)
                print(f"  Final URL: {self.page.url}")

                # Check if we're on community (not on profile.creatio.com login)
                if "community.creatio.com" in self.page.url and "/user/login" not in self.page.url:
                    print(f"  ✓ Community login successful!")
                    return True

            print(f"  ✗ Community login may have failed")
            return False

        except Exception as e:
            print(f"  ✗ Community login error: {e}")
            return False

    def extract_content(self, url: str) -> Optional[dict]:
        """Extract content from current page"""
        try:
            html = self.page.content()
            title = self.page.title()

            # Convert to markdown
            markdown = ""
            if HAS_BS4:
                soup = BeautifulSoup(html, 'html.parser')

                # Remove navigation, footer, scripts
                for tag in soup.find_all(['nav', 'footer', 'header', 'script', 'style', 'aside']):
                    tag.decompose()

                # Try to find main content
                main_content = soup.find('main') or soup.find('article') or soup.find(class_='content') or soup.find(id='content')
                if main_content:
                    content_html = str(main_content)
                else:
                    content_html = str(soup.body) if soup.body else str(soup)

                h = html2text.HTML2Text()
                h.ignore_links = False
                h.ignore_images = False
                h.body_width = 0
                markdown = h.handle(content_html)

            return {
                "url": url,
                "title": title,
                "markdown": markdown,
                "html": html,
            }

        except Exception as e:
            print(f"    Error extracting content: {e}")
            return None

    def save_page(self, data: dict, target: str):
        """Save page content"""
        url = data.get("url", "")
        page_id = self.generate_id(url)

        # Save markdown
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

        # Save HTML
        if data.get("html"):
            html_path = self.output_dir / "html" / f"{target}_{page_id}.html"
            with open(html_path, "w", encoding="utf-8") as f:
                f.write(data["html"])

        # Save metadata
        meta_path = self.output_dir / "metadata" / f"{target}_{page_id}.json"
        with open(meta_path, "w", encoding="utf-8") as f:
            json.dump({
                "url": url,
                "title": data.get("title"),
                "target": target,
                "crawled_at": datetime.now().isoformat(),
            }, f, indent=2)

        return page_id

    def discover_links(self, patterns: List[str]) -> List[str]:
        """Discover links matching patterns on current page"""
        links = self.page.eval_on_selector_all(
            'a[href]',
            'elements => elements.map(el => el.href)'
        )

        matching = []
        for link in links:
            if any(pattern in link for pattern in patterns):
                # Skip image/asset URLs
                if any(ext in link.lower() for ext in ['.png', '.jpg', '.jpeg', '.gif', '.svg', '.pdf', '.zip', '.css', '.js']):
                    continue
                matching.append(link)

        return list(set(matching))

    def crawl_target(self, target_name: str):
        """Crawl a specific target"""
        if target_name not in TARGETS:
            print(f"Unknown target: {target_name}")
            return

        config = TARGETS[target_name]
        start_url = config["start_url"]
        patterns = config["link_patterns"]
        max_pages = config["max_pages"]

        print(f"\n{'='*60}")
        print(f"Crawling: {target_name}")
        print(f"Start URL: {start_url}")
        print(f"Max pages: {max_pages}")
        print(f"{'='*60}")

        # Navigate to start URL
        self.page.goto(start_url, wait_until="networkidle", timeout=30000)
        time.sleep(2)

        # Discover URLs
        to_visit = [start_url]
        visited = set()

        # BFS crawl
        pages_crawled = 0
        while to_visit and pages_crawled < max_pages:
            current_url = to_visit.pop(0)
            normalized = self.normalize_url(current_url)

            if normalized in visited or normalized in self.visited_urls:
                continue

            visited.add(normalized)
            self.visited_urls.add(normalized)

            print(f"  [{pages_crawled + 1}/{max_pages}] {current_url[:70]}...")

            try:
                self.page.goto(current_url, wait_until="networkidle", timeout=30000)
                time.sleep(1)

                # Extract and save content
                data = self.extract_content(current_url)
                if data and data.get("markdown"):
                    self.save_page(data, target_name)
                    self.stats["successful"] += 1
                    self.stats["total_pages"] += 1
                    pages_crawled += 1
                    print(f"    ✓ Saved: {data.get('title', 'Untitled')[:50]}")

                    # Discover more links
                    new_links = self.discover_links(patterns)
                    for link in new_links:
                        link_normalized = self.normalize_url(link)
                        if link_normalized not in visited and link_normalized not in self.visited_urls:
                            to_visit.append(link)
                else:
                    self.stats["failed"] += 1
                    print(f"    ✗ No content")

            except Exception as e:
                print(f"    ✗ Error: {e}")
                self.stats["failed"] += 1

            # Rate limiting
            time.sleep(0.5)

        self.stats["targets"].append(target_name)
        print(f"\n  Completed {target_name}: {pages_crawled} pages")

    def crawl_all(self):
        """Crawl all targets"""
        print(f"\n{'#'*60}")
        print("AUTHENTICATED CRAWL - ALL TARGETS")
        print(f"Output: {self.output_dir}")
        print(f"{'#'*60}")

        with sync_playwright() as p:
            self.browser = p.chromium.launch(headless=True)
            self.context = self.browser.new_context()
            self.page = self.context.new_page()

            # Try login to academy (continue even if fails - public content available)
            academy_login = self.login_academy()
            if not academy_login:
                print("  Continuing without academy auth (public content)")

            # Crawl academy targets regardless of login status
            for target in ["elearning", "training", "certification"]:
                self.crawl_target(target)

            # Try login to community
            community_login = self.login_community()
            if not community_login:
                print("  Continuing without community auth (public content)")

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

            # Login based on target
            if target_name in ["elearning", "training", "certification"]:
                if not self.login_academy():
                    print("Academy login failed, trying anyway...")
            elif target_name == "community":
                if not self.login_community():
                    print("Community login failed, trying anyway...")

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
        print(f"Total pages: {self.stats['total_pages']}")
        print(f"Successful: {self.stats['successful']}")
        print(f"Failed: {self.stats['failed']}")
        print(f"Targets: {', '.join(self.stats['targets'])}")

        md_count = len(list((self.output_dir / "markdown").glob("*.md")))
        print(f"Markdown files: {md_count}")


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Creatio Authenticated Crawler")
    parser.add_argument("--target", choices=list(TARGETS.keys()), help="Crawl specific target")
    parser.add_argument("--all", action="store_true", help="Crawl all targets")
    parser.add_argument("--output-dir", default="./creatio-docs-authenticated", help="Output directory")
    parser.add_argument("--list-targets", action="store_true", help="List available targets")

    args = parser.parse_args()

    if args.list_targets:
        print("Available targets:")
        for name, config in TARGETS.items():
            print(f"  {name}: {config['start_url']}")
        return

    crawler = AuthenticatedCrawler(Path(args.output_dir))

    if args.all:
        crawler.crawl_all()
    elif args.target:
        crawler.crawl_single(args.target)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
