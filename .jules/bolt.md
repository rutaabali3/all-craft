## 2026-09-16 - Pre-cache metadata and guard DOM writes in live search filters
**Learning:** Querying `dataset` attributes and unconditionally assigning `.hidden` or DOM properties across hundreds of cards on every input event introduces redundant layout/style calculations and string allocations (~151ms across 5,000 queries in benchmarks).
**Action:** Pre-compute lowercase search strings (`haystack`, `name`) into an array of card objects at initialization, and guard DOM property assignments with `if (card.element.hidden !== targetState)` to only mutate the DOM when the hidden state actually changes.

## 2026-09-30 - Cache DOM queries outside high-frequency scroll event listeners
**Learning:** Executing DOM queries (`document.getElementById`, `document.querySelector`, `document.querySelectorAll`) inside high-frequency `scroll` event handlers introduces unnecessary DOM tree traversal and lookup overhead on every scroll frame (~8.9x slower in microbenchmarks over 50M calls).
**Action:** Store references to DOM elements (`#mainNav`, `.hero-background`, `.floating-element`) outside event listeners or during initialization so that event listeners only access pre-cached references.
