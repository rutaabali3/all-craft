const { JSDOM } = require('jsdom');
const { performance } = require('perf_hooks');

const dom = new JSDOM(`
<!DOCTYPE html>
<html>
<body>
  ${Array(100).fill().map(() => `
    <div class="pricing-card">
      <button class="btn">Select</button>
    </div>
  `).join('')}
</body>
</html>
`);

const { document } = dom.window;

function testOld() {
    let sum = 0;
    const start = performance.now();
    for (let i = 0; i < 10000; i++) {
        const cards = document.querySelectorAll('.pricing-card');
        for (let j = 0; j < cards.length; j++) {
            cards[j].classList.remove('selected');
        }
    }
    const end = performance.now();
    return end - start;
}

function testNew() {
    const cards = document.querySelectorAll('.pricing-card');
    let sum = 0;
    const start = performance.now();
    for (let i = 0; i < 10000; i++) {
        for (let j = 0; j < cards.length; j++) {
            cards[j].classList.remove('selected');
        }
    }
    const end = performance.now();
    return end - start;
}

const oldTime = testOld();
const newTime = testNew();

console.log(`Old time: ${oldTime.toFixed(2)}ms`);
console.log(`New time: ${newTime.toFixed(2)}ms`);
console.log(`Improvement: ${((oldTime - newTime) / oldTime * 100).toFixed(2)}%`);
