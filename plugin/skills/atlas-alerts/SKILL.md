---
name: atlas-alerts
description: Create, preview, change and read Atlas alerts, which tell the person when something happens in the market and can start a workflow when it does. Use when the person wants to be told about a price level, a large options trade, a move in dealer exposure, a volume spike, a technical cross, or their own trades, or asks what alerts they have and when they went off.
---

# Atlas alerts

An alert watches the market for one thing and tells the person when it
happens. It can also start a workflow, so the plan runs at that moment.

This page says what is possible. An alert needs a name, a type and, for most
types, a ticker; everything else is optional.

- `references/alert-types.json`: every alert type, the conditions each one
  takes, the settings they all share, and a worked example per type.
  `List-Alert-Types` answers with the same thing live.
- `references/tools.md`: every field each alert tool accepts.

## The order that works

1. `List-Alert-Types` (or the reference file) to find the type that matches
   what the person asked for, and copy its example's shape.
2. `Preview-Alert` with the same fields. It checks the alert against recent
   market activity and shows how often it would have gone off, without saving.
3. `Create-Alert` once the person is happy with it.
4. `List-Alerts` shows what they have; `Alert-Fires` shows when each went off.
5. `Update-Alert` takes `alert_id` and `updates` with only what is changing.
   `Delete-Alert` removes one.

## The types

| The person wants to know when | `alert_type` | Main conditions |
|---|---|---|
| A big options trade prints on a ticker | `flow` | `min_premium`, `trade_type` (`sweep`, `block`), `action` (`buy`, `sell`), `min_size`, a strike or an expiry |
| A new trade enters the top of the day's flow, any ticker | `flow_rank` | `top_n` |
| The top 20 flow changes, any ticker | `top_flow` | `top_n` |
| Price crosses a level | `price` | `level`, `direction` (`above`, `below`) |
| One option's own price crosses a level | `contract_price` | `strike`, `expiration_date`, `cp`, `level`, `direction` |
| The biggest dealer-exposure level moves, or exposure changes sides | `king_node` | `metric` (`gamma`, and the other greeks), `move_mode` |
| Price comes near, or crosses, that level | `level_approach` | `metric`, `within_pct`, `region_mode` |
| Volume jumps | `volume_spike` | `threshold_pct` |
| The busiest contract changes | `volume_shift` | none needed |
| Calls or puts take the lead | `options_ratio` | `ratio_source`, `ratio_trigger`, `lead_side`, `lead_x` |
| Price or an indicator crosses another | `technicals` | `watch`, `target` (e.g. `20ema`), `direction`, `timeframe` |
| One of their own trades acts | `trigger_event` | `events` (e.g. `placed`) |

`flow_rank`, `top_flow` and `trigger_event` take no ticker. Every other type
needs `symbol`.

## Settings every alert can carry

| Setting | What it does |
|---|---|
| `conditions.active_from_time`, `active_to_time` | Only watch between these Eastern times, e.g. `09:30` to `11:00` |
| `conditions.active_days` | `weekdays`, or leave out for every day |
| `cooldown_seconds` | The least time between two alerts |
| `conditions.fire_on_start` | Also go off once at the start of each day's window |
| `conditions.expiration_date`, `expiration_range` | Look at one expiry, or a range of them, on the exposure types |
| `notify_discord` | `true` (the default) sends a Discord message when it goes off |
| `notes` | A note that travels with the alert to the workflow it starts |
| `expires_at` | Stop watching after this time |
| `is_active` | `false` saves it switched off |

## Starting something when it goes off

`on_fire` says what else happens, on top of the message:

- `workflow_ids`: run these workflows. This is how a plan trades at the
  moment its level breaks. A workflow can also name the alert itself, with
  `alert_id` on the workflow.
- `reactivate_trigger_ids`: switch these waiting trades back on.
- `trigger`: set up a new waiting trade.
- `order`: place an order at once. This sends a real order with nobody
  watching, so use it only when the person asks for exactly that.

## Templates

**Large call sweeps on one name, mornings only:**

```json
{
  "name": "NVDA big call sweeps",
  "symbol": "NVDA",
  "alert_type": "flow",
  "conditions": {
    "trade_type": "sweep", "action": "buy", "min_premium": 250000,
    "active_from_time": "09:30", "active_to_time": "11:30", "active_days": "weekdays"
  }
}
```

**Price over a level, and run a workflow when it happens:**

```json
{
  "name": "SPY over 600",
  "symbol": "SPY",
  "alert_type": "price",
  "conditions": { "level": 600, "direction": "above" },
  "on_fire": { "workflow_ids": ["<a workflow's id, from Workflow-List>"] },
  "notes": "Only take it if the move comes on rising volume."
}
```

**The main gamma level moves:**

```json
{ "name": "SPY gamma level moves", "symbol": "SPY", "alert_type": "king_node", "conditions": { "metric": "gamma" } }
```

**Price crosses the 20 EMA on the 5-minute chart:**

```json
{
  "name": "SPY over its 20 EMA",
  "symbol": "SPY",
  "alert_type": "technicals",
  "conditions": { "watch": "price", "target": "20ema", "direction": "above", "timeframe": "5m" }
}
```

**Tell me when my own trade is placed:**

```json
{ "name": "My trades", "alert_type": "trigger_event", "conditions": { "events": ["placed"] } }
```

## What to keep in mind

- Use only the condition names the type lists. A name it does not know is
  refused.
- An alert that starts a trading workflow leads to real orders. Say so when
  you connect one.
- Alerts are checked during market hours, 09:30 to 16:00 Eastern.
