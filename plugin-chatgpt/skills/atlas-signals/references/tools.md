# The tools behind this skill (6)

GENERATED from the live server; do not edit by hand. Every field each
tool accepts. Nothing here is required unless the table says so: it is
what is possible.

## `Signal-List`

🟢 reads. Read the plays on the community board, or the private ones.

| Field | Type | Needed | Default |
|---|---|---|---|
| `board` | string | no | `"community"` |
| `group_id` | string | no | `""` |
| `limit` | integer | no | `20` |
| `days` | integer | no | `0` |
| `before` | string | no | `""` |

## `Signal-Show`

🟢 reads. Show ONE play as a card, the same one the Signals tab renders.

| Field | Type | Needed | Default |
|---|---|---|---|
| `signal_id` | string | yes |  |

## `Signal-Groups`

🟢 reads. List the places you can post a play to, and the groups you follow.

Takes nothing.

## `Signal-Pending`

🟢 reads. The plays sent to you that are waiting for your answer: from the groups you pay for or follow with "manual" chosen.

Takes nothing.

## `Signal-Discover`

🟢 reads. Public signal groups other people run, to follow.

Takes nothing.

## `Signal-Group-Performance`

🟢 reads. Closed-trade performance of ONE signal group: a private group you own or belong to, a public group you follow, or the Community board.

| Field | Type | Needed | Default |
|---|---|---|---|
| `group_id` | string | yes |  |
| `mine` | boolean | no | `false` |
| `platform` | string | no | `"other"` |
