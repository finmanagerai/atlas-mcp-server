# The tools behind this skill (6)

GENERATED from the live server; do not edit by hand. Every field each
tool accepts. Nothing here is required unless the table says so: it is
what is possible.

## `Agent-Task-Files`

🟠 changes. Read, edit, test and fix the person's own Atlas agents: the files each agent keeps in its folder (Files > Tasks/<agent>/): check.py (the script Atlas runs for it every few seconds on its sandboxed runner, with `import atlas`: atlas.call, atlas.page), task.md (its job), notes/ and any file it keeps.

| Field | Type | Needed | Default |
|---|---|---|---|
| `action` | string | no | `"agents"` |
| `agent` | string | no | `""` |
| `path` | string | no | `""` |
| `content` | string | no |  |
| `offset` | integer | no |  |
| `limit` | integer | no |  |
| `edit_id` | string | no | `""` |
| `allow_empty` | boolean | no | `false` |
| `by` | string | no | `""` |

The tool's own description, in full:

````text
Read, edit, test and fix the person's own Atlas agents: the files each
    agent keeps in its folder (Files > Tasks/<agent>/): check.py (the script
    Atlas runs for it every few seconds on its sandboxed runner, with
    `import atlas`: atlas.call, atlas.page), task.md (its job), notes/ and any
    file it keeps. Made for outside coding agents (Claude, ChatGPT, Codex, any
    MCP client) so the person never needs a developer to fix an agent.

    START WITH action "guide": how an agent learns a new job safely (a dry run
    first, test, stop before the final press, then live step by step) and how
    to fix one.

    THE GATE: only the person's own agents, only inside each agent's folder.
    Writing check.py RUNS THE AGENT'S OWN TEST first and switches the agent to
    the new script ONLY when the test passes; a failing (or untestable) script
    is kept as drafts/check.py with the error and the agent keeps running the
    script it had. A .py must read as Python and a .json as JSON. task.md
    (change the job with Agent-Task-Update), actions.jsonl and edits.jsonl are
    read-only. Every write or delete answers `change` (lines added/removed, the
    whole diff, the test, whether it runs now), writes a line in the agent's
    Activity naming who changed it, and keeps what it replaced so `undo` puts
    it back. No size cap on editing: a file is read whole and written whole (up
    to the file store's 5 MB for one file).

    Args:
        action: guide | agents (your agents and their folders) | list (one
            agent's files) | read | write | delete | history (every change made
            here, newest first) | undo (put back one change: edit_id, else the newest).
        agent: the agent's name, as action agents shows it (e.g. "options-funding-agent").
        path: the file inside its folder: "check.py", "notes/plan.md".
        content: for write, the WHOLE text of the file (it replaces the file).
        offset: for read, start at this character (only to page a huge file).
        limit: for read, at most this many characters (only to page); for history, how many.
        edit_id: for undo, the change's id from history (default: the newest).
        allow_empty: true to write an empty file on purpose.
        by: ignored (Atlas's own services name who made a change, e.g. the Files tab).
````

## `Agent-Task-Specialists`

🟠 changes. An agent's specialists: list them, spin one up for a job, write what it did, and clean it up when the job is done.

| Field | Type | Needed | Default |
|---|---|---|---|
| `action` | string | no | `"list"` |
| `agent` | string | no | `""` |
| `specialist` | string | no | `""` |
| `name` | string | no | `""` |
| `job` | string | no | `""` |
| `text` | string | no | `""` |
| `computer` | string | no | `""` |
| `project` | string | no | `""` |
| `confirmed_by_person` | boolean | no | `false` |

The tool's own description, in full:

````text
An agent's specialists: list them, spin one up for a job, write what it
    did, and clean it up when the job is done. Every agent has its standing
    specialists (Position watcher, SPX, Learning ...); these are extra ones,
    named by their job, at most 8 per agent.

    - spawn: name, job (the whole brief: what to do, what done looks like).
      In the cloud it starts at once (its agent thinks with the job in front).
      With `computer` it is a working session on one of the person's computers
      (Atlas Studio), like Computer-Session: allowed when the person said yes
      (confirmed_by_person) or agents may work on their computers.
    - note: specialist, text: one line of what it did, kept in the agent's Activity.
    - cleanup: specialist: its computer session (if any) is read and stopped,
      everything it did is written into the Account Manager's chat, then it is
      taken off. Nothing is lost. Standing specialists are never cleaned up.
    - list: the agent's specialists, standing and spun up.

    Args:
        action: list, spawn, note or cleanup.
        agent: the agent's name (a task calling this: its own name).
        specialist: for note and cleanup, the specialist's id or name.
        name: for spawn, what it is called, by its job ("Earnings watcher").
        job: for spawn, the whole brief.
        text: for note, what it did.
        computer: for spawn, a computer of the person's (name or id) to work on.
        project: for spawn on a computer, a project there to work in.
        confirmed_by_person: for spawn on a computer, true only after the person said yes.
````

## `Agent-Task-Test`

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

## `Agent-Task-Templates`

🟢 reads. Starting files for trackers (the small checks Buddy runs for the person): give back, near the stop, near a target, a fast drop, expiry, no plan, a daily loss, a workflow's drawdown, a number on a web page.

| Field | Type | Needed | Default |
|---|---|---|---|
| `name` | string | no | `""` |

## `Agent-Task-Activity`

🟢 reads. A task's Activity history, newest last: each time it woke, what woke it, whether it told the person, what it did in its own words, the tools it used and which model thought.

| Field | Type | Needed | Default |
|---|---|---|---|
| `name` | string | yes |  |
| `limit` | integer | no | `30` |

## `Agent-Task-Update`

🔴 acts. Change a task: its title, its job (prompt), what wakes it, what it may use, its own limits, what trades it leaves alone, or its state (on | stopped | building).

| Field | Type | Needed | Default |
|---|---|---|---|
| `name` | string | yes |  |
| `role` | string | no |  |
| `job` | string | no |  |
| `wakes` | object | no |  |
| `boundaries` | object | no |  |
| `state` | string | no |  |
| `limits` | string | no |  |
| `built` | string | no |  |
| `description` | string | no |  |
| `exclude` | string | no |  |
