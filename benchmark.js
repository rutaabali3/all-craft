const fs = require('fs');
const jsdom = require("jsdom");
const { JSDOM } = jsdom;

const html = fs.readFileSync('projects/tracing-paper-craft/index.html', 'utf8');
const script = fs.readFileSync('projects/tracing-paper-craft/script.js', 'utf8');

function runBenchmark(scriptContent) {
  const dom = new JSDOM(html, { runScripts: "outside-only" });

  // mock requestAnimationFrame and other things if needed
  dom.window.requestAnimationFrame = (cb) => setTimeout(cb, 0);

  // mock IntersectionObserver
  dom.window.IntersectionObserver = class IntersectionObserver {
    constructor(callback, options) {}
    observe() {}
    unobserve() {}
    disconnect() {}
  };

  // mock FormData
  dom.window.FormData = class FormData {
    constructor() {}
  };

  // mock performance
  if (!dom.window.performance) {
    dom.window.performance = {};
  }
  dom.window.performance.getEntriesByType = () => [{loadEventEnd: 0, fetchStart: 0}];

  // load script
  dom.window.eval(scriptContent);

  const buttons = dom.window.document.querySelectorAll('.pricing-card .btn');
  if (buttons.length === 0) {
    console.log("No buttons found");
    return;
  }

  const start = process.hrtime.bigint();

  // simulate 1000 clicks on the first button
  const clickEvent = new dom.window.MouseEvent('click', {
    view: dom.window,
    bubbles: true,
    cancelable: true
  });

  for (let i = 0; i < 10000; i++) {
    buttons[0].dispatchEvent(clickEvent);
  }

  const end = process.hrtime.bigint();
  const timeTaken = Number(end - start) / 1e6; // in milliseconds

  console.log(`Time taken for 10000 clicks: ${timeTaken.toFixed(2)}ms`);
}

console.log("Running baseline...");
runBenchmark(script);
