---
name: atlas-trackers
description: Build a tracker for the person on Atlas - a short Python check that runs by itself while the market is open (as often as every 10 seconds) and tells them, in its own title and words, on their phone and in their chat, when something they care about happens. Covers starting from a template (give back, near the stop, near a target, a fast drop, expiry, no plan, a daily loss, a workflow's drawdown, a number on a web page), reading positions, bars, Atlas tools and web pages (with OCR), keeping it to one workflow, signal group or trade, holding new entries when they allowed it, testing and saving. Use when the person asks to be told about, or protected from, something specific.
---

# Trackers

A tracker is the person's own small check, written by you, that Atlas keeps
and runs for them. They do not have to learn anything: you build it, test it,
keep it, and say in one line what it does. Its file is in their Files under
`Trackers/<name>.py`; changing that file changes the tracker within a minute.

This page says what is possible. `references/tools.md` lists every field of
the tools named here.

## The loop

1. `Buddy-Tracker-Templates` lists starting files, each with what it checks and
   the numbers at its top to change. `Buddy-Tracker-Templates {name}` gives one
   file's whole code. Nothing about them is fixed: change the numbers, the
   check, the words, or start from the closest one and rewrite it.
2. `Buddy-Tracker-Test {code}` runs it. A tracker on bars is stepped through
   today's bars and the answer lists what it would have sent; a tracker that
   uses `import atlas` (a tool, a web page) is run once, now.
3. Show the person, in one line, what it would have sent. Then
   `Buddy-Tracker-Save {name, code, ...}`. Saving again under the same name
   replaces it. `Buddy-Tracker-List` and `Buddy-Tracker-Delete` do the rest.

## The file

```python
import atlas                     # only if it reads a tool or a page

ABOUT = "Tells me when my QQQ calls give back a third"
EVERY_S = 15                     # seconds between runs (10 at the fastest)
SYMBOLS = []                     # tickers whose bars it reads (optional)
TIMEFRAME = "1m"                 # with SYMBOLS: 1m 2m 5m 15m 30m 1h 1d
FROM_PCT, GIVE_BACK = 20, 1 / 3

def check(inputs):
    for p in inputs["positions"]:
        if p["symbol"] != "QQQ" or not p.get("entry") or p.get("peak") is None:
            continue
        best = (p["peak"] / p["entry"] - 1) * 100
        now = (p["now"] / p["entry"] - 1) * 100
        if best >= FROM_PCT and now <= best * (1 - GIVE_BACK):
            return {"fire": True,
                    "title": "QQQ gave back a third",
                    "text": f"Your QQQ calls were up {best:.0f}% and are now {now:+.0f}%.",
                    "numbers": {"best_pct": round(best, 1), "now_pct": round(now, 1)},
                    "key": "qqq-give-back",
                    "buttons": ["take", "hold"],
                    "warning": True}
    return None
```

The constants at the top are read when it is kept (the tool's own arguments
win). `inputs` is:

- `positions`: each trade of theirs: `symbol`, `occ`, `entry`, `peak`, `now`,
  `pnl_pct`, `pnl_cents`, `stop`, `targets`, `expiry`, `strike`,
  `option_type`, `units`, `workflow_id`, `trigger_id`, `watch_id`, `plan`;
- `bars`: `{"SPY": [{timestamp, open, high, low, close, volume}, ...]}` for
  `SYMBOLS`;
- `now`, `timeframe`, `symbols`.

`import atlas` reaches Atlas as the person:

- `atlas.call(tool, **args)`: any Atlas tool that reads;
- `atlas.page(url, find="")`: a web page in the tracker's own browser, with
  the person's kept sign-ins: `{text, numbers, url, title, picture}`. A page
  that asks them to sign in is told to them once ("sign in once in its
  browser: More, then Browser") and the tracker carries on by itself
  afterwards. Never ask them for their sign-in details.
- `atlas.numbers_in(text)`: every number in a text (`$1,234.50` is 1234.5,
  `(2.1%)` is -2.1, `3.4M` is 3400000);
- `atlas.read_text(picture)` / `atlas.read_numbers(picture, box=(x, y, w, h))`:
  OCR, for a number drawn as a picture or a chart. Read the page's words first;
  they are exact.

numpy, pandas and the runner's other libraries are there. There is no
internet except through `atlas`. A tracker reads and tells: it never places,
closes or submits anything (a press that would submit, buy, sell or pay is
refused).

## What it says

Return `None` for nothing, or:

| key | what |
|---|---|
| `fire` | `True` |
| `title` | the headline, as written (60 characters) |
| `text` | one plain line, as written (300 characters) |
| `numbers` | the numbers behind it |
| `key` | said once a day per key |
| `buttons` | up to two of `hold`, `take`, `close`, `close_all`, `stop_today`, `pause` |
| `warning` | `True` when it is against the person (a warning mark) |
| `urgent` | `True` for something that cannot wait (no daily cap) |
| `source` | where the number came from, when not Atlas's own feed |
| `do` | `{"stop_today": True}` or `{"pause_workflows": [ids] or True}` |

Write the title and text the way the person talks. Never "sell now": say what
happened and leave the choice to them.

`do` holds NEW entries for the rest of the New York day: all of them, or one
workflow's (`True` = the workflow of the trade it is about). It happens only
for a tracker kept with `may_act: true`, set only after the person said yes.
It never closes anything. `Buddy-Hold-Entries` lists or lifts a hold.

## Saving

`Buddy-Tracker-Save` takes `name`, `code`, and when wanted:
`every_s` (10 to 3600), `symbols`, `timeframe`, `lookback`, `about`,
`scope` (`{"type": "workflow" | "group" | "trigger", "ids": [...]}`: only
those trades are handed in; default all of theirs), `may_act`, `paused`.

How often: a stop check every 10 to 15 seconds, a give-back every 15 to 30, a
web page every 60 or more.
