---
name: atlas-backtest
description: Turn a plain request like "test if moving average crosses work on SPY" into an honest backtest. Covers the plan to show first (exact rules, period, years held back, costs, no look-ahead, enough trades, a buy-and-hold baseline, a few scenarios), getting the bars from Atlas, running up to 5 scenarios at once, the checks, and a results page. Use when the person asks to backtest, "test this strategy", "would this have worked", or to compare settings of an idea on past prices.
---

# Backtesting an idea, honestly

People who are not coders say "go test this scenario". A backtest with no
years held back, no costs and nothing to compare against will "work" almost
every time, and it means nothing. Most of the value is the plan, made BEFORE
any code.

## 1. Show the plan first

Pick sensible defaults yourself and show them in a few short lines. The
person can change any line; ask only what you truly cannot pick.

1. **The rules, exactly**: when it buys, when it sells, how much. A vague idea
   ("buy the dips") becomes a concrete rule; say what you chose, and make two
   honest readings of it two scenarios.
2. **Symbols and bar size matched to the idea**: a day-trading idea on daily
   bars, or a yearly idea on 1-minute bars, answers nothing.
3. **A period long enough to hold a fall and a rise**: 10 years of daily bars.
   Intraday history is short; say the limit.
4. **Years held back**: choose on the first 70%, judge on the last 30%, which
   nothing looks at until the end.
5. **Costs** on every buy and every sell: stocks and ETFs 0.02% to 0.05% a
   side; options at least half the bid-ask spread a side.
6. **No look-ahead**: decide on a bar's close, act on the next bar; adjusted
   prices; not today's index members over past years.
7. **At least 30 trades**, or say the result is luck.
8. **A baseline**: buying and holding the same symbol over the same years,
   after the same costs. Not beating it means not worth doing.
9. **The scenarios**: the few variations worth testing, one line each. Every
   extra scenario is another chance of a winner by luck: choose on the first
   70%, confirm on the last 30%, and say how many were tried.

For "test if moving average crosses work on SPY and QQQ":

    Idea: hold while the fast average is above the slow one, else cash.
    Scenarios (6): SPY and QQQ, with 10/30, 20/50 and 50/200 day averages.
    Bars: daily, adjusted, 10 years.
    Chosen on: the first 7 years. Judged on: the last 3, never seen.
    Costs: 0.02% on every buy and every sell.
    Rules: decide at the close, act the next day; under 30 trades = "too few".
    To beat: buying and holding the same symbol over the same years.

## 2. Get the bars, then test, at most 5 at once

- **Bars from Atlas**: `Price-Data-OHLCV` with `symbol`, `interval` ("1d",
  "1h", "15m") and `period` ("10y"), or `start` and `end`. Fetch each symbol
  ONCE before the scenarios start; every scenario uses the same bars and the
  same costs. Each call is one request of the person's plan.
- **On the person's own computer** (your app can run Python there): each
  scenario is one plain function; run them in processes, never more than 5 at
  once and never more than the cores minus one:

```python
import os
from concurrent.futures import ProcessPoolExecutor

def test_one(scenario):          # a plain def at the top of the file
    ...                          # the numbers for this one scenario
    return {"name": scenario["name"], "unseen_return": ..., "hold": ..., "trades": ...}

if __name__ == "__main__":       # needed on a Mac and on Windows
    with ProcessPoolExecutor(max_workers=max(1, min(5, (os.cpu_count() or 2) - 1))) as pool:
        results = list(pool.map(test_one, scenarios))   # in the order given
```

  For thousands of settings, vectorbt in one process is faster than any pool.
- **In Atlas's cloud** (no Python where you are): a paused script workflow
  and a test run (the `atlas-script-workflows` skill). Its runner has one
  processor, 1 GB and 5 minutes, so scenarios run one after another there:
  keep a test run to 5 scenarios, and more as further test runs.

The core of a fair test, in pandas:

```python
pos = (close.rolling(fast).mean() > close.rolling(slow).mean()).astype(float).shift(1).fillna(0)
ret = close.pct_change().fillna(0)
strat = pos * ret - pos.diff().abs().fillna(pos.iloc[0]) * cost_bps / 10_000
cut = int(len(close) * 0.7)       # judge on strat[cut:] against ret[cut:]
```

`shift(1)` is the no-look-ahead rule; the second term takes the cost off every
buy and every sell.

## 3. Check it

- **Look-ahead, tested**: change the prices from some bar onward (halve them,
  double them) and confirm the positions up to and including that bar do not
  change. Trading on the same close the signal reads, or a centred average,
  fails this.
- The result with costs is below the one without, with the same trades.
- The buy-and-hold number matches the first and last price of the period.
- The trade count is said, and under 30 is "too few", not a win.

## 4. Show the results

On a page your app can draw (an HTML file, an artifact), plain and readable on
a phone:

- **The answer first, in one sentence**: "None of 6 beat holding on the 3
  years kept back (Nov 2023 to Nov 2026), after costs."
- **One row a scenario**: verdict, return on the unseen years, holding over
  the same years, Sharpe, worst fall, trades. Mark the one chosen on the first
  70%; never re-pick on the unseen years.
- **One chart**: the chosen scenario against holding, with a line where the
  unseen years start.
- **The plan under it**: period, costs, the source and the date of the data,
  how many scenarios were tried.

## 5. Say the answer

- Lead with whether it beat holding on the unseen years after costs, with the
  numbers, the period and the source.
- A loss is an answer. Offer at most two honest next tests, never fifty tweaks
  until something wins.
- Past results are not a promise, and Atlas does not give investment advice.
  Offer to turn a winner into an alert or a workflow (`atlas-alerts`,
  `atlas-workflows`); show it first, and switch nothing on until the person
  says so.
