## 2026-09-16 - Pre-cache metadata and guard DOM writes in live search filters
**Learning:** Querying `dataset` attributes and unconditionally assigning `.hidden` or DOM properties across hundreds of cards on every input event introduces redundant layout/style calculations and string allocations (~151ms across 5,000 queries in benchmarks).
**Action:** Pre-compute lowercase search strings (`haystack`, `name`) into an array of card objects at initialization, and guard DOM property assignments with `if (card.element.hidden !== targetState)` to only mutate the DOM when the hidden state actually changes.

## 2026-09-17 - CSS content-visibility and GPU layer promotion for SVG filter overlays
**Learning:** In pages with large grid structures (160+ project cards) and fixed full-screen SVG noise/grain overlays, scrolling and continuous GSAP animations trigger extensive main-thread layout and full-viewport GPU repaints due to inline SVG `feTurbulence` filter re-compositing.
**Action:** Use `content-visibility: auto; contain-intrinsic-size: 1px 250px;` on card items to defer layout/paint of off-screen DOM nodes, and isolate fixed SVG filter overlays onto dedicated GPU hardware layers using `will-change: transform; transform: translateZ(0);`.
