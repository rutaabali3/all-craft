// Benchmark to measure mousemove performance for card hover effects
const { performance } = require('perf_hooks');

function createMockElement() {
    let getBoundingClientRectCalls = 0;
    const style = { transform: '' };
    const listeners = {};

    const element = {
        style,
        getBoundingClientRectCalls: () => getBoundingClientRectCalls,
        resetCalls: () => { getBoundingClientRectCalls = 0; },
        getBoundingClientRect() {
            getBoundingClientRectCalls++;
            return { left: 100, top: 100, width: 300, height: 200 };
        },
        addEventListener(event, fn) {
            if (!listeners[event]) listeners[event] = [];
            listeners[event].push(fn);
        },
        dispatchEvent(event, payload) {
            if (listeners[event]) {
                listeners[event].forEach(fn => fn.call(element, payload));
            }
        }
    };
    return element;
}

// Global mock DOM environment
global.document = {
    querySelectorAll: () => [],
    addEventListener: () => {},
    createElement: () => ({ style: {}, appendChild: () => {} }),
    head: { appendChild: () => {} },
    body: { appendChild: () => {} }
};
global.window = {
    addEventListener: () => {},
    scrollTo: () => {},
    requestAnimationFrame: (cb) => { cb(); return 1; },
    cancelAnimationFrame: () => {}
};
global.IntersectionObserver = class { observe() {} unobserve() {} };

function setupUnoptimizedHandlers(card) {
    card.addEventListener('mousemove', function(e) {
        const rect = this.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;

        const centerX = rect.width / 2;
        const centerY = rect.height / 2;

        const rotateX = (y - centerY) / 10;
        const rotateY = (centerX - x) / 10;

        this.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateZ(10px)`;
    });
}

function setupOptimizedHandlers(card) {
    let rect = null;
    let rafId = null;

    card.addEventListener('mouseenter', function() {
        rect = this.getBoundingClientRect();
    });

    card.addEventListener('mousemove', function(e) {
        if (!rect) {
            rect = this.getBoundingClientRect();
        }
        const clientX = e.clientX;
        const clientY = e.clientY;

        if (rafId) return;

        rafId = window.requestAnimationFrame(() => {
            rafId = null;
            const x = clientX - rect.left;
            const y = clientY - rect.top;

            const centerX = rect.width / 2;
            const centerY = rect.height / 2;

            const rotateX = (y - centerY) / 10;
            const rotateY = (centerX - x) / 10;

            card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateZ(10px)`;
        });
    });

    card.addEventListener('mouseleave', function() {
        if (rafId) {
            window.cancelAnimationFrame(rafId);
            rafId = null;
        }
        rect = null;
        this.style.transform = '';
    });
}

function runBenchmark() {
    const NUM_MOVES = 200000;

    // Unoptimized
    const card1 = createMockElement();
    setupUnoptimizedHandlers(card1);

    const startUnopt = performance.now();
    card1.dispatchEvent('mouseenter', {});
    for (let i = 0; i < NUM_MOVES; i++) {
        card1.dispatchEvent('mousemove', { clientX: 150 + (i % 50), clientY: 150 + (i % 50) });
    }
    card1.dispatchEvent('mouseleave', {});
    const durationUnopt = performance.now() - startUnopt;
    const callsUnopt = card1.getBoundingClientRectCalls();

    // Optimized
    const card2 = createMockElement();
    setupOptimizedHandlers(card2);

    const startOpt = performance.now();
    card2.dispatchEvent('mouseenter', {});
    for (let i = 0; i < NUM_MOVES; i++) {
        card2.dispatchEvent('mousemove', { clientX: 150 + (i % 50), clientY: 150 + (i % 50) });
    }
    card2.dispatchEvent('mouseleave', {});
    const durationOpt = performance.now() - startOpt;
    const callsOpt = card2.getBoundingClientRectCalls();

    console.log(`Unoptimized: ${durationUnopt.toFixed(2)} ms | getBoundingClientRect calls: ${callsUnopt}`);
    console.log(`Optimized:   ${durationOpt.toFixed(2)} ms | getBoundingClientRect calls: ${callsOpt}`);
    console.log(`Call reduction: ${((1 - callsOpt / callsUnopt) * 100).toFixed(2)}%`);
    console.log(`Speedup factor: ${(durationUnopt / durationOpt).toFixed(2)}x`);
}

runBenchmark();
