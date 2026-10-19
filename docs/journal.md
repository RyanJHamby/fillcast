# fillcast: engineering journal

Dated notes on what I tried, what happened, and why I made each call, including
the dead ends. Entries are appended with `pow log` and `pow run`, so dates match
commit history. Raw outputs for any number quoted in the README live in
[`results/`](../results/).

## 2026-10-18 20:56 EDT (at b1497ce)

Bootstrapped repo as spec-only. Decisions: fillcast is its own repo (not an engine extension); generic engine upgrades land in order-book-engine as tagged releases and fillcast pins one tag as engine/; fillcast-specific code lives only here; spec to be published with empty results so signed timestamps pre-register hypotheses. No code written yet; SPEC.md and ADR 0001 deferred.
