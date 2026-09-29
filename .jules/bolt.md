## 2026-09-16 - Pre-cache metadata and guard DOM writes in live search filters
**Learning:** Querying `dataset` attributes and unconditionally assigning `.hidden` or DOM properties across hundreds of cards on every input event introduces redundant layout/style calculations and string allocations (~151ms across 5,000 queries in benchmarks).
**Action:** Pre-compute lowercase search strings (`haystack`, `name`) into an array of card objects at initialization, and guard DOM property assignments with `if (card.element.hidden !== targetState)` to only mutate the DOM when the hidden state actually changes.

## 2026-09-17 - Limit GSAP stagger animations to visible above-the-fold nodes
**Learning:** Animating all 163 `.project-card` elements with GSAP stagger on page load creates 163 active tween objects running over 4.5 seconds on the main thread and keeps offscreen elements hidden in `opacity: 0` until their stagger turn.
**Action:** Scope `gsap.from` selectors for grid card entrances to above-the-fold items (`.project-card:nth-child(-n+12)`) to cut active tween instances by ~92% while ensuring offscreen cards remain visible immediately.
