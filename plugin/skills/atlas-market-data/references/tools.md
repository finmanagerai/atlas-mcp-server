# The tools behind this skill (34)

GENERATED from the live server; do not edit by hand. Every field each
tool accepts. Nothing here is required unless the table says so: it is
what is possible.

## `Options-Flow`

🟢 reads. Return options-flow trades — historical record across stored streams AND Polygon REST.

| Field | Type | Needed | Default |
|---|---|---|---|
| `view` | string | no | `"board"` |
| `symbol` | string | no |  |
| `symbols` | array | no |  |
| `expiration_date` | string | no |  |
| `strike` | number | no |  |
| `side` | string | no |  |
| `option_symbol` | string | no |  |
| `from_date` | string | no |  |
| `to_date` | string | no |  |
| `limit` | integer | no | `200` |
| `min_premium` | number | no |  |
| `max_premium` | number | no |  |
| `min_tag` | string | no |  |
| `image_format` | string | no |  |
| `platform` | string | no | `"other"` |
| `max_per_ticker` | integer | no | `3` |
| `max_per_expiry` | integer | no |  |
| `expiry_within_days` | integer | no |  |
| `action` | string | no |  |
| `open_close` | string | no |  |
| `trade_type` | string | no |  |
| `min_size` | number | no |  |
| `max_size` | number | no |  |
| `min_volume` | number | no |  |
| `min_open_interest` | number | no |  |
| `min_spot` | number | no |  |
| `max_spot` | number | no |  |
| `from_time` | string | no |  |
| `to_time` | string | no |  |

The tool's own description, in full:

````text
Return options-flow trades — historical record across stored
    streams AND Polygon REST. Not a live feed.

    GIVE IT TIME. A big name (SPY, QQQ, SPX, NVDA) across several expiries, a
    wide date range, or a cold read can take several minutes, up to about ten.
    Wait for it rather than retrying (a retry starts the read again); narrow it
    with expiration_date / expiry_within_days, a strike, min_premium or a
    shorter date range to make it quick.

    ── Three modes (chosen by what you pass) ────────────────────────
      1. **Top-N feed** — `symbol` omitted. Iterates the streamed core
         universe (read from `stream_subscription` table; no hardcoded
         list), pulls each ticker's prints for the current trading day,
         ranks by **premium descending**. Returns the biggest
         block/sweep prints across the universe. Symbols you've queried
         today bubble into the pool too (and retire overnight).

      2. **Single-symbol, no specific contract** — `symbol=X` with no
         `expiration_date`/`strike`/`option_symbol`. Reads stored
         streaming data first; if empty (e.g. off-universe ticker like
         INTC), **automatically falls back to Polygon REST** with
         multi-expiry historical scan: every expiration within the
         next 30 days, top-volume strikes per expiry, trades + matched
         historical NBBO for real `bs`/`side` derivation. Set
         `include_historical_fallback=false` to disable.

      3. **Specific contract** — `symbol=X` with `expiration_date=Y`
         and `strike=Z` (or `option_symbol=O:...`). Stored-only, no
         fallback. Use this when the user wants a specific contract
         drilldown.

      4. **Several names at once** — `symbols=["PANW","NET","CRWD"]` (or a
         comma-separated `symbol`). Pulls each one and RANKS them against
         each other by total premium, with the call/put lean and whether
         the money is opening or closing positions. This is the peer
         comparison — "which of these has the flow" — in ONE call instead
         of one per name, and a ticker with nothing on the tape says so
         rather than being dropped. Up to 8 names.

      5. **`view="contract"`** — the per-hour PREMIUM HISTOGRAM for one
         contract: a bar per market hour (9 AM .. 3 PM ET) stacking
         opening premium over closing, with the dominant side labelled.
         Name the contract the same way mode 3 does. This is the whole
         session off the stored tape, not just the prints in the table,
         and it renders in the same widget as the board.

    ── Defaults applied ─────────────────────────────────────────────
      * **`trade_type`**: defaults to `"block,sweep"` in top-N AND
        single-symbol modes. Pass `trade_type=""` for the full tape.
      * **Block-thresholds** (set via `_BLOCK_PREMIUM_BY_TIER`):
        megacap $100K, midcap $50K, small $2K. Sweeps require
        premium ≥ 50% of the block threshold.
      * **`from_date`**: defaults to the current US-equity trading day
        in America/New_York, anchored to 09:30 ET — pre-open and
        overnight calls roll back to the prior trading day, weekends
        roll back to Friday. The actual date queried is echoed as
        `effective_from_date`.
      * **`expiry_within_days`**: defaults to 30 in top-N mode and
        the single-symbol historical fallback. Filters contracts by
        their expiration date (NOT trade date), so the result mixes
        all near-month expiries rather than collapsing to one.
      * **`max_per_ticker`** = 3 (top-N only): caps rows per ticker
        so one heavy 0DTE doesn't crowd out everyone else.
      * **`max_per_expiry`** = 5 (top-N only): forces variety across
        expiries.
      * **Sort**: every result is ranked by premium descending —
        biggest prints first.

    ── Row shape ────────────────────────────────────────────────────
      Every row is one trade. Never aggregated, never net-flow. Each
      carries:
        * `side` ∈ {"buy", "sell", "unknown"} — derived from
          price-vs-NBBO; "unknown" when confidence is too low to
          commit (no percentage shown).
        * `bs` ∈ {"ask", "above", "mid", "below", "bid", "unknown"} —
          descriptive position relative to the NBBO at print time.
        * `cp` ∈ {"call", "put"}.
        * `open_close` ∈ {"open", "close"} — heuristic. Independent
          of side; doesn't merge counterparties.
        * `type` ∈ {"block", "sweep", "iso", "regular"} — classified
          against the **current** tier thresholds on every read.
        * `time` is the naive ET wall-clock ("2026-05-28T09:35:29",
          no timezone offset) so the widget renders Eastern regardless
          of viewer locale. Use `timestamp_ns` for exact UTC.

    ── "trade date" vs "expiration date" — read carefully ───────────
      When a user says "AMD flow for 05/29/2026" they almost always
      mean "trades PRINTED on 05/29/2026", regardless of which
      expiry. Pass `from_date=2026-05-29` — NOT `expiration_date`.
      `expiration_date` is a contract-identity filter that collapses
      the result to a single expiry chain. Use it only when the user
      explicitly asks for a specific expiry (e.g. "AMD 0DTE only",
      "AMD 6/20 chain").

    ── Non-streamed tickers and staleness ───────────────────────────
      For tickers we don't stream (INTC, GME, etc.) the historical
      fallback gives a snapshot at query time — every call is a fresh
      Polygon pull, no cache. Querying again later in the same day
      surfaces any new prints. The next trading day, the symbol
      automatically retires from the top-N pool unless re-queried —
      so yesterday's block doesn't keep showing as #1 today. To pull
      yesterday's record explicitly: `Options-Flow(symbol=GME,
      from_date=<yesterday>)`.

    Args:
        symbol: Underlying ticker (e.g. SPY); omit for top-N across universe.
        expiration_date: Contract-identity filter (only contracts expiring
                         on this YYYY-MM-DD). Do NOT pass when the user
                         meant "trades on this date" — use from_date.
        strike: Optional strike filter (with expiration_date).
        side: Optional call/put filter on results.
        option_symbol: Optional Polygon-style option symbol filter.
        from_date: Trading-day lower bound (YYYY-MM-DD) — the date the
                   trade printed, NOT the contract's expiry. Defaults to
                   the current trading day (anchored 09:30 ET).
        to_date: Trading-day upper bound (YYYY-MM-DD). Pair with from_date
                 for a single-session query.
        limit: Max trades to return (default 20).
        min_premium: Minimum notional filter in dollars.
        max_premium: Maximum notional filter.
        min_tag: Minimum unusual tag — unusual, very_unusual, extreme_unusual.
        max_per_ticker: Top-N only; cap rows per ticker (default 3).
        max_per_expiry: Top-N only; cap rows per expiration (default 5).
        expiry_within_days: Top-N + historical fallback; only include
                            contracts expiring within N days of today
                            (default 30).
        action: Side filter — "buy" or "sell" (rows derived from NBBO).
        open_close: Filter to "open" or "close" rows.
        trade_type: Comma-list filter — e.g. "block,sweep", "block",
                    "sweep", "iso". Empty string ("") opts back into the
                    full tape (including regular prints).
        min_size / max_size: Contract-count filter.
        min_volume: Minimum daily contract volume.
        min_open_interest: Minimum daily OI.
        min_spot / max_spot: Underlying-price filter.
        from_time / to_time: "HH:MM" ET wall-clock filter on TIME column.
        image_format: Optional 'png' / 'jpeg' to embed a base64 image
                      of the trades table next to the JSON. Ignored on
                      widget-capable clients.
        platform: 'openai' | 'claude' | 'other' (default). Widget-capable
                  clients get the iframe envelope; others get plain JSON.
    
Returns one row per trade: time, ticker, expiry, strike, cp, side, bs, spot,
size, price, premium, type, volume, open_interest, volume_to_oi_ratio, tag.

Reads from the stored options-flow tape (historical record of large prints,
not a real-time feed). Default last 20 rows. Pass symbol only for all
stored trades on that ticker, or narrow with option_symbol /
expiration_date + strike. Optional side filters call vs put.
Unusual tags use volume_to_oi_ratio = volume / open_interest:
  normal (<1), unusual (1-3), very_unusual (3-10), extreme_unusual (>=10).

    
Use for the stored option trade tape (historical record). Requires symbol
unless running the top-N feed; optionally filter by contract or date range.
Default limit 200 — wide enough that the widget's per-contract hourly
histogram has material to aggregate without a second call.
````

## `Options-Flow-Contract`

🟢 reads. Per-hour premium histogram for a single options contract.

| Field | Type | Needed | Default |
|---|---|---|---|
| `symbol` | string | yes |  |
| `expiration_date` | string | no |  |
| `strike` | number | no |  |
| `side` | string | no |  |
| `option_symbol` | string | no |  |
| `from_date` | string | no |  |
| `to_date` | string | no |  |
| `platform` | string | no | `"other"` |

## `Unusual-Flow-Ratio`

🟢 reads. Net call-vs-put POSITIONING from one session of unusual options flow.

| Field | Type | Needed | Default |
|---|---|---|---|
| `symbol` | string | yes |  |
| `date` | string | no |  |
| `expiration` | string | no |  |
| `from_expiration` | string | no |  |
| `to_expiration` | string | no |  |
| `expiration_range` | string | no |  |
| `min_dte` | integer | no |  |
| `max_dte` | integer | no |  |
| `strike_range` | string | no |  |
| `trade_type` | string | no |  |
| `min_tag` | string | no |  |
| `min_premium` | number | no |  |
| `full_session` | boolean | no | `false` |

## `Put-Call-Ratio`

🟢 reads. Call vs put OPEN INTEREST (plus today's volume) for one symbol, over an expiry window and a strike window, read as who LEADS and by how much.

| Field | Type | Needed | Default |
|---|---|---|---|
| `symbol` | string | yes |  |
| `expiration` | string | no |  |
| `from_expiration` | string | no |  |
| `to_expiration` | string | no |  |
| `expiration_range` | string | no |  |
| `min_dte` | integer | no |  |
| `max_dte` | integer | no |  |
| `strike_range` | string | no |  |
| `strikes_around_spot` | integer | no |  |
| `num_expirations` | integer | no | `5` |

## `Top-Volume-and-OI-Contracts`

🟢 reads. Ranked list of highest-volume or highest-open-interest contracts.

| Field | Type | Needed | Default |
|---|---|---|---|
| `symbol` | string | yes |  |
| `expiration` | string | no |  |
| `from_expiration` | string | no |  |
| `to_expiration` | string | no |  |
| `expiration_range` | string | no |  |
| `sort_by` | string | no | `"volume"` |
| `limit` | integer | no | `20` |

## `Volume-and-OI-Charts`

🟢 reads. Volume and/or open-interest bar charts for one symbol.

| Field | Type | Needed | Default |
|---|---|---|---|
| `symbol` | string | yes |  |
| `types` | string | no | `"vol,oi"` |
| `date_range` | string | no |  |
| `image_format` | string | no | `"png"` |
| `platform` | string | no | `"other"` |
| `expiration` | string | no |  |
| `from_expiration` | string | no |  |
| `to_expiration` | string | no |  |
| `expiration_range` | string | no |  |

## `Stock-Quote`

🟢 reads. Get a real-time UNDERLYING stock quote (not an option contract).

| Field | Type | Needed | Default |
|---|---|---|---|
| `symbol` | string | yes |  |

## `Price-Data-OHLCV`

🟢 reads. Get OHLCV historical bars as JSON (not a single live spot price).

| Field | Type | Needed | Default |
|---|---|---|---|
| `symbol` | string | yes |  |
| `interval` | string | no | `"1d"` |
| `period` | string | no | `"3mo"` |
| `start` | string | no |  |
| `end` | string | no |  |
| `timestamp` | string | no |  |
| `bars` | integer | no |  |

## `Multi-Timeframe-Price-Overview`

🟢 reads. Generate three price charts at once: daily (3 months), weekly (1 year), and hourly (5 days).

| Field | Type | Needed | Default |
|---|---|---|---|
| `symbol` | string | yes |  |
| `theme` | string | no | `"dark"` |
| `image_format` | string | no | `"png"` |
| `platform` | string | no | `"other"` |

## `Price-Chart`

🟢 reads. Candlestick price chart with volume + optional indicators.

| Field | Type | Needed | Default |
|---|---|---|---|
| `symbol` | string | yes |  |
| `interval` | string | no | `"1d"` |
| `period` | string | no | `"3mo"` |
| `timeframes` | string | no |  |
| `start` | string | no |  |
| `end` | string | no |  |
| `theme` | string | no | `"dark"` |
| `image_format` | string | no | `"png"` |
| `force_refresh` | boolean | no | `false` |
| `bars` | integer | no |  |
| `markings` | string | no |  |
| `mark` | string | no |  |
| `trend_lines` | string | no |  |
| `indicators` | string | no |  |
| `indicator_colors` | string | no |  |
| `indicators_hidden` | string | no |  |
| `ema` | string | no |  |
| `rsi` | string | no |  |
| `vwap` | string | no |  |
| `macd` | string | no |  |
| `bollinger` | string | no |  |
| `atr` | string | no |  |
| `adx` | string | no |  |
| `cvd` | string | no |  |
| `platform` | string | no | `"other"` |

## `Multi-Chart-View`

🟢 reads. Advanced: combine different chart families and/or symbols in one call (charts= JSON array).

| Field | Type | Needed | Default |
|---|---|---|---|
| `charts` | string | yes |  |
| `image_format` | string | no | `"png"` |
| `platform` | string | no | `"other"` |

## `Chart-Vision-Analysis`

🟢 reads. Answer questions about Atlas charts (Greek heatmaps, net exposure bars, price candles, volume, open interest).

| Field | Type | Needed | Default |
|---|---|---|---|
| `question` | string | yes |  |

## `Ticker-Symbol-Lookup`

🟢 reads. Resolve a company name or partial name to its ticker symbol.

| Field | Type | Needed | Default |
|---|---|---|---|
| `company_name` | string | yes |  |

## `Options-Chain`

🟢 reads. Full options chain — many strikes and sides for one or more expirations.

| Field | Type | Needed | Default |
|---|---|---|---|
| `symbol` | string | yes |  |
| `expiration` | string | no |  |
| `from_expiration` | string | no |  |
| `to_expiration` | string | no |  |
| `expiration_range` | string | no |  |
| `max_expirations` | integer | no | `12` |

## `Single-Option-Quote`

🟢 reads. Fetch live option contract quote(s) from Polygon /quote.

| Field | Type | Needed | Default |
|---|---|---|---|
| `symbol` | string | no |  |
| `expiration_date` | string | no |  |
| `strike` | number | no |  |
| `side` | string | no |  |
| `option_symbol` | string | no |  |
| `quotes` | string | no |  |

## `Option-Expiration-Dates`

🟢 reads. List available option expiration dates for a symbol.

| Field | Type | Needed | Default |
|---|---|---|---|
| `symbol` | string | yes |  |
| `filter` | string | no | `"next_10"` |

## `Historical-Options-Chain`

🟢 reads. The options chain as it stood on a PAST date: daily prices and VOLUME.

| Field | Type | Needed | Default |
|---|---|---|---|
| `symbol` | string | yes |  |
| `expiration` | string | yes |  |
| `date` | string | yes |  |
| `to_date` | string | no |  |
| `strike_window` | integer | no |  |

## `Historical-Contract-Greeks`

🟢 reads. Day-by-day price history, greeks and VOLUME for ONE option contract.

| Field | Type | Needed | Default |
|---|---|---|---|
| `symbol` | string | yes |  |
| `expiration` | string | yes |  |
| `strike` | number | yes |  |
| `side` | string | yes |  |
| `from_date` | string | yes |  |
| `to_date` | string | no |  |
| `include_greeks` | boolean | no | `true` |

## `Greek-Exposure-Single-Expiration`

🟢 reads. NET Greek exposure grid for exactly ONE expiration (one chain fetch).

| Field | Type | Needed | Default |
|---|---|---|---|
| `symbol` | string | yes |  |
| `expiration` | string | yes |  |

## `Greek-Exposure-Multi-Expiration`

🟢 reads. Net Gamma / Delta / Vanna / Theta exposure DATA grid (no chart) across MULTIPLE expirations for one symbol — the OI-weighted per-strike numbers.

| Field | Type | Needed | Default |
|---|---|---|---|
| `symbol` | string | yes |  |
| `num_expirations` | integer | no | `5` |
| `expiration` | string | no |  |
| `from_expiration` | string | no |  |
| `to_expiration` | string | no |  |
| `expiration_range` | string | no |  |

## `Greek-Exposure-Heatmap`

🟢 reads. Greek exposure heatmaps for one symbol — pick which Greeks to render.

| Field | Type | Needed | Default |
|---|---|---|---|
| `symbol` | string | yes |  |
| `greeks` | string | no | `"gamma,delta,vanna,theta"` |
| `strike_range` | string | no |  |
| `date_range` | string | no |  |
| `image_format` | string | no | `"png"` |
| `markings` | string | no |  |
| `platform` | string | no | `"other"` |
| `expiration` | string | no |  |
| `from_expiration` | string | no |  |
| `to_expiration` | string | no |  |
| `expiration_range` | string | no |  |
| `mark` | string | no |  |

## `Net-Exposure-Charts`

🟢 reads. Net exposure bar charts for one symbol — pick which metrics to render.

| Field | Type | Needed | Default |
|---|---|---|---|
| `symbol` | string | yes |  |
| `metrics` | string | no | `"net_gex,net_dex,net_vex,net_tex"` |
| `strike_range` | string | no |  |
| `date_range` | string | no |  |
| `image_format` | string | no | `"png"` |
| `markings` | string | no |  |
| `platform` | string | no | `"other"` |
| `expiration` | string | no |  |
| `from_expiration` | string | no |  |
| `to_expiration` | string | no |  |
| `expiration_range` | string | no |  |
| `mark` | string | no |  |

## `Earnings-Calendar`

🟢 reads. Get the earnings calendar for a date range, optionally filtered by a single symbol.

| Field | Type | Needed | Default |
|---|---|---|---|
| `from_date` | string | yes |  |
| `to_date` | string | yes |  |
| `symbol` | string | no |  |

## `Earnings-Dates`

🟢 reads. Earnings dates for a symbol; limit caps how many rows are returned.

| Field | Type | Needed | Default |
|---|---|---|---|
| `symbol` | string | yes |  |
| `limit` | integer | no | `12` |

## `Financial-Metrics`

🟢 reads. Get basic financial metrics for a stock (P/E, margins, growth, etc.).

| Field | Type | Needed | Default |
|---|---|---|---|
| `symbol` | string | yes |  |
| `metric` | string | no | `"all"` |

## `Income-Statement`

🟢 reads. Income statement for a symbol. freq is 'yearly' or 'quarterly'.

| Field | Type | Needed | Default |
|---|---|---|---|
| `symbol` | string | yes |  |
| `freq` | string | no | `"yearly"` |

## `Balance-Sheet`

🟢 reads. Balance sheet for a symbol. freq is 'yearly' or 'quarterly'.

| Field | Type | Needed | Default |
|---|---|---|---|
| `symbol` | string | yes |  |
| `freq` | string | no | `"yearly"` |

## `EPS-Estimates`

🟢 reads. EPS estimates for upcoming periods.

| Field | Type | Needed | Default |
|---|---|---|---|
| `symbol` | string | yes |  |

## `Revenue-Estimates`

🟢 reads. Revenue estimates for upcoming periods.

| Field | Type | Needed | Default |
|---|---|---|---|
| `symbol` | string | yes |  |

## `Analyst-Price-Targets`

🟢 reads. Analyst price target summary (low, high, mean, median) for a symbol.

| Field | Type | Needed | Default |
|---|---|---|---|
| `symbol` | string | yes |  |

## `SEC-Filings`

🟢 reads. Get recent SEC filings (10-K, 10-Q, 8-K, etc.) for a given stock symbol.

| Field | Type | Needed | Default |
|---|---|---|---|
| `symbol` | string | yes |  |
| `from_date` | string | no |  |
| `to_date` | string | no |  |

## `Insider-Transactions`

🟢 reads. Get insider transactions for a given stock symbol.

| Field | Type | Needed | Default |
|---|---|---|---|
| `symbol` | string | yes |  |
| `from_date` | string | no |  |
| `to_date` | string | no |  |

## `Institutional-Holders`

🟢 reads. Institutional holders for a symbol.

| Field | Type | Needed | Default |
|---|---|---|---|
| `symbol` | string | yes |  |

## `Web-Search`

🟢 reads. LIVE web search for real-time news and facts.

| Field | Type | Needed | Default |
|---|---|---|---|
| `query` | string | yes |  |
| `recency` | string | no | `""` |
