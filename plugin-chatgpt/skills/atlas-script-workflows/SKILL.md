---
name: atlas-script-workflows
description: Build an Atlas workflow that a Python script decides instead of a model. The script (main.py) uses the built-in `atlas` module to read Atlas's market data, send the run's message and ask Atlas AI, with numpy, pandas and the other libraries on Atlas's runner. Covers writing it, the dry run (Workflow-Run test), fixing it, switching it on, and reading its runs and checks. Use when the person wants a rule written as code, a workflow wired to Atlas tools by a script, or a calculation with pandas or a backtest library inside a workflow.
---

# Script workflows

A script workflow is an Atlas workflow whose decision is made by a Python
script, with no model. Atlas keeps everything around the decision: what starts
a run (an alert, a time, another workflow), the log, the person's dashboard. Each run, Atlas runs the workflow's
`main.py` on its own runner, and the script says what to do through a module
called `atlas`, which is already installed there.

This page says what is possible. `references/tools.md` lists every field of
the tools named here.

In this edition a script workflow reads, works numbers out and writes up: it
places no trade. A script that trades is set up in Atlas itself, on the
dashboard.

## The loop

### 1. Create it

`Workflow-Create` with `decided_by: "script"` and the whole script in
`script_code`:

```json
{
  "name": "SPY above its 20-day average",
  "purpose": "analysis",
  "decided_by": "script",
  "script_code": "import atlas\n\nq = atlas.call(\"Stock-Quote\", symbol=\"SPY\")\natlas.notify(f\"SPY is at {q['price']}\")\n",
  "script_settings": [
    { "name": "move_pct", "type": "number", "value": 1 }
  ],
  "trigger_source": "manual",
  "status": "active"
}
```

- `purpose` is `analysis`: the run's result is its message and the files
  it writes.
- **A test runs only on a workflow that is switched on.** `trigger_source:
  "manual"` with `status: "active"` is on, and nothing starts it by itself
  while it is being built: only Run now and a test do.
- `script_settings` are the script's inputs, shown under the script on the
  workflow's page, like a chart script's inputs (see Settings below).
- With no `script_code` the workflow starts with a short starter script.
- The answer carries the workflow's id. `Workflow-Open` reads it back.

### 2. Test it

`Workflow-Run` with `{"workflow_id": "...", "test": true}`. A test is a dry
run: the script runs with today's data, `atlas.call` and `atlas.ask` only
read, `atlas.notify` is recorded and never sent,
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
| `atlas_calls` | each `atlas.call`: the tool, whether it answered, how long it took, the error |
| `settings` | the settings as the script saw them |
| `files_written` | the files the script wrote (not kept in a test) |
| `quiet` | the script said nothing: a real run would send nothing |
| `decision` | `{reasoning}`: the notify lines joined |

### 3. Fix it

`Workflow-Files` with `action: "write"`, `path: "main.py"` and the whole new
text in `content` (it replaces the file). `Workflow-Update` with
`script_code` does the same. `action: "list"` and `"read"` show every file
of the workflow: what earlier runs wrote, `checks.py`, `checks.json`. Then
test again, until the test is clean.

### 4. Give it its start

`Workflow-Update` with `patch` holding what should start it:

- an alert: `trigger_source: "alert"` and `alert_id` (or `alert_ids` for
  several; `List-Alerts`, `Create-Alert`);
- a time: `trigger_source: "cron"` and `schedule` (`"30 9 * * 1-5"`, one line
  per time, Eastern unless `timezone` says otherwise; `"once 2026-11-03
  09:35"` runs once);
- another workflow: `trigger_source: "workflow"` and `source_workflow_ids`.

`status: "paused"` stops it. A workflow left on `manual` runs only when the
person presses Run now.

### 5. Watch it

- `Workflow-Logs`: each run. A script run carries `ai_decision.script`:
  `ok`, `error`, `stdout`, the end of `stderr` when it failed, `notify`, each
  ask, each call.
- `Workflow-Checks`: what `checks.py` found after the last run (below).
- The person sees the same on the workflow's page: Recent runs, Files and
  Checks.

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
atlas.input.get("form_answers")
```

## The `atlas` module

| | |
|---|---|
| `atlas.call(tool, **args)` | any Atlas tool, as the workflow's owner; returns its answer |
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

### The message: `atlas.notify`

```python
import atlas

price = atlas.call("Stock-Quote", symbol="SPY")["price"]
atlas.notify(f"SPY is at {price:.2f}")
atlas.notify("Above its 20-day average.")
```

The run's message, sent on the workflow's own notification switches (Discord,
phone, the side panel's widget) and shown under Recent runs. Several calls
are several paragraphs; at most 20 a run. A run that says nothing sends
nothing.

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
  the person's alerts and workflows) works in every run. A tool that changes
  something is refused in a test: the call raises `AtlasError` with "... was
  not called: a test run calls only tools that read".
- **Budget.** At most 200 `atlas.call`s a run, 5 asks and 20 messages. A tool call waits up to five and a half minutes, but the whole
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
    atlas.notify("Above its average on an ordinary day.")
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
last = atlas.last_run      # ok, error, stdout, notify, asks

if run.wants("ran-clean"):
    run.result("ran-clean", "pass" if last.get("ok") else "fail", "The script ran",
               last.get("error") or "no error")

if run.wants("said-something"):
    n = len(last.get("notify") or [])
    run.result("said-something", "pass" if n else "warn", "It sent a message", f"{n} line(s)")

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

A script that raises or runs out of time or memory FAILS the run. It never falls back to a model.

- **In a test**: `state: "failed"` and `error` in words (`the script main.py
  failed: it ended with exit code 1` and the end of the traceback), plus
  `stderr`.
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

## What to keep in mind

- Switch it on to its real start only when the person says so.
- A script workflow is never followed. It can be shared, found and imported,
  and each copy is a workflow of its own: its own copy of the script, the
  setting names with no values, paused. It cannot be hidden.
- Settings' values are the owner's alone.
- Each run uses one request, whatever it decides; each ask one more.
