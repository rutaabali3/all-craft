## 2026-09-30 - Cache bounding rect and throttle mousemove transform updates via requestAnimationFrame
**Learning:** Calling `getBoundingClientRect()` on every `mousemove` event triggers synchronous layout calculations on every cursor tick, causing forced reflows and high CPU usage.
**Action:** Cache element bounding box on `mouseenter` (resets on `mouseleave`) and wrap `transform` DOM updates in `requestAnimationFrame` with a pending flag to align style updates with frame renders and avoid layout thrashing.

## 2026-09-16 - Pre-cache metadata and guard DOM writes in live search filters
**Learning:** Querying `dataset` attributes and unconditionally assigning `.hidden` or DOM properties across hundreds of cards on every input event introduces redundant layout/style calculations and string allocations (~151ms across 5,000 queries in benchmarks).
**Action:** Pre-compute lowercase search strings (`haystack`, `name`) into an array of card objects at initialization, and guard DOM property assignments with `if (card.element.hidden !== targetState)` to only mutate the DOM when the hidden state actually changes.
