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

1. `Agent-Task-Shelf {"action": "list"}` once: what they already have. Never add one
   twice. (Newer servers name it `Agent-Task-Shelf`; both work.)
2. Say in one line who it is and what it will do for them; on their yes,
   `Agent-Task-Shelf {"action": "add", "role": "Risk Manager"}`. It is ready-made and
   tested: on at once, it says hello itself. Do not build it.
3. Only when they ask for something none of the three does: a custom agent with
   `Agent-Task-Create` (read its description; role = a specific job title, job = their
   words). It builds and tests itself. The `atlas-trackers` skill has the rest.

Deleting one (`Task-Manage {"action": "delete"}`, only when asked) also removes
the alerts it made for itself; the person's own alerts are never touched.

## What the Account Manager does by itself

It fixes only safe, undoable things, checks, and says so in one line: re-runs
a run that failed for a passing reason (once, market open, nothing running);
restarts a stopped computer task once (`Computer-Tasks` resume); switches back
on a workflow Atlas paused by mistake (never one the person paused, or one
paused by its daily cap, loss limit or profit target); fills in the one right
missing broker account. If it fails again it stops and tells. It never
touches trades, sizes, budgets, stops or targets, instructions, tools or
schedules, alerts, money or broker settings, never deletes and never signs
in. When Atlas itself is broken it files `Support-Report` without asking;
never for the person's own side (their broker, their computer off). A quiet
self-check writes 2-4 short lines with numbers into its Activity, not the
phone.

## An agent working on the person's computer: Computer-Session

Opens a working session (a new chat) in Atlas Studio on the person's
computer. `action`: `start` {`context` (the whole brief), `computer`,
`project`, `title`, `about`, `confirmed_by_person`}, `send` {`ref`, `words`},
`read` {`ref`}, `list`, `stop` {`ref`}, `allow` {`on`}.

- Start only on the person's yes (`confirmed_by_person: true`), or to fix
  something that broke ON that computer (`about`) unless the person said
  agents may not (allowed by default). There is no switch on any screen:
  when they say so in their own words, `allow` `on: false` (`on: true` undoes it).
- At most 2 open per agent per computer; no trades, money settings, deleting
  or signing in. It shows in Studio as "<agent>: <title>". Tell the person
  the answer's `say` line.

## The browser (Browser-Open / -Read / -Act / -Tab / -Close)

- One browser per person; each chat or agent gets its own tabs in it (up to
  8), sign-ins shared. A link to another site opens a new tab.
- No timeout: it stays open until closed, so `Browser-Close` when done.
- Switches, check boxes, radios, sliders: each page answer lists them in
  `controls` with a ref; `Browser-Act` `check` / `uncheck` / `set` (text =
  the number), `target: "ref=c3"`.
- `look: true` gives you the page's picture, also shown under that step in
  the chat and kept a day. Use it when you need to see, not on every step.
- A crashed page reopens where it was.
