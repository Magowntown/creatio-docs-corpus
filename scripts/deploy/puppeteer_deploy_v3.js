#!/usr/bin/env node
/**
 * Deploy UsrExcelReportService via Puppeteer
 * Uses keyboard type (slow but reliable)
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
    console.log('=== Puppeteer Deploy v3: UsrExcelReportService ===');
    console.log(`Target: ${CREATIO_URL}`);
    console.log(`Code size: ${NEW_CODE.length} bytes`);
    console.log('NOTE: Using keyboard type - this takes a while but is reliable\n');

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

        // Step 3: Focus and select all
        console.log('\n3. Selecting all code...');
        await page.click('.cm-content');
        await wait(500);

        // Select all
        await page.keyboard.down('Control');
        await page.keyboard.press('a');
        await page.keyboard.up('Control');
        await wait(500);
        console.log('   Selected all');

        // Step 4: Delete selected content
        console.log('\n4. Deleting existing code...');
        await page.keyboard.press('Delete');
        await wait(500);
        console.log('   Deleted');

        // Step 5: Type new code
        console.log('\n5. Typing new code (this will take ~2-3 minutes)...');
        const startTime = Date.now();

        // Type in chunks to show progress
        const chunkSize = 5000;
        const totalChunks = Math.ceil(NEW_CODE.length / chunkSize);

        for (let i = 0; i < NEW_CODE.length; i += chunkSize) {
            const chunk = NEW_CODE.substring(i, i + chunkSize);
            const chunkNum = Math.floor(i / chunkSize) + 1;

            // Use page.keyboard.type with delay:0 for speed
            await page.keyboard.type(chunk, { delay: 0 });

            const elapsed = ((Date.now() - startTime) / 1000).toFixed(1);
            const progress = ((i + chunkSize) / NEW_CODE.length * 100).toFixed(0);
            process.stdout.write(`\r   Progress: ${Math.min(progress, 100)}% (${elapsed}s elapsed, chunk ${chunkNum}/${totalChunks})`);
        }

        const totalTime = ((Date.now() - startTime) / 1000).toFixed(1);
        console.log(`\n   Typing complete in ${totalTime}s`);

        // Verify content
        const contentLength = await page.evaluate(() => {
            const content = document.querySelector('.cm-content');
            return content ? content.textContent.length : 0;
        });
        console.log(`   Content length: ${contentLength} chars (expected ~${NEW_CODE.length})`);

        if (contentLength < NEW_CODE.length * 0.9) {
            console.log('   WARNING: Content length mismatch!');
        }

        // Step 6: Save
        console.log('\n6. Saving...');
        await page.keyboard.down('Control');
        await page.keyboard.press('s');
        await page.keyboard.up('Control');
        await wait(3000);
        console.log('   Save triggered');

        // Step 7: Publish
        console.log('\n7. Publishing...');

        // Find and click Actions button
        const buttons = await page.$$('button');
        let actionsClicked = false;

        for (const btn of buttons) {
            const text = await page.evaluate(el => el.textContent, btn);
            if (text && text.includes('Actions')) {
                await btn.click();
                actionsClicked = true;
                console.log('   Actions menu opened');
                break;
            }
        }

        if (actionsClicked) {
            await wait(1500);

            // Find Publish in dropdown
            const publishClicked = await page.evaluate(() => {
                // Look for menu items
                const items = document.querySelectorAll('[class*="dropdown-item"], [class*="menu-item"], [role="menuitem"], span, div');
                for (const item of items) {
                    const text = item.textContent?.trim();
                    if (text === 'Publish') {
                        item.click();
                        return true;
                    }
                }
                return false;
            });

            if (publishClicked) {
                console.log('   Publish clicked - waiting for compilation (60s)...');
                await wait(60000);
                console.log('   Compilation wait complete');
            } else {
                console.log('   WARNING: Could not find Publish option');
                console.log('   Try clicking Actions → Publish manually');
            }
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
