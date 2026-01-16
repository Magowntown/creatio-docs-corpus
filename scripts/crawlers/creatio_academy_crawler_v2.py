#!/usr/bin/env python3
"""
Creatio Academy Documentation Crawler v2
=========================================
Comprehensive crawler for building an AI training corpus.

Features:
- Hybrid Firecrawl + Playwright approach
- Downloads images (not just indexes)
- Extracts tables with structure preservation
- Captures tabbed content (JS/C#/SQL variants)
- Preserves callouts/admonitions (notes, warnings, tips)
- Downloads attachments (PDFs, ZIPs, samples)
- Proper HTML-to-Markdown with structure
- Expands collapsible/accordion sections
- Captures video embeds and references
- Extracts structured API documentation

Usage:
    python3 creatio_academy_crawler_v2.py [--output-dir OUTPUT] [--section SECTION]
    python3 creatio_academy_crawler_v2.py --use-firecrawl  # Use Firecrawl API
"""

import os
import json
import time
import hashlib
import argparse
import re
import base64
import requests
from datetime import datetime
from pathlib import Path
from urllib.parse import urljoin, urlparse, parse_qs
from typing import Dict, List, Set, Optional, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed

# Optional imports
try:
    from playwright.sync_api import sync_playwright
    HAS_PLAYWRIGHT = True
except ImportError:
    HAS_PLAYWRIGHT = False
    print("Warning: playwright not installed. Install with: pip install playwright && playwright install")

try:
    from bs4 import BeautifulSoup, NavigableString, Tag
    import html2text
    HAS_BS4 = True
except ImportError:
    HAS_BS4 = False
    print("Warning: beautifulsoup4/html2text not installed. Install with: pip install beautifulsoup4 html2text")

try:
    from firecrawl import FirecrawlApp
    HAS_FIRECRAWL = True
except ImportError:
    HAS_FIRECRAWL = False

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Base configuration
BASE_URL = "https://academy.creatio.com"
DOCS_VERSION = "8.x"

# All documentation sections (comprehensive)
SECTIONS = {
    # Products
    "sales": f"/docs/{DOCS_VERSION}/creatio-apps/sales/category/sales-overview",
    "marketing": f"/docs/{DOCS_VERSION}/creatio-apps/marketing/category/marketing-overview",
    "service": f"/docs/{DOCS_VERSION}/creatio-apps/service/category/service-overview",
    "studio": f"/docs/{DOCS_VERSION}/creatio-apps/studio-creatio/category/studio-creatio-overview",
    "financial": f"/docs/{DOCS_VERSION}/creatio-apps/financial-services/category/financial-services",

    # No-code customization
    "no-code-tools": f"/docs/{DOCS_VERSION}/no-code-customization/category/customization-tools",
    "creatio-ai": f"/docs/{DOCS_VERSION}/no-code-customization/category/creatio-ai",
    "bpm-tools": f"/docs/{DOCS_VERSION}/no-code-customization/category/bpm-tools",
    "freedom-ui": f"/docs/{DOCS_VERSION}/no-code-customization/category/freedom-ui-designer",
    "dashboards": f"/docs/{DOCS_VERSION}/no-code-customization/dashboards/category/dashboards",

    # Development
    "dev-getting-started": f"/docs/{DOCS_VERSION}/dev/development-on-creatio-platform/category/getting-started",
    "dev-back-end": f"/docs/{DOCS_VERSION}/dev/development-on-creatio-platform/category/back-end-development",
    "dev-front-end": f"/docs/{DOCS_VERSION}/dev/development-on-creatio-platform/category/front-end-development",
    "dev-integrations": f"/docs/{DOCS_VERSION}/dev/development-on-creatio-platform/category/integrations",
    "marketplace": f"/docs/{DOCS_VERSION}/dev/development-for-creatio-marketplace/app-types",

    # Administration
    "admin": f"/docs/{DOCS_VERSION}/setup-and-administration/category/administration",
    "admin-users": f"/docs/{DOCS_VERSION}/setup-and-administration/category/user-management",
    "admin-security": f"/docs/{DOCS_VERSION}/setup-and-administration/category/access-management",

    # Mobile
    "mobile": f"/docs/{DOCS_VERSION}/mobile/category/mobile-basics",

    # Resources
    "releases": f"/docs/{DOCS_VERSION}/resources/category/releases",
    "glossary": f"/docs/{DOCS_VERSION}/resources/category/glossary",
}

# File type mappings
LANGUAGE_EXTENSIONS = {
    "javascript": "js", "js": "js",
    "typescript": "ts", "ts": "ts",
    "csharp": "cs", "c#": "cs", "cs": "cs",
    "python": "py", "py": "py",
    "sql": "sql",
    "json": "json",
    "xml": "xml",
    "html": "html",
    "css": "css",
    "yaml": "yaml", "yml": "yaml",
    "bash": "sh", "shell": "sh", "sh": "sh",
    "powershell": "ps1", "ps1": "ps1",
    "plaintext": "txt", "text": "txt", "unknown": "txt",
}


class ComprehensiveExtractor:
    """Advanced content extraction from HTML."""

    def __init__(self):
        self.h2t = html2text.HTML2Text() if HAS_BS4 else None
        if self.h2t:
            self.h2t.ignore_links = False
            self.h2t.ignore_images = False
            self.h2t.ignore_tables = False
            self.h2t.body_width = 0  # No line wrapping

    def extract_tables(self, soup: BeautifulSoup) -> List[Dict]:
        """Extract tables with structure preservation."""
        tables = []
        for table in soup.find_all('table'):
            table_data = {
                "headers": [],
                "rows": [],
                "caption": "",
                "html": str(table),
            }

            # Get caption
            caption = table.find('caption')
            if caption:
                table_data["caption"] = caption.get_text(strip=True)

            # Get headers
            thead = table.find('thead')
            if thead:
                for th in thead.find_all('th'):
                    table_data["headers"].append(th.get_text(strip=True))

            # Get rows
            tbody = table.find('tbody') or table
            for tr in tbody.find_all('tr'):
                row = []
                for td in tr.find_all(['td', 'th']):
                    row.append(td.get_text(strip=True))
                if row:
                    table_data["rows"].append(row)

            tables.append(table_data)

        return tables

    def extract_tabbed_content(self, soup: BeautifulSoup) -> List[Dict]:
        """Extract tabbed code examples (JS/C#/SQL variants)."""
        tabbed_content = []

        # Common tab patterns in documentation
        tab_containers = soup.find_all(['div', 'section'], class_=lambda c: c and any(
            x in str(c).lower() for x in ['tabs', 'tab-content', 'code-tabs', 'tabpanel']
        ))

        for container in tab_containers:
            tabs = {"variants": [], "context": ""}

            # Get tab labels
            tab_labels = container.find_all(['button', 'a', 'li'], class_=lambda c: c and 'tab' in str(c).lower())

            # Get tab content panels
            panels = container.find_all(['div', 'pre'], class_=lambda c: c and any(
                x in str(c).lower() for x in ['panel', 'content', 'code']
            ))

            for i, (label, panel) in enumerate(zip(tab_labels, panels)):
                variant = {
                    "label": label.get_text(strip=True) if label else f"Tab {i+1}",
                    "content": panel.get_text(strip=True) if panel else "",
                    "language": self._detect_language(panel),
                }
                tabs["variants"].append(variant)

            if tabs["variants"]:
                tabbed_content.append(tabs)

        return tabbed_content

    def extract_callouts(self, soup: BeautifulSoup) -> List[Dict]:
        """Extract callouts/admonitions (notes, warnings, tips, etc.)."""
        callouts = []

        # Common callout patterns
        callout_selectors = [
            ('[class*="admonition"]', lambda e: e.get('class', [])),
            ('[class*="callout"]', lambda e: e.get('class', [])),
            ('[class*="alert"]', lambda e: e.get('class', [])),
            ('[class*="note"]', lambda e: ['note']),
            ('[class*="warning"]', lambda e: ['warning']),
            ('[class*="tip"]', lambda e: ['tip']),
            ('[class*="info"]', lambda e: ['info']),
            ('[class*="danger"]', lambda e: ['danger']),
            ('[class*="caution"]', lambda e: ['caution']),
        ]

        seen = set()
        for selector, type_getter in callout_selectors:
            for element in soup.select(selector):
                element_id = id(element)
                if element_id in seen:
                    continue
                seen.add(element_id)

                classes = type_getter(element)
                callout_type = "note"  # default
                for cls in classes:
                    cls_lower = str(cls).lower()
                    if 'warning' in cls_lower:
                        callout_type = "warning"
                    elif 'danger' in cls_lower or 'error' in cls_lower:
                        callout_type = "danger"
                    elif 'tip' in cls_lower or 'success' in cls_lower:
                        callout_type = "tip"
                    elif 'info' in cls_lower:
                        callout_type = "info"
                    elif 'caution' in cls_lower:
                        callout_type = "caution"

                # Get title and content
                title_el = element.find(['strong', 'b', 'h4', 'h5', '.title', '[class*="title"]'])
                title = title_el.get_text(strip=True) if title_el else callout_type.capitalize()

                content = element.get_text(strip=True)

                callouts.append({
                    "type": callout_type,
                    "title": title,
                    "content": content,
                    "html": str(element),
                })

        return callouts

    def extract_code_blocks(self, soup: BeautifulSoup) -> List[Dict]:
        """Extract code blocks with language detection and context."""
        code_blocks = []
        seen_code = set()

        for pre in soup.find_all('pre'):
            code_el = pre.find('code') or pre
            code = code_el.get_text()

            # Skip duplicates
            code_hash = hashlib.md5(code.encode()).hexdigest()
            if code_hash in seen_code or len(code.strip()) < 10:
                continue
            seen_code.add(code_hash)

            # Detect language
            language = self._detect_language(code_el)

            # Get surrounding context (preceding paragraph or heading)
            context = ""
            prev = pre.find_previous(['p', 'h1', 'h2', 'h3', 'h4', 'h5'])
            if prev:
                context = prev.get_text(strip=True)[:200]

            # Check if it's part of a tabbed section
            parent_tab = pre.find_parent(class_=lambda c: c and 'tab' in str(c).lower())
            tab_label = ""
            if parent_tab:
                label_el = parent_tab.find_previous(['button', 'a'], class_=lambda c: c and 'tab' in str(c).lower())
                if label_el:
                    tab_label = label_el.get_text(strip=True)

            code_blocks.append({
                "code": code,
                "language": language,
                "context": context,
                "tab_label": tab_label,
                "line_count": len(code.strip().split('\n')),
            })

        return code_blocks

    def extract_images(self, soup: BeautifulSoup, base_url: str) -> List[Dict]:
        """Extract images with metadata."""
        images = []

        for img in soup.find_all('img'):
            src = img.get('src', '')
            if not src or src.startswith('data:'):
                continue

            # Resolve relative URLs
            if not src.startswith(('http://', 'https://')):
                src = urljoin(base_url, src)

            # Get context
            context = ""
            parent = img.find_parent(['figure', 'p', 'div'])
            if parent:
                figcaption = parent.find('figcaption')
                if figcaption:
                    context = figcaption.get_text(strip=True)
                else:
                    # Get nearby text
                    prev = img.find_previous(['p', 'h1', 'h2', 'h3'])
                    if prev:
                        context = prev.get_text(strip=True)[:100]

            images.append({
                "src": src,
                "alt": img.get('alt', ''),
                "title": img.get('title', ''),
                "context": context,
                "width": img.get('width', ''),
                "height": img.get('height', ''),
            })

        return images

    def extract_videos(self, soup: BeautifulSoup) -> List[Dict]:
        """Extract video embeds and references."""
        videos = []

        # YouTube iframes
        for iframe in soup.find_all('iframe'):
            src = iframe.get('src', '')
            if 'youtube' in src or 'youtu.be' in src:
                video_id = self._extract_youtube_id(src)
                videos.append({
                    "type": "youtube",
                    "src": src,
                    "video_id": video_id,
                    "title": iframe.get('title', ''),
                })

        # Video tags
        for video in soup.find_all('video'):
            sources = [s.get('src') for s in video.find_all('source')]
            videos.append({
                "type": "video",
                "src": video.get('src', sources[0] if sources else ''),
                "sources": sources,
                "poster": video.get('poster', ''),
            })

        # Video links (Vimeo, etc.)
        for a in soup.find_all('a', href=True):
            href = a['href']
            if any(x in href for x in ['vimeo.com', 'youtube.com', 'youtu.be', 'wistia.com']):
                videos.append({
                    "type": "link",
                    "src": href,
                    "text": a.get_text(strip=True),
                })

        return videos

    def extract_downloadables(self, soup: BeautifulSoup, base_url: str) -> List[Dict]:
        """Extract downloadable files (PDFs, ZIPs, samples)."""
        downloadables = []

        download_extensions = ['.pdf', '.zip', '.rar', '.xlsx', '.xls', '.docx', '.doc', '.pptx', '.csv']

        for a in soup.find_all('a', href=True):
            href = a['href']
            href_lower = href.lower()

            # Check if it's a downloadable file
            is_download = any(href_lower.endswith(ext) for ext in download_extensions)
            is_download = is_download or 'download' in href_lower
            is_download = is_download or a.get('download') is not None

            if is_download:
                if not href.startswith(('http://', 'https://')):
                    href = urljoin(base_url, href)

                downloadables.append({
                    "url": href,
                    "text": a.get_text(strip=True),
                    "filename": href.split('/')[-1].split('?')[0],
                    "type": self._get_file_type(href),
                })

        return downloadables

    def extract_headings_structure(self, soup: BeautifulSoup) -> List[Dict]:
        """Extract document structure via headings."""
        headings = []

        for heading in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
            level = int(heading.name[1])
            anchor = heading.get('id', '')

            # Check for anchor link inside heading
            anchor_link = heading.find('a', class_=lambda c: c and 'anchor' in str(c).lower())
            if anchor_link and anchor_link.get('href', '').startswith('#'):
                anchor = anchor_link['href'][1:]

            headings.append({
                "level": level,
                "text": heading.get_text(strip=True),
                "anchor": anchor,
            })

        return headings

    def extract_api_documentation(self, soup: BeautifulSoup) -> Dict:
        """Extract structured API documentation if present."""
        api_doc = {
            "endpoints": [],
            "parameters": [],
            "responses": [],
            "examples": [],
        }

        # Look for API-specific patterns
        # Method badges (GET, POST, etc.)
        for badge in soup.find_all(class_=lambda c: c and any(
            x in str(c).lower() for x in ['method', 'http-method', 'verb']
        )):
            method = badge.get_text(strip=True).upper()
            # Find associated endpoint
            endpoint_el = badge.find_next(['code', 'span', 'pre'])
            if endpoint_el:
                api_doc["endpoints"].append({
                    "method": method,
                    "path": endpoint_el.get_text(strip=True),
                })

        # Parameters tables
        for table in soup.find_all('table'):
            headers = [th.get_text(strip=True).lower() for th in table.find_all('th')]
            if any(h in headers for h in ['parameter', 'param', 'name', 'field']):
                for row in table.find_all('tr')[1:]:  # Skip header
                    cells = [td.get_text(strip=True) for td in row.find_all('td')]
                    if len(cells) >= 2:
                        api_doc["parameters"].append({
                            "name": cells[0],
                            "type": cells[1] if len(cells) > 1 else "",
                            "description": cells[2] if len(cells) > 2 else "",
                            "required": 'required' in ' '.join(cells).lower(),
                        })

        return api_doc if any(api_doc.values()) else None

    def expand_collapsibles(self, page) -> None:
        """Expand all collapsible/accordion sections (Playwright)."""
        if not HAS_PLAYWRIGHT:
            return

        try:
            # Click all expandable elements
            page.evaluate('''() => {
                // Click all collapsed items
                document.querySelectorAll('[aria-expanded="false"]').forEach(el => el.click());

                // Click details summary elements
                document.querySelectorAll('details:not([open]) summary').forEach(el => el.click());

                // Click accordion headers
                document.querySelectorAll('[class*="accordion"]:not([class*="open"]) [class*="header"]').forEach(el => el.click());

                // Click "Show more" buttons
                document.querySelectorAll('button, a').forEach(el => {
                    const text = el.textContent?.toLowerCase() || '';
                    if (text.includes('show more') || text.includes('expand') || text.includes('view all')) {
                        el.click();
                    }
                });
            }''')
            time.sleep(0.5)  # Wait for animations
        except Exception:
            pass  # Ignore errors from clicking

    def html_to_clean_markdown(self, html: str, url: str) -> str:
        """Convert HTML to clean, structured Markdown."""
        if not HAS_BS4:
            return html

        soup = BeautifulSoup(html, 'html.parser')

        # Remove scripts, styles, and nav elements
        for tag in soup.find_all(['script', 'style', 'nav', 'header', 'footer', 'aside']):
            tag.decompose()

        # Use html2text for base conversion
        if self.h2t:
            markdown = self.h2t.handle(str(soup))
        else:
            markdown = soup.get_text()

        # Clean up
        markdown = re.sub(r'\n{3,}', '\n\n', markdown)
        markdown = re.sub(r'^\s+', '', markdown, flags=re.MULTILINE)

        return markdown.strip()

    def _detect_language(self, element) -> str:
        """Detect programming language from element."""
        if not element:
            return "unknown"

        # Check class for language hint
        classes = element.get('class', [])
        if isinstance(classes, str):
            classes = [classes]

        for cls in classes:
            cls_str = str(cls).lower()
            match = re.search(r'language-(\w+)', cls_str)
            if match:
                return match.group(1)
            # Direct language class
            for lang in ['javascript', 'typescript', 'csharp', 'python', 'sql', 'json', 'xml', 'html', 'css']:
                if lang in cls_str:
                    return lang

        # Check parent classes
        parent = element.parent
        if parent:
            return self._detect_language(parent) if parent.name != 'body' else "unknown"

        return "unknown"

    def _extract_youtube_id(self, url: str) -> str:
        """Extract YouTube video ID from URL."""
        patterns = [
            r'youtube\.com/watch\?v=([^&]+)',
            r'youtube\.com/embed/([^?]+)',
            r'youtu\.be/([^?]+)',
        ]
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        return ""

    def _get_file_type(self, url: str) -> str:
        """Get file type from URL."""
        url_lower = url.lower()
        for ext in ['.pdf', '.zip', '.xlsx', '.xls', '.docx', '.doc', '.pptx', '.csv', '.rar']:
            if ext in url_lower:
                return ext[1:]  # Remove dot
        return "unknown"


class CreatioAcademyCrawlerV2:
    """Comprehensive Creatio Academy crawler."""

    def __init__(self, output_dir: str = "./creatio-docs", use_firecrawl: bool = False):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.use_firecrawl = use_firecrawl and HAS_FIRECRAWL

        # Initialize Firecrawl if available and requested
        self.firecrawl = None
        if self.use_firecrawl:
            api_key = os.getenv('FIRECRAWL_API_KEY')
            if api_key:
                self.firecrawl = FirecrawlApp(api_key=api_key)
            else:
                print("Warning: FIRECRAWL_API_KEY not set. Falling back to Playwright.")
                self.use_firecrawl = False

        self.extractor = ComprehensiveExtractor()

        # State
        self.visited_urls: Set[str] = set()
        self.failed_urls: List[Dict] = []
        self.pages_crawled: int = 0
        self.stats = {
            "code_examples": 0,
            "images_downloaded": 0,
            "tables": 0,
            "callouts": 0,
            "videos": 0,
            "downloads": 0,
        }

        # Create directory structure
        for subdir in ["html", "markdown", "code", "images", "tables", "metadata", "downloads", "raw"]:
            (self.output_dir / subdir).mkdir(exist_ok=True)

        self.log_file = self.output_dir / "crawl_log.jsonl"
        self.index_file = self.output_dir / "index.json"

    def log(self, message: str, level: str = "INFO"):
        """Log with timestamp."""
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
        if len(path) > 100:
            path = hashlib.md5(path.encode()).hexdigest()[:16] + "_" + path[-80:]
        return path

    def download_image(self, img_url: str, page_filename: str) -> Optional[str]:
        """Download image and return local path."""
        try:
            response = requests.get(img_url, timeout=30)
            if response.status_code == 200:
                # Generate filename
                ext = img_url.split('.')[-1].split('?')[0][:4]
                if ext not in ['png', 'jpg', 'jpeg', 'gif', 'svg', 'webp']:
                    ext = 'png'

                img_hash = hashlib.md5(img_url.encode()).hexdigest()[:12]
                img_filename = f"{page_filename}_{img_hash}.{ext}"
                img_path = self.output_dir / "images" / img_filename

                with open(img_path, 'wb') as f:
                    f.write(response.content)

                return str(img_path)
        except Exception as e:
            self.log(f"Failed to download image {img_url}: {e}", "WARNING")

        return None

    def download_file(self, file_url: str, page_filename: str) -> Optional[str]:
        """Download file attachment and return local path."""
        try:
            response = requests.get(file_url, timeout=60, stream=True)
            if response.status_code == 200:
                # Get filename from URL or Content-Disposition
                filename = file_url.split('/')[-1].split('?')[0]
                if not filename:
                    filename = f"download_{hashlib.md5(file_url.encode()).hexdigest()[:8]}"

                file_path = self.output_dir / "downloads" / f"{page_filename}_{filename}"

                with open(file_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)

                return str(file_path)
        except Exception as e:
            self.log(f"Failed to download file {file_url}: {e}", "WARNING")

        return None

    def extract_with_playwright(self, page, url: str) -> Dict:
        """Extract content using Playwright."""
        result = {
            "url": url,
            "title": "",
            "breadcrumbs": [],
            "content_html": "",
            "content_markdown": "",
            "code_examples": [],
            "tables": [],
            "callouts": [],
            "images": [],
            "videos": [],
            "downloadables": [],
            "headings": [],
            "api_docs": None,
            "sidebar_items": [],
            "related_links": [],
            "version": DOCS_VERSION,
            "crawled_at": datetime.now().isoformat(),
        }

        try:
            # Expand all collapsibles first
            self.extractor.expand_collapsibles(page)

            # Get title
            title_el = page.locator("h1").first
            if title_el.count() > 0:
                result["title"] = title_el.text_content().strip()

            # Get breadcrumbs
            breadcrumbs = page.evaluate('''() => {
                const crumbs = [];
                document.querySelectorAll('[class*="breadcrumb"] a, [class*="Breadcrumb"] a').forEach(a => {
                    const text = a.textContent?.trim();
                    const href = a.getAttribute('href');
                    if (text && href) crumbs.push({text, href});
                });
                return crumbs;
            }''')
            result["breadcrumbs"] = breadcrumbs

            # Get main content HTML - try selectors in order of specificity
            content_html = page.evaluate('''() => {
                // Try selectors in order of preference
                const selectors = [
                    'article.theme-doc-markdown',
                    'article',
                    'main article',
                    '.theme-doc-markdown',
                    '[class*="docItemContainer"]',
                    'main',
                    '[class*="article-content"]',
                    '[class*="markdown-body"]',
                ];

                for (const sel of selectors) {
                    const el = document.querySelector(sel);
                    if (el && el.innerHTML && el.innerHTML.length > 500) {
                        return el.innerHTML;
                    }
                }

                // Fallback to body
                return document.body.innerHTML;
            }''')
            result["content_html"] = content_html

            # Parse with BeautifulSoup for structured extraction
            if HAS_BS4 and content_html:
                soup = BeautifulSoup(content_html, 'html.parser')

                result["code_examples"] = self.extractor.extract_code_blocks(soup)
                result["tables"] = self.extractor.extract_tables(soup)
                result["callouts"] = self.extractor.extract_callouts(soup)
                result["images"] = self.extractor.extract_images(soup, url)
                result["videos"] = self.extractor.extract_videos(soup)
                result["downloadables"] = self.extractor.extract_downloadables(soup, url)
                result["headings"] = self.extractor.extract_headings_structure(soup)
                result["api_docs"] = self.extractor.extract_api_documentation(soup)
                result["content_markdown"] = self.extractor.html_to_clean_markdown(content_html, url)

            # Get sidebar navigation
            sidebar = page.evaluate('''() => {
                const items = [];
                document.querySelectorAll('[class*="sidebar"] a, [class*="menu"] a, [class*="nav"] a').forEach(a => {
                    const href = a.getAttribute('href');
                    const text = a.textContent?.trim();
                    if (href && text && href.includes('/docs/')) {
                        items.push({href, text, active: a.classList.contains('active')});
                    }
                });
                return [...new Map(items.map(i => [i.href, i])).values()];
            }''')
            result["sidebar_items"] = sidebar

            # Get related links
            related = page.evaluate('''() => {
                const links = [];
                document.querySelectorAll('[class*="related"] a, [class*="see-also"] a').forEach(a => {
                    const href = a.getAttribute('href');
                    const text = a.textContent?.trim();
                    if (href && text) links.push({href, text});
                });
                return links;
            }''')
            result["related_links"] = related

        except Exception as e:
            self.log(f"Error extracting from {url}: {e}", "ERROR")

        return result

    def extract_with_firecrawl(self, url: str) -> Dict:
        """Extract content using Firecrawl API."""
        result = {
            "url": url,
            "title": "",
            "content_markdown": "",
            "content_html": "",
            "code_examples": [],
            "tables": [],
            "images": [],
            "headings": [],
            "callouts": [],
            "crawled_at": datetime.now().isoformat(),
            "version": DOCS_VERSION,
        }

        try:
            # Use Firecrawl v2 API
            doc = self.firecrawl.scrape(
                url,
                formats=['markdown', 'html'],
                wait_for=3000,
                only_main_content=True
            )

            if doc:
                result["content_markdown"] = doc.markdown or ''
                result["content_html"] = doc.html or ''

                # Get title from metadata if available
                if hasattr(doc, 'metadata') and doc.metadata:
                    result["title"] = getattr(doc.metadata, 'title', '') or ''

                # Parse HTML for structured data
                if HAS_BS4 and result["content_html"]:
                    soup = BeautifulSoup(result["content_html"], 'html.parser')
                    result["code_examples"] = self.extractor.extract_code_blocks(soup)
                    result["tables"] = self.extractor.extract_tables(soup)
                    result["images"] = self.extractor.extract_images(soup, url)
                    result["headings"] = self.extractor.extract_headings_structure(soup)
                    result["callouts"] = self.extractor.extract_callouts(soup)

        except Exception as e:
            self.log(f"Firecrawl error for {url}: {e}", "ERROR")

        return result

    def save_page(self, content: Dict, download_assets: bool = True):
        """Save all extracted content."""
        filename = self.url_to_filename(content["url"])

        # Save raw HTML
        html_path = self.output_dir / "html" / f"{filename}.html"
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(content.get("content_html", ""))

        # Save Markdown
        md_path = self.output_dir / "markdown" / f"{filename}.md"
        md_content = self._build_markdown(content)
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(md_content)

        # Save code examples
        if content.get("code_examples"):
            code_dir = self.output_dir / "code" / filename
            code_dir.mkdir(exist_ok=True)
            for i, block in enumerate(content["code_examples"]):
                lang = block.get("language", "txt")
                ext = LANGUAGE_EXTENSIONS.get(lang.lower(), "txt")
                code_path = code_dir / f"example_{i}_{lang}.{ext}"
                with open(code_path, "w", encoding="utf-8") as f:
                    f.write(block.get("code", ""))
                self.stats["code_examples"] += 1

        # Save tables as CSV
        if content.get("tables"):
            for i, table in enumerate(content["tables"]):
                table_path = self.output_dir / "tables" / f"{filename}_table_{i}.json"
                with open(table_path, "w", encoding="utf-8") as f:
                    json.dump(table, f, indent=2)
                self.stats["tables"] += 1

        # Download images
        if download_assets and content.get("images"):
            for img in content["images"]:
                if img.get("src"):
                    local_path = self.download_image(img["src"], filename)
                    if local_path:
                        img["local_path"] = local_path
                        self.stats["images_downloaded"] += 1

        # Download files
        if download_assets and content.get("downloadables"):
            for dl in content["downloadables"]:
                if dl.get("url"):
                    local_path = self.download_file(dl["url"], filename)
                    if local_path:
                        dl["local_path"] = local_path
                        self.stats["downloads"] += 1

        # Count other items
        self.stats["callouts"] += len(content.get("callouts", []))
        self.stats["videos"] += len(content.get("videos", []))

        # Save metadata
        meta_path = self.output_dir / "metadata" / f"{filename}.json"
        meta = {k: v for k, v in content.items() if k != "content_html"}
        with open(meta_path, "w", encoding="utf-8") as f:
            json.dump(meta, f, indent=2, default=str)

    def _build_markdown(self, content: Dict) -> str:
        """Build comprehensive Markdown document."""
        md = []

        # YAML frontmatter
        md.append("---")
        md.append(f"url: {content.get('url', '')}")
        md.append(f"title: \"{content.get('title', '')}\"")
        md.append(f"version: {content.get('version', DOCS_VERSION)}")
        md.append(f"crawled_at: {content.get('crawled_at', '')}")
        if content.get("breadcrumbs"):
            path = " > ".join([b.get("text", "") for b in content["breadcrumbs"]])
            md.append(f"path: \"{path}\"")
        md.append("---\n")

        # Title
        if content.get("title"):
            md.append(f"# {content['title']}\n")

        # Breadcrumbs
        if content.get("breadcrumbs"):
            crumbs = " → ".join([f"[{b.get('text', '')}]({b.get('href', '')})" for b in content["breadcrumbs"]])
            md.append(f"📍 {crumbs}\n")

        # Main content
        if content.get("content_markdown"):
            md.append(content["content_markdown"])
            md.append("\n")

        # Callouts
        if content.get("callouts"):
            for callout in content["callouts"]:
                icon = {"note": "📝", "warning": "⚠️", "tip": "💡", "danger": "🚨", "info": "ℹ️"}.get(
                    callout.get("type", "note"), "📝"
                )
                md.append(f"\n> {icon} **{callout.get('title', 'Note')}**")
                md.append(f"> {callout.get('content', '')}\n")

        # Code examples
        if content.get("code_examples"):
            md.append("\n## 💻 Code Examples\n")
            for i, block in enumerate(content["code_examples"]):
                lang = block.get("language", "")
                context = block.get("context", "")
                tab = block.get("tab_label", "")

                header = f"### Example {i+1}"
                if tab:
                    header += f" ({tab})"
                elif lang:
                    header += f" ({lang})"
                md.append(header)

                if context:
                    md.append(f"*{context}*\n")

                md.append(f"```{lang}")
                md.append(block.get("code", ""))
                md.append("```\n")

        # Tables
        if content.get("tables"):
            md.append("\n## 📊 Tables\n")
            for i, table in enumerate(content["tables"]):
                if table.get("caption"):
                    md.append(f"### {table['caption']}\n")

                headers = table.get("headers", [])
                rows = table.get("rows", [])

                if headers:
                    md.append("| " + " | ".join(headers) + " |")
                    md.append("| " + " | ".join(["---"] * len(headers)) + " |")

                for row in rows[:20]:  # Limit rows
                    md.append("| " + " | ".join(str(c) for c in row) + " |")
                md.append("")

        # Videos
        if content.get("videos"):
            md.append("\n## 🎥 Videos\n")
            for video in content["videos"]:
                if video.get("video_id"):
                    md.append(f"- YouTube: https://youtube.com/watch?v={video['video_id']}")
                elif video.get("src"):
                    md.append(f"- {video.get('text', 'Video')}: {video['src']}")

        # Downloadables
        if content.get("downloadables"):
            md.append("\n## 📥 Downloads\n")
            for dl in content["downloadables"]:
                md.append(f"- [{dl.get('text', dl.get('filename', 'Download'))}]({dl.get('url', '')})")

        # API Documentation
        if content.get("api_docs"):
            api = content["api_docs"]
            if api.get("endpoints"):
                md.append("\n## 🔌 API Reference\n")
                for ep in api["endpoints"]:
                    md.append(f"**{ep.get('method', 'GET')}** `{ep.get('path', '')}`\n")

            if api.get("parameters"):
                md.append("### Parameters\n")
                md.append("| Name | Type | Required | Description |")
                md.append("|------|------|----------|-------------|")
                for p in api["parameters"]:
                    req = "✓" if p.get("required") else ""
                    md.append(f"| {p.get('name', '')} | {p.get('type', '')} | {req} | {p.get('description', '')} |")

        # Related links
        if content.get("related_links"):
            md.append("\n## 🔗 Related\n")
            for link in content["related_links"]:
                md.append(f"- [{link.get('text', '')}]({link.get('href', '')})")

        return "\n".join(md)

    def crawl_page(self, page, url: str) -> List[str]:
        """Crawl a single page."""
        if url in self.visited_urls:
            return []

        self.visited_urls.add(url)
        discovered_urls = []

        try:
            self.log(f"Crawling: {url}")

            if self.use_firecrawl and self.firecrawl:
                content = self.extract_with_firecrawl(url)
            else:
                page.goto(url, wait_until='networkidle', timeout=60000)
                time.sleep(2)
                content = self.extract_with_playwright(page, url)

            self.save_page(content)
            self.pages_crawled += 1

            # Discover new URLs
            for item in content.get("sidebar_items", []):
                href = item.get("href", "")
                if href.startswith("/docs/"):
                    full_url = urljoin(BASE_URL, href)
                    if full_url not in self.visited_urls:
                        discovered_urls.append(full_url)

            # Also check in-page links
            if HAS_BS4 and content.get("content_html"):
                soup = BeautifulSoup(content["content_html"], 'html.parser')
                for a in soup.find_all('a', href=True):
                    href = a['href']
                    if href.startswith('/docs/') and f'/docs/{DOCS_VERSION}' in href:
                        full_url = urljoin(BASE_URL, href)
                        if full_url not in self.visited_urls:
                            discovered_urls.append(full_url)

            self.log(f"✓ {content.get('title', url)[:50]} ({len(discovered_urls)} new links)")

        except Exception as e:
            self.log(f"✗ Failed: {url} - {e}", "ERROR")
            self.failed_urls.append({"url": url, "error": str(e)})

        return list(set(discovered_urls))

    def crawl_section(self, page, section_name: str, start_url: str, max_pages: int = 1000):
        """Crawl a documentation section."""
        self.log(f"═══ Starting section: {section_name} ═══")

        queue = [urljoin(BASE_URL, start_url)]
        section_pages = 0

        while queue and section_pages < max_pages:
            url = queue.pop(0)
            new_urls = self.crawl_page(page, url)
            queue.extend(new_urls)
            section_pages += 1
            time.sleep(0.3)  # Rate limiting

        self.log(f"═══ Completed section: {section_name} ({section_pages} pages) ═══")

    def save_index(self):
        """Save crawl index and statistics."""
        index = {
            "crawl_date": datetime.now().isoformat(),
            "base_url": BASE_URL,
            "version": DOCS_VERSION,
            "pages_crawled": self.pages_crawled,
            "failed_urls": self.failed_urls,
            "visited_urls": list(self.visited_urls),
            "statistics": self.stats,
            "crawler_version": "2.0",
        }

        with open(self.index_file, "w") as f:
            json.dump(index, f, indent=2)

        self.log(f"Index saved: {self.pages_crawled} pages")

    def run(self, sections: Optional[List[str]] = None, max_pages_per_section: int = 1000,
            download_assets: bool = True):
        """Run the crawler."""
        sections_to_crawl = sections or list(SECTIONS.keys())

        self.log(f"Starting comprehensive crawl of {len(sections_to_crawl)} sections")
        self.log(f"Using: {'Firecrawl API' if self.use_firecrawl else 'Playwright'}")

        if not self.use_firecrawl and not HAS_PLAYWRIGHT:
            self.log("Playwright not installed. Cannot run.", "ERROR")
            return

        if self.use_firecrawl:
            # Firecrawl mode - use site-wide crawl feature
            for section_name in sections_to_crawl:
                if section_name in SECTIONS:
                    self.log(f"═══ Crawling: {section_name} ═══")
                    start_url = urljoin(BASE_URL, SECTIONS[section_name])
                    try:
                        # Use Firecrawl v2 crawl API
                        crawl_job = self.firecrawl.crawl(
                            start_url,
                            limit=max_pages_per_section,
                            include_paths=[f"/docs/{DOCS_VERSION}/*"],
                            scrape_options={
                                "formats": ["markdown", "html"],
                                "waitFor": 3000,
                                "onlyMainContent": True
                            },
                            poll_interval=5,
                            timeout=600  # 10 min timeout
                        )

                        # Process results from the crawl job
                        if hasattr(crawl_job, 'data') and crawl_job.data:
                            for doc in crawl_job.data:
                                content = {
                                    "url": getattr(doc.metadata, 'url', '') if doc.metadata else '',
                                    "title": getattr(doc.metadata, 'title', '') if doc.metadata else '',
                                    "content_markdown": doc.markdown or '',
                                    "content_html": doc.html or '',
                                    "code_examples": [],
                                    "tables": [],
                                    "images": [],
                                    "headings": [],
                                    "callouts": [],
                                    "crawled_at": datetime.now().isoformat(),
                                    "version": DOCS_VERSION,
                                }

                                # Parse HTML for structured data
                                if HAS_BS4 and content["content_html"]:
                                    soup = BeautifulSoup(content["content_html"], 'html.parser')
                                    content["code_examples"] = self.extractor.extract_code_blocks(soup)
                                    content["tables"] = self.extractor.extract_tables(soup)
                                    content["images"] = self.extractor.extract_images(soup, content["url"])
                                    content["headings"] = self.extractor.extract_headings_structure(soup)
                                    content["callouts"] = self.extractor.extract_callouts(soup)

                                self.save_page(content, download_assets)
                                self.pages_crawled += 1
                                self.log(f"✓ {content.get('title', content['url'])[:50]}")

                    except Exception as e:
                        self.log(f"Firecrawl crawl error: {e}", "ERROR")
        else:
            # Playwright mode
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                context = browser.new_context(
                    viewport={'width': 1920, 'height': 1080},
                    user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                )
                page = context.new_page()

                try:
                    for section_name in sections_to_crawl:
                        if section_name in SECTIONS:
                            self.crawl_section(page, section_name, SECTIONS[section_name], max_pages_per_section)
                finally:
                    browser.close()

        self.save_index()
        self.print_summary()

    def print_summary(self):
        """Print crawl summary."""
        print("\n" + "═" * 60)
        print("CRAWL SUMMARY")
        print("═" * 60)
        print(f"Pages crawled:     {self.pages_crawled}")
        print(f"Failed URLs:       {len(self.failed_urls)}")
        print(f"Code examples:     {self.stats['code_examples']}")
        print(f"Images downloaded: {self.stats['images_downloaded']}")
        print(f"Tables extracted:  {self.stats['tables']}")
        print(f"Callouts found:    {self.stats['callouts']}")
        print(f"Videos found:      {self.stats['videos']}")
        print(f"Files downloaded:  {self.stats['downloads']}")
        print(f"Output directory:  {self.output_dir}")
        print("═" * 60)


def main():
    parser = argparse.ArgumentParser(description="Creatio Academy Comprehensive Crawler v2")
    parser.add_argument("--output-dir", "-o", default="./creatio-docs", help="Output directory")
    parser.add_argument("--section", "-s", action="append", help="Section(s) to crawl")
    parser.add_argument("--max-pages", "-m", type=int, default=1000, help="Max pages per section")
    parser.add_argument("--use-firecrawl", action="store_true", help="Use Firecrawl API")
    parser.add_argument("--no-assets", action="store_true", help="Skip downloading images/files")
    parser.add_argument("--list-sections", action="store_true", help="List available sections")

    args = parser.parse_args()

    if args.list_sections:
        print("Available sections:")
        for name, url in SECTIONS.items():
            print(f"  {name}: {url}")
        return

    crawler = CreatioAcademyCrawlerV2(
        output_dir=args.output_dir,
        use_firecrawl=args.use_firecrawl
    )
    crawler.run(
        sections=args.section,
        max_pages_per_section=args.max_pages,
        download_assets=not args.no_assets
    )


if __name__ == "__main__":
    main()
