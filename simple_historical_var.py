"""
simple_historical_var.py

The simplest possible Value-at-Risk calculation: one asset, one method
(historical VaR), no simulation, no distributional assumptions, no
backtesting. The point of this script is to be small enough to fully
explain out loud without notes.

Data: prices.csv is a SMALL, SYNTHETIC price series (randomly generated,
not real market data) - just enough rows to make the method meaningful.

Run: python simple_historical_var.py
"""

from __future__ import annotations

import pandas as pd


def load_prices(csv_path: str) -> pd.Series:
    """Load a CSV with Date,Close columns; return a Series of prices indexed by date."""
    df = pd.read_csv(csv_path, parse_dates=["Date"])
    return df.set_index("Date")["Close"]


def compute_returns(prices: pd.Series) -> pd.Series:
    """
    Daily simple returns: (price_t - price_t-1) / price_t-1.

    Simple (not log) returns here because they're the more intuitive one to
    explain out loud: "the price moved by X% that day."
    """
    return prices.pct_change().dropna()


def historical_var(returns: pd.Series, confidence: float = 0.95) -> float:
    """
    Historical VaR at the given confidence level.

    confidence=0.95 means: find the loss threshold that was only exceeded
    5% of the time in this sample. We look at the (1 - confidence) quantile
    of the return distribution (the worst tail) and flip its sign, so the
    result is a POSITIVE number representing a loss, not a negative return.
    """
    tail_quantile = 1 - confidence
    worst_case_return = returns.quantile(tail_quantile)
    return -worst_case_return


def explain(var_value: float, confidence: float) -> str:
    """One-sentence plain-English explanation of what the VaR number means."""
    pct_chance = round((1 - confidence) * 100, 1)
    pct_loss = round(var_value * 100, 2)
    return (
        f"Based on this price history, there's roughly a {pct_chance}% chance "
        f"of losing more than {pct_loss}% in a single day."
    )


if __name__ == "__main__":
    prices = load_prices("prices.csv")
    returns = compute_returns(prices)

    print(f"Loaded {len(prices)} prices, {len(returns)} daily returns.\n")

    for confidence in (0.95, 0.99):
        var_value = historical_var(returns, confidence=confidence)
        print(f"{int(confidence * 100)}% historical VaR: {var_value:.4f} "
              f"({var_value * 100:.2f}% of portfolio value)")
        print(explain(var_value, confidence))
        print()
