#!/usr/bin/env python3
"""
Creatio DOM-based Schema Extraction
Extracts code directly from DOM elements
"""

from playwright.sync_api import sync_playwright
import os
from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts._paths import SCREENSHOTS_DIR, ARTIFACTS_DIR, ensure_dirs

ensure_dirs()

CREATIO_URL = os.environ.get("CREATIO_URL", "https://dev-pampabay.creatio.com")
USERNAME = os.environ.get("CREATIO_USERNAME", "")
PASSWORD = os.environ.get("CREATIO_PASSWORD", "")
SCREENSHOT_DIR = str(SCREENSHOTS_DIR)
TARGET_SCHEMA = "UsrPage_ebkv9e8"
SCHEMA_UID = "1d5dfc4d-732d-48d7-af21-9e3d70794734"

def screenshot(page, name):
    os.makedirs(SCREENSHOT_DIR, exist_ok=True)
    path = f"{SCREENSHOT_DIR}/{name}.png"
    page.screenshot(path=path, full_page=True)
    print(f"📸 {name}")
    return path

def wait_for_stable(page, timeout=5000):
    try:
        page.wait_for_load_state('networkidle', timeout=timeout)
    except:
        pass
    page.wait_for_timeout(1000)

with sync_playwright() as p:
    print("🚀 Launching browser...")
    browser = p.chromium.launch(headless=True, args=['--no-sandbox'])
    context = browser.new_context(viewport={'width': 1920, 'height': 1080})
    page = context.new_page()

    # Login
    print("\n1️⃣ Logging in...")
    page.goto(f"{CREATIO_URL}/Login/NuiLogin.aspx", timeout=30000)
    wait_for_stable(page)
    page.fill('input[type="text"]:first-of-type', USERNAME)
    page.fill('input[type="password"]', PASSWORD)
    page.click('[data-item-marker="btnLogin"]')
    page.wait_for_timeout(5000)
    wait_for_stable(page)
    print(f"   ✅ Logged in")

    # Open schema designer
    print(f"\n2️⃣ Opening schema designer...")
    designer_url = f"{CREATIO_URL}/0/ClientApp/#/ClientUnitSchemaDesigner/{SCHEMA_UID}"
    page.goto(designer_url, timeout=30000)
    page.wait_for_timeout(6000)
    wait_for_stable(page)

    # Find all possible editor elements
    print("\n3️⃣ Identifying editor elements...")

    editor_info = page.evaluate('''() => {
        const info = {
            ace_editor: document.querySelectorAll('.ace_editor').length,
            ace_content: document.querySelectorAll('.ace_content').length,
            ace_text_layer: document.querySelectorAll('.ace_text-layer').length,
            ace_line: document.querySelectorAll('.ace_line').length,
            monaco: document.querySelectorAll('.monaco-editor').length,
            code_mirror: document.querySelectorAll('.CodeMirror').length,
            textarea: document.querySelectorAll('textarea').length,
            pre: document.querySelectorAll('pre').length,
        };

        // Find by content
        const allElements = document.querySelectorAll('*');
        let defineFound = false;
        allElements.forEach(el => {
            if (el.textContent && el.textContent.includes('define("UsrPage')) {
                defineFound = true;
            }
        });
        info.defineFound = defineFound;

        return info;
    }''')
    print(f"   Editor info: {editor_info}")

    # Extract code using multiple methods
    print("\n4️⃣ Extracting code...")

    code = page.evaluate('''() => {
        // Method 1: ace_line elements (most reliable for Ace)
        let lines = document.querySelectorAll('.ace_line');
        if (lines.length > 0) {
            let text = [];
            lines.forEach(line => {
                text.push(line.textContent || '');
            });
            return {method: 'ace_line', content: text.join('\\n'), lineCount: lines.length};
        }

        // Method 2: Try ace_text-layer
        const textLayer = document.querySelector('.ace_text-layer');
        if (textLayer) {
            return {method: 'ace_text_layer', content: textLayer.textContent, lineCount: 0};
        }

        // Method 3: Pre elements
        const pre = document.querySelector('pre');
        if (pre) {
            return {method: 'pre', content: pre.textContent, lineCount: 0};
        }

        // Method 4: Any element containing the define statement
        const body = document.body;
        const text = body.innerText;
        if (text.includes('define(')) {
            // Extract just the code portion
            const start = text.indexOf('define(');
            if (start >= 0) {
                // Find the end by looking for closing });
                let depth = 0;
                let end = start;
                for (let i = start; i < text.length; i++) {
                    if (text[i] === '{') depth++;
                    if (text[i] === '}') depth--;
                    if (depth === 0 && text[i] === ';' && text[i-1] === ')') {
                        end = i + 1;
                        break;
                    }
                }
                return {method: 'body_extract', content: text.substring(start, end), lineCount: 0};
            }
        }

        return {method: 'none', content: '', lineCount: 0};
    }''')

    if code and code.get('content'):
        print(f"   ✅ Extracted via: {code.get('method')} ({len(code.get('content', ''))} chars)")

        content = code.get('content', '')

        # Save to file
        output_file = ARTIFACTS_DIR / f"{TARGET_SCHEMA}_extracted.js"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"   📄 Saved to: {output_file}")

        # Print key sections
        print(f"\n   Schema Analysis:")
        print(f"      - Lines extracted: {code.get('lineCount', 'N/A')}")
        print(f"      - Contains define(): {'define(' in content}")
        print(f"      - Contains handlers: {'handlers:' in content}")

        if 'handlers:' in content:
            # Find handlers section
            idx = content.find('handlers:')
            end_idx = min(idx + 100, len(content))
            print(f"\n   Handlers section preview:")
            print(f"   {content[idx:end_idx]}")
    else:
        print("   ⚠ No code extracted")

    # Screenshot final state
    screenshot(page, "dom_01_final")

    # Now let's find a working button handler example
    print("\n5️⃣ Finding button handler example from BGHome_Homepage...")

    # Query for BGHome_Homepage UID
    schema_info = page.evaluate('''async () => {
        try {
            const response = await fetch('/0/odata/SysSchema?$filter=Name eq \\'BGHome_Homepage\\'&$select=UId,Name&$top=1');
            const data = await response.json();
            return data;
        } catch(e) {
            return {error: e.message};
        }
    }''')

    if schema_info and 'value' in schema_info and len(schema_info['value']) > 0:
        example_uid = schema_info['value'][0].get('UId')
        print(f"   Found BGHome_Homepage UID: {example_uid}")

        # Navigate to this schema
        page.goto(f"{CREATIO_URL}/0/ClientApp/#/ClientUnitSchemaDesigner/{example_uid}", timeout=30000)
        page.wait_for_timeout(5000)
        wait_for_stable(page)

        # Extract its code
        example_code = page.evaluate('''() => {
            let lines = document.querySelectorAll('.ace_line');
            if (lines.length > 0) {
                let text = [];
                lines.forEach(line => { text.push(line.textContent || ''); });
                return text.join('\\n');
            }
            return '';
        }''')

        if example_code:
            example_file = ARTIFACTS_DIR / "BGHome_Homepage_example.js"
            with open(example_file, 'w', encoding='utf-8') as f:
                f.write(example_code)
            print(f"   📄 Saved example to: {example_file}")

            # Check for handlers
            if '/**SCHEMA_HANDLERS*/' in example_code:
                start = example_code.find('/**SCHEMA_HANDLERS*/')
                end = example_code.find('/**SCHEMA_HANDLERS*/', start + 20)
                if end > start:
                    handlers = example_code[start:end+len('/**SCHEMA_HANDLERS*/')]
                    print(f"\n   Example handlers ({len(handlers)} chars):")
                    print(f"   {handlers[:800]}...")

    screenshot(page, "dom_02_example")

    print("\n" + "="*60)
    print("EXTRACTION COMPLETE")
    print("="*60)

    browser.close()
    print("\n✅ Done!")
