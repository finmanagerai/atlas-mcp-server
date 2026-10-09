---
name: atlas-triggers-and-trades
description: Set up a direct trade that waits for a price (a trigger) with its stop-loss and take-profit, link trades so that one cancels or starts another (either/or pairs, also called OCO, and follow-ups), place an order now, and manage a trade that is open, in the person's own broker account through Atlas. Use when the person wants to buy or sell now, wants an order to go in when a level is reached, wants a call and a put where only one should fill, or wants to close, take profit on, or move the exits of a trade.
---

# Direct triggers, linked trades and open trades

A direct trade is one the person sets up themselves, with no workflow in
between. Four things, from the simplest up:

- An **order** goes to the broker now.
- A **trigger** is a trade that waits: Atlas watches the price and sends the
  order when the level is reached, then watches the stop-loss and the
  take-profit and closes the trade when one is hit.
- **Linked trades** are two or more triggers that know about each other:
  when one fills, another is cancelled, or another starts waiting.
- An **open trade** can be closed, partly taken off, or have its exits moved.

This page says what is possible. `references/tools.md` lists every field each
of these tools accepts, with the full description of the trade's shape.

## Before anything is placed

1. `Broker-Connections` for the person's accounts. With more than one, show
   the list and ask which. Never choose for them.
2. `Account-Balances` and `Account-Holdings` when the size depends on what
   they have.
3. Preview first. The person sees exactly what would go in, and says yes.

Everything here that places, changes or cancels uses real money. Do it only
when the person says to.

## An order now

1. `Preview-Order` with the `rule` and the `account_id`. Nothing is sent. It
   answers with a `preview_id` and a card the person can accept or cancel.
   `Preview-Multiple-Orders` stages several at once.
2. `Place-Order` with that `preview_id` when they say go.
3. `Cancel-Order` discards a preview, or cancels a placed order that is still
   waiting. `List-Preview-Orders` shows what is staged and what was placed.

## A trade that waits for a price

1. `Preview-Trading-Trigger` with the `rule`. It saves the trade switched off
   and shows it as a card.
2. The person turns it on from the card. When they tell you to instead,
   `Create-Trading-Trigger` with the `preview_id` turns that same one on.
3. `List-Trading-Triggers` shows the waiting and open ones;
   `List-Fired-Triggers` the finished ones.
4. `Update-Trading-Trigger` changes one, `Reactivate-Trigger` switches a
   finished or paused one back on, `Delete-Trading-Trigger` removes it.

## The shape of a trade (`rule`)

| Part | What it holds |
|---|---|
| `execution` | What is traded. Shares: `{ "asset_class": "stock", "quantity": 10 }`. An option: `{ "asset_class": "option", "option_type": "call", "expiry": "2026-11-20", "strike": 600, "contracts": 1 }` |
| `enter` | How to get in: `side` (`buy` or `sell` for shares, `buy_to_open` or `sell_to_open` for options), `order_type` (`market`, or `limit` with `limit_price`), and for a trigger the level to wait for: `trigger: { "metric": "price", "operator": "gte", "value": 600 }` |
| `order_strategy` | `bracket`: a stop-loss and a take-profit, whichever is reached first. `one_triggers_other`: one exit, with its own level to wait for |
| `exit` | With `bracket`: `stop_loss`, `take_profit`, or `take_profit_levels` |

What the exits can be:

- **A stop-loss**, one of: `{ "stop_price": 590 }`, `{ "stop_pct": -30 }`, or
  `{ "trailing_pct": 10 }` (follows the best price and only tightens).
- **One take-profit**: `{ "limit_price": 610 }`.
- **Taking profit in steps**: `take_profit_levels`, e.g.
  `[{ "pct": 30, "quantity": "50%" }, { "pct": 70, "quantity": "remaining" }]`.
  Every level in percent or every level in dollars. A level can move the stop
  once the one before it fills, with `stop_after_pct` or `stop_after_price`.
- **Sizing by money**: pass `trade_budget` in dollars instead of a count.

Two things to get right:

- **On an option, a dollar level is the stock's price**, not the option's. A
  percent is measured on the option's own price.
- **Which side the exits go on.** For a bought call or bought shares, the stop
  is below the entry and the target above. For a bought put it is the other
  way round: the put gains when the stock falls, so its target is below and
  its stop above. An exit on the wrong side closes the trade the moment it
  opens, and is refused.

Shares with a bracket need both a stop and a target, as prices.

## Linked trades

`Create-Trading-Trigger` takes `legs` instead of `rule` to make several
triggers as one set. Each leg is
`{ "rule": ..., "symbol": ..., "account_id": ..., "trade_budget": ... }`.

| The person wants | How |
|---|---|
| **Either/or (OCO)**: two trades, and whichever fills first cancels the other. A call above a level and a put below it | Two legs with `link_mode: "oco"` |
| **One starts the other (OEO)**: the second only begins waiting once the first has filled. An add-on, or a hedge after the entry | Two legs with `link_mode: "oeo"`. The second is saved switched off until then |
| **A bigger or mixed set** | Leave `link_mode` out. Give each leg's `rule` a `label`, and name the others in `cancels_labels` (cancel these when I fill) or `activates_labels` (start these when I fill) |

Things that hold for every set:

- **Every leg must be linked to the set.** A leg that names nobody and that
  nobody names is refused: two loose triggers would both fill.
- **All or nothing.** If one leg cannot be made, the ones already made are
  removed again.
- The answer's `link.legs` lists each leg's id, its label, whether it is on,
  and what it cancels or starts.

The same idea exists elsewhere under other names:

- In a **workflow's trade**, each entry of `output_schema.triggers` takes
  `label`, `cancels_labels` and `activates_labels` (see `atlas-workflows`).
- In a **play**, `second_leg` with `link_mode` (see `atlas-signals`).

## Templates

These are shapes to start from, not rules. Change anything.

**Buy 10 shares at a limit, with a stop and a target:**

```json
{
  "symbol": "NVDA",
  "rule": {
    "execution": { "asset_class": "stock", "quantity": 10 },
    "enter": { "side": "buy", "order_type": "limit", "limit_price": 900,
               "trigger": { "metric": "price", "operator": "lte", "value": 900 } },
    "order_strategy": "bracket",
    "exit": { "stop_loss": { "stop_price": 880 }, "take_profit": { "limit_price": 940 } }
  }
}
```

**Buy a call when the stock breaks a level, take half off at +30%:**

```json
{
  "symbol": "SPY",
  "rule": {
    "execution": { "asset_class": "option", "option_type": "call", "expiry": "2026-11-20", "strike": 600, "contracts": 2 },
    "enter": { "side": "buy_to_open", "order_type": "market",
               "trigger": { "metric": "price", "operator": "gte", "value": 600 } },
    "order_strategy": "bracket",
    "exit": {
      "stop_loss": { "stop_pct": -30 },
      "take_profit_levels": [
        { "pct": 30, "quantity": "50%" },
        { "pct": 70, "quantity": "remaining" }
      ]
    }
  }
}
```

**Put $500 into it, and let the stop follow the price:**

```json
{
  "symbol": "AAPL",
  "trade_budget": 500,
  "rule": {
    "execution": { "asset_class": "option", "option_type": "call", "expiry": "2026-11-20", "strike": 250 },
    "enter": { "side": "buy_to_open", "order_type": "market",
               "trigger": { "metric": "price", "operator": "gte", "value": 248 } },
    "order_strategy": "bracket",
    "exit": { "stop_loss": { "trailing_pct": 20 } }
  }
}
```

**Either/or: a call if it breaks up, a put if it breaks down:**

```json
{
  "link_mode": "oco",
  "legs": [
    {
      "symbol": "SPY",
      "rule": {
        "execution": { "asset_class": "option", "option_type": "call", "expiry": "2026-11-20", "strike": 601, "contracts": 1 },
        "enter": { "side": "buy_to_open", "order_type": "market",
                   "trigger": { "metric": "price", "operator": "gte", "value": 600.5 } },
        "order_strategy": "bracket",
        "exit": { "stop_loss": { "stop_pct": -30 }, "take_profit_levels": [{ "pct": 50, "quantity": "remaining" }] }
      }
    },
    {
      "symbol": "SPY",
      "rule": {
        "execution": { "asset_class": "option", "option_type": "put", "expiry": "2026-11-20", "strike": 598, "contracts": 1 },
        "enter": { "side": "buy_to_open", "order_type": "market",
                   "trigger": { "metric": "price", "operator": "lte", "value": 598.5 } },
        "order_strategy": "bracket",
        "exit": { "stop_loss": { "stop_pct": -30 }, "take_profit_levels": [{ "pct": 50, "quantity": "remaining" }] }
      }
    }
  ]
}
```

**One starts the other: buy shares, and only then start waiting to add:**

```json
{
  "link_mode": "oeo",
  "legs": [
    {
      "symbol": "NVDA",
      "rule": {
        "execution": { "asset_class": "stock", "quantity": 10 },
        "enter": { "side": "buy", "order_type": "limit", "limit_price": 900,
                   "trigger": { "metric": "price", "operator": "lte", "value": 900 } },
        "order_strategy": "bracket",
        "exit": { "stop_loss": { "stop_price": 880 }, "take_profit": { "limit_price": 940 } }
      }
    },
    {
      "symbol": "NVDA",
      "rule": {
        "execution": { "asset_class": "stock", "quantity": 10 },
        "enter": { "side": "buy", "order_type": "market",
                   "trigger": { "metric": "price", "operator": "gte", "value": 915 } },
        "order_strategy": "bracket",
        "exit": { "stop_loss": { "stop_price": 900 }, "take_profit": { "limit_price": 940 } }
      }
    }
  ]
}
```

**A set of three, linked by name.** Either entry cancels the other, and the
breakout starts a follow-up. Each `rule` also carries its `execution`,
`enter`, `order_strategy` and `exit`, as above:

```json
{
  "legs": [
    { "symbol": "SPY", "rule": { "label": "breakout", "cancels_labels": ["breakdown"], "activates_labels": ["add_on"] } },
    { "symbol": "SPY", "rule": { "label": "breakdown", "cancels_labels": ["breakout"] } },
    { "symbol": "SPY", "rule": { "label": "add_on" } }
  ]
}
```

## A trade that is open

| The person says | Tool |
|---|---|
| Close it | `Trade-Close` |
| Take the next target now | `Trade-Take-Profit` |
| Move the stop or the targets | `Trade-Edit-Exit` (`stop_pct`, `stop_price`, `trailing_pct`, `take_profit_pct`, `take_profit_price`, or `levels`) |
| Change where it gets in, before it has | `Trade-Edit-Entry` |
| Pull it before it has filled | `Trade-Cancel-Entry` |

The `trade_id` comes from `List-Trading-Triggers`.

When the trade was started by somebody else (a workflow the person follows, a
play they took), they can close their own position, and the exits stay the
author's to move.

## What to keep in mind

- Option orders go in during the regular session, 09:30 to 16:00 Eastern.
- A trade that is watched by Atlas closes at market when its stop is reached.
- When an answer says an order was not confirmed, it may still have gone
  through. Check the account before trying again.
