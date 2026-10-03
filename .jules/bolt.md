## 2026-09-16 - Pre-cache metadata and guard DOM writes in live search filters
**Learning:** Querying `dataset` attributes and unconditionally assigning `.hidden` or DOM properties across hundreds of cards on every input event introduces redundant layout/style calculations and string allocations (~151ms across 5,000 queries in benchmarks).
**Action:** Pre-compute lowercase search strings (`haystack`, `name`) into an array of card objects at initialization, and guard DOM property assignments with `if (card.element.hidden !== targetState)` to only mutate the DOM when the hidden state actually changes.

## 2026-10-01 - Replace dynamic re.sub with static tuple replacement and presence guard in link rewirers
**Learning:** Calling `re.sub` inside loops across hundreds of HTML files compiles regex patterns on the fly and incurs pattern parsing overhead (~200ms across 163 files with 3,423 `re.sub` calls). For fixed string replacements, `str.replace` with pre-constructed `(old, new)` tuple pairs and a fast substring presence guard (`if '<a href="#"' in text:`) runs in ~4ms (~48x speedup).
**Action:** When performing bulk static HTML text replacements, pre-construct replacement tuples outside loops, check string presence before looping through replacement pairs, and use `str.replace` instead of `re.sub`.
