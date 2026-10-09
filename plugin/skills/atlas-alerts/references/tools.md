# The tools behind this skill (7)

GENERATED from the live server; do not edit by hand. Every field each
tool accepts. Nothing here is required unless the table says so: it is
what is possible.

## `List-Alert-Types`

🟢 reads. The catalog of alert types you can create — read THIS before calling Create-Alert to learn what alerts exist and how to fill each one's conditions.

Takes nothing.

## `Preview-Alert`

🟢 reads. Dry-run an alert spec without persisting or DMing.

| Field | Type | Needed | Default |
|---|---|---|---|
| `name` | string | no | `"preview"` |
| `symbol` | string | no |  |
| `alert_type` | string | no | `"flow"` |
| `stream_type` | string | no | `"flow_trades"` |
| `conditions` | object | no |  |
| `sample_limit` | integer | no | `200` |

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

The tool's own description, in full:

````text
Create a streaming alert that DMs the user on Discord (and optionally
        runs a workflow / arms a trigger / places an order) when a condition
        matches.

        ⚠️ FIRST call **List-Alert-Types** — it returns the live JSON catalog of
        every alert_type, its conditions, and a worked example. That catalog
        (not this docstring) is the source of truth, so it stays correct as
        alerts are added. Map the user's request to a catalog entry, copy its
        example shape, and fill `conditions`. You may leave `stream_type` unset
        (defaulted from alert_type). Friendly flip aliases (gex/dex/vex/tex
        flip) and `expiration_date` scoping are documented in the catalog.

        on_fire — optional action block run on fire, beyond the DM (each key
        optional): {"trigger": {...arm a trading trigger...},
        "reactivate_trigger_id": "...", "order": {...place a LIVE order...}}.
        ⚠️ on_fire.order places a REAL broker order automatically — double-gated
        (needs "live": true AND the server ALERT_LIVE_ORDERS_ENABLED switch);
        otherwise skipped and the user is DM'd it was not armed. Prefer
        on_fire.trigger unless the user explicitly wants an immediate order.
        workflow_id runs a workflow (and that workflow can itself arm a
        trigger). If the connected workflow DMs, the alert's own DM is
        auto-suppressed to avoid duplicates.
        Fan-out: one alert can run MANY workflows and re-arm MANY
        triggers — on_fire.workflow_ids: ["<wf>", ...],
        on_fire.reactivate_trigger_ids: ["<trig>", ...] (the
        legacy singular keys still work and are de-duped in). See
        List-Alert-Types for shapes.

        Args:
            name:        Free-text label (shown in the DM and on the dashboard).
            symbol:      Ticker. Required for all types EXCEPT flow_rank.
            alert_type:  flow | king_node | volume_spike | volume_shift | price |
                         contract_price | level_approach | flow_rank | top_flow |
                         technicals | trigger_event | options_ratio.
                         options_ratio = who LEADS, calls or puts: conditions.
                         ratio_source "open_interest" (checked daily) or
                         "unusual_flow" (premium, checked hourly);
                         ratio_trigger "flip" (the leader changes) or "lead"
                         with lead_side + lead_x (e.g. puts, 2 = "puts lead 2x
                         or more"); optional min_dte / max_dte /
                         strikes_around_spot (default 50) / strike_range.
                         There is NO greek/gamma
                         "flip" TYPE — every Greek / dealer-exposure alert is
                         king_node (conditions.metric picks the Greek), and
                         conditions.move_mode picks what counts as a move: the
                         wall MOVING to a new strike ("node", default) or the
                         net exposure flipping sides ("flip_positive" /
                         "flip_negative" / "flip"), or either ("any").
                         Call List-Alert-Types for the live catalog + each type's
                         conditions.
            stream_type: Usually omit — defaulted from alert_type.
            conditions:  Condition object (see per-type notes above). Three
                         knobs worth knowing, all optional and all defaulting to
                         the long-standing behaviour:
                         • king_node conditions.move_mode — what counts as a
                           move. "node" (default) the wall shifts to a new
                           strike; "node_positive"/"node_negative" only the
                           purple (biggest positive) or yellow (biggest
                           negative) wall shifts; "flip_positive"/
                           "flip_negative"/"flip" the Greek's net exposure
                           crosses zero (the gamma flip); "any" either.
                         • level_approach conditions.region_mode — "near"
                           (default) the price comes close to the level;
                           "flip_positive"/"flip_negative"/"flip" the price
                           CROSSES it. Above the level is the positive side. A
                           crossing follows a Greek wall, so set conditions.
                           metric; to watch a fixed price cross instead, use the
                           "price" type. THIS MEASURES PRICE, NOT EXPOSURE: a
                           ticker deep in negative gamma "crosses to positive"
                           the moment price steps over the wall. A user asking
                           for a "gamma flip" / "GEX flip" wants king_node with
                           move_mode, not this.
                         • conditions.intraday_only (bool, default false) — by
                           default a move that happened while the market was
                           shut still counts, and is reported on the first check
                           after the open. Set true to count only moves during
                           one session. Works on king_node, level_approach,
                           volume_spike, volume_shift, flow_rank, top_flow,
                           price and contract_price.
                         A flip never goes off just because it starts on that
                         side: it needs a real crossing between two checks. And
                         when no expiration_date is pinned the alert follows the
                         front expiry, which becomes a new contract each day —
                         that roll is never reported as a move.
            notify_discord: When true the bot DMs the user on fire.
            workflow_id: Optional — fires the given workflow's run on match
                         (the fire payload is passed as trigger_payload).
            cooldown_seconds: Minimum gap between fires (floor 30, default 60).
            expires_at:  Optional ISO-8601 cutoff after which the alert disarms.
            on_fire:     Optional action block (trigger / reactivate / live
                         order) — see notes above.
            is_active:   true (default) arms the alert now; false creates it
                         pre-disabled (arm later with Update-Alert is_active=true).
            notes:       Optional free-text note (max ~2000 chars). Attach any
                         context or a directive for the workflow this alert
                         triggers — when the alert fires, the note is forwarded
                         to the triggered workflow's agent AND shown in the
                         alert DM. Optional; omit for none.
            created_by_workflow_id: Internal — the alert_creator workflow that
                         authored this alert (set automatically by Manage-Alerts).
                         Leave unset for a stand-alone alert.
````

## `Update-Alert`

🔴 acts. Patch an existing alert's fields without recreating. ``updates`` accepts the same keys Create-Alert exposes (name, symbol, alert_type, stream_type, conditions, notify_discord, workflow_id, cooldown_seconds, expires_at, is_active, notes).

| Field | Type | Needed | Default |
|---|---|---|---|
| `alert_id` | string | yes |  |
| `updates` | object | yes |  |

The tool's own description, in full:

````text
Patch an existing alert's fields without recreating.

        ``updates`` accepts the same keys Create-Alert exposes
        (name, symbol, alert_type, stream_type, conditions,
        notify_discord, workflow_id, cooldown_seconds, expires_at,
        is_active, notes). Any other key is rejected so a typo never
        silently lands in the database. The merged row is re-validated, so
        an update that would make the alert un-evaluatable (e.g. removing
        symbol from a flow alert) fails loudly. Set notes to "" to clear it.

        SEND ONLY WHAT YOU ARE CHANGING. Anything you leave out keeps its
        current value, inside `conditions` and `on_fire` as well as at the
        top level: {"conditions": {"min_premium": 50000}} changes that one
        threshold and leaves the symbol, the active window, fire_on_start and
        every other condition exactly as they were. Set a key to null to
        remove it; a LIST you send (e.g. on_fire.workflow_ids) replaces the
        stored list whole. Do NOT read the alert and send its whole
        conditions block back: restating fields you did not mean to change
        is how an edit to one threshold silently drops another.

        The one exception: if you change `alert_type`, conditions are
        REPLACED rather than merged, because each alert kind has its own
        condition keys and the old kind's must not linger. Send the complete
        conditions for the new kind in that call.
````

## `Delete-Alert`

🟠 changes. Switch an alert off and hide it — one, or a whole pile at once.

| Field | Type | Needed | Default |
|---|---|---|---|
| `alert_id` | string | no | `""` |
| `alert_ids` | array | no |  |
| `purge` | boolean | no | `false` |

## `List-Alerts`

🟢 reads. List the caller's alerts.

| Field | Type | Needed | Default |
|---|---|---|---|
| `active_only` | boolean | no | `true` |
| `platform` | string | no | `"other"` |

## `Alert-Fires`

🟢 reads. Recent alert fires, each with the message it carried.

| Field | Type | Needed | Default |
|---|---|---|---|
| `alert_id` | string | no | `""` |
| `limit` | integer | no | `20` |
