#!/usr/bin/env node
/**
 * Trigger workspace build in Creatio
 */

const puppeteer = require('puppeteer');

const CREATIO_URL = process.env.CREATIO_URL || 'https://dev-pampabay.creatio.com';
const USERNAME = process.env.CREATIO_USERNAME || 'Supervisor';
const PASSWORD = process.env.CREATIO_PASSWORD || 'BayPampa3002!';

const wait = (ms) => new Promise(resolve => setTimeout(resolve, ms));

async function build() {
    console.log('=== Trigger Workspace Build ===');

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

        // Navigate to Configuration section
        console.log('\n2. Opening Configuration...');
        await page.goto(`${CREATIO_URL}/0/Nui/ViewModule.aspx#SectionModuleV2/SysWorkplace`, { waitUntil: 'networkidle2' });
        await wait(5000);

        // Alternative: Go directly to Configuration Manager
        console.log('   Trying configuration manager...');
        await page.goto(`${CREATIO_URL}/0/ClientApp/#/WorkspaceExplorer`, { waitUntil: 'networkidle2' });
        await wait(5000);

        // Look for Compile/Build button
        console.log('\n3. Looking for build options...');

        const pageContent = await page.content();
        const hasCompile = pageContent.includes('Compile') || pageContent.includes('compile');
        const hasBuild = pageContent.includes('Build') || pageContent.includes('build');
        console.log(`   Page has 'Compile': ${hasCompile}`);
        console.log(`   Page has 'Build': ${hasBuild}`);

        // Try clicking any compile/build button
        const buildResult = await page.evaluate(() => {
            const keywords = ['Compile', 'Build', 'Rebuild', 'compile', 'build'];
            const buttons = document.querySelectorAll('button, [role="button"], [class*="button"]');

            for (const btn of buttons) {
                const text = btn.textContent?.trim();
                if (text && keywords.some(k => text.includes(k))) {
                    btn.click();
                    return { clicked: true, text };
                }
            }

            // Try menu items
            const menuItems = document.querySelectorAll('[class*="menu-item"], [role="menuitem"]');
            for (const item of menuItems) {
                const text = item.textContent?.trim();
                if (text && keywords.some(k => text.includes(k))) {
                    item.click();
                    return { clicked: true, text };
                }
            }

            return { clicked: false };
        });

        console.log('   Build result:', buildResult);

        if (buildResult.clicked) {
            console.log('\n4. Waiting for compilation (120s)...');
            await wait(120000);
        } else {
            console.log('\n   No build button found. Trying API...');

            // Try triggering build via API
            const cookies = await page.cookies();
            const bpmcsrf = cookies.find(c => c.name === 'BPMCSRF')?.value || '';

            const apiResult = await page.evaluate(async (csrf) => {
                const endpoints = [
                    '/0/ServiceModel/WorkspaceExplorerService.svc/Build',
                    '/0/rest/WorkspaceExplorerService/Build',
                    '/0/ServiceModel/SourceCodeSchemaManagerService.svc/Compile'
                ];

                for (const endpoint of endpoints) {
                    try {
                        const resp = await fetch(endpoint, {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json',
                                'BPMCSRF': csrf
                            },
                            body: JSON.stringify({})
                        });
                        if (resp.ok) {
                            return { success: true, endpoint };
                        }
                    } catch (e) {}
                }
                return { success: false };
            }, bpmcsrf);

            console.log('   API result:', apiResult);

            if (apiResult.success) {
                console.log('\n4. Build triggered via API. Waiting 120s...');
                await wait(120000);
            }
        }

        console.log('\n=== Done ===');

    } catch (err) {
        console.error('\nERROR:', err.message);
    } finally {
        await browser.close();
    }
}

build();
