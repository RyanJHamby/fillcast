# Fillcast: Public Specification

Status: **spec only. There is no code and there are no results.** This document pre-registers what Fillcast will test. It is a summary of [`DESIGN.md`](DESIGN.md) (v0.2, 2026-10-13); where they differ, `DESIGN.md` governs. The claims register ([`DESIGN.md` §17](DESIGN.md)) is empty.

**Evidence labels.** `[R]` reference (cited in §5), `[H]` hypothesis, `[T]` target. There is no `[M]` (measured) label in this document because nothing has been measured. Predicted sizes below are the author's priors, written before any experiment. Where a size would be a guess with no basis, the entry says "size not predicted" and the pass threshold is fixed and logged with `pow log` before the run.

## 1. Value

**Who benefits.** Anyone who posts passive limit orders and must decide, per price level and moment, whether resting there is worth it: market makers, execution desks, and researchers who backtest passive strategies.

**Which decision improves.** The post/don't-post decision at a price level. Fillcast forecasts two things for a hypothetical one-lot passive order: the distribution of time-to-fill, and the signed price move after the fill (markout), each with calibrated uncertainty. Their product, net of fees, is the **net edge per post**:

$$\mathcal{E}_{\tau,h}(x) = F(\tau \mid x)\,\big(\mathbb{E}[m(h) \mid \text{fill}, x] - f\big)$$

Post when a lower confidence bound on $\mathcal{E}$ exceeds an opportunity-cost threshold. Results are reported as a function of fee $f$, latency $\delta$, and threshold $c$, not as one headline number.

**What is not claimed (non-goal N1).** No alpha, Sharpe, or P&L claim. Replay with shadow orders cannot support one. Nor does the project claim tick-to-trade latency (N2), live trading (N3), or exchange certification (N6).

## 2. Theory

**Queue position and fill hazard.** Under FIFO priority, a passive order fills only after every lot ahead of it has been executed or cancelled and a later execution reaches it. Fill time $T$ is modelled with a discrete-time hazard $h_k(x) = \Pr(T \in (b_{k-1}, b_k] \mid T > b_{k-1}, x)$ on a log-spaced grid, trained with a person-period likelihood. Survival-style fill modelling with queue position as an input is established in the literature `[R]` (Zhong et al. 2025), as is the queue-reactive description of order books `[R]` (Huang, Lehalle, Rosenbaum 2015).

**Adverse selection and markout.** Markout is $m(h) = s\,(\mathrm{mid}(\text{fill time} + h) - p)$ for side $s$. Fills happen disproportionately when the market is moving through the level, so $\mathbb{E}[m \mid \text{fill}] < \mathbb{E}[m]$. This is the cost a passive poster pays for being filled, and it is why fill probability alone is the wrong objective.

**Shadow-order labels remove informative censoring.** An earlier approach would train on real resting orders. Their cancels are informative (participants cancel because they have information), and under dependent competing risks the cancel-free marginal fill time is not identifiable from the data alone `[R]` (Tsiatis 1975). Fillcast instead replays the exact event stream with hypothetical one-lot orders that never cancel. Their only censoring is administrative (a fixed horizon $\tau_{\max}$ or session end), so labels are computed exactly by replay and need no censoring correction. This rests on assumption A1 (a one-lot order does not change others' behavior), which is tested as a sensitivity band, not assumed away.

**Latency delta is a first-class parameter.** The decision is made at $t_n$ using only events received by $t_n$ (the knowability clock). The order arrives at $a_n = t_n + \delta$, where its queue position is not observable at decision time and must be forecast. A model that ignores $\delta$ is expected to be optimistic `[H]`. Every metric is reported on a grid of $\delta \in \{0,\ 50\,\mu\mathrm{s},\ 500\,\mu\mathrm{s},\ 5\,\mathrm{ms}\}$ `[H]` (grid values are provisional).

**Data granularity.** Price-level (L2) data does not reveal queue order, so passive-execution backtests built on it depend on an assumed cancellation rule `[R]` (Danait, Zamora, Boier 2026). Fillcast degrades order-by-order (MBO) ground truth to L2 to measure that loss directly (H4).

## 3. Proposed results

All entries are predictions, not findings. Each H has a metric, a baseline, a pass condition, and a falsifier. Models: M0 is the queue-depletion heuristic, M1 a simple statistical baseline, M3 the int8 MLP (`DESIGN.md` §5.4). CPCV is combinatorial purged cross-validation. $\varepsilon_i$ thresholds are TBD and will be fixed and logged before the corresponding run.

| ID | Prediction (direction, size) | Label | Metric / baseline | Pass condition | Falsifier |
|---|---|---|---|---|---|
| H1 | Learned hazard beats the queue-depletion heuristic M0 on net edge per post. Direction: positive. Size not predicted. | `[H]` | Net edge per post over CPCV paths / M0 | Lower 95% CI of the difference $> 0$ | CI includes 0, or the difference is negative. Published as a null result. |
| H2 | Fill probabilities are calibrated out of sample. Direction: ECE below threshold on every path; learned model at least as good as M0, M1 on IBS. | `[H]` | ECE, IBS / M0, M1 | ECE $\le \varepsilon_1$ on every CPCV path | ECE $> \varepsilon_1$ on any path, or IBS worse than M0 |
| H3 | Ignoring $\delta$ inflates edge. Direction: Edge($\delta{=}0$) $>$ Edge($\delta$), growing with $\delta$. Size not predicted. | `[H]` | Edge($\delta{=}0$) minus Edge($\delta$) | Significant at each $\delta > 0$ | No significant gap at some $\delta > 0$, or edge rises with $\delta$ |
| H4 | L2-inferred queue position is materially wrong. Direction: nonzero position error and degraded calibration and edge; spread across the front/random/back cancel rules is at least several percentage points of completion rate, as seen in prior work on two instruments `[R]`. | `[H]` | Position error, calibration and edge degradation / MBO truth | Quantified with bands under all three rules | Degradation indistinguishable from zero on the products studied (the prior result then fails to generalize) |
| H5 | The integer pipeline is bit-exact and costs little accuracy. Direction: edge delta vs float is small. | `[T]` | Bit equality; edge delta / float model | Bit-exact; edge delta $\le \varepsilon_2$ | Any bit mismatch on the golden vectors, or edge delta $> \varepsilon_2$ |
| H6 | Markout intervals reach nominal coverage, including under shift. Direction: adaptive conformal intervals beat static split conformal on conditional coverage. | `[H]` | Coverage by volatility tercile, time of day, event days / static split conformal | Within $\varepsilon_3$ of nominal in every regime | Outside $\varepsilon_3$ in any regime, or static split conformal does as well |
| H7 | The leak suite is effective. Direction: every planted leak is flagged. | `[T]` | Canary detection rate | 100% of planted leaks flagged | Any planted leak unflagged |
| H8 | HA claims hold under fault injection F1–F8. Direction: zero divergence and zero output loss. Failover time is reported, not targeted. | `[T]` | Divergence, loss, failover time | Zero divergence and zero loss for F1–F8 | Any divergence or loss in any injection. "HA" is then replaced by "deterministic replay with checkpoint recovery". |
| H9 | The hot path meets its budget: event apply $\le$ 150 ns median, feature update $\le$ 150 ns median, int8 inference $\le$ 400 ns median, end-to-end decision $\le$ 1 µs p99. | `[T]` | p50/p99/p99.9 per stage / budget | Reported either way | A missed budget is a legitimate result and is published. |
| H10 | Rust vs C++ ingest. No predicted winner. | `[H]` | Throughput, tail latency, defect count | Reported without a pre-judged winner | Not falsifiable by design; a byte-identical-journal mismatch voids the comparison |
| H11 | Codecs (ITCH/MoldUDP64, OUCH) conform to the published specifications. Direction: zero mismatches. | `[T]` | Round-trip, differential vs an independent reference parser, fuzzing | Zero mismatches on the corpus; fuzzing clean | Any mismatch or fuzzing crash |
| H12 | The point-in-time assurance suite catches planted leakage and passes on a clean pipeline. | `[T]` | PIT1–PIT10 outcomes / planted leaks | Zero false negatives on planted leaks; zero violations on the clean run | A missed planted leak, or a violation on the clean run |
| H13 | The pre-trade risk gate holds. Direction: no limit is exceeded. | `[T]` | Property tests; breach injection | No limit exceeded by any generated sequence | Any generated sequence that passes the gate and exceeds a limit |
| H14 | The Kafka sink is off the latency path. Direction: hot-path p99 and p99.9 unchanged with the sink on. | `[H]` | Hot-path p99/p99.9, sink on vs off / sink off; gaps and duplicates after a broker outage | Latency difference within noise (threshold TBD); zero gaps and duplicates | Difference outside noise, or any gap or duplicate after recovery |

Null and negative results are published in the repository (`DESIGN.md` §9.5). Confidence intervals come from stationary or day-block bootstrap, never row-wise resampling, and the sealed holdout is opened once.

## 4. Publication gate

Nothing is pushed or made public until each item is checked and the author confirms.

- [ ] References not read in full are checked against the originals, or removed from the public version (`DESIGN.md` §18).
- [ ] The name "fillcast" is checked for collisions (GitHub, PyPI, crates.io, trademark-style searches).
- [ ] Engine throughput figures (1.3M vs ~2.5M orders/sec) are reconciled alongside Fillcast.
- [ ] Resume, site, and README numbers and dates agree. Any disagreement is flagged to the author.
- [ ] Claims register is empty, or every entry has an artifact in `results/` naming the hardware.
- [ ] Author has confirmed publication.

## 5. References

Checked on 2026-10-18 against the arXiv abstract page or Crossref record (abstract and bibliographic data only, not read in full):

- Danait, R., Zamora, Y., and Boier, I. *Same Book, Different Fills: Partial Identification of FIFO Execution from Aggregate Order Books.* arXiv:2609.13597, September 2026.
- Zhong, J., Bacry, E., Guilloux, A., and Muzy, J.-F. *KANFormer for Predicting Fill Probabilities via Survival Analysis in Limit Order Books.* arXiv:2512.05734, December 2025.
- Huang, W., Lehalle, C.-A., and Rosenbaum, M. *Simulating and Analyzing Order Book Data: The Queue-Reactive Model.* Journal of the American Statistical Association 110(509):107–122, 2015. doi:10.1080/01621459.2014.982278.
- Tsiatis, A. *A Nonidentifiability Aspect of the Problem of Competing Risks.* Proceedings of the National Academy of Sciences 72(1):20–22, 1975. doi:10.1073/pnas.72.1.20.

`DESIGN.md` §18 lists further references (conformal inference, CPCV, ITCH/OUCH specifications, and others). They are not cited here and remain unverified.
