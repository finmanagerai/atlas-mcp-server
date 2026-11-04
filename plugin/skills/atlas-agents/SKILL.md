---
name: atlas-agents
description: Set up one of the person's three Atlas agents (Risk Manager, Account Manager, Market Analyst) in a sentence, and decide whether what they want is an agent or a workflow. Use when the person wants something watched, looked after or told to them over time, or asks for a trade plan that runs by itself and you must pick between an agent and a workflow.
---

# Agents

Short on purpose. The deep rules are in the tools' own descriptions: read only
the one you need.

## Agent or workflow? Decide first, say it in one line

- **Workflow** = a TRADE PLAN. It runs on an alert or a schedule and places,
  sends or reviews plays ("buy SPY calls when the wall flips", "every 9:35 check
  QQQ and send a play to my group"). See the `atlas-workflows` skill
  (`Workflow-Create`, `Workflow-Templates`; a play: `Signal-Schema`).
- **Agent** = a STANDING WORKER WITH A JOB TITLE. It watches, tells and looks
  after things over time ("watch my positions and tell me at +25%", "tell me
  when a workflow breaks", "read SPX for me each morning"). It is never the
  trade plan.
- Both? The workflow makes the trades; the Risk Manager looks after what they
  buy.

## The only three agents to offer

| Agent | Does |
|---|---|
| Risk Manager | runs the risk plan on every position held: takes at +25/+50/+100%, asks at -30% |
| Account Manager | workflows, signals, brokers, computers: says what broke and why |
| Market Analyst | reads SPX each morning (dealer levels, chart, events), makes a call, checks it |

Never offer another ready-made agent, and never the morning brief as one.

## Make one in a sentence

1. `Task-Shelf {"action": "list"}` once: what they already have. Never add one
   twice. (Newer servers name it `Agent-Task-Shelf`; both work.)
2. Say in one line who it is and what it will do for them; on their yes,
   `Task-Shelf {"action": "add", "role": "Risk Manager"}`. It is ready-made and
   tested: on at once, it says hello itself. Do not build it.
3. Only when they ask for something none of the three does: a custom agent with
   `Task-Create` (read its description; role = a specific job title, job = their
   words). It builds and tests itself. The `atlas-trackers` skill has the rest.

Deleting one (`Task-Manage {"action": "delete"}`, only when asked) also removes
the alerts it made for itself; the person's own alerts are never touched.
