# A timer on your own computer that wakes your assistant

Atlas can keep a run waiting for your assistant (see the
`atlas-agent-run-workflows` and `atlas-agent-run-loop` skills), but it cannot
start your assistant. This page is a worked example of the small script that
does: it asks Atlas whether a run is waiting and starts the assistant only
when one is. It is for a person to read, adapt and switch on themselves. It
is not part of the plugin.

Asking Atlas what is waiting uses no request of your plan. A run your
assistant hands in uses one.

## What you need

- An assistant you can start from a command (the example starts Claude Code;
  use your own assistant's command), already connected to Atlas.
- The Atlas command line: `npm install -g mindvest-atlas`.
- Your Atlas access key, from your dashboard, in a file only you can read
  (`chmod 600`). It never goes in the script or in a chat.
- A file with the standing prompt from the `atlas-agent-run-loop` skill.

## The script

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

`~/.atlas-loop/` holds `key`, `prompt.md`, the `lock` folder while a wake-up
is working, and `loop.log`, which gets one line per wake-up.

## The timer

Every two minutes in market hours, on a computer whose clock is set to
Eastern time (cron uses the computer's own time zone):

```
*/2 9-16 * * 1-5  $HOME/.atlas-loop/wake.sh
```

On Windows, Task Scheduler runs the same steps from a `.cmd` or PowerShell
file.

## Check that it works

Ask your assistant to run the `atlas-agent-run-loop-test` skill. It leaves a
test run waiting and confirms that the timer, not the chat, picked it up.

## Stop it

Switch the workflow off in Atlas, which stops it at once, and remove the
timer line.
