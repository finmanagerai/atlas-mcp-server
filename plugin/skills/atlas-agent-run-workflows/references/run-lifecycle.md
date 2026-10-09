# What Atlas does with a run

This describes behaviour: what each step does and what it needs from you. It
is the same for a workflow Atlas thinks through and for one you run yourself.
The only step that moves is the fourth.

## 1. Something starts the run

| What | How it is set | Notes |
|---|---|---|
| A schedule | `trigger_source: "cron"`, `schedule` | One line per time, in `timezone` (Eastern unless said). `30 9 * * 1-5` repeats. `once 2026-11-03 09:35` runs that once. Repeating lines or `once` lines, not both |
| An alert | `trigger_source: "alert"`, `alert_id` or `alert_ids` | Any of the named alerts starts it. What the alert said travels with the run |
| Either | `trigger_source: "both"` | |
| A person | `trigger_source: "manual"` | Only Run now, or you handing a run in |

A workflow that is paused starts nothing.

## 2. The daily cap

`alert_max_runs_per_day` is how many trades a day the workflow may place from
runs nobody pressed. Once it is used up, the workflow is done until the next
Eastern morning: nothing runs, nothing is left waiting. Each person following
the workflow has an allowance of their own.

## 3. One run at a time, per ticker

A workflow about one ticker is one conversation: a newer run of the same
ticker takes the place of an older one still in progress. A run that arrives
while orders are going in waits behind them. Two different alerts on a
workflow about several tickers are two runs, side by side.

## 4. The decision

Atlas thinking: its model reads the workflow's tools and decides.

You thinking: Atlas leaves the run waiting, you ask for it, and you hand in:

```json
{
  "workflow_id": "the workflow",
  "reasoning": "what you saw and why",
  "act": true,
  "triggers": [ { "one trade, in the trade card's fields": "..." } ],
  "waiting_id": "the waiting run this answers, when it answers one"
}
```

- `act: false`, or no trades, means you looked and decided to do nothing.
- A workflow that only writes things up takes `reasoning` alone.

## 5. The plan

The run's owner must have a request left. A run you hand in uses one every
time. Somebody following a paid workflow is covered by what they pay its
author.

## 6. The trade card is laid over the decision

The workflow's own trade card (`output_schema.triggers`) is the person's
terms:

- A value the card fixes wins. If it says a $500 budget, a 30% stop and two
  targets, every trade from the run carries those, whatever was handed in.
- A value the card leaves empty is filled from the decision.
- A card in `trades_mode: "auto"` is one template applied to every ticker the
  run names.
- A card with several entries is matched to the decision's trades by what
  they are (the ticker, call or put, the label), not by their order.

## 7. Each trade is checked

Refused, with the reason in the run's log, when for example:

- a field the trade needs is missing (an option with no strike or expiry);
- a size and a budget are both given, or neither can be worked out;
- the stop or the target is on the wrong side of the entry;
- a ladder mixes percent and dollar levels, or does not add up to the whole
  position;
- two trades are meant as either/or and only one arrived. Atlas does not
  place half a pair.

## 8. Review, or straight in

`ui_schema.preview_before_place`:

- **on**: the run is held. The person reads it, may edit the trades and the
  write-up, and places it or throws it away. Nothing reaches a broker until
  they do.
- **off**: it goes on at once.

## 9. Orders

By what the workflow is for:

- `trading`: the trade is set up in the workflow's broker account. If it has
  an entry level it waits for the price; otherwise it goes in now. From then
  on Atlas watches the stop and the targets and closes the trade when one is
  reached.
- `draft`: nothing is sent to a broker. The person is told exactly what to
  buy, and later what to sell.
- `analysis`: nothing is traded. The write-up is the result.

Sizing by money (`bracket_trade_budget`) is worked out at the moment of the
buy, from the price actually paid: as many as fit, never over.

## 10. Followers

Everybody following the workflow gets the same trade from the same run: the
same contract, entry, stop and targets, at their own size or budget, in their
own account. Someone who has used up their own cap or plan sits that run out.
Followers can close their own position; only the author moves the exits.

## 11. The record

Every run leaves a line in the workflow's log: when, the write-up, what was
decided, what was placed, or why nothing was. The person is told (a Discord
message and a phone notification, by their own settings). Closed trades add to
the workflow's results.

## 12. While a trade is open

The stop, the targets and a time to be out by are watched by Atlas without any
further run. On a workflow Atlas thinks through, a ladder can ask for a fresh
look after each target fills; on a workflow you run yourself that fresh look
does not happen, and the ladder stands as it was placed. To change an open
trade, use `Trade-Edit-Exit`, `Trade-Take-Profit` or `Trade-Close`.
