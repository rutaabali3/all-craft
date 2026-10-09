const test = require('node:test');
const assert = require('node:assert');

test('search filter state caching and frame scheduling logic', () => {
  let applyCalls = 0;
  let lastTerm = null;
  let lastFilter = null;
  let activeFilter = 'all';
  let searchValue = '';

  const cardData = [
    { name: 'paper craft', category: 'paper', haystack: 'paper craft paper', hidden: false, el: { hidden: false } },
    { name: 'pen stand', category: 'pen', haystack: 'pen stand pen', hidden: false, el: { hidden: false } }
  ];

  const applyFilters = () => {
    const term = searchValue.trim().toLowerCase();
    if (term === lastTerm && activeFilter === lastFilter) {
      return;
    }
    lastTerm = term;
    lastFilter = activeFilter;
    applyCalls++;

    for (let i = 0; i < cardData.length; i++) {
      const card = cardData[i];
      const matchesTerm = !term || card.name.includes(term);
      const matchesFilter = activeFilter === 'all' || card.haystack.includes(activeFilter);
      const show = matchesTerm && matchesFilter;
      const hide = !show;

      if (card.hidden !== hide) {
        card.el.hidden = hide;
        card.hidden = hide;
      }
    }
  };

  // Test 1: First call applies filters
  searchValue = 'paper';
  applyFilters();
  assert.strictEqual(applyCalls, 1);
  assert.strictEqual(cardData[0].hidden, false);
  assert.strictEqual(cardData[1].hidden, true);

  // Test 2: Identical inputs skip filter loop
  applyFilters();
  assert.strictEqual(applyCalls, 1, 'Duplicate applyFilters should be a no-op');

  // Test 3: Changing search term re-evaluates
  searchValue = 'pen';
  applyFilters();
  assert.strictEqual(applyCalls, 2);
  assert.strictEqual(cardData[0].hidden, true);
  assert.strictEqual(cardData[1].hidden, false);

  // Test 4: Frame coalescing logic simulation
  let rafPending = false;
  let rafCallback = null;
  const mockRaf = (cb) => {
    rafCallback = cb;
    return 1;
  };

  const scheduleApplyFilters = () => {
    if (rafPending) return;
    rafPending = true;
    mockRaf(() => {
      rafPending = false;
      applyFilters();
    });
  };

  searchValue = 'p';
  scheduleApplyFilters();
  scheduleApplyFilters(); // Duplicate trigger in same frame
  scheduleApplyFilters();

  assert.strictEqual(applyCalls, 2, 'Should not execute until rAF fires');
  rafCallback();
  assert.strictEqual(applyCalls, 3, 'Should execute once for the coalesced frame');
});
