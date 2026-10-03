## 2026-09-16 - Pre-cache metadata and guard DOM writes in live search filters
**Learning:** Querying `dataset` attributes and unconditionally assigning `.hidden` or DOM properties across hundreds of cards on every input event introduces redundant layout/style calculations and string allocations (~151ms across 5,000 queries in benchmarks).
**Action:** Pre-compute lowercase search strings (`haystack`, `name`) into an array of card objects at initialization, and guard DOM property assignments with `if (card.element.hidden !== targetState)` to only mutate the DOM when the hidden state actually changes.

## 2026-09-17 - Eliminate forced layout thrashing in mousemove and scroll handlers
**Learning:** Calling `getBoundingClientRect()` inside high-frequency `mousemove` events forces synchronous browser layout reflows on every mouse frame (~239ms for 500 events). Multiple unthrottled `scroll` listeners execute unbatched style mutations and DOM queries.
**Action:** Cache element bounding rects on `mouseenter` (re-calculating only when needed) and throttle DOM style updates for mouse move and scroll events using `requestAnimationFrame` with `{ passive: true }` event listeners. Consolidate separate scroll listeners into a single passive handler.
