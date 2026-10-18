const fs = require('fs');
const jsdom = require("jsdom");
const { JSDOM } = jsdom;

const html = fs.readFileSync('projects/modeling-clay-craft/index.html', 'utf-8');
const script = fs.readFileSync('projects/modeling-clay-craft/script.js', 'utf-8');

const dom = new JSDOM(html, { runScripts: "dangerously" });

// Mock IntersectionObserver
dom.window.IntersectionObserver = class IntersectionObserver {
    observe() {}
    unobserve() {}
    disconnect() {}
};

// Run the script to attach listeners
const scriptEl = dom.window.document.createElement("script");
scriptEl.textContent = script;
dom.window.document.body.appendChild(scriptEl);

const buttons = dom.window.document.querySelectorAll('.pricing-card .btn');

// Warm up
for (let i = 0; i < 1000; i++) {
    buttons[i % buttons.length].click();
}

const startTime = process.hrtime.bigint();
const iterations = 10000;
for (let i = 0; i < iterations; i++) {
    // Click random button
    buttons[i % buttons.length].click();
}
const endTime = process.hrtime.bigint();
const durationMs = Number(endTime - startTime) / 1e6;

console.log(`Duration for ${iterations} clicks: ${durationMs} ms`);
