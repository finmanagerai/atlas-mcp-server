---
name: atlas-agent-run-loop-test
description: Prove that the loop which wakes you, the assistant, and runs an Atlas workflow really works, using a throwaway workflow that cannot trade. Tests each link in turn: the tools, a run left waiting by a press, your own wake-up picking a run up with nobody prompting you, and a run started by Atlas's schedule or an alert. Use after setting up a loop with atlas-agent-run-loop, when the person asks "is it actually running by itself", or when a workflow you run has gone quiet.
---

# Testing that the loop calls itself

Setting up a wake-up is not the same as being woken. This test proves it, one
link at a time, with a workflow that only writes things up: it has no broker
account and no trade card, so nothing can be bought or sold.

Tell the person before you start: the test uses one request of their plan for
each run handed in (three or four in all), and shows a test workflow on their
dashboard for a few minutes. `references/tools.md` lists every field of the
tools named here.

## The test workflow

`Workflow-Create`, switched off, then switch it on with `Workflow-Update`:

```json
{
  "name": "Loop test (safe to delete)",
  "purpose": "analysis",
  "status": "paused",
  "trigger_source": "manual",
  "instruction": "Loop test. Write one line saying what woke you and when.",
  "ui_schema": { "run_by": "agent" }
}
```

```json
{ "workflow_id": "<the id>", "patch": { "status": "active" } }
```

Keep the id. Every step below uses it.

## Link 1: the tools, in this conversation

This proves you can see a waiting run and hand one in. It says nothing yet
about waking up.

1. `Workflow-Run` with the `workflow_id`. On a workflow you run, a press does
   not think: it leaves a run waiting.
2. `Workflow-Agent-Waiting-Runs`. The run is listed, with its `waiting_id`.
3. `Workflow-Agent-Report-Progress` with a short line.
4. `Workflow-Agent-Hand-In-Run`:

```json
{
  "workflow_id": "<the id>",
  "waiting_id": "<from step 2>",
  "reasoning": "Loop test, link 1: handed in from the conversation."
}
```

5. A few seconds later, `Workflow-Logs` with the `workflow_id`. **Pass:** the
   newest line carries your sentence, and `Workflow-Agent-Waiting-Runs` no
   longer lists the run.

## Link 2: you wake by yourself

This is the one that matters. A run is left waiting and **you do not touch it
in this conversation**. Only your wake-up may pick it up.

1. Set up the wake-up (`atlas-agent-run-loop`). For the test, make it fire
   every minute or two. Give its standing prompt one extra line: "In a loop
   test, hand in the sentence: Loop test, link 2: woke by myself at <the
   time>."
2. `Workflow-Run` with the `workflow_id`. Note the time.
3. Wait two of your wake-up's intervals. Do nothing with the run meanwhile.
4. `Workflow-Logs`. **Pass:** a new line carries the link 2 sentence, written
   at a time you were not working in this conversation.

When you cannot wait inside one conversation, tell the person what to look
for and when: a line reading "Loop test, link 2" in the workflow's log on
their dashboard, within two intervals.

**If nothing was handed in**, find the link that broke:

| What you see | What it means | What to do |
|---|---|---|
| The run is still listed as waiting, and your wake-up left no trace (no log line, no scheduled run in its history) | The wake-up did not fire | Check the timer itself: the task's schedule, and whether the computer was on |
| The wake-up fired, and the run is still waiting | It woke without the Atlas tools, or not signed in | Open that scheduled run's own output. A scheduled run often has fewer tools than a chat: if it cannot reach Atlas there, that wake-up cannot be used |
| The wake-up fired and tried to hand in, and the log has no new line | The hand-in was refused | Read the answer it got. It names what is wrong |
| The log shows "Waiting for ..." and nothing after it, an hour or more later | The run ran out before you came | Wake more often, or raise how long a run waits (`ui_schema.agent_max_age_s`) |

## Link 3: Atlas starts it, not a press

Run now proved the hand-off. This proves the thing the person actually wants:
a schedule or an alert starting the run with nobody there.

**A schedule.** Give the test workflow one run a few minutes ahead, in
Eastern time:

```json
{
  "workflow_id": "<the id>",
  "patch": { "trigger_source": "cron", "schedule": "once 2026-11-03 09:35", "timezone": "America/New_York" }
}
```

Do nothing. **Pass:** shortly after that minute the log shows "Waiting for
...: its schedule came due", and within one of your intervals a line from
your wake-up after it.

**An alert**, when the real workflow will be started by one. Make an alert
that will go off soon (see `atlas-alerts`; a price level just beside where
the stock is trading, during market hours), then:

```json
{ "workflow_id": "<the id>", "patch": { "trigger_source": "alert", "alert_id": "<the alert's id>" } }
```

**Pass:** when the alert goes off, the waiting run names it
(`what_started_it`, `alert_message`), and your wake-up hands it in. The time
between the two log lines is the real delay the person will live with. Tell
them that number.

## Clean up

- `Workflow-Delete` the test workflow, and `Delete-Alert` the test alert if
  you made one.
- Put the wake-up back to the interval the real workflow needs, and take the
  loop-test line out of its prompt.

## What to tell the person

Say which links passed, in plain words, and give the measured delay:

- "It works end to end. I am woken every 2 minutes in market hours; in the
  test I handed a run in 70 seconds after it came due."
- Or: "The tools work, and nothing wakes me here: scheduled runs on this app
  cannot reach Atlas. Two ways forward: a small script on your computer that
  starts me, or an ordinary Atlas workflow, which Atlas runs itself the
  moment the alert goes off."

Never report the loop as working on link 1 alone.
