# fillcast: engineering journal

Dated notes on what I tried, what happened, and why I made each call, including
the dead ends. Entries are appended with `pow log` and `pow run`, so dates match
commit history. Raw outputs for any number quoted in the README live in
[`results/`](../results/).

## 2026-10-18 20:56 EDT (at b1497ce)

Bootstrapped repo as spec-only. Decisions: fillcast is its own repo (not an engine extension); generic engine upgrades land in order-book-engine as tagged releases and fillcast pins one tag as engine/; fillcast-specific code lives only here; spec to be published with empty results so signed timestamps pre-register hypotheses. No code written yet; SPEC.md and ADR 0001 deferred.

## 2026-10-18 21:02 EDT (at 796a78a)

Wrote SPEC.md and ADR 0001. Adversarial subagent review found: H4/H2/H3/H6/H9 pass conditions and falsifiers were not exact complements; thresholds and primary cell were not fixed in a verifiable way; unlabeled quantitative claims. Fixed in SPEC: added a pre-registration rule (signed commit fixes primary cell, thresholds, planted-leak sets before each run), Holm correction, labels. Open: DESIGN.md s9.3 says the TSE study covered 'two instruments over 18 days' but arXiv:2609.13597 abstract says seven months of 2025 data (reviewer says 18 days is the held-out set, unverified by me); DESIGN left as-is pending decision. References were checked at abstract/Crossref level only. Name check: PyPI/crates.io/npm free; GitHub user FillCast exists (empty, 2022).
