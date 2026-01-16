#!/usr/bin/env python3
"""
Creatio Academy Documentation Crawler
=====================================
Systematically crawls and downloads all documentation from academy.creatio.com
for building an AI training corpus.

Usage:
    python3 creatio_academy_crawler.py [--output-dir OUTPUT] [--section SECTION]
"""

import os
import json
import time
import hashlib
import argparse
import re
from datetime import datetime
from pathlib import Path
from urllib.parse import urljoin, urlparse
from typing import Dict, List, Set, Optional

try:
    from playwright.sync_api import sync_playwright
    HAS_PLAYWRIGHT = True
except ImportError:
    HAS_PLAYWRIGHT = False
    print("Warning: playwright not installed. Install with: pip install playwright && playwright install")

try:
    from bs4 import BeautifulSoup
    HAS_BS4 = True
except ImportError:
    HAS_BS4 = False
    print("Warning: beautifulsoup4 not installed. Install with: pip install beautifulsoup4")

# Base configuration
BASE_URL = "https://academy.creatio.com"
DOCS_VERSION = "8.x"

# Documentation sections to crawl
SECTIONS = {
    "products": f"/docs/{DOCS_VERSION}/creatio-apps/category/overview",
    "no-code": f"/docs/{DOCS_VERSION}/no-code-customization/category/customization-tools",
    "creatio-ai": f"/docs/{DOCS_VERSION}/no-code-customization/category/creatio-ai",
    "bpm-tools": f"/docs/{DOCS_VERSION}/no-code-customization/category/bpm-tools",
    "development": f"/docs/{DOCS_VERSION}/dev/development-on-creatio-platform/category/getting-started",
    "marketplace": f"/docs/{DOCS_VERSION}/dev/development-for-creatio-marketplace/app-types",
    "administration": f"/docs/{DOCS_VERSION}/setup-and-administration/category/administration",
    "mobile": f"/docs/{DOCS_VERSION}/mobile/category/mobile-basics",
    "releases": f"/docs/{DOCS_VERSION}/resources/category/releases",
}

class CreatioAcademyCrawler:
    """Crawler for Creatio Academy documentation."""

    def __init__(self, output_dir: str = "./creatio-docs"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.visited_urls: Set[str] = set()
        self.failed_urls: List[Dict] = []
        self.pages_crawled: int = 0
        self.code_examples: List[Dict] = []
        self.images: List[Dict] = []

        # Create subdirectories
        (self.output_dir / "html").mkdir(exist_ok=True)
        (self.output_dir / "markdown").mkdir(exist_ok=True)
        (self.output_dir / "code").mkdir(exist_ok=True)
        (self.output_dir / "images").mkdir(exist_ok=True)
        (self.output_dir / "metadata").mkdir(exist_ok=True)

        self.log_file = self.output_dir / "crawl_log.jsonl"
        self.index_file = self.output_dir / "index.json"

    def log(self, message: str, level: str = "INFO"):
        """Log a message with timestamp."""
        timestamp = datetime.now().isoformat()
        log_entry = {"timestamp": timestamp, "level": level, "message": message}
        print(f"[{timestamp}] {level}: {message}")
        with open(self.log_file, "a") as f:
            f.write(json.dumps(log_entry) + "\n")

    def url_to_filename(self, url: str) -> str:
        """Convert URL to safe filename."""
        parsed = urlparse(url)
        path = parsed.path.strip("/").replace("/", "_")
        if not path:
            path = "index"
        # Hash long paths
        if len(path) > 100:
            path = hashlib.md5(path.encode()).hexdigest()[:16] + "_" + path[-80:]
        return path

    def extract_content(self, page, url: str) -> Dict:
        """Extract content from a documentation page."""
        result = {
            "url": url,
            "title": "",
            "breadcrumbs": [],
            "content_html": "",
            "content_text": "",
            "code_examples": [],
            "images": [],
            "links": [],
            "sidebar_items": [],
            "version": DOCS_VERSION,
            "crawled_at": datetime.now().isoformat()
        }

        try:
            # Get title
            title_el = page.locator("h1").first
            if title_el.count() > 0:
                result["title"] = title_el.text_content().strip()

            # Get breadcrumbs
            breadcrumbs = page.evaluate('''() => {
                const crumbs = [];
                document.querySelectorAll('[class*="breadcrumb"] a, nav a').forEach(a => {
                    const text = a.textContent?.trim();
                    const href = a.getAttribute('href');
                    if (text && href && href.includes('/docs/')) {
                        crumbs.push({text, href});
                    }
                });
                return crumbs;
            }''')
            result["breadcrumbs"] = breadcrumbs

            # Get main content
            content_el = page.locator("article, main, .content, [class*='article']").first
            if content_el.count() > 0:
                result["content_html"] = content_el.inner_html()
                result["content_text"] = content_el.text_content()

            # Get code examples
            code_blocks = page.evaluate('''() => {
                const blocks = [];
                document.querySelectorAll('pre, code, [class*="code"]').forEach(el => {
                    const code = el.textContent?.trim();
                    const lang = el.className.match(/language-(\w+)/)?.[1] ||
                                 el.parentElement?.className.match(/language-(\w+)/)?.[1] ||
                                 'unknown';
                    if (code && code.length > 10) {
                        blocks.push({code, language: lang});
                    }
                });
                return blocks;
            }''')
            result["code_examples"] = code_blocks

            # Get images
            images = page.evaluate('''() => {
                const imgs = [];
                document.querySelectorAll('img').forEach(img => {
                    const src = img.getAttribute('src');
                    const alt = img.getAttribute('alt') || '';
                    if (src && !src.includes('data:')) {
                        imgs.push({src, alt});
                    }
                });
                return imgs;
            }''')
            result["images"] = images

            # Get all links
            links = page.evaluate('''() => {
                const links = [];
                document.querySelectorAll('a[href]').forEach(a => {
                    const href = a.getAttribute('href');
                    const text = a.textContent?.trim();
                    if (href && text) {
                        links.push({href, text});
                    }
                });
                return links;
            }''')
            result["links"] = links

            # Get sidebar navigation
            sidebar = page.evaluate('''() => {
                const items = [];
                document.querySelectorAll('[class*="sidebar"] a, [class*="nav"] a, [class*="menu"] a').forEach(a => {
                    const href = a.getAttribute('href');
                    const text = a.textContent?.trim();
                    if (href && text && href.includes('/docs/')) {
                        items.push({href, text});
                    }
                });
                return items;
            }''')
            result["sidebar_items"] = sidebar

        except Exception as e:
            self.log(f"Error extracting content from {url}: {e}", "ERROR")

        return result

    def save_page(self, content: Dict):
        """Save extracted page content."""
        filename = self.url_to_filename(content["url"])

        # Save HTML
        html_path = self.output_dir / "html" / f"{filename}.html"
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(content.get("content_html", ""))

        # Save as Markdown
        md_path = self.output_dir / "markdown" / f"{filename}.md"
        md_content = self.html_to_markdown(content)
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(md_content)

        # Save code examples
        if content.get("code_examples"):
            code_dir = self.output_dir / "code" / filename
            code_dir.mkdir(exist_ok=True)
            for i, block in enumerate(content["code_examples"]):
                ext = self.get_extension(block.get("language", "txt"))
                code_path = code_dir / f"example_{i}.{ext}"
                with open(code_path, "w", encoding="utf-8") as f:
                    f.write(block.get("code", ""))

        # Save metadata
        meta_path = self.output_dir / "metadata" / f"{filename}.json"
        with open(meta_path, "w", encoding="utf-8") as f:
            # Don't save full HTML in metadata
            meta = {k: v for k, v in content.items() if k != "content_html"}
            json.dump(meta, f, indent=2)

    def html_to_markdown(self, content: Dict) -> str:
        """Convert extracted content to Markdown format."""
        md = []

        # Title
        if content.get("title"):
            md.append(f"# {content['title']}\n")

        # Metadata
        md.append(f"> **URL:** {content.get('url', 'N/A')}")
        md.append(f"> **Version:** {content.get('version', 'N/A')}")
        md.append(f"> **Crawled:** {content.get('crawled_at', 'N/A')}\n")

        # Breadcrumbs
        if content.get("breadcrumbs"):
            crumbs = " > ".join([b.get("text", "") for b in content["breadcrumbs"]])
            md.append(f"**Path:** {crumbs}\n")

        # Content (basic conversion)
        text = content.get("content_text", "")
        if text:
            # Clean up whitespace
            text = re.sub(r'\n{3,}', '\n\n', text)
            md.append(text)

        # Code examples
        if content.get("code_examples"):
            md.append("\n## Code Examples\n")
            for i, block in enumerate(content["code_examples"]):
                lang = block.get("language", "")
                code = block.get("code", "")
                md.append(f"### Example {i+1} ({lang})\n")
                md.append(f"```{lang}\n{code}\n```\n")

        return "\n".join(md)

    def get_extension(self, language: str) -> str:
        """Get file extension for language."""
        mapping = {
            "javascript": "js",
            "typescript": "ts",
            "csharp": "cs",
            "c#": "cs",
            "python": "py",
            "sql": "sql",
            "json": "json",
            "xml": "xml",
            "html": "html",
            "css": "css",
        }
        return mapping.get(language.lower(), "txt")

    def crawl_page(self, page, url: str) -> List[str]:
        """Crawl a single page and return discovered URLs."""
        if url in self.visited_urls:
            return []

        self.visited_urls.add(url)
        discovered_urls = []

        try:
            self.log(f"Crawling: {url}")
            page.goto(url, wait_until='networkidle', timeout=60000)
            time.sleep(2)  # Allow JS to render

            # Extract content
            content = self.extract_content(page, url)

            # Save content
            self.save_page(content)
            self.pages_crawled += 1

            # Collect code examples
            for block in content.get("code_examples", []):
                self.code_examples.append({
                    "url": url,
                    "title": content.get("title", ""),
                    **block
                })

            # Collect images
            for img in content.get("images", []):
                self.images.append({
                    "url": url,
                    "title": content.get("title", ""),
                    **img
                })

            # Discover new URLs from sidebar and links
            for item in content.get("sidebar_items", []):
                href = item.get("href", "")
                if href and href.startswith("/docs/"):
                    full_url = urljoin(BASE_URL, href)
                    if full_url not in self.visited_urls:
                        discovered_urls.append(full_url)

            for link in content.get("links", []):
                href = link.get("href", "")
                if href and href.startswith("/docs/") and f"/docs/{DOCS_VERSION}" in href:
                    full_url = urljoin(BASE_URL, href)
                    if full_url not in self.visited_urls:
                        discovered_urls.append(full_url)

            self.log(f"✓ Crawled: {content.get('title', url)} ({len(discovered_urls)} new URLs)")

        except Exception as e:
            self.log(f"✗ Failed: {url} - {e}", "ERROR")
            self.failed_urls.append({"url": url, "error": str(e)})

        return discovered_urls

    def crawl_section(self, page, section_name: str, start_url: str, max_pages: int = 500):
        """Crawl an entire documentation section."""
        self.log(f"Starting section: {section_name}")

        queue = [urljoin(BASE_URL, start_url)]
        section_pages = 0

        while queue and section_pages < max_pages:
            url = queue.pop(0)
            new_urls = self.crawl_page(page, url)
            queue.extend(new_urls)
            section_pages += 1

            # Rate limiting
            time.sleep(0.5)

        self.log(f"Completed section: {section_name} ({section_pages} pages)")

    def save_index(self):
        """Save crawl index and statistics."""
        index = {
            "crawl_date": datetime.now().isoformat(),
            "base_url": BASE_URL,
            "version": DOCS_VERSION,
            "pages_crawled": self.pages_crawled,
            "failed_urls": self.failed_urls,
            "visited_urls": list(self.visited_urls),
            "code_examples_count": len(self.code_examples),
            "images_count": len(self.images),
        }

        with open(self.index_file, "w") as f:
            json.dump(index, f, indent=2)

        # Save code examples index
        with open(self.output_dir / "code_examples.json", "w") as f:
            json.dump(self.code_examples, f, indent=2)

        # Save images index
        with open(self.output_dir / "images.json", "w") as f:
            json.dump(self.images, f, indent=2)

        self.log(f"Index saved: {self.pages_crawled} pages, {len(self.code_examples)} code examples")

    def run(self, sections: Optional[List[str]] = None, max_pages_per_section: int = 500):
        """Run the crawler."""
        if not HAS_PLAYWRIGHT:
            self.log("Playwright not installed. Cannot run crawler.", "ERROR")
            return

        sections_to_crawl = sections or list(SECTIONS.keys())

        self.log(f"Starting crawl of {len(sections_to_crawl)} sections")

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(viewport={'width': 1920, 'height': 1080})
            page = context.new_page()

            try:
                for section_name in sections_to_crawl:
                    if section_name in SECTIONS:
                        self.crawl_section(
                            page,
                            section_name,
                            SECTIONS[section_name],
                            max_pages_per_section
                        )
                    else:
                        self.log(f"Unknown section: {section_name}", "WARNING")
            finally:
                browser.close()

        self.save_index()
        self.log("Crawl completed!")

        # Print summary
        print("\n" + "="*60)
        print("CRAWL SUMMARY")
        print("="*60)
        print(f"Pages crawled: {self.pages_crawled}")
        print(f"Failed URLs: {len(self.failed_urls)}")
        print(f"Code examples: {len(self.code_examples)}")
        print(f"Images found: {len(self.images)}")
        print(f"Output directory: {self.output_dir}")


def main():
    parser = argparse.ArgumentParser(description="Creatio Academy Documentation Crawler")
    parser.add_argument("--output-dir", "-o", default="./creatio-docs", help="Output directory")
    parser.add_argument("--section", "-s", action="append", help="Section(s) to crawl (can specify multiple)")
    parser.add_argument("--max-pages", "-m", type=int, default=500, help="Max pages per section")
    parser.add_argument("--list-sections", action="store_true", help="List available sections")

    args = parser.parse_args()

    if args.list_sections:
        print("Available sections:")
        for name, url in SECTIONS.items():
            print(f"  {name}: {url}")
        return

    crawler = CreatioAcademyCrawler(output_dir=args.output_dir)
    crawler.run(sections=args.section, max_pages_per_section=args.max_pages)


if __name__ == "__main__":
    main()
