#!/usr/bin/env node
/**
 * Inspect Creatio Source Code Schema Designer structure
 */

const puppeteer = require('puppeteer');

const CREATIO_URL = 'https://dev-pampabay.creatio.com';
const USERNAME = 'Supervisor';
const PASSWORD = 'BayPampa3002!';
const SCHEMA_UID = 'ed794ab8-8a59-4c7e-983c-cc039449d178';

const wait = (ms) => new Promise(resolve => setTimeout(resolve, ms));

async function inspect() {
    console.log('=== Inspecting Creatio Editor ===');

    const browser = await puppeteer.launch({
        headless: 'new',
        args: ['--no-sandbox', '--disable-setuid-sandbox']
    });

    try {
        const page = await browser.newPage();
        page.setDefaultTimeout(60000);

        // Login
        console.log('\n1. Logging in...');
        await page.goto(CREATIO_URL, { waitUntil: 'networkidle2' });
        await page.waitForSelector('#loginEdit-el');
        await page.type('#loginEdit-el', USERNAME);
        await page.type('#passwordEdit-el', PASSWORD);
        await page.click('#t-comp18-textEl');
        await page.waitForNavigation({ waitUntil: 'networkidle2' });
        console.log('   Login: SUCCESS');

        // Navigate to editor
        console.log('\n2. Opening Schema Designer...');
        await page.goto(`${CREATIO_URL}/0/ClientApp/#/SourceCodeSchemaDesigner/${SCHEMA_UID}`, { waitUntil: 'networkidle2' });
        await page.waitForSelector('[role="textbox"]', { timeout: 15000 });
        await wait(3000);
        console.log('   Editor loaded');

        // Inspect
        console.log('\n3. Inspecting editor structure...');

        const info = await page.evaluate(() => {
            const results = {
                classesContainingEditor: [],
                classesContainingCode: [],
                elementsWithCodeMirror: [],
                textareas: [],
                roleTextbox: [],
                globalVars: []
            };

            // Find elements with "editor" in class
            const allElements = document.querySelectorAll('*');
            allElements.forEach(el => {
                if (el.className && typeof el.className === 'string') {
                    if (el.className.includes('editor') || el.className.includes('Editor')) {
                        results.classesContainingEditor.push({
                            tag: el.tagName,
                            class: el.className.substring(0, 100),
                            hasCodeMirror: !!el.CodeMirror
                        });
                    }
                    if (el.className.includes('code') || el.className.includes('Code')) {
                        results.classesContainingCode.push({
                            tag: el.tagName,
                            class: el.className.substring(0, 100),
                            hasCodeMirror: !!el.CodeMirror
                        });
                    }
                }
                if (el.CodeMirror) {
                    results.elementsWithCodeMirror.push({
                        tag: el.tagName,
                        class: el.className ? el.className.substring(0, 100) : '',
                        id: el.id
                    });
                }
            });

            // Find textareas
            document.querySelectorAll('textarea').forEach(ta => {
                results.textareas.push({
                    class: ta.className,
                    id: ta.id,
                    hasCodeMirror: !!ta.CodeMirror,
                    valueLength: ta.value ? ta.value.length : 0
                });
            });

            // Find role=textbox
            document.querySelectorAll('[role="textbox"]').forEach(el => {
                results.roleTextbox.push({
                    tag: el.tagName,
                    class: el.className ? el.className.substring(0, 100) : '',
                    contentLength: el.textContent ? el.textContent.length : 0
                });
            });

            // Check for known editor globals
            const globals = ['monaco', 'CodeMirror', 'ace', 'editor', 'codeEditor'];
            globals.forEach(g => {
                if (typeof window[g] !== 'undefined') {
                    results.globalVars.push(g);
                }
            });

            return results;
        });

        console.log('\n=== Results ===');
        console.log('\nGlobal variables found:', info.globalVars);
        console.log('\nElements with CodeMirror property:', info.elementsWithCodeMirror.length);
        info.elementsWithCodeMirror.forEach(e => console.log('  ', e));

        console.log('\nClasses containing "editor":', info.classesContainingEditor.length);
        info.classesContainingEditor.slice(0, 10).forEach(e => console.log('  ', e));

        console.log('\nClasses containing "code":', info.classesContainingCode.length);
        info.classesContainingCode.slice(0, 10).forEach(e => console.log('  ', e));

        console.log('\nTextareas:', info.textareas.length);
        info.textareas.forEach(e => console.log('  ', e));

        console.log('\nRole=textbox:', info.roleTextbox.length);
        info.roleTextbox.slice(0, 5).forEach(e => console.log('  ', e));

        // Try to find any way to set the code
        console.log('\n4. Trying to access editor via window...');
        const editorAccess = await page.evaluate(() => {
            // Try various patterns
            const tries = {};

            // Angular
            if (window.ng) {
                tries.angular = true;
            }

            // Monaco
            if (window.monaco && window.monaco.editor) {
                const editors = window.monaco.editor.getEditors();
                tries.monacoEditors = editors.length;
            }

            // Look for editor in iframe
            const iframes = document.querySelectorAll('iframe');
            tries.iframes = iframes.length;

            // CodeMirror global
            if (window.CodeMirror) {
                tries.codeMirrorGlobal = true;
            }

            // Check document.querySelector for common patterns
            const cmWrapper = document.querySelector('.CodeMirror-wrap');
            tries.cmWrap = !!cmWrapper;

            const cmScroll = document.querySelector('.CodeMirror-scroll');
            tries.cmScroll = !!cmScroll;

            return tries;
        });

        console.log('Access methods:', editorAccess);

    } catch (err) {
        console.error('\nERROR:', err.message);
    } finally {
        await browser.close();
    }
}

inspect();
