const fs = require('fs');

const scriptContent = fs.readFileSync('projects/modeling-clay-craft/script.js', 'utf-8');

// Minimal DOM mock without JSDOM
let querySelectorAllCalls = 0;
let closestCalls = 0;
let querySelectorCalls = 0;

class DOMElement {
    constructor(className = '') {
        this.className = className;
        this.classList = {
            classes: new Set(className.split(' ').filter(Boolean)),
            add: (c) => this.classList.classes.add(c),
            remove: (...args) => args.forEach(c => this.classList.classes.delete(c)),
            contains: (c) => this.classList.classes.has(c)
        };
        this.innerHTML = 'btn';
        this.style = {};
        this.listeners = {};
        this.parentElement = this;
    }

    addEventListener(type, cb) {
        if (!this.listeners[type]) this.listeners[type] = [];
        this.listeners[type].push(cb);
    }

    closest(selector) {
        closestCalls++;
        return new DOMElement('pricing-card');
    }

    querySelector(selector) {
        querySelectorCalls++;
        return new DOMElement();
    }

    getBoundingClientRect() {
        return { left: 0, top: 0, width: 100, height: 100 };
    }
}

const mockCards = [new DOMElement('pricing-card'), new DOMElement('pricing-card')];
const mockBtns = [new DOMElement('btn'), new DOMElement('btn')];

global.document = {
    querySelectorAll: (selector) => {
        querySelectorAllCalls++;
        if (selector === '.pricing-card .btn') return mockBtns;
        if (selector === '.pricing-card') return mockCards;
        return [new DOMElement()];
    },
    querySelector: () => new DOMElement(),
    createElement: () => new DOMElement(),
    head: { appendChild: () => {} },
    body: { appendChild: () => {} },
    addEventListener: () => {}
};

global.window = {
    addEventListener: () => {},
    performance: performance,
    pageYOffset: 0,
    innerHeight: 1000
};

global.IntersectionObserver = class {
    observe() {}
};

global.FormData = class {
    constructor() {}
};

// Evaluate the script to bind the listeners
eval(scriptContent);

const ITERATIONS = 100000;
const eventMock = { preventDefault: () => {} };

// Run baseline
const start = performance.now();
for (let i = 0; i < ITERATIONS; i++) {
    mockBtns[0].listeners['click'].forEach(cb => cb.call(mockBtns[0], eventMock));
}
const end = performance.now();

console.log(`Baseline Execution Time for ${ITERATIONS} clicks: ${(end - start).toFixed(2)} ms`);
console.log(`querySelectorAll calls: ${querySelectorAllCalls}`);
