## 2026-09-16 - Pre-cache metadata and guard DOM writes in live search filters
**Learning:** Querying `dataset` attributes and unconditionally assigning `.hidden` or DOM properties across hundreds of cards on every input event introduces redundant layout/style calculations and string allocations (~151ms across 5,000 queries in benchmarks).
**Action:** Pre-compute lowercase search strings (`haystack`, `name`) into an array of card objects at initialization, and guard DOM property assignments with `if (card.element.hidden !== targetState)` to only mutate the DOM when the hidden state actually changes.

## 2026-09-17 - Debounce search input with rAF and delegate filter click events
**Learning:** Attaching event listeners to individual filter buttons and synchronously running card-filtering logic on every keystroke causes frame drops during rapid typing and extra memory overhead for event handlers.
**Action:** Use `requestAnimationFrame` debouncing for input handlers and single-container event delegation with active-state early returns for category filter buttons.
