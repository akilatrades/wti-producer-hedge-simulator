# When does storing crude pay?

A rising futures curve is only the start of the calculation. Does the deferred sale price cover acquisition, storage, financing, insurance and handling?

In the committed EIA sample, **59 of 111 full months were in C1-to-C4 contango; only 12 covered the default assumed costs**. The result is a historical economics screen, not a count of trades that could have been executed.

![Carry after costs](outputs/carry_history.svg)

## Economics

Buy for delivery at C1, store for an assumed three months, and sell for C4 delivery. Per barrel:

`net carry = C4 - C1 - 3*monthly storage - C1*(exp(r*3/12)-1) - C1*insurance*3/12 - handling`

| Input | Default assumption |
|---|---:|
| Storage duration | 3 months |
| Storage | $0.50/bbl/month |
| Annual financing, continuously compounded | 6% |
| Annual insurance on acquisition value | 0.3% |
| Round-trip handling | $0.20/bbl |

Costs are illustrative constants, not observed historical quotes. Acquisition is financed from C1 delivery; storage, insurance and handling are treated as terminal expenses without additional financing. `cost_sensitivity.csv` varies storage from $0.25 to $1.00 and financing from 3% to 10%. `carry_history.csv` also calculates the maximum monthly storage fee the spread could support; a negative value means even free storage would not cover the other costs.

## Data and scope

The committed snapshot contains EIA monthly averages of NYMEX delivery positions C1–C4. The analysis uses January 2015–March 2024; April 2024 is excluded because the source stopped April 5. These are monthly average curves, not simultaneous executable bids and offers. Three months is an approximation; exact delivery dates, terminal access, capacity, quality, transport, shrinkage, credit, margin and liquidity are not modeled. No actual storage trading return is claimed.

Source pages: [C1](https://www.eia.gov/dnav/pet/hist/LeafHandler.ashx?n=PET&s=RCLC1&f=M), [C2](https://www.eia.gov/dnav/pet/hist/LeafHandler.ashx?n=PET&s=RCLC2&f=M), [C3](https://www.eia.gov/dnav/pet/hist/LeafHandler.ashx?n=PET&s=RCLC3&f=M), [C4](https://www.eia.gov/dnav/pet/hist/LeafHandler.ashx?n=PET&s=RCLC4&f=M). Input inherited from the parent repository; exact checksum is saved with the results.

## Reproduce

From this directory, with pandas, numpy and matplotlib installed:

```bash
python -m unittest -v test_model
python run_analysis.py
```

All inputs are committed. Outputs include the monthly decomposition, cost sensitivity and chart. This directory is self-contained for a future separate repository.

## What I learned / what I would do differently

The curve needs to pay for the whole carrying period, not just look upward sloping. I would replace constant costs with dated terminal quotes and financing assumptions, then use daily executable contract prices and actual delivery calendars. The current result explains the economics but cannot establish an arbitrage opportunity.
