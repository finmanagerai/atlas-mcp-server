---
name: atlas-script-workflows
description: Build an Atlas workflow that a Python script decides instead of a model. The script (main.py) uses the built-in `atlas` module to call any Atlas tool, place trades in the trade card's own fields, send the run's message and ask Atlas AI, with numpy, pandas and the other libraries on Atlas's runner. Covers writing it, the dry run (Workflow-Run test), fixing it, switching it on, and reading its runs and checks. Use when the person wants a rule written as code, a workflow wired to Atlas tools by a script, or a calculation with pandas or a backtest library inside a workflow.
---

# Script workflows

A script workflow is an Atlas workflow whose decision is made by a Python
script, with no model. Atlas keeps everything around the decision: what starts
a run (an alert, a time, another workflow), the trade card's checks, the
orders, the log, the person's dashboard. Each run, Atlas runs the workflow's
`main.py` on its own runner, and the script says what to do through a module
called `atlas`, which is already installed there.

This page says what is possible. `references/tools.md` lists every field of
the tools named here. `references/trade-card.json` lists every field of a
trade.

## The loop

### 1. Create it

`Workflow-Create` with `decided_by: "script"` and the whole script in
`script_code`:

```json
{
  "name": "SPY above its 20-day average",
  "purpose": "trading",
  "decided_by": "script",
  "script_code": "import atlas\n\nq = atlas.call(\"Stock-Quote\", symbol=\"SPY\")\natlas.notify(f\"SPY is at {q['price']}\")\n",
  "script_settings": [
    { "name": "broker", "type": "broker", "value": "<an account, from Broker-Connections>" },
    { "name": "max_contracts", "type": "number", "value": 2 }
  ],
  "broker_account_id": "<the same account>"
}
```

- `purpose` is `trading`, `draft` (the order is sent to place by hand) or
  `analysis` (a write-up). Analysis and draft need no broker account.
- **It starts paused, and a paused workflow can be tested.** Nothing starts
  it until it is switched on (step 4).
- A trading workflow switched on needs `broker_account_id`. The script's
  trades go to its first `broker` setting.
- `script_settings` are the script's inputs, shown under the script on the
  workflow's page, like a chart script's inputs (see Settings below).
- With no `script_code` the workflow starts with a short starter script.
- The answer carries the workflow's id. `Workflow-Open` reads it back.

### 2. Test it

`Workflow-Run` with `{"workflow_id": "...", "test": true}`. A test is a dry
run: the script runs with today's data, `atlas.call` and `atlas.ask` only
read, `atlas.trade` and `atlas.notify` are recorded and never placed or sent,
nothing is kept in the workflow's files, and nothing starts after it. It uses
one request, like a run. It answers within about two and a half minutes; if
it says `state: "running"`, call `Workflow-Run` again with the `test_id` it
gave.

What comes back:

| Field | What it is |
|---|---|
| `state` | `done` or `failed` |
| `error` | why it failed, in words, with the end of what the script printed to stderr |
| `stdout`, `stderr` | what the script printed |
| `notify` | what `atlas.notify` would have sent |
| `atlas_trades` | what `atlas.trade` was given |
| `trades` | the same trades after the trade card's fixed values were laid over them |
| `compile_errors` | each trade that would be refused when placed, and why |
| `basket_problems` | linked trades (one cancels the other) that would be dropped |
| `atlas_calls` | each `atlas.call`: the tool, whether it answered, how long it took, the error |
| `settings` | the settings as the script saw them |
| `files_written` | the files the script wrote (not kept in a test) |
| `quiet` | the script traded nothing and said nothing: a real run would send nothing |
| `decision` | `{act, reasoning}`: whether it trades, and the notify lines joined |

### 3. Fix it

`Workflow-Files` with `action: "write"`, `path: "main.py"` and the whole new
text in `content` (it replaces the file). `Workflow-Update` with
`script_code` does the same. `action: "list"` and `"read"` show every file
of the workflow: what earlier runs wrote, `checks.py`, `checks.json`. Then
test again, until the test is clean.

### 4. Switch it on

When the person says so, `Workflow-Update` with `patch` holding
`status: "active"` and what should start it:

- an alert: `trigger_source: "alert"` and `alert_id` (or `alert_ids` for
  several; `List-Alerts`, `Create-Alert`);
- a time: `trigger_source: "cron"` and `schedule` (`"30 9 * * 1-5"`, one line
  per time, Eastern unless `timezone` says otherwise; `"once 2026-11-03
  09:35"` runs once);
- another workflow: `trigger_source: "workflow"` and `source_workflow_ids`.

`status: "paused"` stops it again. `trigger_source: "manual"` runs only when
the person presses Run now.

### 5. Watch it

- `Workflow-Logs`: each run. A script run carries `ai_decision.script`:
  `ok`, `error`, `stdout`, the end of `stderr` when it failed, `notify`, the
  trades, each ask, each call.
- `Workflow-Checks`: what `checks.py` found after the last run (below).
- The person sees the same on the workflow's page: Recent runs, Trades,
  Performance, Files and Checks.

## What a run sees

The script runs from the top of the workflow's folder, so every file of the
workflow is there to open by its path, and what it writes (outside
`input.json`, `atlas_run.json` and `decision.json`) is kept for the next run:

```python
import atlas, json, os, time
state = json.load(open("state/last.json")) if os.path.exists("state/last.json") else {}
price = atlas.call("Stock-Quote", symbol="SPY")["price"]
if state.get("last_price") and price > state["last_price"] * 1.01:
    atlas.notify(f"SPY is up more than 1% since the last run: {price}")
os.makedirs("state", exist_ok=True)
json.dump({"last_price": price, "at": time.time()}, open("state/last.json", "w"))
```

`atlas.input` is what started the run:

```python
import atlas

atlas.input.get("run")       # {"source": "alert" | "cron" | "manual" | "workflow", "fired_at": ..., "source_workflow_id": ...}
atlas.input.get("alert")     # {"id", "message", "payload"}: the alert that started it, with what it measured
atlas.input.get("tools")     # {"Stock-Quote": {"kind": "json", "data": {...}}}: see "Tools called before the script"
atlas.input.get("trade_card")  # the workflow's trade card
atlas.input.get("form_answers")
```

## The `atlas` module

| | |
|---|---|
| `atlas.call(tool, **args)` | any Atlas tool, as the workflow's owner; returns its answer |
| `atlas.trade(**fields)` | one trade, in the trade card's own fields, placed after the run |
| `atlas.notify(text)` | the run's message |
| `atlas.ask(prompt, tools=None, results=False)` | Atlas AI does one piece of work |
| `atlas.settings` | the workflow's settings, by name |
| `atlas.input` | what started the run |
| `atlas.checks()`, `atlas.last_run` | for `checks.py` |
| `atlas.AtlasError` | what a refused or failed call raises, in words |

### Reading data: `atlas.call`

The tool's name exactly as Atlas lists it, and its fields as keyword
arguments. The answer is the tool's JSON as Python dicts and lists. An answer
with an error, or a refusal, raises `atlas.AtlasError`.

```python
import atlas

q = atlas.call("Stock-Quote", symbol="SPY")
price = q["price"]

bars = atlas.call("Price-Data-OHLCV", symbol="SPY", interval="1d", period="6mo")
closes = [b["close"] for b in bars["data"]]          # each bar: timestamp, open, high, low, close, volume

dates = atlas.call("Option-Expiration-Dates", symbol="SPY")["expirations"]   # ["2026-10-20", ...]
chain = atlas.call("Options-Chain", symbol="SPY", expiration=dates[0])

ic = atlas.call("Spread-Quote", symbol="SPY", spread_strategy="iron_condor", expiry="0dte",
                spread_legs_spec={"sell_at": {"mode": "from_price", "value": 10},
                                  "buy_at": {"mode": "further_out", "value": 5}})
print(ic["natural"], ic["max_loss_per_spread"], [(l["action"], l["option_type"], l["strike"]) for l in ic["legs"]])

flow = atlas.call("Options-Flow", symbol="SPY", expiry_within_days=7, min_premium=250000, limit=100)
rows = flow.get("trades") or []      # each row: time_et, expiry, strike, cp (call/put), side, size, price, premium, type
calls = sum(r["premium"] or 0 for r in rows if r.get("cp") == "call")
puts = sum(r["premium"] or 0 for r in rows if r.get("cp") == "put")
```

Print one answer in a test (`print(json.dumps(q, indent=1)[:2000])`) to see
every field before the script leans on one.

### Trades: `atlas.trade`

One call is one trade, in the same fields as a trade card
(`references/trade-card.json`, or `Trigger-Workflow-Schema`). After the run
it goes through everything a trade card's trade does: the card's fixed values
laid over it, the checks, the daily cap, the hold for review when the
workflow has it on, then the broker. It shows in the workflow's Trades and
Performance. At most 25 a run.

```python
import atlas

# 10 shares, a 2% stop and a 4% target
atlas.trade(symbol="SPY", asset_class="stock", quantity=10, enter_side="buy",
            enter_order_type="market", order_strategy="bracket",
            bracket_stop_loss_stop_pct=-2, bracket_take_profit_limit_pct=4)

# one call, at most $500, out half at +30% and the rest at +70%, stop at -30%
q = atlas.call("Stock-Quote", symbol="SPY")
expiry = atlas.call("Option-Expiration-Dates", symbol="SPY")["expirations"][1]
atlas.trade(symbol="SPY", asset_class="option", option_type="call",
            strike=round(q["price"]), expiry=expiry, bracket_trade_budget=500,
            enter_side="buy_to_open", enter_order_type="market",
            order_strategy="bracket", bracket_stop_loss_stop_pct=-30,
            bracket_take_profit_levels=[{"pct": 30, "quantity": "50%"},
                                        {"pct": 70, "quantity": "remaining"}])

# two 0DTE iron condors, 10 from the price and 5 wide, at a 1.20 credit
atlas.trade(symbol="SPY", asset_class="option", spread_strategy="iron_condor",
            expiry="0dte", spreads=2,
            spread_legs_spec={"sell_at": {"mode": "from_price", "value": 10},
                              "buy_at": {"mode": "further_out", "value": 5}},
            enter_order_type="limit", enter_limit_price=1.20,
            spread_take_profit_pct=50, spread_stop={"basis": "premium", "max_loss_pct": 50},
            spread_close_at="15:45")
```

- **Several broker accounts.** A trade goes to the workflow's first `broker`
  setting. `broker=` sends it to another one, by its value or its name:
  `atlas.trade(..., broker=atlas.settings["broker2"])` or
  `atlas.trade(..., broker="broker2")`. A broker that is not one of the
  workflow's settings fails the run.
- An order tool called through `atlas.call` is the owner's own trade, not the
  workflow's: it is placed at once, outside the card's checks, and it does not
  show in the workflow's Performance.
- A test returns each trade in `trades` and `compile_errors` instead of
  placing it.

### The message: `atlas.notify`

```python
import atlas

price = atlas.call("Stock-Quote", symbol="SPY")["price"]
atlas.notify(f"SPY is at {price:.2f}")
atlas.notify("Above its 20-day average: bought 10 shares.")
```

The run's message, sent on the workflow's own notification switches (Discord,
phone, the side panel's widget) and shown under Recent runs. Several calls
are several paragraphs; at most 20 a run. A run that trades nothing and says
nothing sends nothing.

### Atlas AI: `atlas.ask`

```python
import atlas

view = atlas.ask("Where is SPY's largest gamma strike for today's expiration, and is price above it? One line.",
                 tools=["Greek-Exposure-Single-Expiration", "Stock-Quote"])
both = atlas.ask("Summarise today's NVDA flow in two lines.", results=True)   # {"text", "results"}
```

One turn of Atlas AI, as the owner, with the read-only tools (or only the
ones named in `tools`; a tool that changes something is used only when named,
and never in a test). It returns the answer's text, or `{"text", "results"}`
with each tool's answer when `results=True`. Each ask uses one request of the
person's plan, tests included; at most 5 a run.

### Settings

`script_settings` are `[{name, type, value}]`, at most 30. A name is small
letters, digits and `_`. Types:

| type | value |
|---|---|
| `broker` | one of the person's broker accounts (several broker settings are fine) |
| `signal_group` | one of their signal groups |
| `workflow` | one of their workflows |
| `workflow_folder` | one of their workflow folders |
| `alert` | one of their alerts |
| `number` | a number |
| `text` | text |

The picker types take an id or an exact name; the script gets the id. The
script reads them as `atlas.settings["max_contracts"]`, or from the
environment as `ATLAS_MAX_CONTRACTS`. Tickers are written in the script, not
in settings.

## Wiring it to Atlas tools

- **Finding a tool.** `Search-Tools` with a few words (`"gamma exposure"`)
  answers with each tool's exact name; `List-Tool-Safety` lists every tool
  with whether it only reads. `references/tools.md` has the fields of the
  ones this page names; each tool's own description has the rest.
- **Arguments** are the tool's own field names, with JSON values: text,
  numbers, `True`/`False`, lists and dicts.
- **Tools called before the script.** A workflow's `tools` list, with each
  tool's arguments in `tool_args` (`{"Stock-Quote": {"symbol": "SPY"}}`), is
  called first, read-only ones only, and the answers are in
  `atlas.input["tools"]`. A script that calls what it needs itself needs no
  `tools` at all.
- **Read and write.** A tool that reads (quotes, chains, flow, exposure,
  holdings, the person's alerts and workflows) works in every run. A tool
  that changes something (an order, an alert, a workflow, a play) works in a
  real run, as the owner, and is refused in a test: the call raises
  `AtlasError` with "... was not called: a test run calls only tools that
  read".
- **Budget.** At most 200 `atlas.call`s a run, 5 asks, 25 trades and 20
  messages. A tool call waits up to five and a half minutes, but the whole
  run has five: narrow a slow tool (Options-Flow on a big name across many
  expirations can take minutes) with its own filters.

## Libraries on the runner

The runner is Python 3.12 with these libraries, and nothing can be installed
there:

<!-- runner-libraries: generated by mcp-server/scripts/sync_tool_docs.py from calc_runner/requirements.in; do not edit by hand -->
| Library | Import | Version | For |
|---|---|---|---|
| numpy | `numpy` | 2.2.6 | arrays and the maths on them |
| pandas | `pandas` | 2.3.3 | tables and time series: bars, returns, rolling windows |
| scipy | `scipy` | 1.18.1 | statistics, optimisation, interpolation |
| polars | `polars` | 2.0.0 | fast tables, for large data |
| duckdb | `duckdb` | 1.5.6 | SQL over tables and over files in the workflow's folder |
| matplotlib | `matplotlib` | 3.11.2 | charts saved as pictures in the workflow's files (`matplotlib.use("Agg")`) |
| quantstats | `quantstats` | 0.0.86 | performance statistics: Sharpe, drawdown, a report; its download helpers fetch nothing here |
| empyrical-reloaded | `empyrical` | 0.5.12 | risk and return measures as functions: Sharpe, Sortino, alpha, beta, max drawdown |
| PyPortfolioOpt | `pypfopt` | 1.6.0 | portfolio weights: lowest risk, best Sharpe, the efficient frontier |
| riskfolio-lib | `riskfolio` | 7.4.0 | portfolio weights by risk measure: CVaR, risk parity, risk budgets |
| statsforecast | `statsforecast` | 2.1.1 | fast forecasts: ARIMA, ETS, Theta |
| prophet | `prophet` | 1.5.0 | trend and seasonality forecasts |
| vectorbt | `vectorbt` | 1.0.0 | backtests of many settings at once, on arrays |
| backtesting | `backtesting` | 0.6.6 | a backtest of one strategy, bar by bar |
| pandas-ta | `pandas_ta` | 0.4.71b0 | indicators: RSI, MACD, moving averages, ATR, Bollinger bands |
| openpyxl | `openpyxl` | 3.1.5 | Excel workbooks, read and written |
| pdfplumber | `pdfplumber` | 0.11.10 | text and tables out of PDF files |
| ofxparse | `ofxparse` | 0.21 | bank and broker export files (OFX, QFX) |
| beancount | `beancount` | 3.2.3 | double-entry accounting in text: lots and cost basis |

Also there, because the ones above use them: scikit-learn (`sklearn`), statsmodels (`statsmodels`), plotly (`plotly`), numba (`numba`).
<!-- /runner-libraries -->

**There is no internet on the runner.** Nothing in a script can reach a web
page, an outside service or a download library: data comes in through
`atlas.call`. quantstats is there for its maths; its download helpers fetch
nothing.

```python
import atlas
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import os

bars = atlas.call("Price-Data-OHLCV", symbol="QQQ", interval="1d", period="1y")["data"]
df = pd.DataFrame(bars)
df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)
df = df.set_index("timestamp")
df["sma20"] = df["close"].rolling(20).mean()
ret = np.log(df["close"]).diff()
z = (ret.iloc[-1] - ret.tail(60).mean()) / ret.tail(60).std()
vol = ret.tail(20).std() * np.sqrt(252)

os.makedirs("charts", exist_ok=True)
ax = df[["close", "sma20"]].tail(120).plot(figsize=(8, 4))
ax.figure.savefig("charts/qqq.png", dpi=110)     # kept in the workflow's Files

last = df.iloc[-1]
atlas.notify(f"QQQ {last.close:.2f}, 20-day average {last.sma20:.2f}; today's move is {z:+.1f} standard deviations; "
             f"20-day volatility {vol:.0%}")
if last.close > last.sma20 and z < 2:
    atlas.trade(symbol="QQQ", asset_class="stock", quantity=atlas.settings.get("shares") or 5,
                enter_side="buy", enter_order_type="market")
```

**Limits of one run:** five minutes of time and of processor, 1 GB of memory,
one processor, 32 processes. A file written in a run is at most 20 MB, and
the workflow's folder keeps at most 5 MB a file, 50 files and 20 MB (200 MB
across all of the person's workflows). The last 8 KB of what the script
prints is kept, and Recent runs shows up to 4,000 characters of it. A run
that goes over its time or memory is stopped and fails.

## Checks: `checks.py`

A workflow's checks are a `checks.py` in its files (write it with
`Workflow-Files`). It runs after every real run of the script, with that run
as `atlas.last_run`, and when asked (`Workflow-Checks` with `action: "run"`,
or "Run checks now" on the page). It reaches no tool and uses no request: it
reads the workflow's own files and the last run.

```python
import atlas, json, os, time

run = atlas.checks()
last = atlas.last_run      # ok, error, stdout, notify, trades, asks

if run.wants("ran-clean"):
    run.result("ran-clean", "pass" if last.get("ok") else "fail", "The script ran",
               last.get("error") or "no error")

if run.wants("said-something"):
    n = len(last.get("notify") or [])
    run.result("said-something", "pass" if n else "warn", "It sent a message", f"{n} line(s)")

if run.wants("sizes"):
    big = [t for t in last.get("trades") or [] if (t.get("quantity") or 0) > 50]
    run.result("sizes", "fail" if big else "pass", "No trade over 50 shares",
               f"{len(big)} too large" if big else "all within 50")

if run.wants("state-fresh"):
    state = json.load(open("state/last.json")) if os.path.exists("state/last.json") else {}
    age = time.time() - state["at"] if "at" in state else None     # main.py writes "at": time.time()
    run.result("state-fresh", "pass" if age is not None and age < 86400 else "suggestion",
               "The state file is from today", "missing" if age is None else f"{age / 3600:.0f} hours old")

run.done()
```

`result(id, status, title, summary)`: status is `pass`, `fail`, `warn` or
`suggestion`; the summary is one line. Results go to `checks.json`, each run
to `checks/history.jsonl`. `Workflow-Checks` lists them, runs them (all, or
`only` some), and pauses, resumes or deletes one; a paused or deleted check
never runs.

## When something goes wrong

A script that raises, runs out of time or memory, or writes a trade the card
refuses FAILS the run. It never falls back to a model.

- **In a test**: `state: "failed"` and `error` in words (`the script main.py
  failed: it ended with exit code 1` and the end of the traceback), plus
  `stderr`, `compile_errors` and `basket_problems`.
- **In a real run**: the owner is told why in the run's message; Recent runs
  on the workflow's page shows the failure in one line, the messages, each
  ask, and **Show output** for what the script printed; `Workflow-Logs` has
  the same in `ai_decision.script`.

Words a run can fail with:

| Words | What happened |
|---|---|
| `it was stopped after 5 minutes` | the run took too long |
| `it was stopped for using more than 1 GB of memory` | too much data in memory at once |
| `... was not called: a test run calls only tools that read` | a write tool in a test |
| `a run may call Atlas at most 200 times` | the tool-call budget |
| `a run places at most 25 trades` | the trade budget |
| `atlas.trade(broker="...") is not one of this workflow's Broker account settings.` | a broker not in the settings |
| `trade 1 (SPY): ...` in `compile_errors` | a trade missing a field, or a stop on the wrong side |

## What to keep in mind

- A script workflow can place real orders in the person's broker account.
  Switch it on to its real start only when the person says so.
- A script workflow is never followed. It can be shared, found and imported,
  and each copy is a workflow of its own: its own copy of the script, the
  setting names with no values, paused, no broker. It cannot be hidden.
- Settings' values are the owner's alone.
- Each run uses one request, whatever it decides; each ask one more.
