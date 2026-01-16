#!/usr/bin/env node
/**
 * Deploy UsrExcelReportService via Puppeteer
 * Uses CodeMirror API (Creatio's editor)
 */

const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');

const CREATIO_URL = process.env.CREATIO_URL || 'https://dev-pampabay.creatio.com';
const USERNAME = process.env.CREATIO_USERNAME || 'Supervisor';
const PASSWORD = process.env.CREATIO_PASSWORD || 'BayPampa3002!';
const SCHEMA_UID = 'ed794ab8-8a59-4c7e-983c-cc039449d178';

// Read the updated service code
const CODE_PATH = path.join(__dirname, '..', '..', 'source-code', 'UsrExcelReportService_Updated.cs');
const NEW_CODE = fs.readFileSync(CODE_PATH, 'utf8');

// Helper for waiting
const wait = (ms) => new Promise(resolve => setTimeout(resolve, ms));

async function deploy() {
    console.log('=== Puppeteer Deploy: UsrExcelReportService ===');
    console.log(`Target: ${CREATIO_URL}`);
    console.log(`Code size: ${NEW_CODE.length} bytes`);

    const browser = await puppeteer.launch({
        headless: 'new',
        args: ['--no-sandbox', '--disable-setuid-sandbox']
    });

    try {
        const page = await browser.newPage();
        page.setDefaultTimeout(60000);

        // Step 1: Login
        console.log('\n1. Logging in...');
        await page.goto(CREATIO_URL, { waitUntil: 'networkidle2' });
        await page.waitForSelector('#loginEdit-el', { timeout: 10000 });
        await page.type('#loginEdit-el', USERNAME);
        await page.type('#passwordEdit-el', PASSWORD);
        await page.click('#t-comp18-textEl');
        await page.waitForNavigation({ waitUntil: 'networkidle2', timeout: 30000 });

        if (!page.url().includes('/Shell/')) {
            throw new Error('Login failed - unexpected URL: ' + page.url());
        }
        console.log('   Login: SUCCESS');

        // Step 2: Navigate to Source Code Schema Designer
        console.log('\n2. Opening Schema Designer...');
        const designerUrl = `${CREATIO_URL}/0/ClientApp/#/SourceCodeSchemaDesigner/${SCHEMA_UID}`;
        await page.goto(designerUrl, { waitUntil: 'networkidle2' });

        // Wait for CodeMirror to load
        await page.waitForSelector('[role="textbox"]', { timeout: 15000 });
        await wait(2000); // Extra wait for CodeMirror init
        console.log('   Editor loaded: SUCCESS');

        // Step 3: Set code via CodeMirror
        console.log('\n3. Setting code via CodeMirror...');

        const result = await page.evaluate((code) => {
            // Find CodeMirror instance
            const cmElements = document.querySelectorAll('.CodeMirror');
            if (cmElements.length === 0) {
                return { success: false, error: 'No CodeMirror found' };
            }

            const cmElement = cmElements[0];
            const cm = cmElement.CodeMirror;

            if (!cm) {
                return { success: false, error: 'CodeMirror instance not found on element' };
            }

            // Set the value
            cm.setValue(code);

            // Verify
            const newValue = cm.getValue();
            const matches = newValue.length === code.length;

            return {
                success: true,
                originalLength: code.length,
                newLength: newValue.length,
                matches: matches
            };
        }, NEW_CODE);

        if (!result.success) {
            throw new Error('CodeMirror set failed: ' + result.error);
        }

        console.log(`   Code set: ${result.newLength} bytes (matches: ${result.matches})`);

        // Step 4: Save (Ctrl+S)
        console.log('\n4. Saving schema...');
        await page.keyboard.down('Control');
        await page.keyboard.press('s');
        await page.keyboard.up('Control');
        await wait(2000);
        console.log('   Save triggered');

        // Step 5: Publish via Actions menu
        console.log('\n5. Publishing...');

        // Click Actions button
        const actionsClicked = await page.evaluate(() => {
            const btns = Array.from(document.querySelectorAll('button'));
            const actionsBtn = btns.find(b => b.textContent.includes('Actions'));
            if (actionsBtn) {
                actionsBtn.click();
                return true;
            }
            return false;
        });

        if (actionsClicked) {
            await wait(1000);

            // Click Publish in menu
            const publishClicked = await page.evaluate(() => {
                const items = Array.from(document.querySelectorAll('[class*="menu-item"], [role="menuitem"], div'));
                const publishItem = items.find(i => i.textContent && i.textContent.includes('Publish'));
                if (publishItem) {
                    publishItem.click();
                    return true;
                }
                return false;
            });

            if (publishClicked) {
                console.log('   Publish clicked - waiting for compilation...');
                await wait(30000); // Wait for compilation
                console.log('   Compilation wait complete');
            } else {
                console.log('   WARNING: Could not find Publish menu item');
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
