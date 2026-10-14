## 2026-09-16 - Pre-cache metadata and guard DOM writes in live search filters
**Learning:** Querying `dataset` attributes and unconditionally assigning `.hidden` or DOM properties across hundreds of cards on every input event introduces redundant layout/style calculations and string allocations (~151ms across 5,000 queries in benchmarks).
**Action:** Pre-compute lowercase search strings (`haystack`, `name`) into an array of card objects at initialization, and guard DOM property assignments with `if (card.element.hidden !== targetState)` to only mutate the DOM when the hidden state actually changes.

## 2026-09-17 - Defer off-screen asset loading in static craft project templates
**Learning:** Multi-image static catalog pages with 6 PNG images per page download all media upfront, wasting bandwidth and delaying rendering. Adding `loading="lazy"` and `decoding="async"` to secondary catalog images defers 5/6 image downloads (~83% initial request reduction per page) without layout shifts or initial paint delays.
**Action:** Apply `loading="lazy" decoding="async"` to non-hero images across generated static template catalogs, keeping `decoding="async"` on above-the-fold hero images.
