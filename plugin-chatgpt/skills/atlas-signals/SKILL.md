---
name: atlas-signals
description: Read plays (signals) on Atlas, where a play is one trade idea written down in full and shared with a board or a group. Use when the person wants to see what was posted on the community board or in a group they follow, look at one play, find public groups, or see how a group's plays have done.
---

# Reading plays (signals)

A play is one trade somebody is calling: what to buy, where to get in, where
to take profit, where to get out, and how much. It is posted to the community
board or to a group, and the people who follow it can take it.

From here plays are **read**. Posting one, changing one, taking one into an
account, following a group and changing how plays are handled are done in
Atlas itself, on the dashboard. When the person asks for one of those, say so
and point them there.

`references/tools.md` lists every field each of these tools accepts.

## What can be read

| The person asks | Tool |
|---|---|
| What is on the board, or in one group | `Signal-List`: `board` is `community` or `private`, or pass one `group_id`. It reads a page at a time |
| One play in full | `Signal-Show` |
| Which groups they own, follow or may read | `Signal-Groups` |
| Which plays are waiting on their own answer | `Signal-Pending`. They answer on the dashboard |
| Public groups they could follow | `Signal-Discover` |
| How a group's plays have done | `Signal-Group-Performance` |
| Which of their filters a play breaks right now | `Signal-Filter-Check` with its `signal_id`. Say which in plain words |

## Reading one well

- A play's **entry** is where to get in; its **targets** are where to take
  profit, in order; its **stop** is where to get out. On an option, a dollar
  level is the stock's price and a percent is on the option's own price.
- A play can be one of a **linked pair**: when one side fills, the other is
  cancelled, or the other only starts once the first has filled. The play
  says which.
- A play says whether it has been entered and how far it has got. Say what it
  shows; do not guess at what happened after.
- Somebody else's play is their call, not advice from Atlas. Say what it is
  and what its record shows; the decision is the person's.

## Size, the circuit breaker and filters (new on Nov 7, 2026)

These are set by the person in Atlas, on the dashboard, in **Trade settings**
for a group they follow. From here, explain them and point there; do not
promise to change them.

| The person asks | What to tell them |
|---|---|
| "Put $250 into each play" / "3 contracts" | Trade settings: the **Contracts** row. A count, or **Size this trade by an amount of money** and **Most to put into this trade**: Atlas buys as many as fit under it, never more. |
| "Put in less after losses, more after wins" | With money on, the **Auto sizing** row: start from the amount or a % of the account (never over the amount); after N losses in a row put in less by % or $, after N wins more; one step, then back after the opposite result; never under one contract. |
| "Stop taking plays for the day if I lose $200" | **Auto sizing** page, **Circuit breaker**: pause when the day's loss (or profit) reaches a % of the account or $; then **Back tomorrow** (next trading day, 9:30 AM ET), **For a week** or **Until I turn it on**. Automatic taking of that group stops, they are told once, and it comes back by itself. Open trades keep their stops. Back on early: switch **Take every play automatically** on again. |
| "Only SPY", "nothing over $3 a contract", "not on FOMC days" | **Advanced filters** at the bottom of Trade settings: 28 filters (kinds, bid/ask spread, rating, open interest, volume, cost per contract, expiry, entry slip, late entry, earnings, big news days, trades a day, open trades, IV, delta, strike, symbols, time window, days, stock move, gap, day direction, VIX, theta, buying power, pause after a loss, stock price). A filter only skips a play, never changes it; market filters are judged when the play would go in and skip only when the number can be read; a skipped play sends one notice naming the filter. Filters never stop a play taken by hand: the take shows which filters it breaks and offers **Take anyway**. When the person asks before taking one, call `Signal-Filter-Check` and say which it breaks. |
| "Sell everything at TP2" | Trade settings for that group: the target at which everything still held is sold. Later targets do nothing for them; no target moves. |
| A group they own: their own order on the plays they post | The **Trade settings** button on Signals: the account, the size, auto sizing, the circuit breaker (the plays still post to followers while it is tripped, and they can turn their own orders back on there), and the target at which everything still held is sold. |

Every step, with pictures: https://www.mind-vest.io/atlas/setup-guide/whats-new-nov-7
