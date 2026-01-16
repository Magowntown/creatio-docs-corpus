#!/usr/bin/env node
/**
 * Deploy UsrExcelReportService via Puppeteer
 * Uses document.execCommand('insertText') for fast insertion
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
    console.log('=== Puppeteer Deploy v4: UsrExcelReportService ===');
    console.log(`Target: ${CREATIO_URL}`);
    console.log(`Code size: ${NEW_CODE.length} bytes\n`);

    const browser = await puppeteer.launch({
        headless: 'new',
        args: ['--no-sandbox', '--disable-setuid-sandbox']
    });

    try {
        const page = await browser.newPage();
        page.setDefaultTimeout(120000);

        // Step 1: Login
        console.log('1. Logging in...');
        await page.goto(CREATIO_URL, { waitUntil: 'networkidle2' });
        await page.waitForSelector('#loginEdit-el');
        await page.type('#loginEdit-el', USERNAME);
        await page.type('#passwordEdit-el', PASSWORD);
        await page.click('#t-comp18-textEl');
        await page.waitForNavigation({ waitUntil: 'networkidle2' });
        console.log('   Login: SUCCESS');

        // Step 2: Navigate to Schema Designer
        console.log('\n2. Opening Schema Designer...');
        await page.goto(`${CREATIO_URL}/0/ClientApp/#/SourceCodeSchemaDesigner/${SCHEMA_UID}`, { waitUntil: 'networkidle2' });
        await page.waitForSelector('.cm-editor', { timeout: 20000 });
        await wait(3000);
        console.log('   Editor loaded: SUCCESS');

        // Step 3: Insert code using various methods
        console.log('\n3. Inserting code...');

        const insertResult = await page.evaluate((code) => {
            const results = { attempted: [], success: false };

            // Method 1: Find cm-content and use DOM manipulation + input event
            const cmContent = document.querySelector('.cm-content');
            if (cmContent) {
                results.attempted.push('cm-content');

                // Focus the element
                cmContent.focus();

                // Try to find the view through the editor element
                const cmEditor = document.querySelector('.cm-editor');

                // Method 1a: Look for CodeMirror 6 EditorView in various locations
                const possibleViewLocations = [
                    cmEditor?.view,
                    cmEditor?._view,
                    cmEditor?.cmView,
                    window.editorView,
                    document.__editorView
                ];

                for (const view of possibleViewLocations) {
                    if (view && typeof view.dispatch === 'function') {
                        results.attempted.push('EditorView.dispatch');
                        try {
                            const docLength = view.state.doc.length;
                            view.dispatch({
                                changes: { from: 0, to: docLength, insert: code }
                            });
                            results.success = true;
                            results.method = 'EditorView.dispatch';
                            return results;
                        } catch (e) {
                            results.error = e.message;
                        }
                    }
                }

                // Method 1b: Try to access through Angular's NgZone
                if (window.ng) {
                    results.attempted.push('Angular ng');
                    try {
                        const ngContext = cmEditor?.__ngContext__;
                        if (ngContext) {
                            results.ngContext = 'found';
                        }
                    } catch (e) {}
                }

                // Method 1c: Select all and use execCommand
                results.attempted.push('execCommand');
                const selection = window.getSelection();
                const range = document.createRange();
                range.selectNodeContents(cmContent);
                selection.removeAllRanges();
                selection.addRange(range);

                // Try insertText
                const inserted = document.execCommand('insertText', false, code);
                if (inserted) {
                    results.success = true;
                    results.method = 'execCommand.insertText';
                    return results;
                }

                // Method 1d: Input event simulation
                results.attempted.push('InputEvent');
                const inputEvent = new InputEvent('beforeinput', {
                    inputType: 'insertText',
                    data: code,
                    bubbles: true,
                    cancelable: true
                });
                cmContent.dispatchEvent(inputEvent);

                const inputEvent2 = new InputEvent('input', {
                    inputType: 'insertText',
                    data: code,
                    bubbles: true
                });
                cmContent.dispatchEvent(inputEvent2);
            }

            // Method 2: Try textarea fallback (some editors have hidden textarea)
            const textarea = document.querySelector('textarea');
            if (textarea) {
                results.attempted.push('textarea');
                textarea.value = code;
                textarea.dispatchEvent(new Event('input', { bubbles: true }));
                textarea.dispatchEvent(new Event('change', { bubbles: true }));
            }

            return results;
        }, NEW_CODE);

        console.log('   Insert result:', insertResult);

        // Check if content was inserted
        await wait(1000);
        const contentCheck = await page.evaluate(() => {
            const content = document.querySelector('.cm-content');
            return {
                length: content ? content.textContent.length : 0,
                firstChars: content ? content.textContent.substring(0, 50) : ''
            };
        });
        console.log(`   Content check: ${contentCheck.length} chars`);
        console.log(`   First chars: "${contentCheck.firstChars}"`);

        if (contentCheck.length < 1000) {
            console.log('\n   WARNING: Insert methods failed. Falling back to keyboard type...');
            console.log('   This will take 2-3 minutes...');

            // Click and select all
            await page.click('.cm-content');
            await page.keyboard.down('Control');
            await page.keyboard.press('a');
            await page.keyboard.up('Control');
            await wait(500);
            await page.keyboard.press('Delete');
            await wait(500);

            // Type with minimal delay
            const startTime = Date.now();
            await page.keyboard.type(NEW_CODE, { delay: 0 });
            const elapsed = ((Date.now() - startTime) / 1000).toFixed(1);
            console.log(`   Typed ${NEW_CODE.length} chars in ${elapsed}s`);
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

        const buttons = await page.$$('button');
        for (const btn of buttons) {
            const text = await page.evaluate(el => el.textContent, btn);
            if (text && text.includes('Actions')) {
                await btn.click();
                console.log('   Actions menu clicked');
                break;
            }
        }

        await wait(1500);

        const publishClicked = await page.evaluate(() => {
            const elements = document.querySelectorAll('*');
            for (const el of elements) {
                if (el.textContent?.trim() === 'Publish' && el.offsetParent !== null) {
                    el.click();
                    return true;
                }
            }
            return false;
        });

        if (publishClicked) {
            console.log('   Publish clicked - waiting 60s for compilation...');
            await wait(60000);
            console.log('   Done');
        } else {
            console.log('   WARNING: Publish not found. Manual publish required.');
        }

        console.log('\n=== Deploy Complete ===');
        console.log('\nVerify: python3 scripts/testing/test_report_service.py');

    } catch (err) {
        console.error('\nERROR:', err.message);
        process.exit(1);
    } finally {
        await browser.close();
    }
}

deploy();
