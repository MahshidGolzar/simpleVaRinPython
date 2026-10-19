# simple_historical_var

The simplest possible Value-at-Risk calculation: one asset, one method (historical VaR), no simulation, no distributional assumptions, no backtesting.

## Why this exists

`risk_engine_monte_carlo` implements four VaR methods plus two statistical backtests — a lot of surface area. This is the single simplest method, stripped down to something explainable on a whiteboard: look at the worst historical days, read off the threshold.

## Data

`prices.csv` is a **small, synthetic** daily price series (randomly generated with a fixed seed, not real market data) — 60 rows, just enough for the historical quantile to mean something.

## What it does

1. Loads prices from `prices.csv`.
2. Computes daily simple returns: `(price_t - price_t-1) / price_t-1`.
3. Computes historical VaR at a given confidence level: the `(1 - confidence)` quantile of the return distribution, sign-flipped so the result reads as a positive loss number.
4. Prints the result as a plain-English sentence, not just a number.

## Known limitations

- Historical VaR only reflects whatever happened to be in the sample — a calm 60-day window understates risk in a genuine crisis period, and a volatile window overstates it in calm times. (This is exactly why `risk_engine_monte_carlo` also builds parametric and Monte Carlo versions, and backtests them.)
- No backtesting here — this script computes a VaR estimate, it doesn't check whether that estimate was subsequently accurate.
- Synthetic data: fine for demonstrating the method, not a real risk assessment of any actual asset.

## Running

```bash
pip install pandas
python simple_historical_var.py
```
