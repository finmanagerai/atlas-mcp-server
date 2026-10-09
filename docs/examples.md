# Atlas: examples

Things to ask, and the tools an assistant would reach for. The names are the
ones in [tools.md](tools.md).

## To check it works

> Get me a quote for SPY.

→ `Stock-Quote`

> When does NVDA next report, and what do analysts expect?

→ `Earnings-Dates`, `EPS-Estimates`, `Analyst-Price-Targets`

## Scanning options flow

> What are the biggest options trades in the market today?

→ `Options-Flow` with no symbol

> Show me call sweeps over $250k on NVDA today.

→ `Options-Flow` with the symbol, the side and a minimum premium

> Which has more flow right now: PANW, CRWD or NET?

→ `Options-Flow` with all three

> Are calls or puts leading on SPY?

→ `Unusual-Flow-Ratio` for the money traded, `Put-Call-Ratio` for open interest

## Analyzing a stock

> Give me the picture on AAPL before earnings.

→ `Earnings-Dates`, `Multi-Timeframe-Price-Overview`, `EPS-Estimates`, `Options-Flow`

> Where is the largest gamma level on SPY today, and is price above it?

→ `Greek-Exposure-Single-Expiration`, `Stock-Quote`

> Chart NVDA, AMD and AVGO side by side for the last year.

→ `Multi-Chart-View`

> Pull the chain for TSLA for this Friday and show me the 10 strikes around the price.

→ `Option-Expiration-Dates`, `Options-Chain`

## Your account

> What is my buying power, and what am I holding?

→ `Broker-Connections`, `Account-Balances`, `All-Account-Holdings`

> How much of my plan is left this month?

→ `Subscription-Status`

## Workflows

> Every weekday at 9:30, send me a brief on SPY and the five names on my list.

→ `Workflow-Preview`, then `Workflow-Create`

> When SPY breaks above 600, buy the nearest call with $500, take half off at
> +30%, and show me the trade before it goes in.

→ `Create-Alert` for the level, `Trigger-Workflow-Schema`, `Workflow-Preview`, `Workflow-Create`

> What did my SPY workflow do today, and how has it done this month?

→ `Workflow-List`, `Workflow-Logs`, `Workflow-Performance`

## Alerts

> Tell me when a call sweep over $250k prints on NVDA.

→ `List-Alert-Types`, `Preview-Alert`, `Create-Alert`

> Tell me when SPY crosses its 20 EMA on the 5-minute chart.

→ `Create-Alert`

## Plays

> Post it to my group: SPY 780 calls at 2.10, out at +50% and +100%, stop 30%.

→ `Signal-Groups`, `Signal-Post`

> What has been posted on the community board today?

→ `Signal-List`

## Orders and trades

> Preview buying 10 NVDA at 900 with a stop at 880 and a target at 940.

→ `Broker-Connections`, `Preview-Order`

> Place it.

→ `Place-Order` with that preview

> Move the stop on my SPY trade to breakeven.

→ `List-Trading-Triggers`, `Trade-Edit-Exit`

> Close it.

→ `Trade-Close`

## A good habit

Preview before placing, and say what is about to happen before it does. For
what is possible with each of these, and templates to start from, see the
skills under [plugin/skills](../plugin/skills).
