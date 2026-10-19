# The tools behind this skill (19)

GENERATED from the live server; do not edit by hand. Every field each
tool accepts. Nothing here is required unless the table says so: it is
what is possible.

## `Workflow-Create`

🟡 adds. Create a workflow (a recurring AI setup), saved exactly as supplied and paused.

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
| `broker_account_id` | string | no |  |
| `status` | string | no | `"paused"` |
| `visibility` | string | no | `"private"` |
| `trigger_source` | string | no | `"cron"` |
| `run_once_at` | array | no |  |
| `alert_id` | string | no |  |
| `source_workflow_ids` | array | no |  |
| `decided_by` | string | no |  |
| `script` | string | no |  |
| `tool_args` | object | no |  |
| `script_code` | string | no |  |
| `script_settings` | array | no |  |
| `hide_logic` | boolean | no |  |
| `alert_ids` | array | no |  |
| `alert_creator_id` | string | no |  |
| `alert_creator_ids` | array | no |  |
| `notify_discord_dm` | boolean | no |  |
| `notify_phone` | boolean | no |  |
| `notify_widget` | boolean | no |  |
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
Create a workflow (a recurring AI setup), saved exactly as supplied and paused. A trading workflow's trades go in output_schema = {"triggers": [card, ...]}: each card needs symbol + asset_class (an option adds option_type, strike, expiry), a size (contracts / quantity / spreads or bracket_trade_budget), enter_side + enter_order_type, and order_strategy ("bracket" for a stop/target). Every field is typed under output_schema.triggers; worked examples: Trigger-Workflow-Schema.

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
  output_schema: the TRADE / trigger contract the AI fills. OPTIONAL — a workflow does NOT have to place a trade at all; omit it (or leave {}) for purpose analysis/draft, or any trading workflow that should only reason/report this run. When you DO want one, EVERY trade knob is here and editable: symbol, asset_class, option_type (call/put), side (buy/sell), strike, expiry, contracts (option) or quantity (shares), enter_order_type (market/limit) + enter_limit_price, entry watch, bracket stop-loss + take-profit ($ or %), a TRAILING STOP, the take-profit SCALE-OUT LADDER (bracket_take_profit_levels[] + bracket_take_profit_loop), how the exits split across those levels (bracket_exit_split: follow/front/back/even), and label-based OCO/OEO (cancels_labels / activates_labels). SIZING BY MONEY: instead of contracts/quantity a trade can carry bracket_trade_budget (the most it may spend, in dollars) — then OMIT contracts/quantity entirely and Atlas works out how many fit at the price the order actually pays, as close under the budget as whole units allow. Set a budget only when the user asked for one; never invent it. Every card field is typed and described in this tool's input schema under output_schema.triggers[]; Trigger-Workflow-Schema adds the groups, the defaults and worked examples (stock bracket, option limit + 50% target + stop + close time, a ladder by budget, an iron condor, a credit put vertical with a stock stop, a debit call vertical, an OCO pair). On a workflow card order_strategy is REQUIRED ("bracket" for a stop and/or target, "one_triggers_other" for an exit watch or an entry only).
  THE STOP-LOSS IS ONE OF THREE KEYS on a trade (never two): bracket_stop_loss_stop_price (a fixed price), bracket_stop_loss_stop_pct (a fixed percent from entry), or bracket_stop_loss_trailing_pct: a TRAILING STOP, the form's "Trailing %". It sits that many percent behind the BEST price since entry and only ever tightens, on shares and on options: {"bracket_stop_loss_trailing_pct": 20} gets out when the trade gives back 20% from its best. Use it when the person says "trailing stop", "trail it" or "let it run but protect the gain". This is the trade's own stop; the stop that moves up after each ladder level is the level's stop_after_pct / stop_after_price instead.
  ONE CARD, EVERY TICKER: output_schema.trades_mode is 'manual' (the default when absent) or 'auto'. MANUAL = the entries in `triggers` ARE the trades, one per ticker, exactly those. AUTO = `triggers` holds exactly ONE entry used as a TEMPLATE: leave its symbol null so each run picks the tickers itself, leave option_type / label / cancels_labels / activates_labels off so it decides the call-vs-put side and any one-cancels-other pairing, and every value you DO fix on that one entry (a 30% take-profit, a stop, a size, a budget, a ladder) is applied to every trade it creates. Use auto when the user says 'find me the setups' rather than naming tickers. AUTO WITH TWO OR MORE ENTRIES IS REJECTED (400) — only the first would ever be used. `plays_mode` is the same switch for the `plays` list a signal_creator sends.
  PLAYS (signal_creator): output_schema.plays is a list of plays written in the SAME shape as `triggers` — a play IS a trade card, renamed at send time, so every trade field above applies to it. Three things a play carries that a trade does not:
    * `score` on each play: conviction, an integer 1-10. OMIT it to let the run rate each play itself — that is the default and usually right.
    * `plays_reason` (top-level, next to `plays`): ONE sentence every play this workflow sends carries. Omit it and the run writes each play's own from what it saw that run, which is worth more to a follower than a line written weeks earlier. Set it and that sentence is pinned on all.
    * `plays_destinations` (top-level): where they go. A list where 'community' is the public board and anything else is a signal group id (from Signal-Groups). Omit for the board. SEVERAL destinations is still ONE play — one signal, one tracked trade, one exit — reaching everybody across those groups; it is NOT one play per group.
  A play workflow needs NO broker. broker_account_id is optional there and used only by a play carrying `trade_for_me: true`, which puts the AUTHOR's own money in — never set that unless the user asked for it.
  broker_account_id: broker account id to trade in. Required to activate a trading workflow.
  ui_schema: dict of UI/display flags stored verbatim (purpose, notify_discord_dm, notify_phone, notify_widget, notification_format are the common ones; pass any others the form uses here). Merged with the purpose/notify flags below.
  auto_accept_updates: subscriber flag — true auto-applies the author's later edits; false holds the copy at its current revision.
  (A COPY's own size, budget and exit split, execution_overrides, are set with Workflow-Update on an imported copy, not on a fresh create: see "ON A COPY" there.)
  trigger_source: 'cron' (schedule) | 'alert' (an alert fires it) | 'both' | 'manual' (nothing fires it; the user presses Run now) | 'workflow' (other workflows start it: see source_workflow_ids).
  source_workflow_ids: with trigger_source 'workflow', the person's OWN workflows this one runs after, by id or exact name (at most 10; never itself; a copy they follow or a template cannot start anything). Each time one of them finishes a run, this one runs and is told what that run decided ("<name> ran: it decided ..."). A save that would make a loop (A starts B starts A) is refused. Several are fine, like several alerts.
  decided_by: who decides each run. 'atlas' (default) = Atlas's own model reads the tools and decides. 'agent' = YOUR agent decides (the same as ui_schema.run_by "agent", still accepted; see below). 'script' = a Python script in the workflow's files decides, with no model at all: input data in, a decision out.
  script_code: with decided_by 'script', the script itself (Python 3.12, at most 1 MB). It is saved as the workflow's main.py; with none, the workflow starts with a short starter script. Each run it runs on Atlas's own runner (numpy, pandas, scipy and more; NO internet; 5 minutes; 1 GB) and does what it says through the `atlas` module, which is built in:
    import atlas
    atlas.settings["broker"]   # its Settings, by name (also env ATLAS_BROKER)
    atlas.input                  # the alert, the run, the trade card
    atlas.call("Stock-Quote", symbol="SPY")   # ANY Atlas tool, as the owner
    atlas.ask("Where is SPY's gamma wall?", tools=None, results=False)  # Atlas AI does a piece of work
    atlas.trade(symbol="SPY", asset_class="stock", quantity=1, enter_side="buy", enter_order_type="market")   # one whole trade card
    atlas.trade(..., broker=atlas.settings["broker2"])   # in another Broker account setting
    atlas.notify("what this run says")
  atlas.trade TAKES THE TRADE CARD'S FIELDS as named arguments (help(atlas.trade) lists them all): symbol, asset_class "stock"|"option", option_type, strike, expiry; contracts | quantity | spreads | bracket_trade_budget; enter_side, enter_order_type "market"|"limit", enter_limit_price, enter_trigger_operator + enter_trigger_value (a stock price to wait for), enter_at_time; exits bracket_stop_loss_stop_pct (-30) | _stop_price | _trailing_pct, bracket_take_profit_limit_pct (50) | _limit_price, bracket_price_basis, bracket_take_profit_levels [{pct|price, quantity, stop_after_pct?}], bracket_exit_split, exit_at_time, exit_trigger_operator + exit_trigger_value; label / cancels_labels / activates_labels / oco_group; a spread: spread_strategy, spread_side, spread_direction, spread_legs_spec | spread_legs, spread_take_profit_pct | _price, spread_stop, spread_stop_close_with, spread_take_profit_close_with, spread_close_at; and broker. order_strategy is worked out from the exits. A wrong field or value raises atlas.AtlasError at once, naming the field and what it allows; with no trade card on the workflow the leg must be a whole trade, with one the card fills what the leg leaves out.
  atlas.trade places a trade the normal way (the card's fixed values, the checks, the cap, review before it places), and it shows in the workflow's Performance. It goes to the FIRST Broker account setting unless broker= names another. An order tool called with atlas.call acts for the OWNER only and does not show in Performance. atlas.ask runs one Atlas AI turn as the owner with the read-only tools (or the ones named in tools=; a test run only reads), returns its text (or {text, results}), one request each, at most 5 a run. atlas.notify is the run's message, sent on the workflow's own notification switches to the owner; a run that trades nothing and says nothing sends nothing. A decision.json {reasoning, act, triggers} in the folder still works. A script error or a timeout FAILS the run with the error; it never falls back to a model. A SCRIPT WORKFLOW IS NEVER FOLLOWED: it can be shared, found and imported, and every copy is a workflow of its own (its own copy of the script, the setting names with no values, paused, no broker, no updates from the author). It cannot be hidden (hide_logic is refused). An AI workflow that has followers cannot be switched to a script. Purposes trading, draft and analysis only. Each run uses one request.
  script_settings: the script's Settings, like Pine Script inputs: [{name, type, value}], at most 30, name = small letters, digits and _ ("max_contracts"). type is broker (several allowed) | signal_group | workflow | workflow_folder | alert (the value is one of the person's own, by id or exact name) | number | text. Tickers are written in the script. Values are the owner's alone: a copy gets the names with no values.
  script: the script's path in the folder, when it is not main.py.
  THE LOOP FOR A SCRIPT: (1) Workflow-Create decided_by 'script' with script_code (and script_settings); it starts paused, (2) Workflow-Run with test=true, which runs the whole decision with today's data, lets atlas.call only read, places and sends nothing, and answers with what atlas.trade and atlas.notify recorded, the resolved settings, what the script printed and any trade that would not compile, (3) fix with Workflow-Files (write main.py) or Workflow-Update script_code and test again, (4) when the person says so, switch it on with Workflow-Update (status 'active', with its alert or schedule), then read its runs with Workflow-Logs and its checks with Workflow-Checks.
  The atlas-script-workflows skill (the Atlas plugin, Atlas Studio, the CLI's docs/script-workflows.md) has the whole atlas module with examples, the runner's libraries and limits, and checks.py.
  hide_logic: true hides HOW the workflow works from everybody but its owner and collaborators: its instruction, tools, trade card, diagram, script and settings, journal, files and the tools its runs used. Followers still follow (the same trades, the write-up); nobody else can copy it as their own. Not for a script workflow (it has no followers).
  tools / tool_args: optional for a script (it calls tools itself with atlas.call); any read-only tool listed is called first with its saved arguments and its answer is in atlas.input["tools"].
  run_once_at: ['YYYY-MM-DD HH:MM', ...] in `timezone` — specific dates and times to run at, once each (the dashboard's Once chip). Written into schedule as `once` lines for you; use it INSTEAD of schedule.
  schedule: when it runs, in `timezone` (used for cron/both); one line per time. A cron line ('30 9 * * 1-5') recurs; a `once YYYY-MM-DD HH:MM` line fires at that date and time and never again (list several lines for several dates/times). Use cron lines OR once lines, not both. Required to activate a cron workflow.
  timezone: tz name; defaults to 'US/Eastern'. Times are EASTERN unless you pass another zone.
  alert_id: an alert's id (from List-Alerts / Trigger-Workflow-Schema) that drives this workflow when trigger_source includes 'alert'. It must be one of the person's alerts that exists now: its id or its exact name (the name is stored as its id). A made-up id is refused, so create the alert with Create-Alert first and use the id it answers with.
  alert_ids: SEVERAL alerts, as a list of ids — any of them firing runs this workflow. The dashboard calls it 'Also run on these alerts'. Use it instead of alert_id when the person named more than one.
  alert_creator_id / alert_creator_ids: an alert_creator workflow whose own alerts drive this one — the same binding the form's alert-creator picker writes. Singular for one, the list for several.
  alert_max_runs_per_day: cap on alert-driven runs/day (resets each Eastern morning). Omit / null = unlimited.
  notify_discord_dm: true (default) DMs the run result on Discord; false runs silently. Stored in ui_schema.
  notify_phone: true sends the same message, made short, to the person's phone; false keeps it off the phone. Omit = the phone follows notify_discord_dm. Stored in ui_schema.
  notify_widget: true (default) keeps the run's latest message, cut to a few lines, for this workflow's widget in the website's side panel; false does not. Stored in ui_schema.
  status: 'paused' (default) or 'active'.
  visibility: 'private' (default) | 'unlisted' | 'Atlas-public'.
  ui_schema.run_by: "agent" = YOU run this workflow, not Atlas. Atlas keeps the schedule, the alerts, the trade card, the checks, the orders, the followers and the log; the thinking is yours. When a run is due Atlas leaves it waiting for you (Workflow-Agent-Waiting-Runs) and you hand in what you decided (Workflow-Agent-Hand-In-Run), which uses one request each time. `tools` and `instruction` are then your own notes: Atlas does not run them. The card says who it is from; pass ui_schema.from to name your agent yourself. For a workflow that trades, sends the order to place by hand, or writes things up. Leave it out for a workflow Atlas runs, which is the usual case.
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
    --broker-account-id <broker id> --notify-discord-dm true \
    --instruction "When the alert fires, buy 1 PENG call…" \
    --output-schema '{"triggers":[{…from Trigger-Workflow-Schema…}]}'

VERIFY AFTER CREATING: exit 0 / success:true means the row was WRITTEN, not that it holds what you intended — a nested/array field can land the wrong shape with no error (see the CRITICAL dotted-flag warning above). Call Workflow-Open on the returned workflow_id and confirm every field you set (especially output_schema) reads back exactly as intended BEFORE telling the user it's done.
````

## `Workflow-Update`

🔴 acts. Update fields on an existing workflow owned by the caller.

| Field | Type | Needed | Default |
|---|---|---|---|
| `workflow_id` | string | yes |  |
| `patch` | object | no |  |
| `suggest` | boolean | no | `false` |
| `note` | string | no | `""` |
| `notify_phone` | boolean | no |  |
| `notify_widget` | boolean | no |  |
| `decided_by` | string | no |  |
| `script` | string | no |  |
| `tool_args` | object | no |  |
| `script_code` | string | no |  |
| `script_settings` | array | no |  |
| `hide_logic` | boolean | no |  |

## `Workflow-Run`

🔴 acts. Run one of the caller's workflows once, now, instead of waiting for its schedule or alert.

| Field | Type | Needed | Default |
|---|---|---|---|
| `workflow_id` | string | yes |  |
| `form_answers` | object | no |  |
| `test` | boolean | no | `false` |
| `test_id` | string | no | `""` |

The tool's own description, in full:

````text
Run one of the caller's workflows once, now, instead of waiting for its schedule or alert. This is a real run: the workflow follows its saved instruction exactly as a scheduled run does, so a trading workflow with a broker account attached may place the order its trade card describes, and the run counts against the user's plan like any other. Use it only when the user asks to run the workflow now. Returns whether the run was started; read the result with Workflow-Logs a little later.
Args:
  workflow_id: required UUID of the workflow to run.
  form_answers: optional answers to the questions the workflow asks before a manual run, keyed by question id.
  test: true = a TEST run, for any workflow (decided by Atlas or by a script). It runs the whole decision with today's data, then stops where a run held for review stops: nothing is armed, no broker is touched, no daily cap is used, nothing is posted or sent to anybody, the workflow's files keep nothing it wrote, the journal writes nothing, and no workflow that runs after this one is started. It uses one request, like a run. The answer carries the decision (act, reasoning), the trades after the card's fixed values were laid over them, `compile_errors` for any trade that would be refused when placed, `basket_problems`, and for a script its stdout and stderr and the files it wrote. A paused workflow can be tested too (a new one starts paused): that is how one is checked before it is switched on. If the answer says state 'running', call again with test_id.
  test_id: read back a test started earlier (kept for a day).
````

## `Workflow-Files`

🟠 changes. The files one of the person's workflows keeps: what its calculations saved (Python code, tables, charts, notes).

| Field | Type | Needed | Default |
|---|---|---|---|
| `action` | string | no | `"list"` |
| `workflow` | string | no | `""` |
| `path` | string | no | `""` |
| `content` | string | no |  |
| `folder` | string | no | `"yours"` |
| `to` | string | no | `""` |
| `allow_empty` | boolean | no | `false` |

The tool's own description, in full:

````text
The files one of the person's workflows keeps: what its calculations
    saved (Python code, tables, charts, notes). Each run of the workflow can
    read them, so editing a file here (for example the code a calculation
    uses) changes what the next run does. The person sees the same files on
    the workflow's Files screen on the website.

    Keep it organized, never a pile: folders by kind (code/, data/, charts/,
    notes/) or by ticker, folders inside folders up to 6 parts with the file
    (tickers/SPY/2026/10/charts/day.png). A folder exists once a file is in it
    (write "reports/summary.md" and reports/ is there); move renames a file or
    moves a whole folder; delete removes a file or a whole folder.

    Only the person's own workflows. A workflow that follows an author also
    has the author's files, which can be listed and read but never changed.
    Text files only, at most 1 MB from here; 5 MB a file, 20 MB and 50 files a
    workflow. Running code is not done here: the workflow runs it (Workflow-Run).

    Args:
        action: list, read, write, move or delete.
        workflow: the workflow's id or its exact name.
        path: the file inside the folder, e.g. "sizing.py" or "out/returns.csv".
            For read, write and delete.
        content: for write, the whole text of the file (it replaces the file).
            REQUIRED for write; a read answers with the text in `text`, a
            write takes it in `content`. An empty content is refused.
        allow_empty: true to write an EMPTY file on purpose (default false).
        to: for move, the new path of the file or folder, e.g. "data/fills.csv"
            or "archive/2026-10". Nothing is written over: a taken path is refused.
        folder: "yours" (default) or "author" (list and read only, on a
            workflow that follows an author).
````

## `Workflow-Checks`

🟠 changes. The checks of one of the person's script workflows (a workflow a script decides): what each check found, and running, pausing, resuming or deleting one.

| Field | Type | Needed | Default |
|---|---|---|---|
| `action` | string | no | `"list"` |
| `workflow` | string | no | `""` |
| `check_id` | string | no | `""` |
| `only` | array | no |  |

The tool's own description, in full:

````text
The checks of one of the person's script workflows (a workflow a script
    decides): what each check found, and running, pausing, resuming or
    deleting one. The checks are checks.py in the workflow's files (write it
    with Workflow-Files); they run after every run of the script and when
    asked here. They use no request: they read the workflow's own files and
    the last run (atlas.last_run) and reach no tool. The person sees the same
    on the workflow's Checks tab on the website.

    checks.py:
        import atlas
        run = atlas.checks()
        last = atlas.last_run   # the last run: ok, error, stdout, notify, trades
        if run.wants("trades"):
            n = len(last.get("trades") or [])
            run.result("trades", "pass" if n else "warn", "It placed a trade", f"{n} trade(s)")
        run.done()
    result(id, status, title, summary): status is pass, fail, warn or
    suggestion; the summary is one line. A paused or deleted check never runs.

    Args:
        action: list (default), run, pause, resume or delete.
        workflow: the workflow's id or its exact name.
        check_id: for pause, resume and delete, the check's id (as list shows it).
        only: for run, the check ids to run (default: all of them).
````

## `Workflow-Logs`

🟢 reads. Return recent run logs for a workflow the caller owns.

| Field | Type | Needed | Default |
|---|---|---|---|
| `workflow_id` | string | yes |  |
| `limit` | integer | no | `25` |
| `platform` | string | no | `"other"` |

## `Workflow-Open`

🟢 reads. Show the caller's workflows.

| Field | Type | Needed | Default |
|---|---|---|---|
| `workflow_id` | string | no |  |
| `platform` | string | no | `"other"` |

## `Trigger-Workflow-Schema`

🟢 reads. Every field of a TRADE CARD, the shape the trigger tools, Workflow-Create (output_schema.triggers) and a script's atlas.trade all take: type, allowed values, group, stock/option/spread, default; the three must-haves; the usual wrong names; worked examples (stock bracket, option limit + target + stop + close time, ladder by budget, iron condor, credit put vertical, debit call vertical, OCO pair).

Takes nothing.

## `Broker-Connections`

🟢 reads. List all connected brokerage accounts for the authenticated user.

Takes nothing.

## `Search-Tools`

🟢 reads. Find a tool by what it does.

| Field | Type | Needed | Default |
|---|---|---|---|
| `query` | string | no | `""` |
| `limit` | integer | no | `40` |

## `List-Tool-Safety`

🟢 reads. List every Atlas tool by its exact name, with what it says about its own safety: whether it only reads, whether it can change or remove something, whether it reaches outside the user's Atlas account, and a sentence explaining each.

Takes nothing.

## `List-Alerts`

🟢 reads. List the caller's alerts.

| Field | Type | Needed | Default |
|---|---|---|---|
| `active_only` | boolean | no | `true` |
| `platform` | string | no | `"other"` |

## `Stock-Quote`

🟢 reads. Get a real-time UNDERLYING stock quote (not an option contract).

| Field | Type | Needed | Default |
|---|---|---|---|
| `symbol` | string | yes |  |

## `Price-Data-OHLCV`

🟢 reads. Get OHLCV historical bars as JSON (not a single live spot price).

| Field | Type | Needed | Default |
|---|---|---|---|
| `symbol` | string | yes |  |
| `interval` | string | no | `"1d"` |
| `period` | string | no | `"3mo"` |
| `start` | string | no |  |
| `end` | string | no |  |
| `timestamp` | string | no |  |
| `bars` | integer | no |  |

## `Option-Expiration-Dates`

🟢 reads. List available option expiration dates for a symbol.

| Field | Type | Needed | Default |
|---|---|---|---|
| `symbol` | string | yes |  |
| `filter` | string | no | `"next_10"` |

## `Options-Chain`

🟢 reads. Full options chain — many strikes and sides for one or more expirations.

| Field | Type | Needed | Default |
|---|---|---|---|
| `symbol` | string | yes |  |
| `expiration` | string | no |  |
| `from_expiration` | string | no |  |
| `to_expiration` | string | no |  |
| `expiration_range` | string | no |  |
| `max_expirations` | integer | no | `12` |

## `Spread-Quote`

🟢 reads. A spread's legs and its price NOW: each leg's bid and ask, and the spread's natural net (the side each leg would really trade at: sold legs at the bid, bought legs at the ask), its mid, its width and the most one can lose and make.

| Field | Type | Needed | Default |
|---|---|---|---|
| `symbol` | string | yes |  |
| `spread_strategy` | string | yes |  |
| `expiry` | string | no | `"0dte"` |
| `spread_side` | string | no |  |
| `spread_direction` | string | no |  |
| `spread_legs_spec` | object | no |  |
| `spread_legs` | array | no |  |
| `price` | number | no |  |
| `spreads` | integer | no | `1` |

## `Options-Flow`

🟢 reads. Return options-flow trades — a historical record of the trades that printed.

| Field | Type | Needed | Default |
|---|---|---|---|
| `view` | string | no | `"board"` |
| `symbol` | string | no |  |
| `symbols` | array | no |  |
| `expiration_date` | string | no |  |
| `strike` | number | no |  |
| `side` | string | no |  |
| `option_symbol` | string | no |  |
| `from_date` | string | no |  |
| `to_date` | string | no |  |
| `limit` | integer | no | `200` |
| `min_premium` | number | no |  |
| `max_premium` | number | no |  |
| `min_tag` | string | no |  |
| `image_format` | string | no |  |
| `platform` | string | no | `"other"` |
| `max_per_ticker` | integer | no | `3` |
| `max_per_expiry` | integer | no |  |
| `expiry_within_days` | integer | no |  |
| `action` | string | no |  |
| `open_close` | string | no |  |
| `trade_type` | string | no |  |
| `min_size` | number | no |  |
| `max_size` | number | no |  |
| `min_volume` | number | no |  |
| `min_open_interest` | number | no |  |
| `min_spot` | number | no |  |
| `max_spot` | number | no |  |
| `from_time` | string | no |  |
| `to_time` | string | no |  |
| `theme` | string | no | `"dark"` |

## `Greek-Exposure-Single-Expiration`

🟢 reads. NET Greek exposure grid for exactly ONE expiration (one chain fetch).

| Field | Type | Needed | Default |
|---|---|---|---|
| `symbol` | string | yes |  |
| `expiration` | string | yes |  |
