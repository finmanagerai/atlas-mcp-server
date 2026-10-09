---
name: atlas-workflows
description: Build, change, run and review an Atlas workflow, a plan Atlas carries out for the person on a schedule or when an alert goes off. Use when the person wants something done automatically (a morning brief, a setup that trades when a level breaks, plays sent to a group), or asks what a workflow did, how it performed, or to pause, change or delete one.
---

# Atlas workflows

A workflow is the person's plan, written once: what Atlas should read, what it
should decide, and what it should do about it. Atlas then runs it for them, on
a schedule, when an alert goes off, or when they press Run.

This page says what is possible. Nothing below is required unless it says so,
and a workflow with three fields set is a fine workflow.

- `references/tools.md`: every field each workflow tool accepts, with
  `Workflow-Create`'s own field-by-field description in full.
- `references/trade-card.json`: every field of a trade a workflow can place,
  with the rules and worked examples. `Trigger-Workflow-Schema` answers with
  the same thing live, plus the person's own alerts.

## The order that works

1. `Trigger-Workflow-Schema` when the workflow will place a trade or send a
   play, to see the trade's fields.
2. `Workflow-Preview` with what you intend, so the person sees it as a form
   before anything is saved.
3. `Workflow-Create`. A new workflow is saved **paused**.
4. `Workflow-Open` on the id that comes back, and check it reads the way you
   meant, the trade above all.
5. `Workflow-Update` with `status: "active"` when the person says to turn it
   on. `Workflow-Run` runs it once now, to try it.
6. `Workflow-Logs` for what each run decided and why; `Workflow-Performance`
   for the closed trades and the totals.

Do not have the id? `Workflow-List` has it. Never ask the person to paste one.

## What a workflow is made of

| Part | Field | What it can be |
|---|---|---|
| A name | `name` | Any label |
| What it is for | `purpose` | `analysis` reads and writes up, no broker. `trading` may place orders in the person's account. `draft` works out the trade and tells the person, who places it by hand. `alert_creator` sets up alerts each run, which other workflows can run on |
| What it does | `instruction` | Plain words: what to look at, what to decide, when to do nothing |
| What it reads | `tools` | Tool names, exactly as listed, e.g. `Stock-Quote`. A name that does not exist is dropped without an error |
| A note per tool | `tool_params` | `{ "Stock-Quote": { "notes": "SPY. Is it above yesterday's close?" } }`. One or two sentences on what to ask that tool for in this workflow |
| What it does at the end | `output_tools` | Analysis workflows only: tools to call once it has decided, e.g. `Signal-Post` |
| The trade | `output_schema` | Optional. `{ "triggers": [ ... ] }`, each entry one trade. See below |
| What starts it | `trigger_source` | `cron` (a schedule), `alert`, `both`, or `manual` (only Run now) |
| When | `schedule`, `timezone` | One line per time. `30 9 * * 1-5` repeats; `once 2026-11-03 09:35` runs that once. Eastern unless `timezone` says otherwise. `run_once_at` takes a list of dates and times and writes the lines for you |
| Which alert | `alert_id`, `alert_ids` | From `List-Alerts`. `alert_max_runs_per_day` caps how often an alert may run it |
| Where it trades | `snaptrade_account_id` | The broker account, from `Broker-Connections`. Needed to turn on a trading workflow |
| On or off | `status` | `paused` (the default) or `active` |
| Who can see it | `visibility` | `private` (the default), `unlisted`, `Atlas-public` |
| Told when it runs | `notify_discord_dm` | `true` (the default) sends the result as a Discord message |
| Check before it acts | `ui_schema.preview_before_place` | `true` holds each run for the person to approve, edit or throw away (`Workflow-Review`) |
| Questions before a manual run | `ui_schema.run_form` | Up to 20 questions the person answers when they press Run now |
| A journal | `journal_enabled`, `journal_instruction`, `journal_cadences` | Notes Atlas writes after trades or runs and reads back on later ones |

## The trade a workflow places

Each entry of `output_schema.triggers` is one trade. What it can carry:

- **What**: `symbol`, `asset_class` (`stock` or `option`), and for an option
  `option_type`, `strike`, `expiry`.
- **How much**: `contracts` (options) or `quantity` (shares), **or**
  `bracket_trade_budget`, the most to spend in dollars. One or the other.
  With a budget Atlas counts how many fit at the price actually paid.
- **Getting in**: `enter_side`, `enter_order_type` (`market` or `limit` with
  `enter_limit_price`), and optionally a price to wait for
  (`enter_trigger_operator`, `enter_trigger_value`) or a time (`enter_at_time`).
- **Getting out**: with `order_strategy: "bracket"`, a stop-loss and a
  take-profit, in dollars or percent. The stop is exactly one of
  `bracket_stop_loss_stop_price`, `bracket_stop_loss_stop_pct` or
  `bracket_stop_loss_trailing_pct` (follows the best price and only tightens).
- **Taking profit in steps**: `bracket_take_profit_levels`, a list such as
  `[{"pct": 30, "quantity": "50%"}, {"pct": 70, "quantity": "remaining"}]`.
  All levels in percent or all in dollars, never mixed. The last one takes
  whatever is left.
- **A time to be out by**: `exit_at_time`.
- **Either/or**: give two trades a `label` each and list the other's label in
  `cancels_labels`, and whichever fills first cancels the other (a call and a
  put on the same level).
- **Let Atlas pick the tickers**: `output_schema.trades_mode: "auto"` with
  exactly one entry as a template and its `symbol` left empty. Whatever is
  fixed on that entry (a stop, a size, a budget) applies to every trade a run
  makes.

Leave a value out, or set it to null, where the run should decide it. Never
invent a size, a budget or a stop the person did not ask for.

## Templates

These are shapes to start from, not rules. Change anything.

**A brief every weekday morning (reads only):**

```json
{
  "name": "Morning market brief",
  "purpose": "analysis",
  "trigger_source": "cron",
  "schedule": "30 9 * * 1-5",
  "tools": ["Multi-Timeframe-Price-Overview", "Stock-Quote", "Earnings-Calendar", "Web-Search"],
  "tool_params": {
    "Multi-Timeframe-Price-Overview": { "notes": "SPY. The trend and the levels that matter today." },
    "Stock-Quote": { "notes": "Each name on my list. What moved overnight." },
    "Earnings-Calendar": { "notes": "Today. Who reports." },
    "Web-Search": { "notes": "This morning's market headlines and what is moving each name." }
  },
  "instruction": "Write a short brief: the index trend, then one line per name on my list (AAPL, NVDA, MSFT) with what changed and why it matters."
}
```

**A trade when an alert goes off (the person approves each one first):**

```json
{
  "name": "SPY call on the breakout",
  "purpose": "trading",
  "trigger_source": "alert",
  "alert_id": "<an alert's id, from List-Alerts>",
  "alert_max_runs_per_day": 1,
  "snaptrade_account_id": "<the account, from Broker-Connections>",
  "tools": ["Stock-Quote", "Options-Chain"],
  "tool_params": {
    "Stock-Quote": { "notes": "SPY. Confirm it is still above the level the alert watched." },
    "Options-Chain": { "notes": "SPY, the nearest expiry. The call closest to the price." }
  },
  "instruction": "When the alert goes off and SPY is still above the level, buy the call nearest the price. If it has fallen back under, do nothing and say why.",
  "output_schema": {
    "triggers": [
      {
        "symbol": "SPY",
        "asset_class": "option",
        "option_type": "call",
        "strike": null,
        "expiry": null,
        "bracket_trade_budget": 500,
        "enter_side": "buy_to_open",
        "enter_order_type": "market",
        "order_strategy": "bracket",
        "bracket_stop_loss_stop_pct": -30,
        "bracket_take_profit_levels": [
          { "pct": 30, "quantity": "50%" },
          { "pct": 70, "quantity": "remaining" }
        ]
      }
    ]
  },
  "ui_schema": { "preview_before_place": true }
}
```

**A workflow that asks before it runs (pressed by hand):**

```json
{
  "name": "Size up a stock",
  "purpose": "analysis",
  "trigger_source": "manual",
  "tools": ["Stock-Quote", "Multi-Timeframe-Price-Overview", "Options-Flow", "Earnings-Dates"],
  "instruction": "For the stock I name: the trend, where the options money is going, and when it next reports. End with what would change the picture.",
  "ui_schema": {
    "run_form": {
      "enabled": true,
      "fields": [
        { "id": "sym", "label": "What stock are you looking at?", "type": "text", "required": true, "options": [] }
      ]
    }
  }
}
```

## Changing, pausing and removing

- `Workflow-Update` takes a `patch` with only what is changing. Everything
  left out stays as it is.
- A paused workflow is turned back on with `Workflow-Restore`.
- `Workflow-Review` shows a run that is waiting for approval, and places it,
  edits it or throws it away.
- `Workflow-Abort` stops a run in progress.
- `Workflow-Journal` reads and edits the journal; `Workflow-History` shows
  earlier versions and puts one back.
- `Workflow-Discover` and `Workflow-Import` find a public workflow and make
  the person a copy that follows its author. `Workflow-Follow` makes that copy
  their own, or follows the author again.
- `Workflow-Delete` removes one for good. Only when the person asks.

## What to keep in mind

- A trading workflow that is on places real orders in the person's account by
  itself. Turn one on only when they say so, and tell them what it will do.
- Changing an active workflow changes what its next run does. Say what you
  changed.
- If other people follow the person's workflow, their copies take the change
  too.
