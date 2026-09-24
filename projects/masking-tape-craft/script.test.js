const { test } = require('node:test');
const assert = require('node:assert/strict');
const { animateCounter } = require('./script.js');

class MockElement {
    constructor(dataset = {}) {
        this.textContent = '';
        this.dataset = dataset;
    }
}

test('animateCounter increments element textContent over time and reaches target with dataset.suffix', (t) => {
    t.mock.timers.enable();
    const element = new MockElement({ suffix: '+' });

    animateCounter(element, 100, 160);

    // Initial state before timer fires
    assert.strictEqual(element.textContent, '');

    // Advance 1 tick (16ms)
    t.mock.timers.tick(16);
    // target / (160 / 16) = 10 per tick. At 16ms: Math.floor(10) + '+' = '10+'
    assert.strictEqual(element.textContent, '10+');

    // Advance halfway (80ms total)
    t.mock.timers.tick(64);
    assert.strictEqual(element.textContent, '50+');

    // Advance to end (160ms total)
    t.mock.timers.tick(80);
    assert.strictEqual(element.textContent, '100+');

    // Further ticks should not change value since interval was cleared
    t.mock.timers.tick(160);
    assert.strictEqual(element.textContent, '100+');
});

test('animateCounter works without dataset.suffix', (t) => {
    t.mock.timers.enable();
    const element = new MockElement();

    animateCounter(element, 50, 100);

    // Advance to end
    t.mock.timers.tick(200);
    assert.strictEqual(element.textContent, '50');
});

test('animateCounter uses default duration of 2000ms', (t) => {
    t.mock.timers.enable();
    const element = new MockElement({ suffix: '%' });

    animateCounter(element, 1000);

    // After 1000ms (halfway)
    t.mock.timers.tick(1000);
    assert.ok(parseInt(element.textContent) >= 450 && parseInt(element.textContent) <= 550);

    // After 2000ms (completed)
    t.mock.timers.tick(1000);
    assert.strictEqual(element.textContent, '1000%');
});

test('animateCounter handles target equal to 0', (t) => {
    t.mock.timers.enable();
    const element = new MockElement({ suffix: 'k' });

    animateCounter(element, 0, 500);

    t.mock.timers.tick(16);
    assert.strictEqual(element.textContent, '0k');
});
