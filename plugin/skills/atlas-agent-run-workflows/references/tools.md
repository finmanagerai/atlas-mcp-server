# The tools behind this skill (12)

GENERATED from the live server; do not edit by hand. Every field each
tool accepts. Nothing here is required unless the table says so: it is
what is possible.

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

## `Workflow-Update`

🔴 acts. Update fields on an existing workflow owned by the caller.

| Field | Type | Needed | Default |
|---|---|---|---|
| `workflow_id` | string | yes |  |
| `patch` | object | yes |  |
| `suggest` | boolean | no | `false` |
| `note` | string | no | `""` |

## `Workflow-Agent-Waiting-Runs`

🟢 reads. List the runs that are waiting for you, the agent, to do.

Takes nothing.

The tool's own description, in full:

````text
List the runs that are waiting for you, the agent, to do. Read-only.

This is for a workflow you registered to run yourself (Workflow-Create with ui_schema {"run_by": "agent"}). When such a workflow's schedule comes due, one of its alerts goes off, or the person presses Run now, Atlas does not think for you: it leaves a note here and waits. Nobody can call you, so ask: at the start of a conversation, and whenever your own schedule wakes you.

Each run says which workflow, what started it (and what the alert said), when, and how long it is still worth doing. For each one: read the workflow (Workflow-Open), look at the market with the data tools, decide, and hand in the result with Workflow-Agent-Hand-In-Run, passing the run's waiting_id. A run nobody hands in simply expires; nothing is charged for it.

Args: none.
Output: { waiting: [ {waiting_id, workflow_id, workflow_name, started_by, what_started_it, alert_message, waiting_since, seconds_waiting, seconds_left} ], count }.
````

## `Workflow-Agent-Report-Progress`

🟡 adds. Say what you are doing on a run you have not handed in yet, so the person sees it on the workflow's card while you work.

| Field | Type | Needed | Default |
|---|---|---|---|
| `workflow_id` | string | yes |  |
| `text` | string | yes |  |

The tool's own description, in full:

````text
Say what you are doing on a run you have not handed in yet, so the person sees it on the workflow's card while you work. Optional, and it changes nothing but that one line: it starts nothing, places nothing and costs nothing.

For a workflow you registered to run yourself. Call it as often as the step changes ("Reading the options chain", "Checking the 5 minute trend"). The card shows the newest line with your name in front. The line is cleared when you hand the run in, and by itself after about twenty minutes of silence.

Args:
  workflow_id: the workflow you are working on.
  text: one short line, in plain words. Cut at 140 characters.
````

## `Workflow-Agent-Hand-In-Run`

🔴 acts. Hand in what you decided for one run of a workflow you run yourself.

| Field | Type | Needed | Default |
|---|---|---|---|
| `workflow_id` | string | yes |  |
| `reasoning` | string | yes |  |
| `triggers` | array | no |  |
| `act` | boolean | no |  |
| `waiting_id` | string | no | `""` |

The tool's own description, in full:

````text
Hand in what you decided for one run of a workflow you run yourself. This is a real run: from here Atlas does everything it does after its own model decides.

WHAT HAPPENS. The trades you name are laid over the workflow's own trade card (a value the card fixes stays as the card has it), checked, and sized. Then, by the workflow's own settings: with "review before it places" on, the run is held for the person to approve, edit or throw away; with it off, the orders go in, in the workflow's broker account, and anyone following the workflow gets the same trade. The run is written to the workflow's log, the person is told, and it counts against the workflow's daily cap. A run that is refused (a field the trade card does not accept, the cap already spent) says so in the log.

IT USES ONE REQUEST of the person's plan every time, including a run that decides to do nothing.

Because it can place real orders, hand in only what the workflow's instruction and the market actually support. Never invent a size, a budget or a stop the trade card does not carry.

Args:
  workflow_id: the workflow. It must be yours, switched on, and set to be run by an agent.
  reasoning: what you saw and why you decided what you did, in plain words. This is the write-up the person and any followers read. Required.
  triggers: the trades, as a list. Each one uses the trade card's own fields (Trigger-Workflow-Schema lists every one, with examples): symbol, asset_class, option_type, strike, expiry, contracts or quantity, the entry, the stop and the targets. Leave it out, or empty, for a run that decided to do nothing, and always for a workflow that only writes things up.
  act: false to say plainly that you looked and decided to do nothing, even if triggers were sent. Leave it out otherwise.
  waiting_id: the run this answers, from Workflow-Agent-Waiting-Runs. Leave it out when you ran on your own schedule.

Output: { success, accepted, held_for_review, next }. The run itself takes a few seconds: read what it did with Workflow-Logs.

Example (a trade):
  { "workflow_id": "<id>", "waiting_id": "<id>:alert:<alert id>",
    "reasoning": "SPY held above 600 on rising volume after the alert.",
    "triggers": [ { "symbol": "SPY", "asset_class": "option", "option_type": "call", "strike": 601, "expiry": "2026-11-20", "contracts": 1, "enter_side": "buy_to_open", "enter_order_type": "market", "order_strategy": "bracket", "bracket_stop_loss_stop_pct": -30, "bracket_take_profit_limit_pct": 50 } ] }
Example (nothing to do):
  { "workflow_id": "<id>", "reasoning": "Back under the level. Standing aside.", "act": false }
````

## `Workflow-Open`

🟢 reads. Show the caller's workflows.

| Field | Type | Needed | Default |
|---|---|---|---|
| `workflow_id` | string | no |  |
| `platform` | string | no | `"other"` |

## `Workflow-Logs`

🟢 reads. Return recent run logs for a workflow the caller owns.

| Field | Type | Needed | Default |
|---|---|---|---|
| `workflow_id` | string | yes |  |
| `limit` | integer | no | `25` |
| `platform` | string | no | `"other"` |

## `Workflow-Review`

🔴 acts. A workflow set to "review before it places" holds each run until somebody approves it.

| Field | Type | Needed | Default |
|---|---|---|---|
| `workflow_id` | string | yes |  |
| `action` | string | no | `"show"` |
| `review_id` | string | no | `""` |
| `reasoning` | string | no |  |
| `triggers` | array | no |  |

## `Trigger-Workflow-Schema`

🟢 reads. Fetch the canonical schema for AI trigger workflows.

Takes nothing.

## `List-Alerts`

🟢 reads. List the caller's alerts.

| Field | Type | Needed | Default |
|---|---|---|---|
| `active_only` | boolean | no | `true` |
| `platform` | string | no | `"other"` |

## `Create-Alert`

🔴 acts. Create a streaming alert that DMs the user on Discord (and optionally runs a workflow / arms a trigger / places an order) when a condition matches. ⚠️ FIRST call **List-Alert-Types** — it returns the live JSON catalog of every alert_type, its conditions, and a worked example.

| Field | Type | Needed | Default |
|---|---|---|---|
| `name` | string | yes |  |
| `symbol` | string | no |  |
| `alert_type` | string | no | `"flow"` |
| `stream_type` | string | no | `"flow_trades"` |
| `conditions` | object | no |  |
| `notify_discord` | boolean | no | `true` |
| `workflow_id` | string | no |  |
| `cooldown_seconds` | integer | no | `60` |
| `expires_at` | string | no |  |
| `on_fire` | object | no |  |
| `is_active` | boolean | no | `true` |
| `notes` | string | no |  |
| `created_by_workflow_id` | string | no |  |

## `Broker-Connections`

🟢 reads. List all connected brokerage accounts for the authenticated user.

Takes nothing.
