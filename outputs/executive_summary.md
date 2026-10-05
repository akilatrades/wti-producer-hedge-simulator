# Executive Summary

## Objective

Evaluate how WTI futures can reduce monthly price risk for an illustrative producer with 100,000 barrels of expected monthly production, while making residual basis, volume, curve, and model risk explicit.

## Key historical findings

- 75% fixed hedge effectiveness: **90.3%** variance reduction.
- 100% fixed hedge effectiveness: **96.0%** variance reduction.
- Static minimum-variance hedge ratio: **1.016**.
- Rounded minimum-variance implementation: **102 CL contracts**.
- Rounded minimum-variance variance reduction: **96.6%**.
- 95% bootstrap interval for the hedge ratio: **[0.991672, 1.038644]**.
- Walk-forward residual volatility using trailing estimates: **1.460704 $/bbl**.
- Walk-forward residual volatility using a 1.0 hedge benchmark: **1.465999 $/bbl**.

## Risk interpretation

The historical sample shows that WTI futures can materially reduce flat-price variability, but a producer remains exposed to other risks:

- Midland/Cushing basis can move independently of the Cushing-linked futures hedge.
- Actual production can differ from forecast production, creating under- or over-hedged volume.
- The statistically estimated hedge ratio is not constant through time.
- The WTI futures curve changes between backwardation, contango, and relatively flat regimes.

## Governance / model-use note

The results are analytical benchmarks, not trading or hedge recommendations. A production hedge program would also require contract-specific execution, liquidity and margin constraints, policy limits, credit, accounting treatment, and ETRM controls.

See the top-level README and `docs/` for methodology and limitations.
