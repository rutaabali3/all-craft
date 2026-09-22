## 2026-09-16 - Pre-cache metadata and guard DOM writes in live search filters
**Learning:** Querying `dataset` attributes and unconditionally assigning `.hidden` or DOM properties across hundreds of cards on every input event introduces redundant layout/style calculations and string allocations (~151ms across 5,000 queries in benchmarks).
**Action:** Pre-compute lowercase search strings (`haystack`, `name`) into an array of card objects at initialization, and guard DOM property assignments with `if (card.element.hidden !== targetState)` to only mutate the DOM when the hidden state actually changes.

## 2026-09-17 - Avoid animating off-screen DOM elements in large staggers
**Learning:** Targetting all 163 `.project-card` elements in GSAP initial stagger animations created 163 concurrent GSAP tweens on page load, running for over 4.5 seconds and keeping off-screen cards transparent (`opacity: 0`).
**Action:** Restrict entrance stagger animations to top-of-fold items (`:nth-child(-n+12)`) to keep initial animation active duration under 0.85s while allowing off-screen elements to render immediately with CSS `content-visibility: auto`.
