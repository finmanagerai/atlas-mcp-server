---
name: atlas-agent-run-loop
description: Set up the loop that wakes you, the assistant, by itself and has you run an Atlas workflow from start to finish with nobody prompting you. Covers the wake-up (your own scheduler, or a small script on the person's computer), the check that costs nothing when no run is waiting, and the stages of one run (read the workflow, gather the data side by side, decide once, hand it in). Use when the person says "just keep doing this for me", wants a workflow you run to go on a schedule or when an Atlas alert goes off, or asks how you will know when to run.
---

# The loop that wakes you and runs the workflow

Nobody can call an assistant. Atlas can watch a schedule and an alert, and it
can keep a run waiting for you, but it cannot start you. So a workflow you run
yourself (see `atlas-agent-run-workflows`) needs three things that you set up
once:

1. **A wake-up.** Something that starts you on a timer.
2. **A gate.** A check that costs nothing, so you only do work when a run is
   waiting.
3. **The run.** The same stages Atlas goes through when it thinks a workflow
   through itself.

This page says what is possible and gives shapes to start from. Change
anything. `references/tools.md` lists every field of the tools named here.
When it is set up, prove it with the `atlas-agent-run-loop-test` skill before
telling the person it works.

## 1. The wake-up

Use the first of these that you really have. Do not assume: test it.

| What wakes you | When it fits | What to check |
|---|---|---|
| **Your host's own scheduler** (scheduled tasks, automations, routines) | You have one, and a scheduled run can use the Atlas tools | That a scheduled run is signed in to Atlas and can call its tools. Many hosts run scheduled work with fewer tools than a chat has |
| **The person's computer** (cron on macOS and Linux, Task Scheduler on Windows) starting you without a window | You can be started from a command, for example `claude -p "<prompt>"` or `codex exec "<prompt>"`, or from a short script on an agent SDK | The computer is on and awake at those times. The command is allowed to use the Atlas tools without asking |
| **A server or a CI schedule** running the same script | The person wants it to run while their computer is off | Where the access key is kept. It belongs in that service's own protected settings, never in the script |
| **Nothing** | You cannot be started on a timer at all | Say so plainly. An ordinary Atlas workflow, which Atlas runs itself the moment its schedule or alert comes due, is the better choice |

**How often.** The delay between an alert going off and you acting is the time
between two wake-ups.

| What starts the workflow on Atlas | A sensible wake-up |
|---|---|
| An alert | Every 1 to 5 minutes, 09:30 to 16:00 Eastern, Monday to Friday |
| A schedule | A minute after each scheduled time |
| Nothing (you keep the time) | At your own times. There is no gate to check: go straight to the run |

Asking Atlas what is waiting uses no request of the person's plan, however
often you ask. Reading market data does, and so does handing a run in (one
request each time). Tell the person the delay and the cost you set up.

## 2. The gate

Before any thinking, ask one thing: is a run waiting?

- With the tools: `Workflow-Agent-Waiting-Runs`. `count` is 0 when there is
  nothing to do. Stop there.
- From a script, before you are even started: the Atlas command line
  (`npm install -g mindvest-atlas`) asks the same thing, so the model is only
  started when there is work.

```bash
#!/usr/bin/env bash
# Wakes the assistant only when Atlas has a run waiting for it.
set -euo pipefail
DIR="$HOME/.atlas-loop"                        # key, prompt.md, loop.log live here
export ATLAS_TOKEN="$(cat "$DIR/key")"         # the person's Atlas access key
mkdir "$DIR/lock" 2>/dev/null || exit 0        # one wake-up at a time
trap 'rmdir "$DIR/lock"' EXIT

count=$(atlas workflow-agent-waiting-runs \
  | python3 -c 'import json,sys; print(json.load(sys.stdin).get("count", 0))')
echo "$(date +%FT%T%z) waiting=$count" >> "$DIR/loop.log"
[ "$count" -gt 0 ] || exit 0

# Start yourself, with the Atlas tools allowed and the standing prompt below.
claude -p "$(cat "$DIR/prompt.md")" >> "$DIR/loop.log" 2>&1
```

And the line that runs it every two minutes in market hours, on a computer
whose clock is set to Eastern time (cron uses the computer's own time zone):

```
*/2 9-16 * * 1-5  $HOME/.atlas-loop/wake.sh
```

Things that hold for any version of this:

- **The key is the person's.** They copy it from their Atlas dashboard into a
  file only they can read, or into the scheduler's own protected settings. Never ask them to
  paste it into the chat, and never write it into the script.
- **One wake-up at a time.** A run can take longer than the gap between two
  wake-ups. The lock above makes the second one leave quietly.
- **Keep a log line per wake-up.** It is how you, and the test, know the
  wake-up is firing.
- With a host scheduler there is no script: the scheduled task's prompt is the
  standing prompt below, and its first step is the gate.

## 3. One run, in stages

This is the order Atlas itself works in. Keeping to it is what makes a run
quick and the result checkable.

### Take the run

`Workflow-Agent-Waiting-Runs`. For each waiting run you get the workflow, what
started it, the alert's own message when an alert did, and how long it has
waited.

- Judge by `seconds_waiting` whether it is still worth doing. An alert from
  forty minutes ago is usually stale: hand in "nothing to do" with the reason,
  or leave it to run out.
- Several runs of **different** workflows are independent: do them side by
  side if you can start helpers. Runs of the **same** workflow go one at a
  time, newest first.

### Read the brief

`Workflow-Open`. The workflow carries everything the person set:

| Part | What it is to you |
|---|---|
| `instruction` | The plan, in words |
| `tools`, with a note per tool | Which data to read, and what to look for in each |
| `output_schema.triggers` | The trade card. A value it fixes is the person's and is not yours to change. A value it leaves empty is yours to fill |
| `output_tools` | Things to do after you have decided |
| `purpose` | `trading`, `draft` (the person places it by hand) or `analysis` (a write-up only) |
| `ui_schema.preview_before_place` | On: your run is held for the person to approve. Off: it goes in |

Two more reads keep one run consistent with the last:

- `Workflow-Logs` with a small `limit`: what you concluded last time.
- `List-Trading-Triggers`: what this workflow already has waiting or open.
  Do not enter a ticker it already holds.

### Gather, side by side

Make every read that does not depend on another at the same time: the quote,
the options chain, the flow, the dealer exposure, the chart. Then the reads
that depend on those (the chain for the expiry you settled on, one contract's
quote). Each read uses one request, so read what the plan needs and no more.

`Workflow-Agent-Report-Progress` with one short line between stages ("Reading
the options chain", "Deciding") shows on the person's card while you work.

### Decide, once

Gathering and deciding are separate. Decide after the data is in, one time:

- Trade or not. "Nothing to do" is a full answer.
- For a trade, start from the card's own entry, keep what it fixes, fill what
  it left empty.
- Write `reasoning` for a reader: what you saw, and why this follows from the
  plan.

Check it yourself before handing it in, because Atlas will:

- an option names its strike and its expiry;
- a size or a budget, never both, and none the card does not carry;
- the stop and the target are on the right side of the entry (for a bought
  put the target is below and the stop above);
- every level of a ladder in percent, or every level in dollars, and the
  amounts add up to the whole position;
- two trades meant as either/or arrive together.

### Hand it in

`Workflow-Agent-Hand-In-Run` with the `workflow_id`, the `waiting_id` of the
run you took, your `reasoning`, and the trades (or `act: false`). Read the
answer. If it is refused, fix what it names and hand it in once more; never
send the same thing again unchanged. A few seconds later `Workflow-Logs`
shows what the run did.

### Afterwards

Anything the workflow asks for after a decision (`output_tools`: post a play,
set an alert) comes now, with the decision in front of you. A tool that
answers with an error did not do the thing: fix the cause, then call again.

Then stop. One wake-up, one pass. The next wake-up starts fresh, so keep
nothing in your head between them: what happened is in the workflow's log and
its open trades.

## The standing prompt

What the wake-up hands you each time. Change the wording; keep the order.

```
You are running Atlas workflows for me with nobody watching.
1. Call Workflow-Agent-Waiting-Runs. If count is 0, stop now.
2. For each waiting run: skip it with a one-line hand-in if it has waited too
   long to matter. Otherwise open the workflow (Workflow-Open), read its last
   log line and what it already has open, and report progress.
3. Read the data the workflow names, as many reads at once as you can.
4. Decide once. Keep every value the trade card fixes. Fill only what it left
   empty. Do nothing if the plan does not clearly call for a trade.
5. Hand the run in with Workflow-Agent-Hand-In-Run and its waiting_id, then
   check Workflow-Logs.
6. Stop. Do not wait for another run.
Never ask me a question during a run: nobody is here to answer. If something
is unclear, hand in "nothing to do" and say what was unclear.
```

## What to tell the person

- How you are woken, how often, and so how late you can be on an alert.
- What has to stay on for it to keep working (their computer, the scheduled
  task).
- That each run you hand in uses one request, and each data read one more.
- That the trade card's terms and the workflow's review switch are theirs:
  you fill in the blanks, and with review on nothing is placed until they
  approve it.
- How to stop it: switch the workflow off in Atlas, and remove the scheduled
  task or the cron line.
