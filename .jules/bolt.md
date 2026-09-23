## 2026-09-16 - Pre-cache metadata and guard DOM writes in live search filters
**Learning:** Querying `dataset` attributes and unconditionally assigning `.hidden` or DOM properties across hundreds of cards on every input event introduces redundant layout/style calculations and string allocations (~151ms across 5,000 queries in benchmarks).
**Action:** Pre-compute lowercase search strings (`haystack`, `name`) into an array of card objects at initialization, and guard DOM property assignments with `if (card.element.hidden !== targetState)` to only mutate the DOM when the hidden state actually changes.

## 2026-09-23 - Offscreen rendering containment with content-visibility: auto
**Learning:** Rendering large card grids (100+ items) causes significant layout reflow overhead (~19.5ms) whenever container styling or filtering state triggers style recalculations.
**Action:** Apply `content-visibility: auto; contain-intrinsic-size: auto 250px;` to `.project-card` or similar repeating grid items. This defers rendering of offscreen elements, reducing style recalculation and reflow execution time by ~88-94% without breaking search, filtering, or page scroll geometry.
