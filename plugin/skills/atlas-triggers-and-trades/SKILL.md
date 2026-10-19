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

This page says what is possible. Two references go with it:

- `references/trade-card-fields.md`: **every field of a trade**, by group, with
  its allowed values, what it applies to (stock, option, spread), what happens
  when it is left out, and worked examples on every road. Generated from the
  server; `Trigger-Workflow-Schema` answers with the same thing live.
- `references/tools.md`: every field each tool accepts.

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

## A trade that waits for a price: the trade card

`Preview-Trading-Trigger`, `Create-Trading-Trigger` and
`Update-Trading-Trigger` take the **trade card's fields as their own
parameters**: the same fields a workflow's trade and a script's `atlas.trade`
take, so one shape works everywhere.

Every trade needs three things:

1. **What**: `symbol` and `asset_class` (`"stock"` or `"option"`). An option
   adds `option_type` (`"call"` or `"put"`), `strike` and `expiry`
   (YYYY-MM-DD). A spread adds `spread_strategy` and `expiry`.
2. **How much**: `quantity` (shares), `contracts` (options) or `spreads`, **or**
   `bracket_trade_budget` in dollars (the count is worked out at the fill).
   One of them, never two.
3. **How it enters**: `enter_side` (`buy` / `sell`, or `buy_to_open` /
   `sell_to_open` on an option; not on a spread) and `enter_order_type`
   (`"market"`, or `"limit"` with `enter_limit_price`). To wait for a stock
   price first, add `enter_trigger_operator` (`lt`, `lte`, `gt`, `gte`, `eq`)
   and `enter_trigger_value`.

Exits are optional (no stop and no target is an entry only):

- **A stop**, one of: `bracket_stop_loss_stop_pct` (`-30` = the option's
  premium down 30%), `bracket_stop_loss_stop_price`, or
  `bracket_stop_loss_trailing_pct` (follows the best price, only tightens).
- **A target**, one of: `bracket_take_profit_limit_pct` (`50` = up 50%) or
  `bracket_take_profit_limit_price`; or several with
  `bracket_take_profit_levels`.
- **A time to be out by**: `exit_at_time`, an ISO date-time with its offset
  (`"2026-12-18T15:45:00-05:00"`).
- `order_strategy` is worked out from the exits you set when you leave it out.

Then:

1. `Preview-Trading-Trigger` with the card. It saves the trade switched off,
   shows it as a card, and answers with `understood` (the trade, the size, the
   entry and the exits, in words) and `warnings` (anything defaulted, worked
   out, or not used). Read both to the person. A wrong card is refused with
   every problem named by its field and what it allows.
2. The person turns it on from the card. When they tell you to instead,
   `Create-Trading-Trigger` with the `preview_id` turns that same one on.
3. `List-Trading-Triggers` shows the waiting and open ones;
   `List-Fired-Triggers` the finished ones.
4. `Update-Trading-Trigger` with the `trigger_id` and only the card fields you
   are changing (`bracket_stop_loss_stop_price: 4.2`, say).
   `Reactivate-Trigger` switches a finished or paused one back on,
   `Delete-Trading-Trigger` removes it.

Two things to get right:

- **On an option, a dollar level is the stock's price**, not the option's,
  unless `bracket_price_basis` is `"contract"`. A percent is measured on the
  option's own price.
- **Which side the exits go on.** For a bought call or bought shares, the stop
  is below the entry and the target above. For a bought put it is the other
  way round: the put gains when the stock falls, so its target is below and
  its stop above. An exit on the wrong side closes the trade the moment it
  opens, and is refused.

Shares with a bracket need both a stop and a target, as prices (or a trailing
stop).

The older `rule` object (`{order_strategy, execution, enter, exit}`) still
works: send the card fields or `rule`, not both.

## Linked trades

`Create-Trading-Trigger` takes `legs` instead of one card to make several
triggers as one set. Each leg is a card with its own `symbol` (or the older
`{ "rule": ..., "symbol": ..., "account_id": ..., "trade_budget": ... }`).
`Preview-Trading-Trigger` with the same `legs` checks each one and says it
back, saving nothing.

| The person wants | How |
|---|---|
| **Either/or (OCO)**: two trades, and whichever fills first cancels the other. A call above a level and a put below it | Two legs with `link_mode: "oco"` |
| **One starts the other (OEO)**: the second only begins waiting once the first has filled. An add-on, or a hedge after the entry | Two legs with `link_mode: "oeo"`. The second is saved switched off until then |
| **A bigger or mixed set** | Leave `link_mode` out. Give each leg a `label`, and name the others in `cancels_labels` (cancel these when I fill) or `activates_labels` (start these when I fill) |

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
`references/trade-card-fields.md` has more: an option with a limit entry, a
50% target, a stop and a close time; a ladder sized by a budget; an iron
condor; a credit put vertical with a stop on the stock; a debit call vertical.

**Buy 10 shares at a limit, with a stop and a target:**

```json
{
  "symbol": "NVDA", "asset_class": "stock", "quantity": 10,
  "enter_side": "buy", "enter_order_type": "limit", "enter_limit_price": 900,
  "enter_trigger_operator": "lte", "enter_trigger_value": 900,
  "bracket_stop_loss_stop_price": 880, "bracket_take_profit_limit_price": 940
}
```

**Buy a call when the stock breaks a level, take half off at +30%:**

```json
{
  "symbol": "SPY", "asset_class": "option", "option_type": "call",
  "expiry": "2026-11-20", "strike": 600, "contracts": 2,
  "enter_side": "buy_to_open", "enter_order_type": "market",
  "enter_trigger_operator": "gte", "enter_trigger_value": 600,
  "bracket_stop_loss_stop_pct": -30,
  "bracket_take_profit_levels": [
    { "pct": 30, "quantity": "50%" },
    { "pct": 70, "quantity": "remaining" }
  ]
}
```

**Put $500 into it, and let the stop follow the price:**

```json
{
  "symbol": "AAPL", "asset_class": "option", "option_type": "call",
  "expiry": "2026-11-20", "strike": 250, "bracket_trade_budget": 500,
  "enter_side": "buy_to_open", "enter_order_type": "market",
  "enter_trigger_operator": "gte", "enter_trigger_value": 248,
  "bracket_stop_loss_trailing_pct": 20
}
```

**Sell an iron condor for a net credit:**

```json
{
  "symbol": "SPY", "asset_class": "option", "spread_strategy": "iron_condor",
  "expiry": "0dte", "spreads": 2,
  "spread_legs_spec": { "sell_at": { "mode": "from_price", "value": 10 },
                        "buy_at": { "mode": "further_out", "value": 5 } },
  "enter_order_type": "limit", "enter_limit_price": 1.20,
  "spread_take_profit_pct": 50,
  "spread_stop": { "basis": "premium", "max_loss_pct": 50 },
  "spread_close_at": "15:45"
}
```

Every leg of a spread goes to the broker as ONE order at a net price; the
strikes follow the stock's price until it is placed. `Spread-Quote` shows each
leg's bid and ask and the net now.

**Either/or: a call if it breaks up, a put if it breaks down:**

```json
{
  "link_mode": "oco",
  "legs": [
    { "symbol": "SPY", "asset_class": "option", "option_type": "call", "expiry": "2026-11-20",
      "strike": 601, "contracts": 1, "enter_side": "buy_to_open", "enter_order_type": "market",
      "enter_trigger_operator": "gte", "enter_trigger_value": 600.5,
      "bracket_stop_loss_stop_pct": -30, "bracket_take_profit_limit_pct": 50 },
    { "symbol": "SPY", "asset_class": "option", "option_type": "put", "expiry": "2026-11-20",
      "strike": 598, "contracts": 1, "enter_side": "buy_to_open", "enter_order_type": "market",
      "enter_trigger_operator": "lte", "enter_trigger_value": 598.5,
      "bracket_stop_loss_stop_pct": -30, "bracket_take_profit_limit_pct": 50 }
  ]
}
```

**One starts the other: buy shares, and only then start waiting to add:**

```json
{
  "link_mode": "oeo",
  "legs": [
    { "symbol": "NVDA", "asset_class": "stock", "quantity": 10, "enter_side": "buy",
      "enter_order_type": "limit", "enter_limit_price": 900,
      "enter_trigger_operator": "lte", "enter_trigger_value": 900,
      "bracket_stop_loss_stop_price": 880, "bracket_take_profit_limit_price": 940 },
    { "symbol": "NVDA", "asset_class": "stock", "quantity": 10, "enter_side": "buy",
      "enter_order_type": "market", "enter_trigger_operator": "gte", "enter_trigger_value": 915,
      "bracket_stop_loss_stop_price": 900, "bracket_take_profit_limit_price": 940 }
  ]
}
```

**A set of three, linked by name.** Either entry cancels the other, and the
breakout starts a follow-up. Each leg also carries its own card fields, as
above:

```json
{
  "legs": [
    { "symbol": "SPY", "label": "breakout", "cancels_labels": ["breakdown"], "activates_labels": ["add_on"] },
    { "symbol": "SPY", "label": "breakdown", "cancels_labels": ["breakout"] },
    { "symbol": "SPY", "label": "add_on" }
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
- When a stop is reached Atlas closes with a marketable limit (the bid less a
  small allowance, re-priced twice, then market); a target sells as a limit
  at its own price.
- When an answer says an order was not confirmed, it may still have gone
  through. Check the account before trying again.
