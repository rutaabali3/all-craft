const { JSDOM } = require("jsdom");
const { performance } = require("perf_hooks");

let html = "";
for (let i = 0; i < 1000; i++) {
  html += `<div class="pricing-card"><button class="btn">Click ${i}</button></div>`;
}

const dom = new JSDOM(html);
const document = dom.window.document;
const window = dom.window;

// Unoptimized
function setupUnoptimized() {
    const btns = document.querySelectorAll('.pricing-card .btn');
    btns.forEach(btn => {
        // remove existing listeners if any by just storing function
        btn.onclick = function(e) {
            e.preventDefault();
            document.querySelectorAll('.pricing-card').forEach(card => {
                card.classList.remove('selected');
            });
            this.closest('.pricing-card').classList.add('selected');
        };
    });
    return btns;
}

// Optimized
function setupOptimized() {
    const pricingCards = document.querySelectorAll('.pricing-card');
    const btns = document.querySelectorAll('.pricing-card .btn');
    btns.forEach(btn => {
        btn.onclick = function(e) {
            e.preventDefault();
            pricingCards.forEach(card => {
                card.classList.remove('selected');
            });
            this.closest('.pricing-card').classList.add('selected');
        };
    });
    return btns;
}

function runBenchmark(name, setupFn) {
    const btns = setupFn();
    const event = new dom.window.Event('click', { bubbles: true });

    // Warmup
    for (let i = 0; i < 50; i++) {
        btns[i].onclick(event);
    }

    const start = performance.now();
    for (let i = 0; i < 1000; i++) {
        btns[i].onclick(event);
    }
    const end = performance.now();

    console.log(`${name}: ${end - start} ms`);
}

runBenchmark("Unoptimized", setupUnoptimized);
runBenchmark("Optimized", setupOptimized);
