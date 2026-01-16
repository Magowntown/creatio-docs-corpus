#!/usr/bin/env node
/**
 * Test Puppeteer browser automation for Creatio
 * Goal: Login and navigate to Source Code Schema Designer
 */

const puppeteer = require('puppeteer');

const CREATIO_URL = process.env.CREATIO_URL || 'https://dev-pampabay.creatio.com';
const USERNAME = process.env.CREATIO_USERNAME || 'Supervisor';
const PASSWORD = process.env.CREATIO_PASSWORD || 'BayPampa3002!';
const SCHEMA_UID = 'ed794ab8-8a59-4c7e-983c-cc039449d178';

async function test() {
    console.log('=== Puppeteer Test ===');
    console.log(`Target: ${CREATIO_URL}`);

    const browser = await puppeteer.launch({
        headless: 'new',
        args: ['--no-sandbox', '--disable-setuid-sandbox']
    });

    try {
        const page = await browser.newPage();
        page.setDefaultTimeout(30000);

        // Step 1: Navigate to login
        console.log('\n1. Navigating to login page...');
        await page.goto(CREATIO_URL, { waitUntil: 'networkidle2' });
        console.log(`   URL: ${page.url()}`);

        // Step 2: Login
        console.log('\n2. Logging in...');
        await page.waitForSelector('#loginEdit-el', { timeout: 10000 });
        await page.type('#loginEdit-el', USERNAME);
        await page.type('#passwordEdit-el', PASSWORD);
        // Click login button - try multiple selectors
        const loginBtnSelectors = [
            '#t-comp18-textEl',
            '[class*="login-button"]',
            'button:has-text("Log In")',
            '.login-button',
            '[id*="loginBtn"]'
        ];

        let clicked = false;
        for (const sel of loginBtnSelectors) {
            try {
                await page.click(sel);
                clicked = true;
                console.log(`   Clicked: ${sel}`);
                break;
            } catch (e) {
                // Try next selector
            }
        }

        if (!clicked) {
            // Try XPath for "Log In" text
            const [loginBtn] = await page.$x("//div[contains(text(), 'Log In')]");
            if (loginBtn) {
                await loginBtn.click();
                clicked = true;
                console.log('   Clicked via XPath');
            }
        }

        if (!clicked) {
            console.log('   Could not find login button');
            return;
        }

        // Wait for redirect to shell
        await page.waitForNavigation({ waitUntil: 'networkidle2', timeout: 30000 });
        console.log(`   URL after login: ${page.url()}`);

        if (page.url().includes('/Shell/')) {
            console.log('   Login: SUCCESS');
        } else {
            console.log('   Login: FAILED (unexpected URL)');
            return;
        }

        // Step 3: Navigate to Source Code Schema Designer
        console.log('\n3. Navigating to Source Code Schema Designer...');
        const designerUrl = `${CREATIO_URL}/0/ClientApp/#/SourceCodeSchemaDesigner/${SCHEMA_UID}`;
        await page.goto(designerUrl, { waitUntil: 'networkidle2' });
        console.log(`   URL: ${page.url()}`);

        // Wait for editor to load
        await page.waitForSelector('[class*="monaco"], [class*="editor"], textarea', { timeout: 15000 });
        console.log('   Editor loaded: SUCCESS');

        // Step 4: Check if we can find the code editor
        console.log('\n4. Looking for code editor...');

        // Try multiple selectors
        const selectors = [
            '.monaco-editor',
            '[data-mode-id="csharp"]',
            'textarea[class*="inputarea"]',
            '.view-lines',
            '[role="textbox"]'
        ];

        for (const sel of selectors) {
            const found = await page.$(sel);
            console.log(`   ${sel}: ${found ? 'FOUND' : 'not found'}`);
        }

        // Get page content sample
        const pageContent = await page.content();
        const hasMonaco = pageContent.includes('monaco');
        const hasCodeMirror = pageContent.includes('CodeMirror');
        console.log(`\n   Monaco in page: ${hasMonaco}`);
        console.log(`   CodeMirror in page: ${hasCodeMirror}`);

        // Check for window.monaco
        const hasWindowMonaco = await page.evaluate(() => {
            return typeof window.monaco !== 'undefined';
        });
        console.log(`   window.monaco: ${hasWindowMonaco}`);

        console.log('\n=== Test Complete ===');

    } catch (err) {
        console.error('\nERROR:', err.message);
    } finally {
        await browser.close();
    }
}

test();
