# The tools behind this skill (8)

GENERATED from the live server; do not edit by hand. Every field each
tool accepts. Nothing here is required unless the table says so: it is
what is possible.

## `Buddy-Tracker-Templates`

🟢 reads. Starting files for trackers (the small checks Buddy runs for the person): give back, near the stop, near a target, a fast drop, expiry, no plan, a daily loss, a workflow's drawdown, a number on a web page.

| Field | Type | Needed | Default |
|---|---|---|---|
| `name` | string | no | `""` |

## `Buddy-Tracker-Test`

🟢 reads. Test a tracker (a small Python check the chat writes for the person) on today's bars, and show what it would have caught: each bar of today's session is handed to its check() in turn, and the answer lists the messages it would have sent, with the time of each.

| Field | Type | Needed | Default |
|---|---|---|---|
| `code` | string | no | `""` |
| `symbols` | array | no |  |
| `timeframe` | string | no | `"5m"` |
| `lookback` | string | no | `"1d"` |
| `positions` | array | no |  |
| `name` | string | no | `""` |
| `scope` | object | no |  |

The tool's own description, in full:

````text
Test a tracker (a small Python check the chat writes for the person) on
today's bars, and show what it would have caught: each bar of today's
session is handed to its check() in turn, and the answer lists the
messages it would have sent, with the time of each. Nothing is kept or
sent. Uses one request.

The flow: the person asks ("tell me when SPY loses VWAP and my calls are
red"), write the check, test it here, show the person what it caught, then
keep it with Buddy-Tracker-Save. Test a saved one again by its `name`.

A tracker that uses `import atlas` (a tool, a web page) is tried once,
live, now, instead of bar by bar.

Args:
    code: the whole Python file. It must define def check(inputs): and return None (nothing to say) or {"fire": True, "title": "short headline", "text": "one short line, sent as written", "numbers": {...}, "key": "said once a day per key", "buttons": up to 2 of hold|take|close|close_all|stop_today|pause, "warning": true when it is against the person, "urgent": true to skip the daily cap, "source": where the number came from, "do": {"stop_today": true} or {"pause_workflows": [ids] or true} (done only if kept with may_act)}. inputs = {"now", "timeframe", "symbols", "bars": {"SPY": [{"timestamp", "open", "high", "low", "close", "volume"}, ...]}, "positions": [{"symbol", "occ", "entry", "peak", "now", "pnl_pct", "pnl_cents", "stop", "targets", "expiry", "units", "workflow_id", "trigger_id", "watch_id", "plan"}], "replay"}. numpy, pandas and the runner's libraries are there. `import atlas` reaches Atlas as the person: atlas.call(tool, **args) (tools that read), atlas.page(url, find) (a web page in the tracker's own browser: text, numbers, picture; a sign-in page is told to the person once), atlas.numbers_in(text), atlas.read_numbers(picture) (OCR). Top-level EVERY_S / SYMBOLS / TIMEFRAME / LOOKBACK / ABOUT are read when it is kept. Start from a template: Buddy-Tracker-Templates.
    symbols: the tickers whose bars it reads (at most 5), e.g. ["SPY"]. The first is
        the one whose bars are stepped through. None = the code's SYMBOLS, or no bars.
    timeframe: bar size: 1m, 2m, 5m, 15m, 30m, 1h or 1d.
    lookback: how far back the bars go: 1d, 5d, 1mo or 3mo.
    positions: optional positions to test with (same keys as inputs.positions);
        without them the person's watched positions are used.
    name: test a saved tracker instead of `code` (its symbols are used unless given).
    scope: only these trades: {"type": "workflow" | "group" | "trigger", "ids": [...]}, or "all".
````

## `Buddy-Tracker-Save`

🟠 changes. Keep a tracker in the person's files so Buddy runs it by itself, as often as every 10 seconds, while the market is open; when its check fires, the person is told in their chat and on their phone in the tracker's own title and words.

| Field | Type | Needed | Default |
|---|---|---|---|
| `name` | string | yes |  |
| `code` | string | yes |  |
| `symbols` | array | no |  |
| `timeframe` | string | no | `""` |
| `lookback` | string | no | `""` |
| `every_s` | integer | no |  |
| `every_min` | integer | no |  |
| `about` | string | no | `""` |
| `chat_id` | string | no | `""` |
| `paused` | boolean | no |  |
| `scope` | object | no |  |
| `may_act` | boolean | no |  |

The tool's own description, in full:

````text
Keep a tracker in the person's files so Buddy runs it by itself, as
often as every 10 seconds, while the market is open; when its check fires,
the person is told in their chat and on their phone in the tracker's own
title and words. Test it first with Buddy-Tracker-Test and show the person
what it caught. Saving under a name already kept replaces that tracker. At
most 20. Its file is in the person's Files under trackers/.

Args:
    name: a short word, e.g. spy-vwap-calls (lower case, digits, - and _).
    code: the whole Python file. It must define def check(inputs): and return None (nothing to say) or {"fire": True, "title": "short headline", "text": "one short line, sent as written", "numbers": {...}, "key": "said once a day per key", "buttons": up to 2 of hold|take|close|close_all|stop_today|pause, "warning": true when it is against the person, "urgent": true to skip the daily cap, "source": where the number came from, "do": {"stop_today": true} or {"pause_workflows": [ids] or true} (done only if kept with may_act)}. inputs = {"now", "timeframe", "symbols", "bars": {"SPY": [{"timestamp", "open", "high", "low", "close", "volume"}, ...]}, "positions": [{"symbol", "occ", "entry", "peak", "now", "pnl_pct", "pnl_cents", "stop", "targets", "expiry", "units", "workflow_id", "trigger_id", "watch_id", "plan"}], "replay"}. numpy, pandas and the runner's libraries are there. `import atlas` reaches Atlas as the person: atlas.call(tool, **args) (tools that read), atlas.page(url, find) (a web page in the tracker's own browser: text, numbers, picture; a sign-in page is told to the person once), atlas.numbers_in(text), atlas.read_numbers(picture) (OCR). Top-level EVERY_S / SYMBOLS / TIMEFRAME / LOOKBACK / ABOUT are read when it is kept. Start from a template: Buddy-Tracker-Templates.
    symbols: the tickers whose bars it reads (at most 5), e.g. ["SPY"]; none = the code's
        SYMBOLS, or no bars (a tracker on positions, a page or a tool).
    timeframe: bar size: 1m, 2m, 5m, 15m, 30m, 1h or 1d.
    lookback: how far back the bars go: 1d, 5d, 1mo or 3mo.
    every_s: how often it runs, in seconds (10 at the fastest, 3600 at most; default the
        code's EVERY_S, else 60). Faster for a stop, slower for a page.
    every_min: older way, in minutes.
    scope: only these trades: {"type": "workflow" | "group" | "trigger", "ids": [...]}
        (a workflow, a signal group, one trade), or "all" (default).
    may_act: true ONLY after the person said yes: its "do" (no new entries today, pause a
        workflow's new entries today) is then done when it fires. Never closes anything.
    about: one line saying what it watches, in the person's words.
    chat_id: the chat its messages go to (default: the person's most recent chat).
    paused: true to keep it without running it.
````

## `Buddy-Tracker-List`

🟢 reads. The trackers the person keeps (the small checks Buddy runs for them): each one's name, what it watches, its tickers and bar size, how often it runs and whether it is paused.

Takes nothing.

## `Buddy-Tracker-Delete`

🟠 changes. Delete one of the person's trackers: it stops running and its file is removed.

| Field | Type | Needed | Default |
|---|---|---|---|
| `name` | string | yes |  |

## `Buddy-Hold-Entries`

🟠 changes. Hold or let through the person's NEW entries for the rest of today (New York): the step a tracker's "No new entries" / "Pause it" button asks for, and what a tracker kept with may_act does by itself.

| Field | Type | Needed | Default |
|---|---|---|---|
| `action` | string | no | `"list"` |
| `workflow_ids` | array | no |  |
| `workflow_id` | string | no | `""` |

## `Buddy-Watch-List`

🟢 reads. What Atlas is watching for the person, each with its plan, plus their level, check interval, muted tickers and anything paused today.

Takes nothing.

## `Account-Activity`

🟢 reads. Show recent ACTIVITY on the caller's account — every workflow RUN (its reasoning, what it decided, and any error) plus the TRADES those runs fired — newest first.

| Field | Type | Needed | Default |
|---|---|---|---|
| `workflow_id` | string | no | `""` |
| `trigger_id` | string | no | `""` |
| `symbol` | string | no | `""` |
| `include` | string | no | `"all"` |
| `limit` | integer | no | `25` |
