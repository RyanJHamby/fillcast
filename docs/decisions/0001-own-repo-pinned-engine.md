# 0001. Fillcast is its own repo with a pinned engine

- Status: accepted
- Date: 2026-10-18
- Deciders: Ryan Hamby

## Context

Fillcast's substrate is the author's order book engine
([order-book-engine](https://github.com/RyanJHamby/order-book-engine), C++20,
price-time matching, SPSC ingestion). `DESIGN.md` §4.5 lists engine changes the
project needs: fixed-point tick prices, a flat price ladder, and add/cancel/modify
with priority rules. Those changes are useful to any user of the engine. Fillcast
also needs components that are meaningless outside it: shadow-order labeler,
journal, feature kernel, models.

Two further constraints apply. The spec is to be published with empty results so
that signed commit timestamps pre-register the hypotheses (`DESIGN.md` §9.1). And
the engine has its own published benchmark claims, with open items, which must not
be silently changed by Fillcast work (`DESIGN.md` §17).

## Decision

1. Fillcast is its own repository, not an extension of the engine repo.
2. Generic engine upgrades (fixed-point ticks, flat ladder, cancel/modify) land in
   order-book-engine and ship as tagged releases.
3. Fillcast pins exactly one engine tag as `engine/`, as a git submodule or subtree.
   Moving the pin is a deliberate, signed commit with a journal entry.
4. Fillcast-specific code (shadow orders, journal, features, models) lives only in
   this repo, never in the engine.
5. The spec is published with empty results. Results enter only from captured runs
   in `results/`, with hardware named.

## Consequences

- The engine stays general-purpose and its history and benchmark claims stay its own.
- Fillcast results are reproducible against a named engine tag.
- Cross-repo changes need two steps (tag the engine, then bump the pin), which is
  slower than editing one tree.
- The engine currently has no tags, so nothing is pinned yet. The pin is created
  when the upgrade in `DESIGN.md` §15 (W1-2) produces the first tagged release.
- Engine throughput figures are reconciled before the two projects are cited
  together (`DESIGN.md` §17; publication gate in `SPEC.md` §4).

## Alternatives considered

- **Extend the engine repo in place.** Mixes research-specific code and hypotheses
  into a general engine, and entangles two sets of claims. Rejected.
- **Copy the engine source into Fillcast.** The copy drifts from upstream and
  breaks the link between Fillcast results and a named engine version. Rejected in
  favour of a pinned tag.
- **Unpinned dependency on engine `main`.** Results could not be tied to a version.
  Rejected.
