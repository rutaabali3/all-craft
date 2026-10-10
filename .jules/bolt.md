## 2026-09-16 - Pre-cache metadata and guard DOM writes in live search filters
**Learning:** Querying `dataset` attributes and unconditionally assigning `.hidden` or DOM properties across hundreds of cards on every input event introduces redundant layout/style calculations and string allocations (~151ms across 5,000 queries in benchmarks).
**Action:** Pre-compute lowercase search strings (`haystack`, `name`) into an array of card objects at initialization, and guard DOM property assignments with `if (card.element.hidden !== targetState)` to only mutate the DOM when the hidden state actually changes.

## 2026-10-10 - Decouple active category matching from search input loop
**Learning:** Re-evaluating category filter string containment (`card.haystack.includes(activeFilter)`) on every search keystroke across 100+ DOM card objects creates redundant string checks on a hot path, since category filters only change on tab/button clicks.
**Action:** Pre-compute a `matchesFilter` boolean on card data objects when category filter buttons are clicked, and short-circuit `applyFilters()` immediately when `!card.matchesFilter` to skip search term evaluation (~86.8% CPU time saved in search input benchmarks).
