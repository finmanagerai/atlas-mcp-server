# The tools behind this skill (17)

GENERATED from the live server; do not edit by hand. Every field each
tool accepts. Nothing here is required unless the table says so: it is
what is possible.

## `Signal-Schema`

🟢 reads. READ THIS BEFORE POSTING OR TAKING A PLAY.

Takes nothing.

## `Signal-Groups`

🟢 reads. List the places you can post a play to, and the groups you follow.

Takes nothing.

## `Signal-Post`

🔴 acts. Post a trade play — to the community board, or to one of your groups.

| Field | Type | Needed | Default |
|---|---|---|---|
| `symbol` | string | yes |  |
| `side` | string | no | `"buy"` |
| `asset_class` | string | no | `"option"` |
| `option_type` | string | no | `"call"` |
| `strike` | number | no |  |
| `expiration_date` | string | no | `""` |
| `contracts` | integer | no |  |
| `quantity` | integer | no |  |
| `trade_budget` | number | no |  |
| `entry` | number | no |  |
| `entry_unit` | string | no | `""` |
| `entry_operator` | string | no | `""` |
| `entries` | array | no |  |
| `targets` | array | no |  |
| `tps` | array | no |  |
| `stop` | number | no |  |
| `tp_unit` | string | no | `"pct"` |
| `stop_unit` | string | no | `"pct"` |
| `enter_at` | string | no | `""` |
| `exit_at` | string | no | `""` |
| `reason` | string | no | `""` |
| `score` | integer | no |  |
| `called_at` | string | no | `""` |
| `group_id` | string | no | `""` |
| `trade_for_me` | boolean | no | `false` |
| `snaptrade_account_id` | string | no | `""` |
| `second_leg` | object | no |  |
| `link_mode` | string | no | `""` |

The tool's own description, in full:

````text
Post a trade play — to the community board, or to one of your groups.

    WHAT IT DOES. A play is one trade idea written down in full: the contract
    (or stock), where to get in, where to take profit, where to get out. This
    tool publishes one under the user's name, where the people who follow that
    board or group see it and can take it. Use it only when the user asks to
    post a play, and post what they said. It is a real action with real
    effects: the play is visible to other people at once, followers who chose
    automatic taking get an order placed for them, and if the user is in the
    trade themselves (a broker account on the play) their own order is placed
    too. To change or withdraw a play afterwards use Signal-Update or
    Signal-Delete; to read plays use Signal-List.

    A LINKED PAIR (two trades, one idea): give the other trade as `second_leg`
    (the same field names as this tool: symbol, option_type, strike,
    expiration_date, entries, targets, stop, the units...) and say how the two
    are linked in `link_mode`: "oco" = whichever fills first cancels the other
    (a call and a put on the same level); "oeo" = the second leg starts only
    once THIS one fills (a follow-up). A second leg with no link_mode is
    refused: a linked play is one of those two, never two loose trades. Both
    legs post together, show as linked, and anyone who takes one takes both.

    Anyone can post their own play: the board is open, and posting costs
    nothing. This is the whole form, so a play called out loud can be written
    down in full — the contract, how much, where to get in, where to take
    profit, where to get out, and when.

    POST ONLY WHAT THE USER DICTATED. This publishes a call under their name
    and can place a real order; never invent or "improve" a play they did not
    ask for. Fill in what they said and leave the rest empty — every field
    below has a sensible default, and an empty field is never a guess.

    CHANGING A PLAY THAT IS STILL LIVE? Use Signal-Update, not this. Posting
    again leaves the first call on the board as well, so the same trade sits
    there twice and both are armed. This tool is for a NEW call only.

    SEND EVERY NUMBER THE USER GAVE, UNDER THE NAMES BELOW. A field name this
    tool does not recognise is a number that never arrives, and a play whose
    entry or targets went missing is a DIFFERENT TRADE published under a
    person's name. The shapes that work, exactly:
        entries: [733.20]  or  [{"price": 733.20, "quantity": 2}]
        targets: [734.50, 736, 737.40]
                 or [{"target": 734.50, "quantity": "33%"}, …]
    (`price`/`amount` are accepted as aliases, but the names above are the
    ones to use.) Nothing posts if you send entries or targets and none of them
    can be read — you get an error naming the shape, so fix it and call again.
    Never drop the field to make an error go away.

    `reason` IS NOT WHERE INSTRUCTIONS GO. Nothing reads it but a person, so
    anything written there happens to nobody. A trailing stop is the one that
    keeps getting typed as prose: "Trail: stop to entry at TP1, stop to TP1 at
    TP2" moved no stop on any of the five plays it went out on (2026-08-14).
    It belongs in `stop_after` — and WHICH LEVEL you put it on is the part
    everyone gets wrong:

      A LEVEL'S stop_after GUARDS THE RUN INTO THAT LEVEL. It arms the moment
      the PREVIOUS target fills, not when its own does. So:
        • TP1 carries NO stop_after. Entry→TP1 is guarded by the play's own
          `stop`, which is the baseline. Anything you put on TP1 is dead.
        • TRAILING STARTS AT TP2 AND GOES UP. TP2's stop_after is what the
          stop becomes once TP1 pays; TP3's is what it becomes once TP2 pays.

    THE SAME RULE IN EITHER UNIT — the rung it goes on never changes, only
    what the number means. "Stop to entry once TP1 pays, stop to TP1 once TP2
    pays" on a three-rung ladder:

      PRICE ladder (tp_unit "price" — the stock's price):
        targets: [{"target": 183.5, "quantity": "33%"},
                  {"target": 187.5, "quantity": "33%", "stop_after": 0},
                  {"target": 193, "quantity": "remaining",
                   "stop_after": 183.5, "stop_after_unit": "price"}]

      PERCENT ladder (tp_unit "pct" — % of the entry premium):
        targets: [{"target": 50, "quantity": "33%"},
                  {"target": 100, "quantity": "33%", "stop_after": 0},
                  {"target": 150, "quantity": "remaining", "stop_after": 50}]

    Read either one the same way: TP1 bare (the baseline `stop` owns it). TP2
    carries 0, which is break-even, and is the stop AFTER TP1 pays. TP3 carries
    TP1's own level — 183.5 as a price, or 50 as a percent — and is the stop
    after TP2 pays. `stop_after_unit` is "pct" unless you say "price", so on a
    percent ladder you just write the number. 0 always means break-even.

    Describing a trailing stop in `reason` without setting it is REFUSED, and
    so is putting one on TP1 where it would never fire. Keep `reason` for why
    you like the trade.

    THEN CHECK IT. Call Signal-List or Signal-Show afterwards and compare what
    came back against what the user asked for, field by field: entry there, all
    the targets there, stop, size, direction, units. Report what you verified,
    not what you sent. If a call times out or errors, READ THE BOARD BEFORE
    RETRYING — posting again "because the first one failed" is how the same
    play ends up on the board four times, all of them armed.

    Args:
        symbol: The ticker, e.g. "SPY".
        side: "buy" or "sell".
        asset_class: "option" (default) or "stock".
        option_type: "call" or "put". Options only.
        strike: The strike price. Options only.
        expiration_date: Expiry as YYYY-MM-DD. Options only.
        contracts: How many contracts the CALLER is taking. Options only.
        quantity: How many shares the CALLER is taking. Stock only.
            Both size the caller's OWN position only — a follower always trades
            their own budget, never the number posted here.
            DO NOT SEND EITHER UNLESS THE USER STATED A SIZE. Left out, the
            play is sized from the poster's own per-trade budget at the price
            it actually pays. Sending a number OVERRIDES that budget — so a
            reflexive "contracts": 1 quietly turns someone's $1,000 limit into
            one contract, which is the opposite of what they set it for. You
            may ASK how many they want; you may not invent it.
        trade_budget: THE SAME ANSWER IN MONEY, in dollars — "put $500 into
            it" is trade_budget: 500. Atlas works out how many that buys at the
            price the order actually pays, as close under the amount as whole
            units allow and never over. It REPLACES contracts / quantity: send
            ONE of them, never both, because they are two instructions for one
            thing and only one survives. Use whichever the user actually said:
            "two contracts" is a count, "about $500 worth" / "500 dollars into
            it" is a budget. Sizes the CALLER only, exactly like the count.
        entry: The price to get in at. Leave empty for "take it now, at market".
        entry_unit: WHICH price `entry` is, and this matters — the same number
            means two different trades:
              "contract" (default) — the option's own price. Gets in with a
                  limit at that premium, so it fills at your price or not at
                  all.
              "price" — the STOCK's price. Watches the stock and buys at market
                  when it gets there.
            HOW TO TELL: compare the number to the STRIKE. The option's own
            price is a small fraction of it; the stock trades right around it.
            On a 780 strike, 2.10 is the premium ("contract") and 773 is the
            stock ("price"). A "SPY 780 call, get in at 773" is the STOCK at
            773. Stock plays are always "price". Atlas refuses a number that
            cannot be what it is labelled — read the error and fix the unit,
            do not drop the field.
        entry_operator: Which way the stock has to move to count. REQUIRED
            whenever entry_unit is "price" — there is NO default, because the
            two are opposite trades and guessing picks one of them:
              "gte" — at or ABOVE. "reclaims 225.50", "breaks 225.50",
                  "above 225.50", "through 225.50", a breakout.
              "lte" — at or BELOW. "dips to 225.50", "pulls back to 225.50",
                  "under 225.50", buying weakness.
            Read the user's own words and set it. If they did not say, ASK —
            do not assume the dip. Ignored when entry_unit is "contract".
        entries: Scaling in — several entries instead of one, in fill order,
            e.g. [{"price": 1.20, "quantity": 2}, {"price": 0.95,
            "quantity": 3}]. Use `entry` for the normal single-entry play.
        tps: The same thing as `targets`, under the name Signal-Schema and the
            stored play both use. Either name works; send ONE of them.
        targets: Take-profit levels, in order. Either plain numbers — [50, 100]
            — or the full shape when the user says how much comes off where:
            [{"target": 50, "quantity": "40%", "stop_after": 0},
             {"target": 100, "quantity": "remaining", "stop_after": 50}].
            quantity is a number, a "40%", or "remaining"; the last level always
            closes what is left. stop_after MOVES THE STOP once that level pays
            — 0 means break-even, 50 means lock in 50 — and stop_after_unit
            ("pct" default, or "price") says what it is in. Left unsaid, the
            levels split the position evenly and the stop does not move.
        stop: Where to get out if it goes wrong. Write it as a positive number;
            it is stored as a loss either way.
        tp_unit / stop_unit: What those numbers mean — "pct" (% of the
            contract's price, the default), "contract" ($ of the contract's own
            price) or "price" ($ of the stock's price). stop_unit may also be
            "trail": a TRAILING stop, where `stop` is a % distance behind the
            best price since entry (share price on a stock, premium on an
            option), tightening only. Same strike test as
            entry_unit: a target of 790 on a 780 strike is the STOCK, not a
            790% gain. And nothing you BUY can lose more than 100%, so a stop
            of 223 is a price, never a percentage.
        enter_at: Get in at a TIME instead of (or as well as) a price, e.g.
            "15:30" for today, or "2026-08-12 15:30". New York time.
        exit_at: Close the position at this time whatever it is doing. Same
            format as enter_at.
        reason: Why you are calling it. Your followers read this.
        score: How strong the call is, 1 to 10. DEFAULTS TO 10, not 1 — a play
            called without a number is being called without reservation. SET IT
            whenever the user rates the play ("this one's a 6", "low
            conviction", "I really like this one"), and change it later with
            Signal-Update if they change their mind. Never invent a rating they
            did not give. It is an opinion only: nothing sizes, filters or
            places off it.
        group_id: One of your groups (from Signal-Groups) — private, and it
            reaches the people who follow that group. Leave empty to post to the
            community board, where anybody can read it and NOBODY trades it
            automatically. The board allows 20 plays per person per day (resets
            at midnight New York time); groups have no limit.
        trade_for_me: Place it in YOUR OWN account too. Off unless the user says
            to take their own play.
        snaptrade_account_id: Which account to use. Leave empty in almost every
            case — Atlas uses the broker the user saved for posting. Pass one
            only when they name an account for this play, or when Signal-Broker
            shows they have not saved one.
        second_leg: The other trade of a linked pair, as a dict of this tool's
            own fields (symbol, side, asset_class, option_type, strike,
            expiration_date, contracts, entries, targets, stop, tp_unit,
            stop_unit, entry_unit, entry_operator, reason, score). Omit for a
            play that stands alone.
        link_mode: "oco" or "oeo". Required with second_leg, refused without.
````

## `Signal-Update`

🔴 acts. Change a play that is still live, instead of posting a second one.

| Field | Type | Needed | Default |
|---|---|---|---|
| `signal_id` | string | yes |  |
| `symbol` | string | no | `""` |
| `side` | string | no | `""` |
| `option_type` | string | no | `""` |
| `strike` | number | no |  |
| `expiration_date` | string | no | `""` |
| `contracts` | integer | no |  |
| `quantity` | integer | no |  |
| `trade_budget` | number | no |  |
| `entry` | number | no |  |
| `entry_unit` | string | no | `""` |
| `entry_operator` | string | no | `""` |
| `entries` | array | no |  |
| `targets` | array | no |  |
| `tps` | array | no |  |
| `stop` | number | no |  |
| `tp_unit` | string | no | `""` |
| `stop_unit` | string | no | `""` |
| `enter_at` | string | no | `""` |
| `exit_at` | string | no | `""` |
| `reason` | string | no | `""` |
| `score` | integer | no |  |

## `Signal-Delete`

🔴 acts. Take down a play you posted, before anybody is in it.

| Field | Type | Needed | Default |
|---|---|---|---|
| `signal_id` | string | yes |  |

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

## `Signal-Take`

🔴 acts. Take a play: place it in YOUR OWN account, now.

| Field | Type | Needed | Default |
|---|---|---|---|
| `signal_id` | string | yes |  |
| `snaptrade_account_id` | string | no | `""` |
| `contracts` | integer | no |  |
| `partner_contracts` | integer | no |  |
| `late` | boolean | no | `false` |
| `max_per_trade` | number | no |  |
| `exit_split` | array | no |  |

The tool's own description, in full:

````text
Take a play: place it in YOUR OWN account, now. Places a real order.

    A LINKED play (see `link` on Signal-Show / Signal-List) is taken as a
    pair: both legs go in, wired so that one filling cancels the other (OCO)
    or starts it (OEO). `contracts` sizes this leg, `partner_contracts` the
    other; leave both empty to size from the user's per-trade budget.

    Read Signal-Schema if you need to explain what the play actually says
    before somebody puts money on it.

    Nothing on the community board trades on its own — this is what puts your
    money on somebody else's call. Only when the user asks for this specific
    play.

    Taking a play off the COMMUNITY board uses one request from the user's
    monthly plan, and only if an order actually reaches their broker. Taking a
    play from a group they subscribe to uses none — that subscription already
    covers it.

    Args:
        signal_id: The play's id, from Signal-List.
        snaptrade_account_id: Which account. Leave empty in almost every case —
            Atlas uses the broker the user saved for taking plays (see
            Signal-Broker).
        contracts: How many of THIS play. Empty = the user's per-trade budget.
        partner_contracts: How many of the linked play, when there is one.
            Empty = the same as `contracts`, else the budget.
        late: A play that has ALREADY entered is refused unless this is True.
            Taking it then is a late entry at today's price, not the price
            that was called: say so to the user and send True only when they
            still want in.
        max_per_trade: Dollars this one take may spend, instead of a count.
            Atlas buys as many as that covers at the price being paid.
        exit_split: How many of YOUR position come off at each of the play's
            targets, first target first, e.g. [2, 1] for three taken on a
            two-target play (the last target takes what is left). Only on a
            play with two or more targets; empty = your saved exit split.
````

## `Signal-My-Order`

🔴 acts. Change or cancel YOUR OWN order on somebody else's play, while it is still waiting to enter.

| Field | Type | Needed | Default |
|---|---|---|---|
| `signal_id` | string | yes |  |
| `cancel` | boolean | no | `false` |
| `contracts` | integer | no |  |
| `max_per_trade` | number | no |  |
| `snaptrade_account_id` | string | no | `""` |
| `exit_split` | array | no |  |

## `Signal-Pending`

🟢 reads. The plays sent to you that are waiting for your answer: from the groups you pay for or follow with "manual" chosen.

Takes nothing.

## `Signal-Answer`

🔴 acts. Say yes or no to a play that was sent to you (see Signal-Pending).

| Field | Type | Needed | Default |
|---|---|---|---|
| `signal_id` | string | yes |  |
| `accept` | boolean | yes |  |

## `Signal-Discover`

🟢 reads. Public signal groups other people run, to follow.

Takes nothing.

## `Signal-Follow`

🔴 acts. Follow a public signal group (or stop following it), and set how its plays are handled for you.

| Field | Type | Needed | Default |
|---|---|---|---|
| `group_id` | string | yes |  |
| `follow` | boolean | no | `true` |
| `accept_mode` | string | no | `""` |
| `snaptrade_account_id` | string | no | `""` |
| `max_per_trade` | number | no |  |
| `contracts` | integer | no |  |

The tool's own description, in full:

````text
Follow a public signal group (or stop following it), and set how its
    plays are handled for you.

    "Import" a whole group of plays: it appears in the user's Signals list as a
    group they read but do not post to, and every play in it can be taken with
    Signal-Take. Only a group its owner made public can be followed.

    TRADE SETTINGS (the group card's "Trade settings" popup). By default a
    follow is MANUAL: nothing is placed, each play is taken by hand. With
    accept_mode "auto", every play posted to the group from then on is placed
    for the user at post time, sized from their budget and sent to their
    account, and billed one Atlas request when an order goes in — the same as
    pressing Take now on it. The settings apply to the NEXT play posted; nothing
    already placed changes. Only the settings you send change; a bare call on a
    group already followed keeps what was chosen.

    Args:
        group_id: The group, from Signal-Discover.
        follow: True to follow (the default), False to stop. Settings are
            ignored when stopping.
        accept_mode: "auto" or "manual". Omit to leave it as it is.
        snaptrade_account_id: The user's own broker account to place auto (and
            hand) takes of this group's plays in. "default" clears it back to
            their default account. Omit to leave it as it is.
        max_per_trade: The most one play from this group may spend, in dollars.
            0 clears it back to their default per-trade budget. Omit to leave
            it as it is.
        contracts: A fixed number of contracts (shares on a stock play) per
            play instead of a budget; wins over the budget when set. 0 clears
            it. Omit to leave it as it is.
````

## `Signal-Trade-Settings`

🔴 acts. See or change how plays are traded for you: the "Trade settings" of the Signals page, for one group or for everything.

| Field | Type | Needed | Default |
|---|---|---|---|
| `group_id` | string | no | `""` |
| `accept_mode` | string | no | `""` |
| `snaptrade_account_id` | string | no |  |
| `max_per_trade` | number | no |  |
| `contracts` | integer | no |  |
| `allow_author_close` | boolean | no |  |
| `exit_split` | string | no | `""` |
| `notify_board_dm` | boolean | no |  |
| `budget_account_id` | string | no | `""` |

## `Signal-Group-Create`

🟡 adds. Make a new signal group: a place of your own to post plays to.

| Field | Type | Needed | Default |
|---|---|---|---|
| `name` | string | yes |  |

## `Signal-Group-Update`

🔴 acts. Rename a signal group you own, make it public or private, or tag it. visibility "Atlas-public" puts the group under Discover for every Atlas member to follow and read, and sends every play posted to it to the community board as well. "private" (the default every group starts with) takes it back off Discover; people already following keep reading until they stop.

| Field | Type | Needed | Default |
|---|---|---|---|
| `group_id` | string | yes |  |
| `name` | string | no | `""` |
| `visibility` | string | no | `""` |
| `tags` | array | no |  |

## `Signal-Group-Performance`

🟢 reads. Closed-trade performance of ONE signal group: a private group you own or belong to, a public group you follow, or the Community board.

| Field | Type | Needed | Default |
|---|---|---|---|
| `group_id` | string | yes |  |
| `mine` | boolean | no | `false` |
| `platform` | string | no | `"other"` |
