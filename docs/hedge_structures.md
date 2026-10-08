# Producer structures and pricing

All prices and option premiums are USD/bbl. Let F be the inception forward, S the terminal reference, b the physical basis, Q barrels and h the hedged fraction. Physical revenue is Q(S+b).

- Short futures or receive-fixed swap: add Qh(F-S).
- Collar: add Qh[max(Kp-S,0)-max(S-Kc,0)].
- Three-way: additionally subtract Qh max(Klow-S,0).

The collar ceiling solves Black-76 call premium = put premium. The three-way ceiling solves call premium = bought put premium minus sold put premium. One expiry, common constant volatility, continuously compounded rate and European exercise are assumed. An actual commodity swap is valued by discounted fixed-versus-forward cash flows; Black-76 prices the option legs, not the swap.

For positive F,K, d1=[ln(F/K)+sigma²T/2]/(sigma sqrt(T)) and d2=d1-sigma sqrt(T). Call value is exp(-rT)[F N(d1)-K N(d2)]; put follows put-call parity. Expiry and zero-vol limits are handled explicitly. Invalid prices are rejected, not clipped.

`run_structures.py` saves the seeded lognormal terminal distribution summary, strikes, payoff grid, observed benchmark basis and a separate location-basis stress grid. The distribution uses zero basis and is risk neutral, so expected revenues are not forecasts. All structures share the same paths. Costs, bid/ask, credit, daily margin, volume uncertainty and average-price settlement are excluded. Costless means zero modeled inception net premium before those costs.

## Basis data boundary

`outputs/monthly_analysis.csv` is the pre-existing public-source project snapshot. The new module subtracts its `futures_exit` from `spot_exit` without regenerating or reclassifying those observations. Both are monthly endpoint proxies; futures contract identity and synchronous timestamp controls are missing. Its largest spread must not be described as observed Midland basis. Location stress values (-15,-5,0,+5 USD/bbl) are explicit assumptions, not a fitted distribution.

## Sources and interpretation

- [CME collar education](https://www.cmegroup.com/education/courses/option-strategies/collars): long physical/futures exposure, long put, short call.
- [EIA Cushing spot history](https://www.eia.gov/dnav/pet/hist/LeafHandler.ashx?n=PET&s=RWTC&f=D).
- [FRED DCOILWTICO](https://fred.stlouisfed.org/series/DCOILWTICO) and Yahoo CL=F underpin the original saved monthly history.

The tests reconcile put-call parity, zero premium, a negative terminal payoff, swap/futures equivalence and the loss of downside protection below the sold put.
