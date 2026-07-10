import { chromium } from "playwright";
import fs from "node:fs";

const shotsDir = "./screenshots";
fs.mkdirSync(shotsDir, { recursive: true });

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1400, height: 900 } });

const errors = [];
page.on("console", (msg) => {
  if (msg.type() === "error") errors.push(msg.text());
});
page.on("pageerror", (err) => errors.push(String(err)));

async function shot(name) {
  await page.screenshot({ path: `${shotsDir}/${name}.png`, fullPage: true });
  console.log(`Saved ${shotsDir}/${name}.png`);
}

console.log("Navigating to login page...");
await page.goto("http://localhost:5174/login", { waitUntil: "networkidle" });
await shot("01_login");

await page.fill('input#email', "analyst@acme.com");
await page.fill('input#password', "Password123");
await shot("02_login_filled");

await Promise.all([
  page.waitForURL("http://localhost:5174/", { timeout: 15000 }),
  page.click('button[type="submit"]'),
]);
await page.waitForSelector("text=Dashboard", { timeout: 15000 });
await shot("03_dashboard");

console.log("Navigating to Documents...");
await page.click('a:has-text("Documents")');
await page.waitForSelector("text=Your Documents");
await shot("04_documents");

console.log("Navigating to Chat...");
await page.click('a:has-text("Chat")');
await page.waitForSelector('button:has-text("New Conversation")');
await page.click('button:has-text("New Conversation")');
await page.waitForTimeout(1000);
await shot("05_chat_empty");

const textarea = page.locator("textarea");
await textarea.fill("What is our remote work policy?");
await shot("06_chat_message_typed");

await page.click('button:has-text("Send")');
await page.waitForTimeout(4000);
await shot("07_chat_response");

console.log("Navigating to Conflicts...");
await page.click('a:has-text("Conflicts")');
await page.waitForSelector("text=Identified Conflicts");
await shot("08_conflicts");

console.log("Navigating to Recommendations...");
await page.click('a:has-text("Recommendations")');
await page.waitForSelector("text=AI Recommendations");
await shot("09_recommendations");

console.log("Console errors captured:", errors.length ? errors : "none");
fs.writeFileSync(`${shotsDir}/console_errors.json`, JSON.stringify(errors, null, 2));

await browser.close();
console.log("Done.");
