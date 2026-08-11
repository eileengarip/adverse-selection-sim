# Toy Market-Making Simulator

A simulation of a market maker quoting a two-sided market against a mix of uninformed
and informed traders, built to understand why a positive spread is not by itself enough to make money.

Written in Python with no dependencies beyond `matplotlib`.

---

## The model

A single asset with a true value `V` that follows a random walk, `V += N(0, sigma)`
each step. The true value is never directly observable by the market maker.

The market maker holds an estimate `M` of fair value which lags the truth by one
step, and quotes symmetrically around it:

```
bid = M - spread/2
ask = M + spread/2
```

One trader arrives per step. With probability `p_informed`, they observe the true
`V` and trade only when it is profitable for them to do so. This means buying if `V > ask` and selling if `V < bid`; otherwise, they won't trade. Otherwise, they are a noise trader who buys or sells on a coin flip regardless of price.

P&L (profits and losses) is tracked as cash plus inventory marked to the final true value:

```
pnl = cash + inventory * V
```

Default parameters: `sigma = 0.1`, `p_informed = 0.2`, `n = 2000` steps,
averaged over 100 independent runs.

---

## Results

### Adverse selection

### Break-even spread


### The mistake that taught me most

---

## Limitations

---

## Running it

---

## Next steps

---

## References

- Glosten & Milgrom (1985), *Bid, Ask and Transaction Prices in a Specialist
  Market with Heterogeneously Informed Traders*
- Avellaneda & Stoikov (2008), *High-frequency Trading in a Limit Order Book*
