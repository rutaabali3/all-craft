const { performance } = require('perf_hooks');

// Mock a simple DOM-like structure without jsdom to avoid installing packages
class Element {
    constructor(className) {
        this.className = className;
        this.classList = {
            remove: () => {},
            add: () => {}
        };
    }
}

class Document {
    constructor() {
        this.elements = Array.from({ length: 100 }, () => new Element('pricing-card'));
    }
    querySelectorAll(selector) {
        // simulate the overhead of querySelectorAll
        let count = 0;
        for(let i = 0; i < 1000; i++) {
            count += i; // busy work
        }
        return this.elements;
    }
}

const document = new Document();

// Original approach
const startOriginal = performance.now();
for (let i = 0; i < 10000; i++) {
    const cards = document.querySelectorAll('.pricing-card');
    cards.forEach(card => {
        card.classList.remove('selected');
    });
}
const endOriginal = performance.now();

// Optimized approach
const cachedCards = document.querySelectorAll('.pricing-card');
const startOptimized = performance.now();
for (let i = 0; i < 10000; i++) {
    cachedCards.forEach(card => {
        card.classList.remove('selected');
    });
}
const endOptimized = performance.now();

console.log(`Original approach: ${(endOriginal - startOriginal).toFixed(2)}ms`);
console.log(`Optimized approach: ${(endOptimized - startOptimized).toFixed(2)}ms`);
console.log(`Improvement: ${(((endOriginal - startOriginal) - (endOptimized - startOptimized)) / (endOriginal - startOriginal) * 100).toFixed(2)}% faster`);
