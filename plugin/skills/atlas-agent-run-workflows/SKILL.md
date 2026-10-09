---
name: atlas-agent-run-workflows
description: Register an Atlas workflow that you, the assistant, run yourself, and hand in each run's result so Atlas checks it, places it, logs it and shows it on the person's dashboard like any other workflow. Use when the person wants their own assistant to do the thinking for a workflow (on your schedule or when an Atlas alert goes off), or asks you to check what runs are waiting for you.
---

# Workflows you run yourself

An ordinary Atlas workflow is thought through by Atlas. This kind is thought
through by you. Atlas keeps everything around the thinking: the schedule, the
alerts, the trade's fields and checks, the orders, the followers, the run log
and the person's dashboard. On the dashboard it looks like any other workflow,
except its description says who it is from ("From: Claude").

This page says what is possible. `references/run-lifecycle.md` describes, step
by step, what Atlas does with a run. `references/tools.md` lists every field of
the tools. `references/trade-card.json` lists every field of a trade.

## The three steps

### 1. Register it

`Workflow-Create` with `ui_schema: { "run_by": "agent" }`. Everything else is
an ordinary workflow (see the `atlas-workflows` skill): a name, what it is for,
what starts it, the trade card, the broker account, private or public. The
answer carries the workflow's id. Keep it.

```json
{
  "name": "SPY breakout, run by me",
  "purpose": "trading",
  "ui_schema": { "run_by": "agent", "preview_before_place": true },
  "trigger_source": "alert",
  "alert_id": "<an alert's id, from List-Alerts>",
  "alert_max_runs_per_day": 2,
  "snaptrade_account_id": "<the account, from Broker-Connections>",
  "instruction": "My own notes: buy the nearest call when SPY holds above the level on rising volume.",
  "output_schema": {
    "triggers": [
      {
        "symbol": "SPY", "asset_class": "option", "option_type": "call",
        "strike": null, "expiry": null, "bracket_trade_budget": 500,
        "enter_side": "buy_to_open", "enter_order_type": "market",
        "order_strategy": "bracket", "bracket_stop_loss_stop_pct": -30,
        "bracket_take_profit_levels": [
          { "pct": 30, "quantity": "50%" }, { "pct": 70, "quantity": "remaining" }
        ]
      }
    ]
  }
}
```

- It can be for trading, for sending the order to place by hand (`draft`), or
  for writing things up (`analysis`).
- `instruction` and `tools` are your own notes here. Atlas does not run them.
- The trade card is the person's terms. Whatever it fixes (a budget, a stop,
  the targets) is applied to every trade you hand in; what it leaves empty is
  yours to fill each run.
- `ui_schema.from` names you, if you want a name other than the one you signed
  in with.
- An existing workflow becomes yours to run with `Workflow-Update`, patch
  `{ "ui_schema": { "run_by": "agent" } }`.
- Switch it on (`status: "active"`) when the person says to.

### 2. Find out when a run is due

There are two ways, and a workflow can use either or both.

**Atlas keeps the time.** Give the workflow a schedule or an alert, as for any
workflow. When it comes due, Atlas does not think: it leaves the run waiting
for you. Nobody can call an assistant, so you ask:
`Workflow-Agent-Waiting-Runs`. Ask at the start of a conversation and whenever
your own scheduler wakes you.

```json
{
  "waiting": [
    {
      "waiting_id": "<workflow id>:alert:<alert id>",
      "workflow_id": "<workflow id>",
      "workflow_name": "SPY breakout, run by me",
      "started_by": "alert",
      "what_started_it": "the alert \"SPY over 600\" went off",
      "alert_message": "SPY crossed 600.02",
      "waiting_since": "2026-11-03T14:31:07+00:00",
      "seconds_waiting": 95,
      "seconds_left": 3505
    }
  ],
  "count": 1
}
```

A run waits about an hour when an alert started it and about a day when a
schedule did (`ui_schema.agent_max_age_s` sets it). After that it is gone:
judge by `seconds_waiting` whether it is still worth doing. A run nobody hands
in costs nothing.

**You keep the time.** Run whenever your own schedule says, and hand in the
result. Set `trigger_source: "manual"` so nothing on Atlas starts it.

How quickly you act on an alert is how often you ask. If you cannot wake
yourself at all, say so: the person may prefer an ordinary workflow, which
Atlas runs the moment the alert goes off.

### 3. Do the run, and hand it in

1. `Workflow-Open` for the workflow's notes and its trade card.
2. Look at the market with the data tools (see `atlas-market-data`).
3. Optional: `Workflow-Agent-Report-Progress` with one short line as you go
   ("Reading the options chain"). The person sees it on the card.
4. `Workflow-Agent-Hand-In-Run` with what you decided.

A trade. Start from the workflow's own trade card entry, keep what it fixes
exactly as it is, fill in what it left empty (here the strike and the expiry),
and send the whole entry:

```json
{
  "workflow_id": "<workflow id>",
  "waiting_id": "<workflow id>:alert:<alert id>",
  "reasoning": "SPY held above 600 for three 5-minute bars on rising volume after the alert.",
  "triggers": [
    {
      "symbol": "SPY", "asset_class": "option", "option_type": "call",
      "strike": 601, "expiry": "2026-11-20", "bracket_trade_budget": 500,
      "enter_side": "buy_to_open", "enter_order_type": "market",
      "order_strategy": "bracket", "bracket_stop_loss_stop_pct": -30,
      "bracket_take_profit_levels": [
        { "pct": 30, "quantity": "50%" }, { "pct": 70, "quantity": "remaining" }
      ]
    }
  ]
}
```

Nothing to do:

```json
{ "workflow_id": "<workflow id>", "reasoning": "Back under the level within two bars. Standing aside.", "act": false }
```

A write-up (a workflow that only analyses):

```json
{ "workflow_id": "<workflow id>", "reasoning": "The index is above all three averages. Breadth narrowed. Two names on the list report tonight." }
```

`reasoning` is always required: it is what the person, and anyone following
the workflow, reads.

## What happens after you hand it in

It is a normal run from there. In order:

1. The person's plan is checked and **one request is used**, whatever you
   decided, including nothing.
2. Your trades are laid over the workflow's trade card. A value the card
   fixes stays as the card has it.
3. Each trade is checked. One that does not make sense (a missing field, a
   stop on the wrong side, a mixed ladder) is refused and the log says why.
4. The workflow's daily cap is applied.
5. **Review, or straight in**, by the workflow's own switch
   (`ui_schema.preview_before_place`): on, the run is held for the person to
   approve, edit or throw away; off, the orders go in.
6. People following the workflow get the same trade, at their own size.
7. The run is written to the workflow's log and the person is told.

`Workflow-Logs` shows what the run did a few seconds later.
`Workflow-Review` shows a run that is being held.

## What to keep in mind

- This can place real orders, for the person and for anyone following the
  workflow. Hand in only what the notes and the market support.
- Never invent a size, a budget or a stop the trade card does not carry.
- One decision per run. Handing the same one in twice within a few seconds is
  taken once.
- A copy of your workflow that somebody else follows runs when yours does.
- To set an alert or post a play yourself, use `Create-Alert` or `Signal-Post`
  directly: those need no workflow.
