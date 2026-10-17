## 2026-09-16 - Pre-cache metadata and guard DOM writes in live search filters
**Learning:** Querying `dataset` attributes and unconditionally assigning `.hidden` or DOM properties across hundreds of cards on every input event introduces redundant layout/style calculations and string allocations (~151ms across 5,000 queries in benchmarks).
**Action:** Pre-compute lowercase search strings (`haystack`, `name`) into an array of card objects at initialization, and guard DOM property assignments with `if (card.element.hidden !== targetState)` to only mutate the DOM when the hidden state actually changes.

## 2026-10-17 - Throttled passive scroll handler and pre-cached DOM elements across static project pages
**Learning:** Having multiple unthrottled `window.addEventListener('scroll')` listeners per subpage with redundant `document.querySelector` and DOM style assignments causes style recalcs and layout thrashing on every scroll pixel tick (489 total unthrottled listeners across 163 pages).
**Action:** Consolidate scroll effects into a single passive listener throttled via `requestAnimationFrame`, pre-cache target DOM element references (`navbar`, `heroBackground`, `floatingElements`), and guard class toggles (`navbar.classList.toggle('scrolled', shouldBeScrolled)` with `isScrolled` check).
