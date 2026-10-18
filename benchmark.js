const { JSDOM } = require('jsdom');
const fs = require('fs');

const html = fs.readFileSync('projects/files-craft/index.html', 'utf8');
const dom = new JSDOM(html);
const document = dom.window.document;

// Original function implementation
function original() {
    const cards = document.querySelectorAll('.pricing-card');
    cards.forEach(card => {
        card.classList.remove('selected');
    });
}

// Optimized function implementation
function optimized(cards) {
    cards.forEach(card => {
        card.classList.remove('selected');
    });
}

const ITERATIONS = 100000;
const cards = document.querySelectorAll('.pricing-card');

const startOriginal = process.hrtime.bigint();
for (let i = 0; i < ITERATIONS; i++) {
    original();
}
const endOriginal = process.hrtime.bigint();

const startOptimized = process.hrtime.bigint();
for (let i = 0; i < ITERATIONS; i++) {
    optimized(cards);
}
const endOptimized = process.hrtime.bigint();

console.log(`Original: ${Number(endOriginal - startOriginal) / 1000000} ms`);
console.log(`Optimized: ${Number(endOptimized - startOptimized) / 1000000} ms`);
