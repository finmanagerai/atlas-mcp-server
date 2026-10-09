# The tools behind this skill (21)

GENERATED from the live server; do not edit by hand. Every field each
tool accepts. Nothing here is required unless the table says so: it is
what is possible.

## `Broker-Connections`

🟢 reads. List all connected brokerage accounts for the authenticated user.

Takes nothing.

## `Account-Balances`

🟢 reads. Cash balance, buying power, and equity for one linked brokerage account.

| Field | Type | Needed | Default |
|---|---|---|---|
| `account_id` | string | yes |  |

## `Account-Holdings`

🟢 reads. Everything held in one linked brokerage account: stocks, ETFs, options, crypto and more.

| Field | Type | Needed | Default |
|---|---|---|---|
| `account_id` | string | yes |  |

## `All-Account-Holdings`

🟢 reads. Everything held across ALL linked brokerage accounts: stocks, ETFs, options, crypto and more, each tagged with the account it is in. `accounts` lists every account with how many positions it has and when the broker last reported them, or why it could not be read.

Takes nothing.

## `Preview-Trading-Trigger`

🟡 adds. Save a trigger as a PREVIEW: the exact trigger row, validated and shaped like a live one, but NOT armed.

| Field | Type | Needed | Default |
|---|---|---|---|
| `rule` | object | yes |  |
| `symbol` | string | no |  |
| `account_id` | string | no |  |
| `trade_budget` | number | no |  |

## `Create-Trading-Trigger`

🔴 acts. Persist a price-trigger rule.

| Field | Type | Needed | Default |
|---|---|---|---|
| `rule` | object | no |  |
| `symbol` | string | no |  |
| `account_id` | string | no |  |
| `preview_id` | string | no |  |
| `trade_budget` | number | no |  |
| `legs` | array | no |  |
| `link_mode` | string | no | `""` |

The tool's own description, in full:

````text
Persist a price-trigger rule. IMPORTANT: Do NOT call this tool directly — call Preview-Trading-Trigger first and let the user confirm by clicking 'Activate trigger' in the preview card. This tool is invoked by the widget on the user's behalf.

ARMING A PREVIEW: pass preview_id (from Preview-Trading-Trigger). The saved preview row itself is armed in place — same id, no duplicate. rule and symbol may be omitted (the saved ones stand) or given to edit on the way; account_id is required if the preview was saved without one.

SIZE BY MONEY: pass `trade_budget` (in DOLLARS) INSTEAD of a contract count or share quantity when the person said an amount — 'put $500 into it'. Atlas works out how many fit at the price the order actually pays, as close under the budget as whole units allow and never over, and re-sizes at the real fill. Never send both a budget and a count.

LINKED TRIGGERS (OCO / OEO): pass `legs` INSTEAD of `rule` — a list of {rule, symbol?, account_id?, trade_budget?} — to create several triggers as one set. Two legs + link_mode 'oco': whichever fills first cancels the other. Two legs + link_mode 'oeo': the SECOND leg starts watching only once the FIRST fills (it is saved unarmed until then; List shows it as 'waiting'). For a bigger or mixed set leave link_mode out, give each leg's rule a `label`, and name the others under `cancels_labels` (cancel these when I fill) or `activates_labels` (start these when I fill). Every leg must be linked to the set: a leg nobody names and that names nobody is refused, because two unlinked triggers both fill and the size doubles. If any leg cannot be created, the ones already made are removed again, so you never end up with half a set. The reply's `link.legs` lists each leg's id, label, whether it is armed, and the ids it cancels or starts.

A trigger you create here is SOLO — it has no subscribers. To move or adjust an EXISTING shared trade (one a workflow fanned out to subscribers), edit that trigger with Update-Trading-Trigger instead; a new trigger created here would only run for you and leave every subscriber on the old trade.

The background worker monitors live prices and executes orders automatically when conditions fire — one real broker order at a time, in sequence.

━━ order_strategy ━━
  'one_triggers_other' (default): enter trigger fires → enter order placed → worker then watches exit trigger → exit order placed.
  'bracket': enter trigger fires → enter order placed → worker then watches BOTH stop_loss AND take_profit simultaneously → whichever price is hit first fires a single close order. THIS WORKS FOR OPTIONS. The worker simulates OCO by placing one order at a time — it is fully safe and is the correct way to set both a stop-loss and a take-profit on an options position. Do NOT refuse to use bracket for options.

━━ rule.execution ━━
  Stocks: {asset_class:'stock', quantity:N}
  Options: {asset_class:'option', option_type:'call'|'put', expiry:'YYYY-MM-DD', strike:N, contracts:N}

━━ rule.enter ━━ (REQUIRED for both strategies)
  {side, order_type, limit_price?, trigger:{metric:'price', operator:'lt'|'lte'|'gt'|'gte'|'eq', value:N}}
  Stock sides: 'buy' | 'sell'
  Option sides: 'buy_to_open' | 'sell_to_open'

━━ WHICH SIDE OF THE ENTRY AN EXIT GOES ON ━━ (rejected at compile)
  A stop-loss and a take-profit carry NO operator. Their DIRECTION IS THE
  NUMBER, read off where it sits relative to the entry:
    long stock | LONG CALL | short put   → stop BELOW entry, target ABOVE
    short stock | LONG PUT | short call  → stop ABOVE entry, target BELOW
  THE LONG PUT IS THE ONE THAT GETS INVERTED. You bought it because you
  expect the underlying to FALL, so falling is the PROFIT: its target is
  BELOW the entry and its stop is ABOVE. Same shape for a short call.
  (Those are UNDERLYING levels. exit.price_basis='contract' measures the
  option's own premium, where the only question is long premium — stop
  below, target above — or short premium, which reverses it.)
  A leg on the wrong side is not a slightly-wrong stop: it is ALREADY TRUE
  at the entry price, so the position closes on the tick it opened.
  The same rule governs a one_triggers_other exit WATCH, which does carry
  an operator: at the price the ENTRY fires, the exit must NOT already
  hold. enter gte 500 + exit lte 520 is refused — 500 is already ≤ 520.
  A stop under a breakout entry is exit lte 490. NEVER reuse the entry
  operator for the exit; they point opposite ways.

━━ rule.exit for one_triggers_other ━━
  {side, order_type, limit_price?, trigger:{...}} — single close leg.
  Option close sides: 'sell_to_close' | 'buy_to_close'. Plain 'sell' / 'buy' are accepted too and mean the same thing — on an option, selling to close IS selling. Same for the entry: 'buy'/'sell' resolve to buy_to_open/sell_to_open. An OPENING side in an exit is always refused.

━━ rule.exit for bracket (stocks AND options) ━━
  IMPORTANT — the price fields in this block mean DIFFERENT things for stocks vs options:
    * Stocks (native broker bracket): stop_price and limit_price       are SHARE PRICES the broker uses verbatim. limit_price on       stop_loss turns it into a stop-limit; limit_price on       take_profit is the sell-limit price.
    * Options (worker-simulated OCO): stop_price, limit_price,       and take_profit_levels[].price are all UNDERLYING PRICE       LEVELS — the worker watches the underlying ticker (e.g.       SPY) and fires a MARKET close on the option leg the moment       the underlying crosses the level. They are NOT option       contract prices. stop_loss.limit_price is IGNORED for       options (always market) so a gap-through can never strand       the position.
  Fields:
  stop_loss?: {stop_price:N, limit_price?:N} | {stop_pct:N} | {trailing_pct:N}
    trailing_pct = a TRAILING STOP that follows the price (stocks AND options): a DISTANCE in percent behind the best price since the entry — the SHARE price on a stock, the contract premium on an option — tightening only, never loosening. 10 = the stop sits 10% under the highest price seen since the fill (over the lowest, on a short). It IS the stop: give it alone, never beside stop_price / stop_pct. On a stock it makes the bracket worker-watched (Atlas holds the exit instead of the broker), so a stock with a trailing stop may have a stop and no target.
  take_profit?: {limit_price:N}
  take_profit_levels?: [{price:N | pct:N, quantity:'40%'|5|'remaining', stop_after_pct?:N, stop_after_price?:N, close_limit_price?:N}, ...] — scaled exit: close a fraction/count at each level in sequence. Each level takes price (a $ level — UNDERLYING for options) OR pct (% move from the entry contract premium). quantity formats: '40%' (percent of original), 5 (absolute), 'remaining' (whatever is left). stop_after_pct / stop_after_price is the per-level TRAILING STOP, and it belongs on the level you are heading TOWARD: a level's stop move arms when the level BEFORE it fills. So 'move my stop once TP1 fills' is stop_after_pct on TP2 (take_profit_levels[1]), NOT on TP1. Anything on TP1 is dropped and the reply says so, because entry-to-TP1 is guarded by exit.stop_loss and nothing on TP1 could ever move it. Give stop_after_pct for a % trailing stop (measured from the ENTRY PREMIUM, sign kept: 0 = breakeven, +20 = 20% ABOVE entry premium = locked-in profit, -10 = 10% below) OR stop_after_price for a $ one — pick at most ONE per level. close_limit_price is the CONTRACT PREMIUM that level's sell is SUBMITTED at — the price on the order, not the target that fires it. Omit it and that level closes at MARKET. It is a plain limit: nothing re-prices or chases it, so a price the market never reaches simply does not fill and that level keeps waiting (the stop-loss, which is always market, a close time, or a ladder review still end the trade). Never invent one — set it only when the user asked for a specific close price. To EDIT a level's trailing stop, resend take_profit_levels with that level's stop_after_pct/stop_after_price changed. On a WORKFLOW trade template you may set the key to null to let Atlas decide it at run time (the decision step fills it); a plain manual trigger has no decision step, so give a concrete number there (a null is rejected). Omit both keys to keep the current stop. At least one of stop_loss, take_profit, or take_profit_levels is required.
  take_profit_loop?: true — only with take_profit_levels on a workflow-bound trigger: after each non-final level fills, the workflow re-runs and the AI re-decides the remaining ladder (adjust targets, move the stop, or exit the remainder now).
  Direction is derived per-threshold at fire time from the entry price the worker stamped on phase advance: a threshold below entry fires on a drop, above fires on a rise. You do NOT declare bullish / bearish anywhere.

━━ Examples ━━
  sequential (stock): {"execution":{"asset_class":"stock","quantity":10},"enter":{"side":"buy","order_type":"market","trigger":{"metric":"price","operator":"lte","value":600}},"exit":{"side":"sell","order_type":"market","trigger":{"metric":"price","operator":"gte","value":650}}}
  bracket (stock):    {"order_strategy":"bracket","execution":{"asset_class":"stock","quantity":10},"enter":{"side":"buy","order_type":"market","trigger":{"metric":"price","operator":"lte","value":600}},"exit":{"stop_loss":{"stop_price":585},"take_profit":{"limit_price":640}}}
  bracket (option — worker-simulated OCO with scaled TP): {"order_strategy":"bracket","execution":{"asset_class":"option","option_type":"call","contracts":10,"expiry":"2026-04-17","strike":710},"enter":{"side":"buy_to_open","order_type":"market","trigger":{"metric":"price","operator":"gte","value":712}},"exit":{"stop_loss":{"stop_price":709},"take_profit_levels":[{"price":715,"quantity":"40%"},{"price":718,"quantity":"40%"},{"price":722,"quantity":"remaining"}]}}

━━ Multi-execution (one trigger → multiple orders) ━━
  Use executions[] instead of a single execution block to fire several orders simultaneously when the trigger fires. Each leg has its own symbol, execution, and enter (side + order_type). The top-level enter carries only the trigger condition (no side/order_type).
  Strategies:
    • one_triggers_other (default): each leg fires-and-forgets, no shared exit. Use for one-shot multi-asset baskets.
    • bracket: basket-level stop_loss / take_profit on the WATCH underlying. ALL legs must be OPTIONS. Spread legs may have mixed side/option_type (a bull call spread has long + short legs) — you do NOT declare a direction. The worker derives fire direction per threshold from the entry price: a threshold sitting BELOW the entry price fires on a drop, ABOVE fires on a rise. Just set the numeric SL/TP levels you want; the system handles the rest. Strategies with no single fire direction (iron condor / long strangle — exit on EITHER side of a range) still need separate triggers + cancels_labels because a single SL/TP can't express two-sided exits.
  Example (OTO): when SPY crosses 580 buy NVDA×5 AND AMD×5:
  {"enter":{"trigger":{"metric":"price","operator":"gte","value":580}},"executions":[{"symbol":"NVDA","execution":{"asset_class":"stock","quantity":5},"enter":{"side":"buy","order_type":"market"}},{"symbol":"AMD","execution":{"asset_class":"stock","quantity":5},"enter":{"side":"buy","order_type":"market"}}]}
  Example (multi-exec bracket, bull call spread): SPY ≥ 580 enters a +580/-585 call spread; basket SL at SPY 575, TP at SPY 590.
  {"order_strategy":"bracket","symbol":"SPY","enter":{"trigger":{"metric":"price","operator":"gte","value":580}},"executions":[{"symbol":"SPY","execution":{"asset_class":"option","option_type":"call","strike":580,"expiry":"2026-05-30","contracts":5},"enter":{"side":"buy_to_open","order_type":"market"}},{"symbol":"SPY","execution":{"asset_class":"option","option_type":"call","strike":585,"expiry":"2026-05-30","contracts":5},"enter":{"side":"sell_to_open","order_type":"market"}}],"exit":{"stop_loss":{"stop_price":575},"take_profit":{"limit_price":590}}}

━━ When should it run (rule.meta) ━━
  The dashboard's Schedule / Alert / Both picker for a standalone trigger. Omit meta for a plain price trigger (fires when the price condition is met). Otherwise rule.meta = {trigger_source, schedule, timezone, alert_id}:
    trigger_source: 'cron' (fires on the schedule; the price condition is not used to enter) | 'alert' (fires when alert_id goes off) | 'both' (schedule OR alert OR the price condition).
    schedule: one line per time — a 5-field cron line ('30 9 * * 1-5') recurs; 'once YYYY-MM-DD HH:MM' fires at that date and time and never again (several once lines for several moments). Cron lines OR once lines, not both. Times are in timezone (default US/Eastern).
    alert_id: an alert's id (List-Alerts) for 'alert' / 'both'.
  Example: {"meta":{"trigger_source":"cron","schedule":"once 2026-09-15 09:30"}, ...}

━━ Other fields ━━
  symbol: string — the WATCH ticker (the price being monitored, e.g. SPY). For multi-execution this is what the trigger fires on; the executions[] symbols are what gets bought/sold.
  account_id: string — REQUIRED. Triggers fire automatically in the background so the user MUST explicitly confirm which broker account receives the order before you call this tool. Call Broker-Connections to list accounts, present them to the user, and wait for their explicit choice. Never infer or auto-select the account — a wrong account fires a real automated trade in the wrong place.
````

## `Update-Trading-Trigger`

🔴 acts. Edit one trading trigger in place.

| Field | Type | Needed | Default |
|---|---|---|---|
| `trigger_id` | string | yes |  |
| `rule` | object | no |  |
| `is_active` | boolean | no |  |
| `symbol` | string | no |  |
| `account_id` | string | no |  |

## `Delete-Trading-Trigger`

🟠 changes. Delete a trading trigger.

| Field | Type | Needed | Default |
|---|---|---|---|
| `trigger_id` | string | yes |  |

## `List-Trading-Triggers`

🟢 reads. List the user's trading triggers — watching (is_active=true), paused, and saved PREVIEWS (is_active=false with rule._preview).

| Field | Type | Needed | Default |
|---|---|---|---|
| `is_active` | boolean | no |  |
| `symbol` | string | no |  |
| `limit` | integer | no | `50` |
| `platform` | string | no | `"other"` |

## `List-Fired-Triggers`

🟢 reads. List the user's completed (fired) triggers from the archive.

| Field | Type | Needed | Default |
|---|---|---|---|
| `symbol` | string | no |  |
| `limit` | integer | no | `50` |

## `Reactivate-Trigger`

🔴 acts. Move a fired trigger from the archive back to the active triggers table, resetting it to phase='enter' so it starts monitoring prices again from scratch.

| Field | Type | Needed | Default |
|---|---|---|---|
| `fired_trigger_id` | string | yes |  |

## `Preview-Order`

🟡 adds. Stage an order for the user to review.

| Field | Type | Needed | Default |
|---|---|---|---|
| `rule` | object | yes |  |
| `symbol` | string | no |  |
| `account_id` | string | no |  |
| `phase` | string | no | `"enter"` |

The tool's own description, in full:

````text
Stage an order for the user to review. Nothing is sent to the broker.
Saves the order as a preview and returns a preview_id plus a link the user opens to Accept or Cancel. No trade is submitted until it is accepted there, or Place-Order is called with that preview_id. Pass every field the order needs: this tool does not guess a side or an option type.
Rule schema:
  rule.execution = contract identity ONLY: asset_class ('stock'|'option'), quantity (stocks) or option_type/expiry/strike/contracts (options). Side, order_type, and limit_price live on the per-phase blocks below.
  rule.enter = {side, order_type, limit_price?} — required. side is 'buy'|'sell' for stocks or 'buy_to_open'|'sell_to_open' for options. limit_price is REQUIRED when order_type='limit' (no shorthand for mid/bid/ask — pass the numeric price you want to work).
  rule.order_strategy? = 'one_triggers_other' (default) or 'bracket'.
    one_triggers_other: worker fires enter, then polls exit trigger.
    bracket (stocks): native broker OCO — entry + stop_loss + take_profit in one broker call.
    bracket (options): worker-simulated OCO — entry placed first, then worker watches stop_loss AND take_profit simultaneously and fires whichever is hit first. FULLY SUPPORTED for options. Use this whenever the user wants both a stop-loss and a take-profit on an options position.
  rule.exit? (one_triggers_other) = {side, order_type, limit_price?} — single close leg with a trigger condition.
  rule.exit? (bracket) = {stop_loss?: {stop_price, limit_price?}, take_profit?: {limit_price}, take_profit_levels?: [{price:N, quantity:'40%'|5|'remaining'}, ...]} — at least one of stop_loss / take_profit / take_profit_levels required.
  phase: optional 'enter'|'exit' — which leg this preview targets (default 'enter').
Types / example:
    stock example:  {"execution":{"asset_class":"stock","quantity":10},"enter":{"side":"buy","order_type":"market"},"exit":{"side":"sell","order_type":"market"}}
    option example: {"execution":{"asset_class":"option","option_type":"call","contracts":1,"expiry":"2026-04-15","strike":702},"enter":{"side":"buy_to_open","order_type":"limit","limit_price":3.10},"exit":{"side":"sell_to_close","order_type":"limit","limit_price":4.50}}
    bracket (stock):  {"order_strategy":"bracket","execution":{"asset_class":"stock","quantity":10},"enter":{"side":"buy","order_type":"market","trigger":{"metric":"price","operator":"lte","value":600}},"exit":{"stop_loss":{"stop_price":585},"take_profit":{"limit_price":640}}}
    bracket (option): {"order_strategy":"bracket","execution":{"asset_class":"option","option_type":"call","contracts":10,"expiry":"2026-04-17","strike":710},"enter":{"side":"buy_to_open","order_type":"market","trigger":{"metric":"price","operator":"gte","value":712}},"exit":{"stop_loss":{"stop_price":709},"take_profit_levels":[{"price":715,"quantity":"40%"},{"price":718,"quantity":"40%"},{"price":722,"quantity":"remaining"}]}}
  symbol: string — underlying ticker (e.g. 'SPY'); optional if included in the rule.
  account_id: string — the broker account to use, from Broker-Connections.
ACCOUNT RULE: If the user has more than one connected broker account, you MUST show them the list (call Broker-Connections) and ask which account to use BEFORE calling this tool. Never guess or auto-select — a wrong account executes a real trade in the wrong place. Only omit account_id when the user has exactly one broker account connected.
````

## `Preview-Multiple-Orders`

🟡 adds. Preview multiple orders at once — e.g. buy 5 NVDA, 5 MSFT, and 5 ASML in one shot.

| Field | Type | Needed | Default |
|---|---|---|---|
| `orders` | array | yes |  |
| `account_id` | string | no |  |

## `Place-Order`

🔴 acts. Send an order to the user's own connected broker account.

| Field | Type | Needed | Default |
|---|---|---|---|
| `rule` | object | no |  |
| `symbol` | string | no |  |
| `account_id` | string | no |  |
| `preview_id` | string | no |  |
| `phase` | string | no | `"enter"` |

The tool's own description, in full:

````text
Send an order to the user's own connected broker account. This is a real order with real money: only when the user says to place it. A bracket order goes in with its stop-loss and take-profit, and when one of the two fills the other is cancelled. Two modes:
  * Pass preview_id to place an already-staged preview — the saved rule/account/phase are authoritative.
  * Pass rule (+ symbol, optional phase) directly to skip the preview step entirely (used by the trigger worker and by clients that maintain their own confirmation UI).
Types / example:
  preview_id: string — id returned by Preview-Order (optional).
  rule: object — same schema as Preview-Order (required if no preview_id).
  symbol: string — underlying ticker (optional if in the rule).
  phase: string — 'enter' or 'exit' (default 'enter'); ignored when preview_id is given.
  account_id: string — the broker account to use, from Broker-Connections.
ACCOUNT RULE: If the user has more than one connected broker account, you MUST show them the list (call Broker-Connections) and ask which account to use BEFORE calling this tool. Never guess or auto-select — a wrong account submits a real order to the wrong broker.
````

## `Cancel-Order`

🔴 acts. Cancel one order, staged or already sent.

| Field | Type | Needed | Default |
|---|---|---|---|
| `preview_id` | string | yes |  |

## `List-Preview-Orders`

🟢 reads. List the user's recent staged/placed/failed orders.

| Field | Type | Needed | Default |
|---|---|---|---|
| `statuses` | array | no |  |
| `limit` | integer | no | `50` |

## `Trade-Close`

🔴 acts. Close a position NOW — everything still open on it, at market.

| Field | Type | Needed | Default |
|---|---|---|---|
| `trade_id` | string | yes |  |
| `exit_price` | number | no |  |

## `Trade-Take-Profit`

🔴 acts. Sell the NEXT take-profit rung now, without waiting for its price.

| Field | Type | Needed | Default |
|---|---|---|---|
| `trade_id` | string | yes |  |
| `level` | integer | no |  |

## `Trade-Edit-Exit`

🔴 acts. Move a LIVE trade's stop or targets — the pencil on the trade card, from the chat, the CLI or the API (owner, 2026-09-10).

| Field | Type | Needed | Default |
|---|---|---|---|
| `trade_id` | string | yes |  |
| `stop_pct` | number | no |  |
| `stop_price` | number | no |  |
| `trail_pct` | number | no |  |
| `trailing_pct` | number | no |  |
| `take_profit_pct` | number | no |  |
| `take_profit_price` | number | no |  |
| `levels` | array | no |  |

## `Trade-Edit-Entry`

🔴 acts. Move the price an order is waiting to enter at, or turn back on an order that was taken off before it filled.

| Field | Type | Needed | Default |
|---|---|---|---|
| `trade_id` | string | yes |  |
| `entry_value` | number | no |  |
| `turn_back_on` | boolean | no | `false` |

## `Trade-Cancel-Entry`

🔴 acts. Take an order OFF before it fills.

| Field | Type | Needed | Default |
|---|---|---|---|
| `trade_id` | string | yes |  |
