## 2026-09-16 - Pre-cache metadata and guard DOM writes in live search filters
**Learning:** Querying `dataset` attributes and unconditionally assigning `.hidden` or DOM properties across hundreds of cards on every input event introduces redundant layout/style calculations and string allocations (~151ms across 5,000 queries in benchmarks).
**Action:** Pre-compute lowercase search strings (`haystack`, `name`) into an array of card objects at initialization, and guard DOM property assignments with `if (card.element.hidden !== targetState)` to only mutate the DOM when the hidden state actually changes.

## 2026-09-16 - Pre-compile regexes and fast-path substring check for batch HTML rewiring
**Learning:** Re-compiling dynamic regexes inside file-processing loops across hundreds of HTML files without checking for substring presence leads to significant execution overhead (~221ms for 10 runs across 163 files).
**Action:** Pre-compile `re.Pattern` objects prior to looping through files and check `if 'href="#"' not in text:` to immediately skip non-matching files (~18ms for 10 runs, an ~11.8x speedup).
