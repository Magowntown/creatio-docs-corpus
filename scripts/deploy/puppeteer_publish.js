#!/usr/bin/env node
/**
 * Publish UsrExcelReportService schema (code already saved)
 */

const puppeteer = require('puppeteer');

const CREATIO_URL = process.env.CREATIO_URL || 'https://dev-pampabay.creatio.com';
const USERNAME = process.env.CREATIO_USERNAME || 'Supervisor';
const PASSWORD = process.env.CREATIO_PASSWORD || 'BayPampa3002!';
const SCHEMA_UID = 'ed794ab8-8a59-4c7e-983c-cc039449d178';

const wait = (ms) => new Promise(resolve => setTimeout(resolve, ms));

async function publish() {
    console.log('=== Puppeteer Publish: UsrExcelReportService ===');

    const browser = await puppeteer.launch({
        headless: 'new',
        args: ['--no-sandbox', '--disable-setuid-sandbox']
    });

    try {
        const page = await browser.newPage();
        page.setDefaultTimeout(120000);

        // Login
        console.log('\n1. Logging in...');
        await page.goto(CREATIO_URL, { waitUntil: 'networkidle2' });
        await page.waitForSelector('#loginEdit-el');
        await page.type('#loginEdit-el', USERNAME);
        await page.type('#passwordEdit-el', PASSWORD);
        await page.click('#t-comp18-textEl');
        await page.waitForNavigation({ waitUntil: 'networkidle2' });
        console.log('   Login: SUCCESS');

        // Navigate to Schema Designer
        console.log('\n2. Opening Schema Designer...');
        await page.goto(`${CREATIO_URL}/0/ClientApp/#/SourceCodeSchemaDesigner/${SCHEMA_UID}`, { waitUntil: 'networkidle2' });
        await page.waitForSelector('.cm-editor', { timeout: 20000 });
        await wait(3000);
        console.log('   Editor loaded');

        // Take screenshot of current state
        await page.screenshot({ path: 'test-artifacts/before_publish.png' });
        console.log('   Screenshot saved: test-artifacts/before_publish.png');

        // Find Actions button
        console.log('\n3. Looking for Actions button...');

        const buttonsInfo = await page.evaluate(() => {
            const buttons = Array.from(document.querySelectorAll('button'));
            return buttons.map(b => ({
                text: b.textContent?.trim(),
                class: b.className,
                visible: b.offsetParent !== null
            }));
        });

        console.log('   Buttons found:');
        buttonsInfo.filter(b => b.visible).forEach(b => console.log(`     - "${b.text}"`));

        // Click Actions
        console.log('\n4. Clicking Actions...');
        const actionsClicked = await page.evaluate(() => {
            const buttons = document.querySelectorAll('button');
            for (const btn of buttons) {
                if (btn.textContent?.includes('Actions') && btn.offsetParent !== null) {
                    btn.click();
                    return { clicked: true, text: btn.textContent?.trim() };
                }
            }
            return { clicked: false };
        });

        console.log('   Actions result:', actionsClicked);

        if (actionsClicked.clicked) {
            await wait(2000);

            // Screenshot the dropdown
            await page.screenshot({ path: 'test-artifacts/actions_menu.png' });
            console.log('   Screenshot saved: test-artifacts/actions_menu.png');

            // Look for menu items
            console.log('\n5. Looking for Publish option...');

            const menuInfo = await page.evaluate(() => {
                // Get all visible text elements
                const allElements = document.querySelectorAll('*');
                const menuItems = [];

                for (const el of allElements) {
                    if (el.offsetParent !== null &&
                        el.childElementCount === 0 &&
                        el.textContent?.trim()) {
                        const text = el.textContent.trim();
                        if (text.length < 50) {
                            menuItems.push({
                                text,
                                tag: el.tagName,
                                class: el.className?.substring(0, 50) || ''
                            });
                        }
                    }
                }

                // Filter for potential menu items
                return menuItems.filter(m =>
                    m.text.includes('Publish') ||
                    m.text.includes('Save') ||
                    m.text.includes('Compile') ||
                    m.text.includes('Build')
                );
            });

            console.log('   Menu items found:');
            menuInfo.forEach(m => console.log(`     - "${m.text}" (${m.tag})`));

            // Click Publish
            const publishResult = await page.evaluate(() => {
                const allElements = document.querySelectorAll('*');
                for (const el of allElements) {
                    const text = el.textContent?.trim();
                    if (text === 'Publish' && el.offsetParent !== null) {
                        // Check if it's a clickable element
                        el.click();
                        return { clicked: true, tag: el.tagName, class: el.className };
                    }
                }
                return { clicked: false };
            });

            console.log('   Publish result:', publishResult);

            if (publishResult.clicked) {
                console.log('\n6. Waiting for compilation (90s)...');
                await wait(90000);

                await page.screenshot({ path: 'test-artifacts/after_publish.png' });
                console.log('   Screenshot saved: test-artifacts/after_publish.png');
            } else {
                // Try clicking via CSS selector patterns
                console.log('   Trying alternative selectors...');

                const altResult = await page.evaluate(() => {
                    // Look for dropdown items
                    const selectors = [
                        '[class*="dropdown"] [class*="item"]',
                        '[class*="menu"] [class*="item"]',
                        '[role="menuitem"]',
                        'li',
                        'span'
                    ];

                    for (const sel of selectors) {
                        const items = document.querySelectorAll(sel);
                        for (const item of items) {
                            if (item.textContent?.trim() === 'Publish') {
                                item.click();
                                return { clicked: true, selector: sel };
                            }
                        }
                    }
                    return { clicked: false };
                });

                console.log('   Alt result:', altResult);

                if (altResult.clicked) {
                    console.log('\n6. Waiting for compilation (90s)...');
                    await wait(90000);
                }
            }
        }

        console.log('\n=== Done ===');

    } catch (err) {
        console.error('\nERROR:', err.message);
    } finally {
        await browser.close();
    }
}

publish();
