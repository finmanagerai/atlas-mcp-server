---
name: atlas-signals
description: Read plays (signals) on Atlas, where a play is one trade idea written down in full and shared with a board or a group. Use when the person wants to see what was posted on the community board or in a group they follow, look at one play, find public groups, or see how a group's plays have done.
---

# Reading plays (signals)

A play is one trade somebody is calling: what to buy, where to get in, where
to take profit, where to get out, and how much. It is posted to the community
board or to a group, and the people who follow it can take it.

From here plays are **read**. Posting one, changing one, taking one into an
account, following a group and changing how plays are handled are done in
Atlas itself, on the dashboard. When the person asks for one of those, say so
and point them there.

`references/tools.md` lists every field each of these tools accepts.

## What can be read

| The person asks | Tool |
|---|---|
| What is on the board, or in one group | `Signal-List`: `board` is `community` or `private`, or pass one `group_id`. It reads a page at a time |
| One play in full | `Signal-Show` |
| Which groups they own, follow or may read | `Signal-Groups` |
| Which plays are waiting on their own answer | `Signal-Pending`. They answer on the dashboard |
| Public groups they could follow | `Signal-Discover` |
| How a group's plays have done | `Signal-Group-Performance` |

## Reading one well

- A play's **entry** is where to get in; its **targets** are where to take
  profit, in order; its **stop** is where to get out. On an option, a dollar
  level is the stock's price and a percent is on the option's own price.
- A play can be one of a **linked pair**: when one side fills, the other is
  cancelled, or the other only starts once the first has filled. The play
  says which.
- A play says whether it has been entered and how far it has got. Say what it
  shows; do not guess at what happened after.
- Somebody else's play is their call, not advice from Atlas. Say what it is
  and what its record shows; the decision is the person's.
