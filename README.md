# fillcast

Queue-aware fill and adverse-selection forecasting for passive orders. For a
hypothetical one-lot resting order at any price level, Fillcast aims to forecast
the distribution of time-to-fill and the signed post-fill price move (markout),
with calibrated uncertainty, from order-by-order (MBO) market data. The decision
it targets is whether to post, expressed as net edge per post.

## Status

**Spec only. No code and no results yet.** This repo currently holds the
standing design document: [`docs/DESIGN.md`](docs/DESIGN.md) (v0.2, 2026-10-13;
rendered as [`docs/fillcast-design.pdf`](docs/fillcast-design.pdf)). Every
quantitative statement in it is labelled as a reference, hypothesis, or target.
Nothing is labelled as measured, and the claims register (§17) is empty.

The substrate will be [order-book-engine](https://github.com/RyanJHamby/order-book-engine),
pinned at a tagged release. No tag is pinned yet.

## How this was built

The design document was drafted with an AI assistant (Claude); I direct the
architecture and review what it writes. No implementation exists yet, so no code
has been written by AI or by me. When implementation starts, AI-written code will
be reviewed and verified before it is committed, and this section will be updated
to say so. The [engineering journal](docs/journal.md) records decisions and dead
ends, and [`results/`](results/) will hold the raw output behind any number
quoted here.

## License

MIT, see [LICENSE](LICENSE).
