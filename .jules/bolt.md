## 2026-09-16 - Pre-cache metadata and guard DOM writes in live search filters
**Learning:** Querying `dataset` attributes and unconditionally assigning `.hidden` or DOM properties across hundreds of cards on every input event introduces redundant layout/style calculations and string allocations (~151ms across 5,000 queries in benchmarks).
**Action:** Pre-compute lowercase search strings (`haystack`, `name`) into an array of card objects at initialization, and guard DOM property assignments with `if (card.element.hidden !== targetState)` to only mutate the DOM when the hidden state actually changes.

## 2026-09-17 - Frame coalescing and search state memoization in root index filter
**Learning:** Live search filtering bound directly to `input` events executes synchronous card iterations on every keypress, including modifier keys and duplicate state triggers, causing main-thread stutter on large project lists.
**Action:** Schedule DOM filter updates via `requestAnimationFrame` to batch rapid typing events into single frame updates, short-circuit sub-string searches, and return early when `term` and `activeFilter` have not changed.
