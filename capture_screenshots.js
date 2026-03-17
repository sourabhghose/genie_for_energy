#!/usr/bin/env node
/**
 * Screenshot Capture Script
 *
 * Captures real Databricks workspace screenshots to replace the
 * generated documentation images. Run this script while logged
 * into a Databricks workspace in Chrome.
 *
 * Usage:
 *   npm install playwright    # one-time
 *   node capture_screenshots.js [workspace-url]
 *
 * The script launches a visible browser so you can log in if needed.
 * After login, it navigates to each page and captures screenshots.
 */

const { chromium } = require('playwright');
const path = require('path');
const readline = require('readline');

const IMAGES_DIR = path.join(__dirname, 'images');
const DEFAULT_WORKSPACE = process.argv[2] || 'https://e2-demo-west.cloud.databricks.com';
const SCHEMA = 'sourabh_energy_workshop';

const SCREENSHOTS = [
  {
    name: '01-workshop-folder.png',
    url: `${DEFAULT_WORKSPACE}/#workspace/Users/sourabh.ghose@databricks.com/genie-code-energy-workshop`,
    description: 'Workshop notebooks folder',
  },
  {
    name: '03-catalog-tables.png',
    url: `${DEFAULT_WORKSPACE}/explore/data/main/${SCHEMA}`,
    description: 'Catalog Explorer - energy tables',
  },
  {
    name: '04-customers-sample.png',
    url: `${DEFAULT_WORKSPACE}/explore/data/main/${SCHEMA}/raw_customers`,
    description: 'raw_customers table details',
  },
  {
    name: '05-skills-folder.png',
    url: `${DEFAULT_WORKSPACE}/#workspace/Users/sourabh.ghose@databricks.com/.assistant/skills`,
    description: 'Agent Skills folder',
  },
];

function prompt(question) {
  const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
  return new Promise(resolve => rl.question(question, answer => { rl.close(); resolve(answer); }));
}

(async () => {
  console.log('\n=== Databricks Screenshot Capture ===\n');
  console.log(`Workspace: ${DEFAULT_WORKSPACE}`);
  console.log(`Output:    ${IMAGES_DIR}\n`);

  const browser = await chromium.launch({ headless: false, args: ['--window-size=1440,900'] });
  const context = await browser.newContext({ viewport: { width: 1440, height: 900 } });
  const page = await context.newPage();

  console.log('Opening workspace... If you see a login page, please sign in.\n');
  await page.goto(DEFAULT_WORKSPACE, { waitUntil: 'domcontentloaded', timeout: 30000 });
  await page.waitForTimeout(3000);

  const currentUrl = page.url();
  if (currentUrl.includes('login') || currentUrl.includes('okta') || currentUrl.includes('accounts.')) {
    console.log('Login page detected. Please sign in through the browser window.');
    await prompt('Press Enter after you have logged in and see the workspace... ');
    await page.waitForTimeout(3000);
  }

  for (const shot of SCREENSHOTS) {
    console.log(`Capturing: ${shot.description}...`);
    try {
      await page.goto(shot.url, { waitUntil: 'networkidle', timeout: 30000 });
    } catch {
      console.log('  (page still loading, waiting...)');
    }
    await page.waitForTimeout(6000);

    const filePath = path.join(IMAGES_DIR, shot.name);
    await page.screenshot({ path: filePath, fullPage: false });
    console.log(`  Saved: ${shot.name}`);
  }

  console.log('\n--- Optional: Genie Code pane screenshot ---');
  console.log('To capture the Genie Code pane:');
  console.log('1. Open a notebook (e.g., 01_energy_data_explorer)');
  console.log('2. Click the Genie Code icon to open the pane');
  console.log('3. Type a prompt like "/fix this join"');
  const doGenie = await prompt('Would you like to capture a Genie Code screenshot now? (y/n) ');

  if (doGenie.toLowerCase() === 'y') {
    console.log('Navigate to the notebook and open Genie Code.');
    await prompt('Press Enter when ready to capture... ');
    await page.screenshot({
      path: path.join(IMAGES_DIR, '02-genie-code-pane.png'),
      fullPage: false,
    });
    console.log('  Saved: 02-genie-code-pane.png');
  }

  await browser.close();
  console.log('\nAll screenshots captured! Images are in ./images/');
})();
