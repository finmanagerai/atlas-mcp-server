# The trade card: every field

GENERATED from Trigger-Workflow-Schema (the engine's own field catalog); do not edit by hand.

One shape on every road:

- Preview-Trading-Trigger / Create-Trading-Trigger / Update-Trading-Trigger: pass the card fields as top-level parameters (symbol, asset_class, ...). Preview first: it answers with what it understood (entry, size, exits, legs) and warnings for anything ignored or defaulted. The older `rule` object (the nested shape) still works.
- A linked set (OCO / OEO) on the trigger tools: Create-Trading-Trigger with legs = [{card fields...}, ...] and link_mode "oco" or "oeo"; Preview-Trading-Trigger with the same legs checks them without saving.
- A workflow: Workflow-Create / Workflow-Update output_schema = {"triggers": [card, ...]} (order_strategy is required there).
- A script workflow: atlas.trade(**card) in main.py, one call per trade (atlas.trade checks each field before the run hands in).

## Every trade needs

1. WHAT: symbol + asset_class ("stock" | "option"); an option also needs option_type, strike, expiry; a spread needs spread_strategy + expiry (and spread_side + spread_direction for a vertical).
2. HOW MUCH: quantity (shares), contracts (options) or spreads (a spread), OR bracket_trade_budget in dollars. One of them, never two.
3. HOW IT ENTERS: enter_side (not on a spread) and enter_order_type ("market", or "limit" with enter_limit_price). Add enter_trigger_operator + enter_trigger_value to wait for a stock price first.

## Fields

`For` says which trades read the field (stock, option, spread). `Left out` is what happens without it. The last column is the whole rule.

### What to trade

The ticker, stock or option, and for an option its type, strike and expiry.

| Field | Type | Allowed | For | Left out | What it is |
|---|---|---|---|---|---|
| `symbol` | string |  | stock/option/spread |  | The ticker, e.g. "SPY". Required.<br>The ticker, e.g. "SPY". On a workflow card left null (auto mode) the run picks it. |
| `asset_class` | string | `stock`, `option` | stock/option/spread |  | "stock" or "option" (a spread is "option").<br>Stock or options contract |
| `option_type` | string | `call`, `put` | option |  | "call" or "put". Required for an option.<br>Call or put |
| `strike` | number |  | option |  | The strike in dollars, one the chain lists. Required for an option.<br>Option strike in dollars. Must be a concrete number the chain exposes. |
| `expiry` | date |  | option/spread |  | YYYY-MM-DD. A spread also takes "0dte" or "friday".<br>Option expiration as YYYY-MM-DD. |

### How much

A count (contracts or shares, or whole spreads) OR a budget in dollars, never both.

| Field | Type | Allowed | For | Left out | What it is |
|---|---|---|---|---|---|
| `contracts` | integer |  | option |  | How many option contracts (a whole number). Or give bracket_trade_budget instead.<br>Positive integer number of option contracts. |
| `quantity` | number |  | stock |  | How many shares. Or give bracket_trade_budget instead.<br>Positive number of shares. |
| `bracket_trade_budget` | number |  | stock/option/spread |  | The most to spend on this trade, in dollars; the count is worked out at the fill. Never with contracts / quantity / spreads.<br>The most this trade may spend, in dollars. When the author sets it the SIZE is not authored at all: the worker works out how many contracts / shares fit at the premium the order actually pays, landing as close under the budget as whole units allow. OMIT `contracts` / `quantity` entirely when this is set — anything you put there is discarded. Never invent a budget: echo the template value or leave it out. |
| `spreads` | integer |  | spread |  | How many whole spreads. Or give bracket_trade_budget instead.<br>Whole spreads (each leg goes for spreads x its ratio). Or give bracket_trade_budget instead: the budget over the most ONE spread can lose, floored, worked out at the fill. |

### Entry

Buy or sell, market or limit, and an optional price to wait for before entering.

| Field | Type | Allowed | For | Left out | What it is |
|---|---|---|---|---|---|
| `enter_side` | string | `buy`, `sell`, `buy_to_open`, `sell_to_open` | stock/option |  | Stock: "buy" or "sell". Option: "buy_to_open" or "sell_to_open" ("buy"/"sell" are accepted).<br>shares: 'buy' or 'sell'. options: 'buy_to_open' or 'sell_to_open' (plain buy/sell are accepted and resolved). |
| `enter_order_type` | string | `market`, `limit` | stock/option/spread |  | "market" or "limit".<br>market fills immediately; limit waits for the price. |
| `enter_limit_price` | number |  | stock/option/spread |  | The limit price (an option: its premium; a spread: the NET). Required when enter_order_type is "limit".<br>Required when enter_order_type is limit. |
| `enter_trigger_metric` | string | `price`, `ask`, `bid`, `last` | stock/option/spread | "price" | Leave it "price" (or out).<br>Leave it as "price" (or omit it). The worker compares against the live price whatever this says — bid/ask/last are accepted for old rules but behave identically, so this is not a decision to spend time on. Whether there IS a watch is decided by enter_trigger_value, not by this. |
| `enter_trigger_operator` | string | `lt`, `lte`, `gt`, `gte`, `eq` | stock/option/spread |  | lt \| lte \| gt \| gte \| eq: how the stock price compares with enter_trigger_value.<br>Compare metric to enter_trigger_value. Must be one of: lt, lte, gt, gte, eq. Omit for a market/immediate entry. |
| `enter_trigger_value` | number |  | stock/option/spread | enter right away | A STOCK price to wait for before entering. Leave out to enter now.<br>Price the worker watches before entering. Set it (with metric + operator) to WAIT for a level. OMIT it (None) to enter right away. It is INDEPENDENT of enter_order_type: a watch decides WHEN, the order type decides HOW — watching a price and then buying at market is the normal case. |

### Exits

The stop and the take-profit (a bracket), or a second price watch (one_triggers_other).

| Field | Type | Allowed | For | Left out | What it is |
|---|---|---|---|---|---|
| `order_strategy` | string | `bracket`, `one_triggers_other` | stock/option | bracket when a stop or target is set, one_triggers_other when an exit watch is set (the trigger tools and atlas.trade work it out; a workflow card must say it) | "bracket" (a stop and/or target) or "one_triggers_other" (a second price watch).<br>bracket = broker-managed stop+target (OCO). one_triggers_other = worker evaluates a second watch. |
| `bracket_stop_loss_stop_price` | number |  | stock/option |  | Stop at a price: the share price (stock), the STOCK price (option, unless bracket_price_basis is "contract").<br>For options: UNDERLYING price level (unless bracket_price_basis is "contract") — when SPY reaches this, Atlas closes the option at MARKET (or one limit at bracket_stop_loss_limit_price, if set; a limit entry with no stop limit closes as a limit at the stop only on the contract basis). NOT the contract price. For stocks: broker-managed stop trigger on the share price. WHICH SIDE: a stop sits where the trade LOSES — BELOW the entry for long stock / a long CALL / a short put, ABOVE it for short stock / a long PUT / a short call. A long put profits as the underlying FALLS, so its stop is above. A stop on the wrong side is already true at entry and is REJECTED at compile. |
| `bracket_stop_loss_limit_price` | number |  | stock/option | as the entry: a limit entry closes the stop as a limit at the stop's price, a market entry at market | How the stop closes: one limit at this price.<br>Optional. How the stop closes when you want a limit at your own price. Stocks with a broker bracket: turns the broker stop into a stop-limit order at this share price. Options (and stocks the worker manages): when the stop is reached, Atlas cancels its open take-profit orders and sends ONE day limit at this price (a contract premium for an option), with no allowance, rounded to the tick in your favour; if the market is already through it the order rests. Leave it empty and the stop follows the ENTRY: a limit entry closes the stop as a limit at the stop's own price (a premium on the contract basis, a share price for a stock), a market entry closes it at MARKET. A stop measured on the STOCK price of an option has no premium to use, so it closes at market. |
| `bracket_stop_loss_stop_pct` | number |  | option |  | Stop as a % move of the option premium from the fill, negative: -30 = close when it has lost 30%.<br>Percent move from entry — e.g. -35 closes when the contract premium drops 35% from fill. Mutually exclusive with the $ variant; pick one. |
| `bracket_stop_loss_trailing_pct` | number |  | stock/option |  | A trailing stop: % behind the best price since the fill. Instead of the other two stops.<br>A TRAILING stop, for shares and options: a distance in percent behind the best price since the entry (the SHARE price on a stock, the contract premium on an option), tightening only — 10 closes when the price gives back 10% from its best since the fill. It IS the stop: mutually exclusive with bracket_stop_loss_stop_price and bracket_stop_loss_stop_pct; send exactly one of the three. Always positive. |
| `bracket_take_profit_limit_price` | number |  | stock/option |  | Target at a price: the share price (stock), the STOCK price (option, unless bracket_price_basis is "contract").<br>For options: UNDERLYING price level (unless bracket_price_basis is "contract") — when SPY reaches this, Atlas sells the option at market, or as a limit when exit_order_type is limit or (exit_order_type left out) the entry was a limit. NOT the contract price. For stocks: broker-managed sell limit on the share price. WHICH SIDE: a target sits where the trade WINS — ABOVE the entry for long stock / a long CALL / a short put, BELOW it for short stock / a long PUT / a short call. A target on the wrong side is already true at entry and is REJECTED at compile. |
| `bracket_take_profit_limit_pct` | number |  | option |  | Target as a % gain on the option premium: 50 = sell when it is up 50%.<br>Percent move from entry — e.g. 40 closes when the contract premium rises 40% from fill. Mutually exclusive with the $ variant; pick one. |
| `bracket_price_basis` | string | `contract` | option | the stock price | "contract" = $ stop/target levels are the OPTION premium, not the stock price.<br>Set to "contract" when the take-profit / stop levels are the OPTION's own price rather than the underlying. A $ level then means "the contract trades at this premium", which is how the Triggers form, the Discord bot and signal plays already express them. Percent levels are contract-priced by definition and need no basis. Omit for underlying levels — that is the default and covers every stock leg. |
| `exit_order_type` | string | `market`, `limit` | stock/option | as the entry: a limit entry sells at the target as a limit, a market entry at market | How the take-profit is sent: "market", or "limit" (at exit_limit_price, or with none at the target). The time close, close-all and an AI exit are always market.<br>How the TAKE-PROFIT close is sent (the card's "Same as entry \| Market \| Limit"; for one_triggers_other, how the exit watch's close is sent). "market": market, even after a limit entry. "limit": a limit at exit_limit_price, or with no exit_limit_price a limit AT THE TARGET. Left out = SAME AS ENTRY: a limit entry sells as a limit at the target, a market entry at market. A level's own close_limit_price always wins. The stop has its own choice (bracket_stop_loss_order_type); a time close is always market. |
| `bracket_stop_loss_order_type` | string | `market`, `limit` | stock/option | as the entry: a limit entry closes the stop as a limit at the stop's price, a market entry at market | How the stop closes: "market", or "limit" (at bracket_stop_loss_limit_price, or with none at the stop's own price).<br>How the STOP closes (the card's "Same as entry \| Market \| Limit"). "market": market, even after a limit entry. "limit": a Day limit at bracket_stop_loss_limit_price, or with no limit price at the stop's own price (a premium on the contract basis, the share price for a stock; a trailing stop at its trailed level), never chased: if the market is already through it, it rests. Left out = SAME AS ENTRY: a limit entry closes the stop as a limit at the stop's price, a market entry at market. A stop measured on the STOCK price of an option has no premium for a limit, so it closes at market. Needs a stop (bracket_stop_loss_stop_price / _stop_pct / _trailing_pct). |
| `exit_limit_price` | number |  | stock/option |  | The price on the take-profit's limit (option premium or share price). Optional: left out, a limit sells at the target. Required for an exit watch set to "limit".<br>Optional CONTRACT price the limit CLOSE rests at (option premium, or share price for stocks). Left out with exit_order_type "limit", a take-profit sells as a limit AT ITS TARGET (a stock-price target on an option: at the live bid). Required only for a one_triggers_other exit watch set to limit. This is NOT an underlying threshold; it is the price on the close order. |
| `exit_trigger_metric` | string | `price`, `ask`, `bid`, `last` | stock/option | "price" | one_triggers_other only. Leave it "price".<br>Leave it as "price" (or omit it) — same as the entry watch metric, the worker compares against the live price whatever this says. Omit exit_trigger_value for an enter-only trade with no exit watch. |
| `exit_trigger_operator` | string | `lt`, `lte`, `gt`, `gte`, `eq` | stock/option |  | one_triggers_other only: lt \| lte \| gt \| gte \| eq, pointing AWAY from the entry.<br>Comparison operator for the exit watch. Must be one of: lt, lte, gt, gte, eq. NOT the same as enter_trigger_operator — they point OPPOSITE ways. The exit must not already hold at the price the entry fires: a stop under a `gte 500` breakout entry is `lte 490`, never `lte 520` (already true at 500) and never `gte` anything at or below 500. Omit for an enter-only trade. |
| `exit_trigger_value` | number |  | stock/option |  | one_triggers_other only: the stock price that closes the trade.<br>Target price for the exit watch. OMIT it (None) for an enter-only trade with no second watch. |

### Take-profit ladder

Several targets, each selling part of the position, with an optional stop move after each.

| Field | Type | Allowed | For | Left out | What it is |
|---|---|---|---|---|---|
| `bracket_take_profit_levels` | array |  | stock/option/spread |  | Several targets: [{pct \| price, quantity, stop_after_pct?, stop_after_price?, close_limit_price?}]. Instead of a single target.<br>Scaled multi-level take-profit ("multi ladder view") — an ARRAY, one object per level, e.g. [{"pct":30,"quantity":"50%","stop_after_pct":20},{"pct":70,"quantity":"remaining"}]. Each level: EXACTLY ONE of `price` ($ level — UNDERLYING for options) or `pct` (% move from the entry contract premium, positive). ALL levels MUST share ONE unit — every level `pct` OR every level `price`, NEVER a mix (a mixed ladder is rejected at compile). `quantity` is a number of contracts/shares, a percent string like "40%", or "remaining"; the LAST level should be "remaining". TRAILING STOP per level (moves the stop-loss AFTER that level fills): give `stop_after_pct` for a % trailing stop (% from entry premium; may be positive = lock in profit) OR `stop_after_price` for a $ one — pick at most ONE. NEVER on the FIRST level: a level's stop_after arms when the PREVIOUS target fills, so level 0 has none and the trade's own stop-loss owns the run to TP1. Set that key to null to let Atlas DECIDE the trailing stop at run time (a template AI slot the decision step fills — like a null price/pct); OMIT both keys to keep the current stop. Mutually exclusive with the single bracket_take_profit_limit_price / _pct. |
| `bracket_take_profit_loop` | boolean |  | stock/option | false | Workflows only: re-run the AI after each target to re-decide the rest.<br>Boolean. Only with bracket_take_profit_levels. When true, after each level fills the workflow re-runs and the AI re-decides the remaining ladder. Echo the template value verbatim; never invent it. |
| `bracket_exit_split` | string | `follow`, `front`, `back`, `even` | stock/option/spread | "follow" (the amounts as written) | How much comes off at each target: follow \| front \| back \| even.<br>How much of the position comes off at each take-profit level: "follow" (the amounts as written — the default), "front" (most out at the first target), "back" (most left on for the last), "even" (the same at each). Only affects a ladder with 2+ levels; the last level always closes whatever is left. Echo the template value verbatim; never invent it. |

### Timing

A clock time to enter at, and a clock time to close whatever is left.

| Field | Type | Allowed | For | Left out | What it is |
|---|---|---|---|---|---|
| `enter_at_time` | string |  | stock/option/spread |  | Enter at this clock time (ISO-8601 WITH an offset), or at the entry watch, whichever comes first.<br>Absolute date+time to ENTER at, ISO-8601 with an offset (e.g. "2026-07-10T09:35:00-04:00" or "2026-07-10T13:35:00Z"). Whichever comes first — this clock time OR the entry watch price — fires the entry. Leave None to ignore; AI may set it. A time-only entry (no watch price) is allowed. |
| `exit_at_time` | string |  | stock/option/spread | none: nothing closes it by the clock | Close whatever is left at this clock time (ISO-8601 WITH an offset), at market, or at the stop/target, whichever comes first. Only when you set it.<br>Absolute date+time to FORCE-CLOSE at, ISO-8601 with an offset (e.g. "2026-07-10T15:55:00-04:00" or "2026-07-10T19:55:00Z"). Whichever comes first — this clock time OR the SL/TP (or exit watch) — closes ALL remaining at market. Leave None and there is NO time close: nothing closes the trade by the clock unless it is set here. AI may set it. |

### Linked trades

Two or more trades that cancel (OCO) or start (OEO) each other.

| Field | Type | Allowed | For | Left out | What it is |
|---|---|---|---|---|---|
| `oco_group` | string |  | stock/option/spread |  | A label shared by trades of one run: the first to fill cancels the rest.<br>Optional label. Triggers in the same workflow run that share this label form a one-cancels-others basket — when one fires, the rest deactivate. Works cross-ticker. |
| `label` | string |  | stock/option/spread |  | A name for this trade so others can point at it.<br>Optional name for THIS trigger/leg so other legs in the same run can reference it via cancels_labels (OCO) or activates_labels (OEO). Cross-ticker is fine — the label is the only key. |
| `cancels_labels` | array |  | stock/option/spread |  | Labels of the trades this one CANCELS when it fills (OCO).<br>Optional ARRAY of other legs' `label` values. When THIS leg fires it DEACTIVATES those legs (one-cancels-others). Use for a call+put pair where the first to fill kills the other. (oco_group is the simpler symmetric form; cancels_labels is the explicit directed form.) |
| `activates_labels` | array |  | stock/option/spread |  | Labels of the trades this one STARTS when it fills (OEO).<br>Optional ARRAY of other legs' `label` values. When THIS leg fires it ARMS those legs (one-triggers-other) — e.g. an entry leg that, once filled, activates a staged hedge leg. |

### Spreads

Vertical, iron condor, butterfly, iron butterfly, straddle, strangle: one multi-leg order at a net price.

| Field | Type | Allowed | For | Left out | What it is |
|---|---|---|---|---|---|
| `spread_strategy` | string | `vertical`, `iron_condor`, `butterfly`, `iron_butterfly`, `straddle`, `strangle` | spread |  | Makes the card a spread: vertical \| iron_condor \| butterfly \| iron_butterfly \| straddle \| strangle.<br>Makes this card a SPREAD: every leg goes to the broker as ONE multi-leg order at a net price, never a leg on its own. vertical (needs spread_side + spread_direction), iron_condor, butterfly (middle x2), iron_butterfly, straddle, strangle. A spread card uses the spread_* fields below and none of the single option's (option_type, strike, bracket_stop_loss_*, bracket_take_profit_limit_*). |
| `spread_side` | string | `credit`, `debit` | spread |  | A vertical: "credit" or "debit".<br>A vertical spread: credit (sell the strike nearer the money, buy one further out) or debit (buy near the money, sell further toward the target). The other strategies are what they are: iron condor and iron butterfly credit; butterfly, straddle, strangle debit. |
| `spread_direction` | string | `bull`, `bear` | spread |  | A vertical: "bull" (put credit / call debit) or "bear" (call credit / put debit).<br>A vertical spread: bull (a put credit spread or a call debit spread) or bear (a call credit spread or a put debit spread). |
| `spread_legs_spec` | object |  | spread | 10 from the price, 5 further out (a debit vertical 2 and 5; a centre at 0; a strangle 5) | Where the strikes go: {sell_at: {mode, value}, buy_at: {mode, value}}.<br>An object {sell_at, buy_at}; each is {mode, value} or {mode: "strike", strikes: [...]}. The first handle (sell_at on a credit spread, condor and butterfly; buy_at on a debit vertical, straddle and strangle) is `from_price`: dollars from the stock's price (a condor/strangle puts one each side; 0 = at the price for a centre). The second is `further_out`: dollars further out from the first strikes (a butterfly's wings from its centre). Exact strikes: put strike then call strike (condor, strangle), or lower then upper (wings). The strikes FOLLOW THE PRICE until the trade is placed, then land on the nearest listed strikes. Omit for the defaults: 10 and 5 (a debit vertical 2 and 5; a centre at 0; a strangle 5). |
| `spread_legs` | array |  | spread |  | Exact legs instead: [{action, option_type, strike, ratio}].<br>Optional, instead of spread_legs_spec: every leg typed out, [{action: buy\|sell, option_type: call\|put, strike, ratio}]. Each strike must be listed. A sold call or put must be covered by a bought one: a naked short is refused. |
| `spread_take_profit_pct` | number |  | spread | none: no target | Target: % of the credit kept (credit) or % gained (debit). "none" for no target.<br>A credit spread: the % of the credit kept (50 closes when it can be bought back for half the credit). A debit spread: the % gained on the debit. Closed once the spread's natural price is there: as a limit at that net when the entry was a limit, at market when it was market. Left out (or "none"): no target. Or use spread_take_profit_price, or bracket_take_profit_levels (steps in whole spreads: [{pct, quantity}], the last closes the rest). |
| `spread_take_profit_price` | number |  | spread |  | Target as a NET price.<br>The net the spread closes at (a credit spread: bought back for this; a debit spread: sold for this). |
| `spread_stop` | object |  | spread | none: no stop | {basis: "stock", below?, above?} or {basis: "premium", max_loss_pct \| spread_price}, or "none".<br>An object. On the STOCK: {"basis": "stock", "below": 572, "above": 592} (either side optional; either crossing closes the whole trade). On the PREMIUM: {"basis": "premium", "max_loss_pct": 50} (stop once the loss reaches that % of the most it can lose: width less credit, or the debit paid) or {"basis": "premium", "spread_price": 3.10} (a credit spread whose cost to close rises to it, a debit spread whose value falls to it). Judged on the natural price. Left out (or "none"): no stop. |
| `spread_take_profit_close_with` | string | `market`, `limit` | spread | as the entry: a limit (net) entry closes the targets as limits at their nets, a market entry at market | How the targets close: "market" or "limit" (at the target's own net).<br>market: each target closes in one market order once the natural price is there. limit: one limit at the target's own net. Left out: as the entry (a limit net entry closes the targets as limits, a market entry at market). |
| `spread_stop_close_with` | string | `market`, `limit` | spread | as the entry: a limit (net) entry closes the stop as a limit at its net, a market entry at market | How the stop closes: "market" or "limit" (at the stop's own net).<br>market: every leg closed in one market order. limit: one limit at the stop's own net, not chased (premium stops only). Left out: as the entry (a limit net entry closes the stop as a limit, a market entry at market). |
| `spread_close_at` | string |  | spread | none: nothing closes it by the clock | HH:MM ET on the expiry day: close whatever is left then, at market. Or "none".<br>A time HH:MM (ET) on the expiry day to close whatever is left, at market. Left out (or "none"): no close time, nothing is closed by the clock. exit_at_time (an ISO date-time) wins when given. |

## Worked examples

Each one is the same card on three roads: the arguments of `Preview-Trading-Trigger` (arm it with `Create-Trading-Trigger` and the preview_id once the person says yes), a script's `atlas.trade(...)`, and an entry of a workflow's `output_schema.triggers`.

### Stock bracket

Buy 10 AAPL at market now; stop at $240, take profit at $270 (share prices). A stock bracket needs BOTH a stop price and a target price: the broker holds them as one order.

`Preview-Trading-Trigger`:

```json
{
  "symbol": "AAPL",
  "asset_class": "stock",
  "quantity": 10,
  "enter_side": "buy",
  "enter_order_type": "market",
  "order_strategy": "bracket",
  "bracket_stop_loss_stop_price": 240,
  "bracket_take_profit_limit_price": 270
}
```

In a script:

```python
import atlas
atlas.trade(symbol="AAPL", asset_class="stock", quantity=10, enter_side="buy", enter_order_type="market", order_strategy="bracket", bracket_stop_loss_stop_price=240, bracket_take_profit_limit_price=270)
```

### Option: limit entry, 50% take profit, stop, close time

Buy 2 SPY 680 calls expiring 2026-12-18 with a $2.50 limit (Atlas sends it once the ask is at or under 2.50); sell when the premium is up 50%; stop when it is down 30%; close whatever is left at 15:45 ET on the expiry day.

`Preview-Trading-Trigger`:

```json
{
  "symbol": "SPY",
  "asset_class": "option",
  "option_type": "call",
  "strike": 680,
  "expiry": "2026-12-18",
  "contracts": 2,
  "enter_side": "buy_to_open",
  "enter_order_type": "limit",
  "enter_limit_price": 2.5,
  "order_strategy": "bracket",
  "bracket_take_profit_limit_pct": 50,
  "bracket_stop_loss_stop_pct": -30,
  "exit_at_time": "2026-12-18T15:45:00-05:00"
}
```

In a script:

```python
import atlas
atlas.trade(symbol="SPY", asset_class="option", option_type="call", strike=680, expiry="2026-12-18", contracts=2, enter_side="buy_to_open", enter_order_type="limit", enter_limit_price=2.5, order_strategy="bracket", bracket_take_profit_limit_pct=50, bracket_stop_loss_stop_pct=-30, exit_at_time="2026-12-18T15:45:00-05:00")
```

### Option ladder sized by a budget

When SPY falls to 670 or below, buy SPY 665 puts with up to $1,000 (the count is worked out at the fill); sell half at +30%, a quarter at +60% and move the stop to breakeven, the rest at +100% with the stop moved to +30%; stop at -40% before the first target.

`Preview-Trading-Trigger`:

```json
{
  "symbol": "SPY",
  "asset_class": "option",
  "option_type": "put",
  "strike": 665,
  "expiry": "2026-12-18",
  "bracket_trade_budget": 1000,
  "enter_side": "buy_to_open",
  "enter_order_type": "market",
  "enter_trigger_operator": "lte",
  "enter_trigger_value": 670,
  "order_strategy": "bracket",
  "bracket_stop_loss_stop_pct": -40,
  "bracket_take_profit_levels": [
    {
      "pct": 30,
      "quantity": "50%"
    },
    {
      "pct": 60,
      "quantity": "25%",
      "stop_after_pct": 0
    },
    {
      "pct": 100,
      "quantity": "remaining",
      "stop_after_pct": 30
    }
  ]
}
```

In a script:

```python
import atlas
atlas.trade(symbol="SPY", asset_class="option", option_type="put", strike=665, expiry="2026-12-18", bracket_trade_budget=1000, enter_side="buy_to_open", enter_order_type="market", enter_trigger_operator="lte", enter_trigger_value=670, order_strategy="bracket", bracket_stop_loss_stop_pct=-40, bracket_take_profit_levels=[{"pct": 30, "quantity": "50%"}, {"pct": 60, "quantity": "25%", "stop_after_pct": 0}, {"pct": 100, "quantity": "remaining", "stop_after_pct": 30}])
```

### Iron condor

Sell 2 SPY 0DTE iron condors 10 from the price, 5 wide, at a 1.20 net credit limit (Atlas watches the natural credit and sends it at 1.20); take profit at 50% of the credit; stop at 50% of the most it can lose; close at 15:45 ET.

`Preview-Trading-Trigger`:

```json
{
  "symbol": "SPY",
  "asset_class": "option",
  "spread_strategy": "iron_condor",
  "expiry": "0dte",
  "spread_legs_spec": {
    "sell_at": {
      "mode": "from_price",
      "value": 10
    },
    "buy_at": {
      "mode": "further_out",
      "value": 5
    }
  },
  "spreads": 2,
  "enter_order_type": "limit",
  "enter_limit_price": 1.2,
  "spread_take_profit_pct": 50,
  "spread_stop": {
    "basis": "premium",
    "max_loss_pct": 50
  },
  "spread_stop_close_with": "market",
  "spread_close_at": "15:45"
}
```

In a script:

```python
import atlas
atlas.trade(symbol="SPY", asset_class="option", spread_strategy="iron_condor", expiry="0dte", spread_legs_spec={"sell_at": {"mode": "from_price", "value": 10}, "buy_at": {"mode": "further_out", "value": 5}}, spreads=2, enter_order_type="limit", enter_limit_price=1.2, spread_take_profit_pct=50, spread_stop={"basis": "premium", "max_loss_pct": 50}, spread_stop_close_with="market", spread_close_at="15:45")
```

### Credit put vertical with a stop on the stock

Sell 2 SPY bull put credit spreads expiring Friday: the short put $5 under the price, the long put $5 further out, for at least a $0.80 net credit; take profit at 50% of the credit; close everything if SPY trades below 640.

`Preview-Trading-Trigger`:

```json
{
  "symbol": "SPY",
  "asset_class": "option",
  "spread_strategy": "vertical",
  "spread_side": "credit",
  "spread_direction": "bull",
  "expiry": "friday",
  "spread_legs_spec": {
    "sell_at": {
      "mode": "from_price",
      "value": 5
    },
    "buy_at": {
      "mode": "further_out",
      "value": 5
    }
  },
  "spreads": 2,
  "enter_order_type": "limit",
  "enter_limit_price": 0.8,
  "spread_take_profit_pct": 50,
  "spread_stop": {
    "basis": "stock",
    "below": 640
  }
}
```

In a script:

```python
import atlas
atlas.trade(symbol="SPY", asset_class="option", spread_strategy="vertical", spread_side="credit", spread_direction="bull", expiry="friday", spread_legs_spec={"sell_at": {"mode": "from_price", "value": 5}, "buy_at": {"mode": "further_out", "value": 5}}, spreads=2, enter_order_type="limit", enter_limit_price=0.8, spread_take_profit_pct=50, spread_stop={"basis": "stock", "below": 640})
```

### Debit call vertical

Buy 1 QQQ bull call debit spread expiring 2026-12-18 at market: the long call $2 above the price, the short call $5 further out; take profit when the spread is up 80%; stop when half the debit is lost.

`Preview-Trading-Trigger`:

```json
{
  "symbol": "QQQ",
  "asset_class": "option",
  "spread_strategy": "vertical",
  "spread_side": "debit",
  "spread_direction": "bull",
  "expiry": "2026-12-18",
  "spread_legs_spec": {
    "buy_at": {
      "mode": "from_price",
      "value": 2
    },
    "sell_at": {
      "mode": "further_out",
      "value": 5
    }
  },
  "spreads": 1,
  "enter_order_type": "market",
  "spread_take_profit_pct": 80,
  "spread_stop": {
    "basis": "premium",
    "max_loss_pct": 50
  }
}
```

In a script:

```python
import atlas
atlas.trade(symbol="QQQ", asset_class="option", spread_strategy="vertical", spread_side="debit", spread_direction="bull", expiry="2026-12-18", spread_legs_spec={"buy_at": {"mode": "from_price", "value": 2}, "sell_at": {"mode": "further_out", "value": 5}}, spreads=1, enter_order_type="market", spread_take_profit_pct=80, spread_stop={"basis": "premium", "max_loss_pct": 50})
```

### OCO pair: a call above, a put below, the first to fill cancels the other

Buy 1 SPY 690 call if SPY reaches 685, or 1 SPY 660 put if SPY falls to 665; whichever enters first cancels the other. Each has its own stop and target on the premium.

`Preview-Trading-Trigger` (checks both, saves nothing) and `Create-Trading-Trigger`:

```json
{
  "link_mode": "oco",
  "legs": [
    {
      "symbol": "SPY",
      "asset_class": "option",
      "option_type": "call",
      "strike": 690,
      "expiry": "2026-12-18",
      "contracts": 1,
      "enter_side": "buy_to_open",
      "enter_order_type": "market",
      "enter_trigger_operator": "gte",
      "enter_trigger_value": 685,
      "order_strategy": "bracket",
      "bracket_stop_loss_stop_pct": -30,
      "bracket_take_profit_limit_pct": 50,
      "label": "call_side",
      "cancels_labels": [
        "put_side"
      ]
    },
    {
      "symbol": "SPY",
      "asset_class": "option",
      "option_type": "put",
      "strike": 660,
      "expiry": "2026-12-18",
      "contracts": 1,
      "enter_side": "buy_to_open",
      "enter_order_type": "market",
      "enter_trigger_operator": "lte",
      "enter_trigger_value": 665,
      "order_strategy": "bracket",
      "bracket_stop_loss_stop_pct": -30,
      "bracket_take_profit_limit_pct": 50,
      "label": "put_side",
      "cancels_labels": [
        "call_side"
      ]
    }
  ]
}
```

In a script:

```python
import atlas
atlas.trade(symbol="SPY", asset_class="option", option_type="call", strike=690, expiry="2026-12-18", contracts=1, enter_side="buy_to_open", enter_order_type="market", enter_trigger_operator="gte", enter_trigger_value=685, order_strategy="bracket", bracket_stop_loss_stop_pct=-30, bracket_take_profit_limit_pct=50, label="call_side", cancels_labels=["put_side"])
atlas.trade(symbol="SPY", asset_class="option", option_type="put", strike=660, expiry="2026-12-18", contracts=1, enter_side="buy_to_open", enter_order_type="market", enter_trigger_operator="lte", enter_trigger_value=665, order_strategy="bracket", bracket_stop_loss_stop_pct=-30, bracket_take_profit_limit_pct=50, label="put_side", cancels_labels=["call_side"])
```

## Names that are not fields

| Written | Use |
|---|---|
| `side` | enter_side |
| `order_type` | enter_order_type |
| `limit_price` | enter_limit_price |
| `entry_price` | enter_limit_price |
| `limit` | enter_limit_price |
| `qty` | quantity (shares) or contracts (options) |
| `shares` | quantity |
| `budget` | bracket_trade_budget |
| `trade_budget` | bracket_trade_budget |
| `stop` | bracket_stop_loss_stop_price (a price) or bracket_stop_loss_stop_pct (a %, negative) |
| `stop_loss` | bracket_stop_loss_stop_price (a price) or bracket_stop_loss_stop_pct (a %, negative) |
| `stop_loss_pct` | bracket_stop_loss_stop_pct (negative: -30 = lost 30%) |
| `stop_pct` | bracket_stop_loss_stop_pct (negative: -30 = lost 30%) |
| `stop_price` | bracket_stop_loss_stop_price |
| `trailing_stop` | bracket_stop_loss_trailing_pct |
| `trailing_pct` | bracket_stop_loss_trailing_pct |
| `take_profit` | bracket_take_profit_limit_price (a price) or bracket_take_profit_limit_pct (a %) |
| `take_profit_pct` | bracket_take_profit_limit_pct |
| `tp_pct` | bracket_take_profit_limit_pct |
| `target` | bracket_take_profit_limit_price (a price) or bracket_take_profit_limit_pct (a %) |
| `targets` | bracket_take_profit_levels |
| `take_profit_levels` | bracket_take_profit_levels |
| `ladder` | bracket_take_profit_levels |
| `close_at` | exit_at_time (an ISO date-time with its offset, e.g. "2026-12-18T15:45:00-05:00"); on a spread, spread_close_at "15:45" |
| `close_time` | exit_at_time (an ISO date-time with its offset) |
| `exit_time` | exit_at_time (an ISO date-time with its offset) |
| `enter_time` | enter_at_time (an ISO date-time with its offset) |
| `entry_time` | enter_at_time (an ISO date-time with its offset) |
| `expiration` | expiry |
| `expiration_date` | expiry |
| `exp` | expiry |
| `type` | option_type |
| `right` | option_type |
| `strategy` | order_strategy (single trades) or spread_strategy (spreads) |
| `trigger_price` | enter_trigger_value (with enter_trigger_operator) |
| `watch_price` | enter_trigger_value (with enter_trigger_operator) |
| `num_spreads` | spreads |
| `stop_loss_price` | bracket_stop_loss_stop_price |
| `take_profit_price` | bracket_take_profit_limit_price |
