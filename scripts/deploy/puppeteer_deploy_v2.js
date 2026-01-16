#!/usr/bin/env node
/**
 * Deploy UsrExcelReportService via Puppeteer
 * Uses keyboard shortcuts (Ctrl+A, paste) for CodeMirror 6
 */

const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');

const CREATIO_URL = process.env.CREATIO_URL || 'https://dev-pampabay.creatio.com';
const USERNAME = process.env.CREATIO_USERNAME || 'Supervisor';
const PASSWORD = process.env.CREATIO_PASSWORD || 'BayPampa3002!';
const SCHEMA_UID = 'ed794ab8-8a59-4c7e-983c-cc039449d178';

const CODE_PATH = path.join(__dirname, '..', '..', 'source-code', 'UsrExcelReportService_Updated.cs');
const NEW_CODE = fs.readFileSync(CODE_PATH, 'utf8');

const wait = (ms) => new Promise(resolve => setTimeout(resolve, ms));

async function deploy() {
    console.log('=== Puppeteer Deploy v2: UsrExcelReportService ===');
    console.log(`Target: ${CREATIO_URL}`);
    console.log(`Code size: ${NEW_CODE.length} bytes`);

    const browser = await puppeteer.launch({
        headless: 'new',
        args: [
            '--no-sandbox',
            '--disable-setuid-sandbox'
        ]
    });

    try {
        const page = await browser.newPage();
        page.setDefaultTimeout(60000);

        // Grant clipboard permissions
        const context = browser.defaultBrowserContext();
        await context.overridePermissions(CREATIO_URL, ['clipboard-read', 'clipboard-write']);

        // Step 1: Login
        console.log('\n1. Logging in...');
        await page.goto(CREATIO_URL, { waitUntil: 'networkidle2' });
        await page.waitForSelector('#loginEdit-el', { timeout: 10000 });
        await page.type('#loginEdit-el', USERNAME);
        await page.type('#passwordEdit-el', PASSWORD);
        await page.click('#t-comp18-textEl');
        await page.waitForNavigation({ waitUntil: 'networkidle2', timeout: 30000 });

        if (!page.url().includes('/Shell/')) {
            throw new Error('Login failed');
        }
        console.log('   Login: SUCCESS');

        // Step 2: Navigate to Schema Designer
        console.log('\n2. Opening Schema Designer...');
        await page.goto(`${CREATIO_URL}/0/ClientApp/#/SourceCodeSchemaDesigner/${SCHEMA_UID}`, { waitUntil: 'networkidle2' });

        // Wait for CodeMirror editor
        await page.waitForSelector('.cm-editor', { timeout: 15000 });
        await wait(2000);
        console.log('   Editor loaded: SUCCESS');

        // Step 3: Focus editor and select all
        console.log('\n3. Setting code via clipboard...');

        // Click on editor to focus
        await page.click('.cm-content');
        await wait(500);

        // Select all (Ctrl+A)
        await page.keyboard.down('Control');
        await page.keyboard.press('a');
        await page.keyboard.up('Control');
        await wait(300);

        // Set clipboard content and paste
        await page.evaluate((code) => {
            navigator.clipboard.writeText(code);
        }, NEW_CODE);
        await wait(300);

        // Paste (Ctrl+V)
        await page.keyboard.down('Control');
        await page.keyboard.press('v');
        await page.keyboard.up('Control');
        await wait(1000);

        // Verify content was set
        const contentLength = await page.evaluate(() => {
            const editor = document.querySelector('.cm-content');
            return editor ? editor.textContent.length : 0;
        });
        console.log(`   Content length after paste: ${contentLength} chars`);

        if (contentLength < 1000) {
            console.log('   WARNING: Content seems too short, paste may have failed');
            console.log('   Trying alternative: direct input simulation...');

            // Alternative: Use EditorView transactions via Angular
            const setResult = await page.evaluate((code) => {
                // Try to find the EditorView instance
                const cmEditor = document.querySelector('.cm-editor');
                if (!cmEditor) return { success: false, error: 'No cm-editor' };

                // CodeMirror 6 stores view in a property
                const view = cmEditor.view || cmEditor._view || cmEditor.cmView;
                if (view && view.dispatch) {
                    // Use transaction to replace content
                    view.dispatch({
                        changes: {
                            from: 0,
                            to: view.state.doc.length,
                            insert: code
                        }
                    });
                    return { success: true, method: 'dispatch' };
                }

                // Try Angular component access
                const ngComponent = cmEditor.__ngContext__;
                if (ngComponent) {
                    return { success: false, error: 'Has Angular context but no direct access' };
                }

                return { success: false, error: 'No EditorView found' };
            }, NEW_CODE);

            console.log('   Alternative result:', setResult);
        }

        // Step 4: Save
        console.log('\n4. Saving...');
        await page.keyboard.down('Control');
        await page.keyboard.press('s');
        await page.keyboard.up('Control');
        await wait(3000);
        console.log('   Save triggered');

        // Step 5: Publish
        console.log('\n5. Publishing...');

        // Click Actions button
        const actionsBtn = await page.$('button');
        const buttons = await page.$$('button');
        let actionsClicked = false;

        for (const btn of buttons) {
            const text = await page.evaluate(el => el.textContent, btn);
            if (text && text.includes('Actions')) {
                await btn.click();
                actionsClicked = true;
                break;
            }
        }

        if (actionsClicked) {
            await wait(1000);

            // Look for Publish option
            const menuItems = await page.$$('[class*="menu"], [role="menu"], [class*="dropdown"]');
            console.log(`   Found ${menuItems.length} menu elements`);

            // Try clicking any element containing "Publish"
            const publishClicked = await page.evaluate(() => {
                const all = document.querySelectorAll('*');
                for (const el of all) {
                    if (el.textContent === 'Publish' ||
                        (el.textContent && el.textContent.trim() === 'Publish')) {
                        el.click();
                        return true;
                    }
                }
                return false;
            });

            if (publishClicked) {
                console.log('   Publish clicked - waiting for compilation...');
                await wait(45000);
                console.log('   Compilation wait complete');
            } else {
                console.log('   WARNING: Could not find Publish option');
                console.log('   Code is saved but NOT published. Manual publish required.');
            }
        } else {
            console.log('   WARNING: Could not find Actions button');
        }

        console.log('\n=== Deploy Complete ===');
        console.log('\nVerify with:');
        console.log('  python3 scripts/testing/test_report_service.py');

    } catch (err) {
        console.error('\nERROR:', err.message);
        process.exit(1);
    } finally {
        await browser.close();
    }
}

deploy();
