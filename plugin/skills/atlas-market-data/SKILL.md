---
name: atlas-market-data
description: Scan options flow and analyze real-time stock market data with Atlas. Use when the person asks what is trading in the options market, wants a quote, a chart, price history, an options chain, where dealer exposure sits, or a company's earnings, financials or filings.
---

# Scanning options flow and analyzing market data

Every tool here only reads. Each call uses one request of the person's plan,
so ask the narrowest tool that answers the question rather than pulling
everything.

`references/tools.md` lists every field each of these tools accepts.

## Which tool for what

| The person asks | Tool |
|---|---|
| What are the biggest options trades today? | `Options-Flow` with no symbol |
| What is the flow on one stock? | `Options-Flow` with `symbol` |
| Which of these names has the flow? | `Options-Flow` with `symbols` (up to 8) |
| How did one contract trade through the day? | `Options-Flow-Contract` |
| Are calls or puts leading? | `Unusual-Flow-Ratio` (by money traded), `Put-Call-Ratio` (by open interest) |
| Which contracts are busiest? | `Top-Volume-and-OI-Contracts` |
| What is the price right now? | `Stock-Quote` |
| Price history as numbers | `Price-Data-OHLCV` |
| The trend across timeframes | `Multi-Timeframe-Price-Overview` |
| A chart | `Price-Chart`; several side by side, `Multi-Chart-View` |
| One option's price and greeks | `Single-Option-Quote` (one or several contracts) |
| The whole chain | `Options-Chain`; which dates exist, `Option-Expiration-Dates` |
| A chain or a contract on a past date | `Historical-Options-Chain`, `Historical-Contract-Greeks` |
| Where is dealer exposure concentrated? | `Greek-Exposure-Single-Expiration` (one date), `Greek-Exposure-Multi-Expiration` (a range), `Greek-Exposure-Heatmap` and `Net-Exposure-Charts` (as pictures) |
| Earnings, financials, estimates | `Earnings-Calendar`, `Earnings-Dates`, `Financial-Metrics`, `Income-Statement`, `Balance-Sheet`, `EPS-Estimates`, `Revenue-Estimates`, `Analyst-Price-Targets` |
| Filings and who owns it | `SEC-Filings`, `Insider-Transactions`, `Institutional-Holders` |
| News and anything happening now | `Web-Search` |
| A company name, not a ticker | `Ticker-Symbol-Lookup` first |

## Options flow, the parts that get mixed up

- **It is a record of trades that already printed**, not a live stream. Ask
  again later in the day to see what came after.
- **The day a trade printed is not the day the contract expires.** "AMD flow
  for the 29th" almost always means trades on the 29th: that is `from_date`.
  `expiration_date` narrows to contracts expiring that day; use it only when
  the person names an expiry.
- By default it shows the large trades (blocks and sweeps). Pass
  `trade_type: ""` for everything.
- A big name over many expiries can take minutes. Wait for it; a retry starts
  the read again. Narrow it with a strike, an expiry, `min_premium` or a
  shorter date range to make it quick.
- Each row is one trade: which side (bought or sold, when it can be told),
  call or put, size, premium, and whether it looks like a position being
  opened or closed.

## Examples of what is possible

- "What is the unusual flow on NVDA today, calls only, over $250k?"
  → `Options-Flow` with `symbol: "NVDA"`, `side: "call"`, `min_premium: 250000`
- "Which has more flow: PANW, CRWD or NET?"
  → `Options-Flow` with `symbols: ["PANW", "CRWD", "NET"]`
- "Where is the biggest gamma level on SPY today, and is price above it?"
  → `Greek-Exposure-Single-Expiration` for today's expiry, then `Stock-Quote`
- "Give me the picture on AAPL before earnings."
  → `Earnings-Dates`, `Multi-Timeframe-Price-Overview`, `EPS-Estimates`,
    `Options-Flow` with `symbol: "AAPL"`

Say what the numbers show. What to do about them is the person's call.
