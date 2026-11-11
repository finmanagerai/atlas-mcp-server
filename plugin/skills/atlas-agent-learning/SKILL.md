---
name: atlas-agent-learning
description: Teach one of the person's Atlas agents a new job, or fix one that went wrong, from any coding agent connected to Atlas (Claude, ChatGPT, Codex, Cursor, the atlas CLI). Covers reading the agent's folder (check.py, task.md, notes) with Agent-Task-Files, a dry run first, saving check.py through the agent's own test (it switches only when the test passes), stopping before the final press on the first live version, going live one step at a time, undo, and spinning up and cleaning up specialists with Agent-Task-Specialists. Use when the person says "go learn this", "teach my agent to ...", or "my agent did X, fix it".
---


# Teaching an Atlas agent a new job, and fixing one

For any coding agent connected to Atlas (Claude, ChatGPT, Codex, Cursor, the
`atlas` command line). You work on the person's OWN agents only, through two
tools: `Agent-Task-Files` (their files) and `Agent-Task-Specialists` (extra
helpers for a job). The person says something like **"go learn this: <the
job>"** or **"my agent did X, fix it"**. Do the whole job; don't hand steps
back to them.

## What an agent is

Every agent has a folder, `Files > Tasks/<agent>/`:

| File | What it is | You may |
|---|---|---|
| `check.py` | The script Atlas runs for it every few seconds, on a sandboxed runner | write (through its test, see below) |
| `task.md` | Its job in words, written from its record | read; change the job with `Agent-Task-Update` |
| `notes/` | Its notes, plans, what it learned | read, write |
| `actions.jsonl` | Its Activity (what it did) | read only |
| `edits.jsonl` | Every change made through `Agent-Task-Files` | read only |
| `drafts/check.py` | A script whose test did not pass | read, fix, write again as `check.py` |

`check.py` defines `def check(inputs):` and returns `None` (nothing to say)
or `{"fire": True, "title": ..., "text": ..., "key": ...}`. `inputs` holds
`now`, `bars`, `positions`, and `event` when a trade's exit woke it. With
`import atlas`, `atlas.call(tool, **args)` reads any Atlas tool and
`atlas.page(url, find)` reads a web page in the agent's own browser.
`Agent-Task-Templates` has working examples to start from. Everything the
script needs goes inside `check.py`: other `.py` files in the folder are not
run.

## The steps (in this order, every time)

1. **Read before you touch.** `Agent-Task-Files action=agents`, then
   `action=list` and `action=read` for `check.py`, `task.md` and
   `notes/`. Read `Agent-Task-Activity` for what it did lately. Say in one
   line what you think is wrong, or what the new job needs.
2. **Dry run first.** Write the new script so it only *reads* and *says*:
   it returns `fire` with what it WOULD do ("would trim 1 of 3 at TP1"),
   never pressing. Test it on its own with `Agent-Task-Test` (code + the
   agent's name): it replays today's bars, or runs once live if it uses
   `atlas`. Nothing is kept and nothing is sent.
3. **Save it.** `Agent-Task-Files action=write path=check.py content=<whole
   file>`. Atlas runs the agent's own test; the agent switches to the new
   script only when it passes. If it fails, the answer has the error and the
   script waits in `drafts/check.py`; the agent keeps running its old one.
   Fix the cause and write it again. Never say "it's running" unless the
   answer says `switched: true` and `running: true`.
4. **Stop before the final press.** When the job ends in a press (buy,
   sell, submit, close), the first live version goes up to the last step and
   STOPS there: it opens the page, finds the button, checks the count and
   the position are what the plan expects, and fires a message naming the
   press it would make. Watch one real occurrence in its Activity.
5. **Go live step by step.** Then let it press, one kind of press at a
   time (first the trim, later the close), each only after the page shows
   exactly what the plan expects (one position, the expected count). After
   each press it reads the page back and says what changed. Keep the old
   behaviour as a fallback: if the page differs, it does not press; it wakes
   the agent to do it.
6. **Write down what it learned** in `notes/` (e.g. `notes/learned.md`):
   what the page looks like, what the person corrected, what to watch for.
7. **Report** to the person in a few lines: what you changed (the answer's
   `change` has the lines added/removed), the test result, and whether it
   runs now. Every change is in the agent's Activity under your name, and
   `action=undo` puts any change back.

## Its own notes: learn and adapt

Every agent keeps ONE small notes file for itself, `notes/learned.md`, handed
to it on every wake. Before any browser, computer or Studio step it reads
them. When a step fails and it finds what works (another button, a new page
layout, a wait, a sign-in), it tries again and writes what it learned in one
or two lines under a heading for that site or flow:

```
## rixtrade.com positions
- The Trim button is under the position's ... menu since 2026-11-11.
- Wait for "Positions (1)" before reading the count.
```

When a screen changes, it REPLACES that heading's lines instead of adding
below them. The whole file stays short (about 40 lines); what no longer helps
is dropped. Nothing about the person goes here (that is their Memory). You can
read and fix these notes with `Agent-Task-Files` like any other file.

## Guardrails you never cross

- Only the person's own agents, only inside each agent's folder. A path out
  of it is refused.
- A script never replaces a working one without passing its test.
- Never touch the person's money settings, brokers or other agents to make
  a script pass. If a fix needs something only they can give (a sign-in, a
  yes), ask in one line.
- Keep it fast: an exit is pressed within a second of its fire, so a script
  that presses does the minimum before the press.

## Specialists

For a side job (watch earnings for a week, rebuild a dashboard, fix
something on their computer), spin up a specialist rather than bloating the
agent: `Agent-Task-Specialists action=spawn agent=<agent> name="Earnings
watcher" job=<the whole brief>`. With `computer=<name>` it works in Atlas
Studio on that computer. Each step goes in with `action=note`. When the job is
done, `action=cleanup`: its history moves into the Account Manager's chat, so
nothing is lost.
