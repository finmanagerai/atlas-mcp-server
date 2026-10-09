---
name: atlas-signals
description: Post, read, take and manage plays (signals) on Atlas, where a play is one trade idea written down in full and shared with a board or a group. Use when the person wants to post a trade call, read what was posted, take a play into their own account, follow a group, or change how plays are handled for them.
---

# Plays (signals)

A play is one trade somebody is calling: what to buy, where to get in, where
to take profit, where to get out, and how much. It is posted to the community
board or to a group, and the people who follow it can take it.

This page says what is possible. Almost every field is optional: a play can be
as little as a contract and "take it now".

- `references/play.json`: every field of a play, the rule about units, and
  worked examples. `Signal-Schema` answers with the same thing live.
- `references/tools.md`: every field each play tool accepts.

## Posting one

1. `Signal-Groups` for where the person can post: the community board, and
   the groups they own or may post in. Use an id from it as `group_id`; leave
   `group_id` out for the board.
2. `Signal-Post` with what the person said, and nothing they did not say.
3. To change one that is up, `Signal-Update`, not a second post: posting again
   leaves both on the board. `Signal-Delete` takes one down.

Posting is a real action. The play is visible to other people at once, people
who chose automatic taking get an order placed for them, and with
`trade_for_me` the person's own order goes in too. Post only what they said.

### What a play can carry

| Part | Fields | Notes |
|---|---|---|
| The contract | `symbol`, `asset_class` (`option` or `stock`), `side`, `option_type`, `strike`, `expiration_date` | Only `symbol` is required |
| Getting in | `entries` (`[{ "price": 2.10 }]`) or `entry`, with `entry_unit` | Leave empty for "take it now, at market" |
| Taking profit | `tps` (`[{ "target": 50, "quantity": "50%" }, ...]`) with `tp_unit` | `quantity` is `"50%"`, a count, or `"remaining"`; the last takes what is left |
| Getting out | `stop` with `stop_unit` | Written as a positive number |
| How much | `contracts` or `quantity`, **or** `trade_budget` in dollars | One or the other |
| When | `enter_at`, `exit_at` | Optional times to get in by, or be out by |
| Why, and how sure | `reason`, `score` (1 to 10) | A play with no score counts as 10 |
| Where | `group_id` | Empty for the community board |
| In it yourself | `trade_for_me`, `snaptrade_account_id` | Places the author's own order |
| Two trades, one idea | `second_leg`, `link_mode` | `"oco"`: whichever fills first cancels the other. `"oeo"`: the second starts only once the first fills |

### The one thing that goes wrong: units

Every number has a unit field saying what it is measured in. On a 780 call:

- `2.10` is the option's own price: `"contract"`
- `773` is the stock's price: `"price"`
- `50` is a percentage: `"pct"`

`entry_unit` is `contract` or `price`. `tp_unit` is `pct`, `contract` or
`price`. `stop_unit` is those three or `trail` (a stop that follows the best
price). When what the person said does not settle it, ask them. A wrong unit
is a different trade.

### Templates

**Buy the calls at a price, two targets, a stop:**

```json
{
  "symbol": "SPY", "option_type": "call", "strike": 780, "expiration_date": "2026-11-20",
  "entries": [{ "price": 2.10 }], "entry_unit": "contract",
  "tps": [{ "target": 50, "quantity": "50%" }, { "target": 100, "quantity": "remaining" }],
  "tp_unit": "pct",
  "stop": 30, "stop_unit": "pct",
  "reason": "Holding above yesterday's high with call buying on the tape.",
  "score": 7
}
```

**Wait for the stock to pull back, then buy:**

```json
{
  "symbol": "SPY", "option_type": "call", "strike": 780, "expiration_date": "2026-11-20",
  "entries": [{ "price": 773 }], "entry_unit": "price", "entry_operator": "lte",
  "tps": [{ "target": 50, "quantity": "remaining" }], "tp_unit": "pct",
  "trade_budget": 500
}
```

**Take it now, the author will call the exit:**

```json
{ "symbol": "SPY", "option_type": "put", "strike": 772, "expiration_date": "2026-11-20", "entries": [], "tps": [] }
```

**A call and a put on the same level, whichever fills first:**

```json
{
  "symbol": "SPY", "option_type": "call", "strike": 780, "expiration_date": "2026-11-20",
  "entries": [{ "price": 781 }], "entry_unit": "price", "entry_operator": "gte",
  "second_leg": {
    "symbol": "SPY", "option_type": "put", "strike": 778, "expiration_date": "2026-11-20",
    "entries": [{ "price": 777 }], "entry_unit": "price", "entry_operator": "lte"
  },
  "link_mode": "oco"
}
```

## Reading and taking

- `Signal-List` reads a board a page at a time: `board` is `community` or
  `private`, or pass one `group_id`. `Signal-Show` shows one play.
- `Signal-Take` takes a play into the person's own account. It can carry
  their own size (`contracts`), their own limit for the trade
  (`max_per_trade`), and the account. Taking places a real order.
- `Signal-My-Order` changes or pulls the person's own order on a play.
- `Signal-Pending` and `Signal-Answer` are for plays waiting on the person's
  yes or no.

## Groups and following

- `Signal-Discover` finds public groups. `Signal-Follow` follows one or stops,
  and sets how its plays are handled: `accept_mode` is `manual` (the default:
  nothing is placed, each play is taken by hand) or `auto` (each new play is
  placed for the person, sized from their budget).
- `Signal-Trade-Settings` reads and saves the person's defaults: which
  account, and the budget for one trade.
- `Signal-Group-Create`, `Signal-Group-Update` and `Signal-Group-Performance`
  are for a group the person runs.

## Once a play is a trade

Only the author steers it: `Trade-Take-Profit` and `Trade-Edit-Exit` are the
author's. Somebody who took a play can close their own position with
`Trade-Close`. See the `atlas-triggers-and-trades` skill.

## What to keep in mind

- Ask for targets. A play with none is allowed, and is rarely what was meant.
- Never send a size and a budget together.
- Switch a follow to `auto` only when the person asks for it: from then on
  orders are placed for them without a question each time.
