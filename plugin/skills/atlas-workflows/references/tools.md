# The tools behind this skill (21)

GENERATED from the live server; do not edit by hand. Every field each
tool accepts. Nothing here is required unless the table says so: it is
what is possible.

## `Trigger-Workflow-Schema`

🟢 reads. Fetch the canonical schema for AI trigger workflows.

Takes nothing.

## `Workflow-Preview`

🟢 reads. Preview a new workflow, or changes to an existing one, without saving anything.

| Field | Type | Needed | Default |
|---|---|---|---|
| `workflow_id` | string | no |  |
| `proposed` | object | no |  |
| `platform` | string | no | `"other"` |

## `Workflow-Create`

🟡 adds. Create a workflow (a recurring AI setup) on the caller's account, saved EXACTLY as supplied.

| Field | Type | Needed | Default |
|---|---|---|---|
| `name` | string | no |  |
| `schedule` | string | no |  |
| `timezone` | string | no | `"US/Eastern"` |
| `tools` | array | no |  |
| `output_tools` | array | no |  |
| `tool_params` | object | no |  |
| `instruction` | string | no |  |
| `output_schema` | object | no |  |
| `snaptrade_account_id` | string | no |  |
| `status` | string | no | `"paused"` |
| `visibility` | string | no | `"private"` |
| `trigger_source` | string | no | `"cron"` |
| `run_once_at` | array | no |  |
| `alert_id` | string | no |  |
| `alert_ids` | array | no |  |
| `alert_creator_id` | string | no |  |
| `alert_creator_ids` | array | no |  |
| `notify_discord_dm` | boolean | no |  |
| `purpose` | string | no |  |
| `alert_max_runs_per_day` | integer | no |  |
| `notification_format` | string | no |  |
| `journal_enabled` | boolean | no |  |
| `journal_instruction` | string | no |  |
| `journal_allow_prompt_edit` | boolean | no |  |
| `journal_cadences` | array | no |  |
| `journal_run_at` | string | no |  |
| `journal_mode` | string | no |  |
| `ui_schema` | object | no |  |
| `auto_accept_updates` | boolean | no |  |
| `type` | string | no |  |
| `is_template` | boolean | no |  |
| `parent_id` | string | no |  |

The tool's own description, in full:

````text
Create a workflow (a recurring AI setup) on the caller's account, saved EXACTLY as supplied. New workflows default to status='paused'.

FIRST call Trigger-Workflow-Schema — it returns the CANONICAL output_schema (the trade contract) plus the alert wiring options and the caller's existing alerts, so you can see EVERY field and fill them all before you act (don't hand-encode a trade into the instruction).

Args — pass each as a flag; this is the FULL field set (nothing lives only in the dashboard):
  name: human label.
  instruction: plain-English of what the AI should do each run.
  purpose: 'trading' (may place orders) | 'analysis' (reads + reports, no broker) | 'draft' (signals only) | 'alert_creator' (does NOT trade — each run it sets up alerts, which other workflows can then run on; see alert_creator_id below). Stored in ui_schema.
  tools: the names of the tools the run may read, each written exactly as the tool is listed (e.g. 'Stock-Quote'). Never guess or invent a tool name/slug variant; an unrecognized name is silently dropped at run time with no error, so the workflow quietly never gets that tool. Search-Tools, where it is offered, answers with the exact id of every tool a workflow can use: copy the id from there. Name a tool HERE, not in prose in the instruction.
  output_tools: ANALYSIS WORKFLOWS ONLY (purpose 'analysis'). Tool names the AI calls AT THE END, after it has decided. A trading workflow acts through its trade card, a draft through its play, a creator through what it creates — on those this list is ignored and the dashboard hides the step, so do not send it. `tools` are what it READS first; these are what it DOES when it is done — the same list format, including 'cmcp:<app>:<tool>' and 'mcp:<server_id>:<tool>'. Use this for an analysis workflow that should ACT (place through a broker MCP, write somewhere) rather than only report: an input tool would be called before there was anything to act on. Omit or [] for no output stage.
  tool_params: per-tool notes, keyed by the SAME string as in tools / output_tools: { "Stock-Quote": { "notes": "..." }, "mcp:<server_id>:<tool>": { "notes": "..." } }. The key is `notes` (the run, the flow graph and the form all read it; `description` is accepted as an alias and stored as notes).
  WRITE A NOTE FOR EVERY TOOL YOU LIST, IN `tools` AND IN `output_tools`. Do not leave one without. The note is what the run is told about that tool, on top of the tool's general description: a tool with no note is used on a guess, and the person opening the workflow sees an empty box under it. One or two plain sentences, written for THIS workflow, never a copy of the tool's own description:
    - an INPUT tool (`tools`): what to ask it for (which symbol, expiration, timeframe, how far back) and what in its answer matters to the decision. E.g. Greek-Exposure-Single-Expiration: "SPY, today's expiration. Find the strike with the largest gamma and say whether price is above or below it."
    - an OUTPUT tool (`output_tools`): when to call it and what to send. E.g. Signal-Post: "Only when the write-up ends in a trade. Post that one contract with its entry, two targets and the stop."
  The answer lists any tool you left without a note under `tools_without_notes`: fill them with Workflow-Update before you tell the person the workflow is ready.
  output_schema: the TRADE / trigger contract the AI fills. OPTIONAL — a workflow does NOT have to place a trade at all; omit it (or leave {}) for purpose analysis/draft, or any trading workflow that should only reason/report this run. When you DO want one, EVERY trade knob is here and editable: symbol, asset_class, option_type (call/put), side (buy/sell), strike, expiry, contracts (option) or quantity (shares), enter_order_type (market/limit) + enter_limit_price, entry watch, bracket stop-loss + take-profit ($ or %), a TRAILING STOP, the take-profit SCALE-OUT LADDER (bracket_take_profit_levels[] + bracket_take_profit_loop), how the exits split across those levels (bracket_exit_split: follow/front/back/even), and label-based OCO/OEO (cancels_labels / activates_labels). SIZING BY MONEY: instead of contracts/quantity a trade can carry bracket_trade_budget (the most it may spend, in dollars) — then OMIT contracts/quantity entirely and Atlas works out how many fit at the price the order actually pays, as close under the budget as whole units allow. Set a budget only when the user asked for one; never invent it. Fetch the exact shape from Trigger-Workflow-Schema.
  THE STOP-LOSS IS ONE OF THREE KEYS on a trade (never two): bracket_stop_loss_stop_price (a fixed price), bracket_stop_loss_stop_pct (a fixed percent from entry), or bracket_stop_loss_trailing_pct: a TRAILING STOP, the form's "Trailing %". It sits that many percent behind the BEST price since entry and only ever tightens, on shares and on options: {"bracket_stop_loss_trailing_pct": 20} gets out when the trade gives back 20% from its best. Use it when the person says "trailing stop", "trail it" or "let it run but protect the gain". This is the trade's own stop; the stop that moves up after each ladder level is the level's stop_after_pct / stop_after_price instead.
  ONE CARD, EVERY TICKER: output_schema.trades_mode is 'manual' (the default when absent) or 'auto'. MANUAL = the entries in `triggers` ARE the trades, one per ticker, exactly those. AUTO = `triggers` holds exactly ONE entry used as a TEMPLATE: leave its symbol null so each run picks the tickers itself, leave option_type / label / cancels_labels / activates_labels off so it decides the call-vs-put side and any one-cancels-other pairing, and every value you DO fix on that one entry (a 30% take-profit, a stop, a size, a budget, a ladder) is applied to every trade it creates. Use auto when the user says 'find me the setups' rather than naming tickers. AUTO WITH TWO OR MORE ENTRIES IS REJECTED (400) — only the first would ever be used. `plays_mode` is the same switch for the `plays` list a signal_creator sends.
  PLAYS (signal_creator): output_schema.plays is a list of plays written in the SAME shape as `triggers` — a play IS a trade card, renamed at send time, so every trade field above applies to it. Three things a play carries that a trade does not:
    * `score` on each play: conviction, an integer 1-10. OMIT it to let the run rate each play itself — that is the default and usually right.
    * `plays_reason` (top-level, next to `plays`): ONE sentence every play this workflow sends carries. Omit it and the run writes each play's own from what it saw that run, which is worth more to a follower than a line written weeks earlier. Set it and that sentence is pinned on all.
    * `plays_destinations` (top-level): where they go. A list where 'community' is the public board and anything else is a signal group id (from Signal-Groups). Omit for the board. SEVERAL destinations is still ONE play — one signal, one tracked trade, one exit — reaching everybody across those groups; it is NOT one play per group.
  A play workflow needs NO broker. snaptrade_account_id is optional there and used only by a play carrying `trade_for_me: true`, which puts the AUTHOR's own money in — never set that unless the user asked for it.
  snaptrade_account_id: broker account id to trade in. Required to activate a trading workflow.
  ui_schema: dict of UI/display flags stored verbatim (purpose, notify_discord_dm, notification_format are the common ones; pass any others the form uses here). Merged with the purpose/notify flags below.
  auto_accept_updates: subscriber flag — true auto-applies the author's later edits; false holds the copy at its current revision.
  (A COPY's own size, budget and exit split, execution_overrides, are set with Workflow-Update on an imported copy, not on a fresh create: see "ON A COPY" there.)
  trigger_source: 'cron' (schedule) | 'alert' (an alert fires it) | 'both' | 'manual' (nothing fires it; the user presses Run now).
  run_once_at: ['YYYY-MM-DD HH:MM', ...] in `timezone` — specific dates and times to run at, once each (the dashboard's Once chip). Written into schedule as `once` lines for you; use it INSTEAD of schedule.
  schedule: when it runs, in `timezone` (used for cron/both); one line per time. A cron line ('30 9 * * 1-5') recurs; a `once YYYY-MM-DD HH:MM` line fires at that date and time and never again (list several lines for several dates/times). Use cron lines OR once lines, not both. Required to activate a cron workflow.
  timezone: tz name; defaults to 'US/Eastern'. Times are EASTERN unless you pass another zone.
  alert_id: an alert's id (from List-Alerts / Trigger-Workflow-Schema) that drives this workflow when trigger_source includes 'alert'.
  alert_ids: SEVERAL alerts, as a list of ids — any of them firing runs this workflow. The dashboard calls it 'Also run on these alerts'. Use it instead of alert_id when the person named more than one.
  alert_creator_id / alert_creator_ids: an alert_creator workflow whose own alerts drive this one — the same binding the form's alert-creator picker writes. Singular for one, the list for several.
  alert_max_runs_per_day: cap on alert-driven runs/day (resets each Eastern morning). Omit / null = unlimited.
  notify_discord_dm: true (default) DMs the run result on Discord; false runs silently. Stored in ui_schema.
  status: 'paused' (default) or 'active'.
  visibility: 'private' (default) | 'unlisted' | 'Atlas-public'.
  ui_schema.no_subscribers: true = 'keep this one personal'. Anyone who imports or duplicates it still gets a copy, but the copy stands on its own — it never follows this workflow's runs and never receives its edits. Use it for workflows about the owner's own account (balance checks, position reviews). Default false. Copies that already exist are unaffected.
  ui_schema.preview_before_place: true = 'let me review each run before it places'. The workflow still RUNS in full — same tools, same reasoning — and then stops before anything reaches a broker: what it decided waits in the dashboard for the owner to read, edit or throw away, and only Place arms it. Set it when the user asks to check trades before they go in, or wants to approve what an alert-creator sets up. Every purpose holds: a trading or draft workflow holds its trades, an analysis one holds its write-up, and a creator makes its alerts SWITCHED OFF until approved. Default false, which places as soon as it decides. OWNER ROWS ONLY — a subscriber copy rides the author's run and has none of its own to hold.
  journal_enabled / journal_instruction / journal_cadences / journal_run_at / journal_mode / journal_allow_prompt_edit: the workflow's JOURNAL (the "Keep a journal" part of the Reasoning step). With it on, Atlas writes notes about how the workflow did and reads them back on every later run. journal_enabled=true turns it on; journal_instruction says what to write down, in plain words. WHEN IT WRITES (`journal_cadences`, a list: tick as many as you like, exactly the boxes under "When should Atlas write?" in the form):
    per_trade      After every trade (or play) finishes. Only for a workflow that trades, sends the order, or sends plays.
    on_alert_fire  After an alert it made goes off. Only for a workflow that creates alerts.
    per_run        After every run, including a run that decided to do nothing. Any workflow. THE one for a workflow that only analyses, which never closes a trade.
    daily | 3d | weekly | monthly   Once a day, every 3 days, every week, every month, looking back over that stretch. These four run at `journal_run_at` ("HH:MM", Eastern, default 16:10). `journal_run_at` means nothing for the first three, which write when the thing happens.
  A name not on this list is refused, not dropped. Leave `journal_cadences` out to keep what is saved (a new journal starts on per_trade).
WHO WRITES (`journal_mode`): "atlas" (the default) writes on the cadences above; "manual" keeps the journal as the person's own notes, which Atlas reads on every run and never adds to. journal_allow_prompt_edit=true lets the journal rewrite this workflow's instructions, and only when journal_instruction tells it to. Turn a journal on only when the person asked for one. To change any of this later, or to read or edit what is written, use Workflow-Journal.
  ui_schema.run_form: ask the person some QUESTIONS before a manual run, and hand their answers to the agent as part of the instruction for that one run. MANUAL workflows only (trigger_source 'manual') — it is answered by somebody pressing Run now, and nothing else presses a manual workflow. Shape: {"enabled": true, "fields": [{"id": "q1", "label": "What stock are you looking at?", "type": "text", "required": true, "options": []}]}. `label` IS the question, in the words the person will read. `type` is one of: text (free form, the default), date, time, select (pick one), multiselect (pick several). `options` is the list of choices and is REQUIRED for select/multiselect, ignored for everything else. `id` is any stable string — answers are keyed by it, so keep it when editing. Up to 20 questions.
    A question with no `label` is ignored, and a form with no usable question runs as if it were off. Submitting the form ALWAYS parks the run for review, whatever preview_before_place says: the person typed the inputs, so they see what those inputs produced before anything acts. The form TRAVELS with a copy — import a workflow that asks questions and it asks you the same ones.

Example (a manual workflow that asks before it runs, flags):
  atlas workflow-update --id <workflow id> --trigger-source manual \
    --patch.ui-schema.run-form '{"enabled":true,"fields":[{"id":"sym","label":"What stock are you looking at?","type":"text","required":true,"options":[]},{"id":"side","label":"Calls or puts?","type":"select","required":true,"options":["calls","puts"]}]}'

Example (alert-driven trading workflow, flags):
  atlas workflow-create --name "PENG breakout" --purpose trading \
    --trigger-source alert --alert-id <alert id> \
    --tools stock-quote --tools options-chain \
    --snaptrade-account-id <broker id> --notify-discord-dm true \
    --instruction "When the alert fires, buy 1 PENG call…" \
    --output-schema '{"triggers":[{…from Trigger-Workflow-Schema…}]}'

VERIFY AFTER CREATING: exit 0 / success:true means the row was WRITTEN, not that it holds what you intended — a nested/array field can land the wrong shape with no error (see the CRITICAL dotted-flag warning above). Call Workflow-Open on the returned workflow_id and confirm every field you set (especially output_schema) reads back exactly as intended BEFORE telling the user it's done.
````

## `Workflow-Update`

🔴 acts. Update fields on an existing workflow owned by the caller.

| Field | Type | Needed | Default |
|---|---|---|---|
| `workflow_id` | string | yes |  |
| `patch` | object | yes |  |
| `suggest` | boolean | no | `false` |
| `note` | string | no | `""` |

The tool's own description, in full:

````text
Update fields on an existing workflow owned by the caller. Send only the keys you want to change via `patch` — omitted keys stay as-is.
SUGGESTING A CHANGE TO SOMEONE ELSE'S WORKFLOW: pass `suggest: true` to send the edit to that workflow's author to review instead of saving it. Use it when the user helps out on a workflow someone else wrote (they were added as a collaborator) and wants to propose something rather than change their own copy — the author sees exactly what would change, before and after, and nothing happens unless they accept it. Same `patch`; the only difference is where it goes. Only for a workflow the caller does NOT own; on your own workflow just save. Ask the user which they want — never decide it for them.
With `suggest`, ALWAYS send `note` — a sentence or two on WHY, in the user's own words where you have them, and your reasoning where you don't. The author reads it in Discord before they open anything, and a change that arrives with no reason behind it is one they have to guess at. A flip to status='active' fails if the workflow has no broker account. This runs the SAME logic as the dashboard form, so an AI edit forks / arms / fans out identically.
SEND ONLY WHAT YOU ARE CHANGING, in ONE call. Anything you leave out keeps the value it already has, and that holds INSIDE nested objects too, not just at the top level. To change the reasoning, send `instruction` alone; do NOT restate tools, tool_params or output_schema 'to be safe'. Restating a field you did not mean to touch is the most common way an edit damages the rest of a workflow: your copy of it replaces what is stored, so anything your copy lost is gone.
Nested objects (output_schema, ui_schema, tool_params, execution_overrides) MERGE: a key you name is changed, a key you omit is kept, a key set to null is REMOVED. LISTS are the exception: a list you send replaces the stored list whole, because there is no unambiguous way to say 'change item 2'. So when you touch output_schema.triggers or a bracket_take_profit_levels ladder, include every item you want to keep.
The patch accepts EVERY workflow field: name, instruction, purpose (via ui_schema), tools, output_tools (what it CALLS once it has decided — see Workflow-Create), tool_params (the note on each tool: when you ADD a tool to tools or output_tools, send its note in the same patch, see Workflow-Create for what a note says; the answer lists the ones still empty under `tools_without_notes`), output_schema (OPTIONAL — no trade is ever forced; omit/clear it to {} for a no-trade workflow; output_schema.trades_mode 'auto' turns its ONE trigger entry into a template Atlas repeats across the tickers it picks, and 'manual' — the default — means the entries ARE the trades; plays_mode does the same for `plays`. Switching a section to auto means sending exactly ONE entry for it, with symbol null; two or more is a 400. A signal_creator's plays also take a per-play `score` (1-10; omit to let the run rate them), a top-level `plays_reason` (one sentence every play carries; omit to let the run write each one) and a top-level `plays_destinations` ('community' and/or group ids — several destinations is ONE play reaching everybody across them, not one play per group)), execution_overrides (a copy's own size, budget and exit split: see ON A COPY below), snaptrade_account_id, trigger_source, schedule, timezone, alert_id, alert_max_runs_per_day, notify_discord_dm + notification_format (via ui_schema), auto_accept_updates, status, visibility.
ON A COPY of somebody else's workflow, these are the person's OWN and changing them never stops the copy following its author:
  - THEIR BUDGET: execution_overrides {"budget_cents": 50000} = the most ONE trade may spend in their account, in CENTS (50000 is $500). Atlas works out how many contracts or shares fit when it buys. It replaces any size they had set.
  - THEIR SIZE instead of a budget: execution_overrides {"fixed_contracts": 2} (always 2 contracts) or {"contract_multiplier": 0.5} (half the author's count); for shares fixed_quantity / quantity_multiplier. A size and a budget are one decision: setting one clears the other.
  - HOW THEIR POSITION COMES OFF at the author's targets: execution_overrides {"exit_split": "follow" | "front" | "back" | "even"}.
    A key set to null is removed, and the copy is back on the author's own size. Their stop and targets are the author's; changing those makes the copy their own.
  - LET THE AUTHOR CLOSE THIS TRADE FOR ME: ui_schema {"allow_owner_manual_exit": false} means the author pressing Close all or Take profit now no longer reaches this copy; it stays in until its own stop or target. true (the default) lets the author's press close it too. It covers only what a person presses: the automatic stop and targets always run. On the AUTHOR's own workflow the same key is "Let people who copy this have their trades closed with mine".
  Also theirs, as on any workflow: name, snaptrade_account_id (their broker), alert_id (their own alert beside the author's), alert_max_runs_per_day, visibility, notify settings and status.
trigger_source SWITCHES FREELY at any time — cron<->alert<->both<->manual — by sending trigger_source PLUS whatever it now needs (schedule for cron/both, alert_id for alert/both) in the SAME patch call. A schedule or alert_id left over from the PREVIOUS source is harmless (only the ACTIVE source is read) — you never need a separate call to clear the old one first.
CRITICAL — NEVER build an ARRAY field (output_schema triggers/bracket_take_profit_levels, or any list) with the CLI's per-index dotted flags (--patch.output-schema.triggers.0.symbol SPY --patch.output-schema.triggers.1.symbol QQQ). The CLI's dotted-path builder ALWAYS creates a plain object for numeric segments, never a real array — it silently rewrites your list as {'0': {...}, '1': {...}}, which the dashboard then reads as empty (Array.isArray fails), looking exactly like your edit was dropped even though it saved. Instead pass the WHOLE array-containing value as ONE JSON-string flag, e.g. --patch.output-schema '{"triggers":[{"symbol":"SPY", ...},{"symbol":"QQQ", ...}]}', or call this tool directly with a real `patch` object (not the CLI) when your MCP client supports it.
EDITING ONE TRADE FIELD (contracts, side, call/put, strike, a ladder level): the trades live in the output_schema.triggers LIST, and a list is sent whole. Workflow-Open first, take the current triggers array, change the field you mean to, and send that array back with every trade still in it. Everything OUTSIDE the list (and every other workflow field) is left alone by itself; you only need to restate the list. Call Trigger-Workflow-Schema for the exact field names.
EDITING ONE ui_schema KNOB (e.g. just purpose, or turning review-before-it-places on with {"preview_before_place": true}, or the run form with {"run_form": {…}}): send patch.ui_schema with ONLY the key(s) you are changing (e.g. {"purpose": "analysis"}). Every other knob (notify_discord_dm, notification_format, no_subscribers, preview_before_place, run_form, the flow diagram) is left exactly as it was. Same for tool_params: {"Web-Search": {"notes": "..."}} changes that one tool's note and leaves every other tool's params untouched.
VERIFY AFTER UPDATING: a 200/success:true means the row was WRITTEN, not that it now holds what you intended — call Workflow-Open right after and confirm every field you changed reads back exactly as intended (especially any array field) BEFORE telling the user it's done.
Args:
  workflow_id: required UUID.
  patch: dict of the fields to change. Scalar fields are fine as dotted CLI flags, e.g. --patch.trigger-source alert --patch.alert-id <id> --patch.status active — but ANY array-valued field must be passed as a single JSON-string flag (see CRITICAL note above), never decomposed.
````

## `Workflow-List`

🟢 reads. List the caller's workflows (id, name, status, schedule, visibility) for programmatic discovery.

Takes nothing.

## `Workflow-Open`

🟢 reads. Show the caller's workflows.

| Field | Type | Needed | Default |
|---|---|---|---|
| `workflow_id` | string | no |  |
| `platform` | string | no | `"other"` |

## `Workflow-Run`

🔴 acts. Run one of the caller's workflows once, now, instead of waiting for its schedule or alert.

| Field | Type | Needed | Default |
|---|---|---|---|
| `workflow_id` | string | yes |  |
| `form_answers` | object | no |  |

## `Workflow-Review`

🔴 acts. A workflow set to "review before it places" holds each run until somebody approves it.

| Field | Type | Needed | Default |
|---|---|---|---|
| `workflow_id` | string | yes |  |
| `action` | string | no | `"show"` |
| `review_id` | string | no | `""` |
| `reasoning` | string | no |  |
| `triggers` | array | no |  |

## `Workflow-Abort`

🟠 changes. Stop a workflow run that is in progress right now.

| Field | Type | Needed | Default |
|---|---|---|---|
| `workflow_id` | string | yes |  |
| `run_id` | string | no | `""` |

## `Workflow-Logs`

🟢 reads. Return recent run logs for a workflow the caller owns.

| Field | Type | Needed | Default |
|---|---|---|---|
| `workflow_id` | string | yes |  |
| `limit` | integer | no | `25` |
| `platform` | string | no | `"other"` |

## `Workflow-Performance`

🟢 reads. Closed-trade performance for one workflow the caller owns.

| Field | Type | Needed | Default |
|---|---|---|---|
| `workflow_id` | string | yes |  |
| `platform` | string | no | `"other"` |

## `Workflow-Journal`

🟠 changes. Read or change a workflow's JOURNAL.

| Field | Type | Needed | Default |
|---|---|---|---|
| `workflow_id` | string | yes |  |
| `action` | string | no | `"show"` |
| `text` | string | no |  |
| `instruction` | string | no |  |
| `enabled` | boolean | no |  |
| `cadences` | array | no |  |
| `run_at` | string | no |  |
| `allow_prompt_edit` | boolean | no |  |
| `mode` | string | no |  |
| `entry_id` | string | no |  |
| `pinned` | boolean | no |  |
| `limit` | integer | no | `20` |

The tool's own description, in full:

````text
Read or change a workflow's JOURNAL.

When journalling is on, Atlas writes a short note every time one of this workflow's trades finishes — re-checking the same charts and numbers it used when it opened the trade, so it can see what changed — and reads those notes back on every later run. It is history and memory for a strategy.

YOU CAN CHANGE WHAT IS ALREADY WRITTEN. The entries are not a read-only record: when the user asks you to fix, rewrite, tidy, shorten, merge, de-duplicate or remove what the journal says, do it with this tool — one entry at a time with `edit`/`delete`, or the whole thing at once with `write`. Never tell them it cannot be done, and never send journal text through Workflow-Update, which does not carry entries.

actions:
  show   — (default) the journal so far, plus any changes it made to the workflow's instructions. Each entry comes back with an `id`.
  add    — add ONE entry, with `text`. Set pinned=true to keep it at the top, where Atlas always reads it.
  edit   — rewrite ONE entry: `entry_id` from `show`, plus the new `text` and/or `pinned`.
  delete — remove ONE entry: `entry_id` from `show`. It is gone for good.
  write  — replace the whole journal with your own text. Blank lines start a new entry. This is the same free-form box the dashboard shows. Use it to rewrite several entries at once — read `show` first, or you will drop what you did not mean to touch.
  update — turn journalling on/off (`enabled`), set what Atlas should write down (`instruction`), when it writes (`cadences`, `run_at`), who writes it (`mode`), or allow/stop it editing the instructions (`allow_prompt_edit`). Pass only what you want to change. WHEN IT WRITES (`cadences`, a list: tick as many as you like, exactly the boxes under "When should Atlas write?" in the form):
    per_trade      After every trade (or play) finishes. Only for a workflow that trades, sends the order, or sends plays.
    on_alert_fire  After an alert it made goes off. Only for a workflow that creates alerts.
    per_run        After every run, including a run that decided to do nothing. Any workflow. THE one for a workflow that only analyses, which never closes a trade.
    daily | 3d | weekly | monthly   Once a day, every 3 days, every week, every month, looking back over that stretch. These four run at `run_at` ("HH:MM", Eastern, default 16:10). `run_at` means nothing for the first three, which write when the thing happens.
  A name not on this list is refused, not dropped. Leave `cadences` out to keep what is saved (a new journal starts on per_trade).
WHO WRITES (`mode`): "atlas" (the default) writes on the cadences above; "manual" keeps the journal as the person's own notes, which Atlas reads on every run and never adds to.
  revert — put back the instructions Atlas replaced. Give an entry_id from `show`, or omit it to undo the most recent change.

Only ever on the user's say-so. The journal is what the strategy has learned, and rewriting it un-asked changes how every later run trades.

`instruction` is plain English and it is the authority: Atlas records what it says and nothing more. It is ALSO what decides whether Atlas may edit the workflow's own instructions — with allow_prompt_edit on, Atlas still only rewrites them when this text explicitly tells it to, never on its own judgement. Every rewrite is saved, so `revert` can always undo it.

Atlas can also look things up while journalling (charts, exposure, flow, quotes) when the instruction asks it to, e.g. "check where the GEX wall sits now". It can only READ: it can never place an order or change anything from here.

Only the workflow's author has a journal: copies read the author's rather than keeping their own.
````

## `Workflow-History`

🟠 changes. A workflow's earlier versions, and going back to one.

| Field | Type | Needed | Default |
|---|---|---|---|
| `workflow_id` | string | yes |  |
| `version_id` | string | no | `""` |
| `restore` | boolean | no | `false` |

## `Workflow-Restore`

🔴 acts. Turn a PAUSED workflow back on.

| Field | Type | Needed | Default |
|---|---|---|---|
| `workflow_id` | string | yes |  |

## `Workflow-Delete`

🟠 changes. Permanently delete a workflow owned by the caller.

| Field | Type | Needed | Default |
|---|---|---|---|
| `workflow_id` | string | yes |  |

## `Workflow-Discover`

🟢 reads. Search the public workflow marketplace (Discover).

| Field | Type | Needed | Default |
|---|---|---|---|
| `query` | string | no | `""` |
| `limit` | integer | no | `25` |

## `Workflow-Import`

🟡 adds. Clone a workflow into the caller's account — their OWN, or any public/unlisted one.

| Field | Type | Needed | Default |
|---|---|---|---|
| `workflow_id` | string | yes |  |

## `Workflow-Follow`

🟠 changes. Stop following a workflow's author, or follow them again.

| Field | Type | Needed | Default |
|---|---|---|---|
| `workflow_id` | string | yes |  |
| `follow` | boolean | no | `true` |

## `Workflow-Folder-List`

🟢 reads. List your workflow folders and which workflows are filed in each.

Takes nothing.

## `Workflow-Folder-Create`

🟡 adds. Create a workflow folder to organize your Workflows list.

| Field | Type | Needed | Default |
|---|---|---|---|
| `name` | string | yes |  |
| `color` | string | no |  |
| `workflow_id` | string | no | `""` |
| `workflow_ids` | array | no |  |

## `Workflow-Folder-Move`

🟠 changes. File one or more of your workflows into a folder.

| Field | Type | Needed | Default |
|---|---|---|---|
| `group_id` | string | yes |  |
| `workflow_id` | string | no | `""` |
| `workflow_ids` | array | no |  |
