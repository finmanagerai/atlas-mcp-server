# Atlas tools

GENERATED from the live server. Do not edit by hand: it is rewritten from
the same list the server hands to every client, so it cannot fall behind.

160 tools at `https://atlasmcp.finmanagerai.com/mcp`. The names are the
ones your client shows (some add a prefix of their own, such as `mcp__atlas__`).

Each tool says what it can do at its worst, and your client uses that to
decide when to ask you first:

- 🟢 **reads** (95): looks something up and changes nothing.
- 🟡 **adds** (16): makes something new of yours (a preview, a
  folder, a copy) and touches nothing else.
- 🟠 **changes** (19): changes or removes something of yours.
- 🔴 **acts** (30): can send or change a real order, start a run,
  or change what other people see. Only on your say-so.

## Stocks

| Tool | | What it does |
|---|---|---|
| `Multi-Timeframe-Price-Overview` | 🟢 reads | Generate three price charts at once: daily (3 months), weekly (1 year), and hourly (5 days). |
| `Price-Data-OHLCV` | 🟢 reads | Get OHLCV historical bars as JSON (not a single live spot price). |
| `Stock-Quote` | 🟢 reads | Get a real-time UNDERLYING stock quote (not an option contract). |

## Options

| Tool | | What it does |
|---|---|---|
| `Historical-Contract-Greeks` | 🟢 reads | Day-by-day price history, greeks and VOLUME for ONE option contract. |
| `Historical-Options-Chain` | 🟢 reads | The options chain as it stood on a PAST date: daily prices and VOLUME. |
| `Option-Expiration-Dates` | 🟢 reads | List available option expiration dates for a symbol. |
| `Options-Chain` | 🟢 reads | Full options chain — many strikes and sides for one or more expirations. |
| `Single-Option-Quote` | 🟢 reads | Fetch live option contract quote(s) from Polygon /quote. |

## Greek Exposure

| Tool | | What it does |
|---|---|---|
| `Greek-Exposure-Heatmap` | 🟢 reads | Greek exposure heatmaps for one symbol — pick which Greeks to render. |
| `Greek-Exposure-Multi-Expiration` | 🟢 reads | Net Gamma / Delta / Vanna / Theta exposure DATA grid (no chart) across MULTIPLE expirations for one symbol — the OI-weighted per-strike numbers. |
| `Greek-Exposure-Single-Expiration` | 🟢 reads | NET Greek exposure grid for exactly ONE expiration (one chain fetch). |
| `Net-Exposure-Charts` | 🟢 reads | Net exposure bar charts for one symbol — pick which metrics to render. |
| `Put-Call-Ratio` | 🟢 reads | Call vs put OPEN INTEREST (plus today's volume) for one symbol, over an expiry window and a strike window, read as who LEADS and by how much. |

## Options Flow

| Tool | | What it does |
|---|---|---|
| `Options-Flow` | 🟢 reads | Return options-flow trades — historical record across stored streams AND Polygon REST. |
| `Options-Flow-Contract` | 🟢 reads | Per-hour premium histogram for a single options contract. |
| `Top-Volume-and-OI-Contracts` | 🟢 reads | Ranked list of highest-volume or highest-open-interest contracts. |
| `Unusual-Flow-Ratio` | 🟢 reads | Net call-vs-put POSITIONING from one session of unusual options flow. |
| `Volume-and-OI-Charts` | 🟢 reads | Volume and/or open-interest bar charts for one symbol. |

## Charts

| Tool | | What it does |
|---|---|---|
| `Chart-Vision-Analysis` | 🟢 reads | Answer questions about Atlas charts (Greek heatmaps, net exposure bars, price candles, volume, open interest). |
| `Multi-Chart-View` | 🟢 reads | Advanced: combine different chart families and/or symbols in one call (charts= JSON array). |
| `Price-Chart` | 🟢 reads | Candlestick price chart with volume + optional indicators. |

## Fundamentals

| Tool | | What it does |
|---|---|---|
| `Balance-Sheet` | 🟢 reads | Balance sheet for a symbol. freq is 'yearly' or 'quarterly'. |
| `Financial-Metrics` | 🟢 reads | Get basic financial metrics for a stock (P/E, margins, growth, etc.). |
| `Income-Statement` | 🟢 reads | Income statement for a symbol. freq is 'yearly' or 'quarterly'. |

## Estimates

| Tool | | What it does |
|---|---|---|
| `Analyst-Price-Targets` | 🟢 reads | Analyst price target summary (low, high, mean, median) for a symbol. |
| `EPS-Estimates` | 🟢 reads | EPS estimates for upcoming periods. |
| `EPS-Trend` | 🟢 reads | EPS trend for a symbol. |
| `Growth-Estimates` | 🟢 reads | Analyst growth estimates across horizons for a symbol. |
| `Revenue-Estimates` | 🟢 reads | Revenue estimates for upcoming periods. |

## Calendar

| Tool | | What it does |
|---|---|---|
| `Earnings-Calendar` | 🟢 reads | Get the earnings calendar for a date range, optionally filtered by a single symbol. |
| `Earnings-Dates` | 🟢 reads | Earnings dates for a symbol; limit caps how many rows are returned. |
| `IPO-Calendar` | 🟢 reads | Get the IPO calendar for a date range. |

## Ownership

| Tool | | What it does |
|---|---|---|
| `Insider-Transactions` | 🟢 reads | Get insider transactions for a given stock symbol. |
| `Institutional-Holders` | 🟢 reads | Institutional holders for a symbol. |
| `SEC-Filings` | 🟢 reads | Get recent SEC filings (10-K, 10-Q, 8-K, etc.) for a given stock symbol. |
| `Senate-Lobbying-Data` | 🟢 reads | Get US political lobbying data for a company. |

## Brokerage

| Tool | | What it does |
|---|---|---|
| `Account-Activity` | 🟢 reads | Show recent ACTIVITY on the caller's account — every workflow RUN (its reasoning, what it decided, and any error) plus the TRADES those runs fired — newest first. |
| `Account-Balances` | 🟢 reads | Cash balance, buying power, and equity for one linked brokerage account. |
| `Account-Holdings` | 🟢 reads | Everything held in one linked brokerage account: stocks, ETFs, options, crypto and more. |
| `Account-Symbol-Lookup` | 🟢 reads | Resolve how a ticker is represented inside a linked brokerage account (instrument id and related fields). |
| `All-Account-Holdings` | 🟢 reads | Everything held across ALL linked brokerage accounts: stocks, ETFs, options, crypto and more, each tagged with the account it is in. `accounts` lists every account with… |
| `Broker-Connections` | 🟢 reads | List all connected brokerage accounts for the authenticated user. |
| `Transaction-History` | 🟢 reads | Transaction history for one linked brokerage account. |

## Trading — Orders

| Tool | | What it does |
|---|---|---|
| `Cancel-Order` | 🔴 acts | Cancel one order, staged or already sent. |
| `List-Preview-Orders` | 🟢 reads | List the user's recent staged/placed/failed orders. |
| `Place-Order` | 🔴 acts | Send an order to the user's own connected broker account. |
| `Preview-Multiple-Orders` | 🟡 adds | Preview multiple orders at once — e.g. buy 5 NVDA, 5 MSFT, and 5 ASML in one shot. |
| `Preview-Order` | 🟡 adds | Stage an order for the user to review. |

## Trading — Triggers

| Tool | | What it does |
|---|---|---|
| `Create-Trading-Trigger` | 🔴 acts | Persist a price-trigger rule. |
| `Delete-Trading-Trigger` | 🟠 changes | Delete a trading trigger. |
| `List-Fired-Triggers` | 🟢 reads | List the user's completed (fired) triggers from the archive. |
| `List-Trading-Triggers` | 🟢 reads | List the user's trading triggers — watching (is_active=true), paused, and saved PREVIEWS (is_active=false with rule._preview). |
| `Preview-Trading-Trigger` | 🟡 adds | Save a trigger as a PREVIEW: the exact trigger row, validated and shaped like a live one, but NOT armed. |
| `Reactivate-Trigger` | 🔴 acts | Move a fired trigger from the archive back to the active triggers table, resetting it to phase='enter' so it starts monitoring prices again from scratch. |
| `Trigger-Workflow-Schema` | 🟢 reads | Fetch the canonical schema for AI trigger workflows. |
| `Update-Trading-Trigger` | 🔴 acts | Edit one trading trigger in place. |

## Trades in progress

| Tool | | What it does |
|---|---|---|
| `Trade-Cancel-Entry` | 🔴 acts | Take an order OFF before it fills. |
| `Trade-Close` | 🔴 acts | Close a position NOW — everything still open on it, at market. |
| `Trade-Edit-Entry` | 🔴 acts | Move the price an order is waiting to enter at, or turn back on an order that was taken off before it filled. |
| `Trade-Edit-Exit` | 🔴 acts | Move a LIVE trade's stop or targets — the pencil on the trade card, from the chat, the CLI or the API (owner, 2026-09-10). |
| `Trade-Take-Profit` | 🔴 acts | Sell the NEXT take-profit rung now, without waiting for its price. |

## Plays (signals)

| Tool | | What it does |
|---|---|---|
| `Signal-Answer` | 🔴 acts | Say yes or no to a play that was sent to you (see Signal-Pending). |
| `Signal-Broker` | 🟠 changes | See or set the DEFAULT broker account plays go to. |
| `Signal-Delete` | 🔴 acts | Take down a play you posted, before anybody is in it. |
| `Signal-Discover` | 🟢 reads | Public signal groups other people run, to follow. |
| `Signal-Follow` | 🔴 acts | Follow a public signal group (or stop following it), and set how its plays are handled for you. |
| `Signal-Group-Create` | 🟡 adds | Make a new signal group: a place of your own to post plays to. |
| `Signal-Group-Delete` | 🟠 changes | Delete a signal group you own. |
| `Signal-Group-Performance` | 🟢 reads | Closed-trade performance of ONE signal group: a private group you own or belong to, a public group you follow, or the Community board. |
| `Signal-Group-Update` | 🔴 acts | Rename a signal group you own, make it public or private, or tag it. visibility "Atlas-public" puts the group under Discover for every Atlas member to follow and read… |
| `Signal-Groups` | 🟢 reads | List the places you can post a play to, and the groups you follow. |
| `Signal-List` | 🟢 reads | Read the plays on the community board, or the private ones. |
| `Signal-My-Order` | 🔴 acts | Change or cancel YOUR OWN order on somebody else's play, while it is still waiting to enter. |
| `Signal-Pending` | 🟢 reads | The plays sent to you that are waiting for your answer: from the groups you pay for or follow with "manual" chosen. |
| `Signal-Post` | 🔴 acts | Post a trade play — to the community board, or to one of your groups. |
| `Signal-Schema` | 🟢 reads | READ THIS BEFORE POSTING OR TAKING A PLAY. |
| `Signal-Show` | 🟢 reads | Show ONE play as a card, the same one the Signals tab renders. |
| `Signal-Take` | 🔴 acts | Take a play: place it in YOUR OWN account, now. |
| `Signal-Trade-Settings` | 🔴 acts | See or change how plays are traded for you: the "Trade settings" of the Signals page, for one group or for everything. |
| `Signal-Update` | 🔴 acts | Change a play that is still live, instead of posting a second one. |

## Strategy

| Tool | | What it does |
|---|---|---|
| `Autofetch-Strategy` | 🟢 reads | Given a question in natural language, return the best-matching strategies for this user (up to 10), including titles, content, and related material. |
| `Fetch-Strategy` | 🟢 reads | Load one strategy by id with full content and related material. |
| `List-Strategy` | 🟢 reads | List this user's strategies (id, title, visibility, dates) without full body text. |
| `Strategy-Create` | 🟡 adds | Create a new strategy. - title: name (required). - content: optional JSON string; leave empty for a blank strategy. - visibility: private, invite-only, unlisted… |
| `Strategy-Delete` | 🟠 changes | Delete one of your strategies, for good. strategy_id: the UUID from List-Strategy or Strategy-Open. |
| `Strategy-Discover` | 🟢 reads | Search the public strategy marketplace (Discover). |
| `Strategy-Duplicate` | 🟡 adds | Duplicate a shared strategy into your library. |
| `Strategy-Import` | 🟡 adds | Copy a catalog or shared strategy into this user's account as a new private strategy (content and attachments). - strategy_id: id of the strategy to copy (required). |
| `Strategy-Open` | 🟢 reads | Read the signed-in user's strategy. |
| `Strategy-Preview` | 🟢 reads | Same as Strategy-Open but echoes edits you propose, so you can show them to the person in the chat. |
| `Strategy-Save-Instructions` | 🟠 changes | Save the user's strategy-selection notes. - instructions: text to store; leave empty to clear. |
| `Strategy-Update` | 🔴 acts | Save changes to an existing strategy. |

## Workflow

| Tool | | What it does |
|---|---|---|
| `Workflow-Abort` | 🟠 changes | Stop a workflow run that is in progress right now. |
| `Workflow-Agent-Hand-In-Run` | 🔴 acts | Hand in what you decided for one run of a workflow you run yourself. |
| `Workflow-Agent-Report-Progress` | 🟡 adds | Say what you are doing on a run you have not handed in yet, so the person sees it on the workflow's card while you work. |
| `Workflow-Agent-Waiting-Runs` | 🟢 reads | List the runs that are waiting for you, the agent, to do. |
| `Workflow-Apply-Updates` | 🟠 changes | Manually pull the latest parent author edits into an imported workflow that has auto_accept_updates=false. |
| `Workflow-Collab-Find` | 🟢 reads | Find a person on Atlas to share a workflow with, by name or username. |
| `Workflow-Collab-Remove` | 🟠 changes | Take somebody off your workflow, or leave one you were added to. |
| `Workflow-Create` | 🟡 adds | Create a workflow (a recurring AI setup) on the caller's account, saved EXACTLY as supplied. |
| `Workflow-Delete` | 🟠 changes | Permanently delete a workflow owned by the caller. |
| `Workflow-Discover` | 🟢 reads | Search the public workflow marketplace (Discover). |
| `Workflow-Duplicate` | 🟡 adds | Duplicate a workflow into your library — YOUR OWN, or any shared one. |
| `Workflow-Export` | 🟢 reads | Export a workflow's full flow graph + markdown rendering. |
| `Workflow-Folder-Create` | 🟡 adds | Create a workflow folder to organize your Workflows list. |
| `Workflow-Folder-Disband` | 🟠 changes | Disband (delete) a folder. |
| `Workflow-Folder-Discover` | 🟢 reads | Folders of workflows other people have shared. |
| `Workflow-Folder-Import` | 🟡 adds | Import a shared folder: you get your own copy of every shared workflow in it, in a folder of your own. |
| `Workflow-Folder-List` | 🟢 reads | List your workflow folders and which workflows are filed in each. |
| `Workflow-Folder-Move` | 🟠 changes | File one or more of your workflows into a folder. |
| `Workflow-Folder-Remove` | 🟠 changes | Remove one or more workflows from a folder. |
| `Workflow-Folder-Update` | 🔴 acts | Rename, recolour or reorder a workflow folder, or change who can see it. |
| `Workflow-Follow` | 🟠 changes | Stop following a workflow's author, or follow them again. |
| `Workflow-History` | 🟠 changes | A workflow's earlier versions, and going back to one. |
| `Workflow-Import` | 🟡 adds | Clone a workflow into the caller's account — their OWN, or any public/unlisted one. |
| `Workflow-Journal` | 🟠 changes | Read or change a workflow's JOURNAL. |
| `Workflow-List` | 🟢 reads | List the caller's workflows (id, name, status, schedule, visibility) for programmatic discovery. |
| `Workflow-Logs` | 🟢 reads | Return recent run logs for a workflow the caller owns. |
| `Workflow-Open` | 🟢 reads | Show the caller's workflows. |
| `Workflow-Operate` | 🔴 acts | Pause or turn on a workflow that somebody else owns and has made you an operator of. |
| `Workflow-Performance` | 🟢 reads | Closed-trade performance for one workflow the caller owns. |
| `Workflow-Preview` | 🟢 reads | Preview a new workflow, or changes to an existing one, without saving anything. |
| `Workflow-Proposal-Comment` | 🟡 adds | Leave feedback on a suggested change. |
| `Workflow-Proposal-List` | 🟢 reads | List the changes people have suggested to a workflow. |
| `Workflow-Proposal-Show` | 🟢 reads | Read one suggested change in full, with both sides of the diff. `base` is what the workflow said when the suggestion was written, `proposed` is what it would say, and… |
| `Workflow-Restore` | 🔴 acts | Turn a PAUSED workflow back on. |
| `Workflow-Review` | 🔴 acts | A workflow set to "review before it places" holds each run until somebody approves it. |
| `Workflow-Run` | 🔴 acts | Run one of the caller's workflows once, now, instead of waiting for its schedule or alert. |
| `Workflow-Update` | 🔴 acts | Update fields on an existing workflow owned by the caller. |

## Account

| Tool | | What it does |
|---|---|---|
| `Get-Instructions` | 🟢 reads | Read the signed-in user's saved instructions (read-only). |
| `Subscription-Status` | 🟢 reads | Get the authenticated user's subscription tier, monthly usage, remaining requests, and limits. |

## Memory

| Tool | | What it does |
|---|---|---|
| `Memory-Check-Already-Remembered` | 🟢 reads | Check whether something is already remembered, before you write it. |
| `Memory-Forget` | 🟠 changes | Forget one memory because it is wrong or out of date. |
| `Memory-List` | 🟢 reads | Everything Atlas remembers about the signed-in person, by tier (short term: hours; long term: weeks; permanent: kept), with how full each tier is, who stored each… |
| `Memory-Recall` | 🟢 reads | What Atlas remembers about the signed-in person that bears on a question. |
| `Memory-Restore` | 🟡 adds | Bring back a memory that was forgotten. |
| `Memory-Update` | 🟠 changes | Change one memory: its words, its importance (1 to 10), where it is kept (short / long / permanent), its kind, its key, its project, or pin it so nothing automatic ever… |
| `Memory-Write` | 🟠 changes | Keep something durable about the signed-in person: a correction they made, a preference, a fact about them or their trading. |

## Search

| Tool | | What it does |
|---|---|---|
| `Connection-Check-Fetch` | 🟢 reads | A connection check, not a page reader. |
| `Connection-Check-Search` | 🟢 reads | A connection check, not a search. |
| `Mcp-Call` | 🔴 acts | Run one tool on a service the user has connected to their own Atlas account (the website's Connect page, MCP Servers). |
| `Mcp-Tools` | 🟢 reads | List the services the user has connected to their own Atlas account, and the tools each one offers. |
| `Search-Tools` | 🟢 reads | Find a tool by what it does. |
| `Ticker-Symbol-Lookup` | 🟢 reads | Resolve a company name or partial name to its ticker symbol. |
| `Web-Search` | 🟢 reads | LIVE web search for real-time news and facts. |

## Alerts

| Tool | | What it does |
|---|---|---|
| `Alert-Fires` | 🟢 reads | Recent alert fires, each with the message it carried. |
| `Create-Alert` | 🔴 acts | Create a streaming alert that DMs the user on Discord (and optionally runs a workflow / arms a trigger / places an order) when a condition matches. ⚠️ FIRST call… |
| `Delete-Alert` | 🟠 changes | Switch an alert off and hide it — one, or a whole pile at once. |
| `List-Alert-Types` | 🟢 reads | The catalog of alert types you can create — read THIS before calling Create-Alert to learn what alerts exist and how to fill each one's conditions. |
| `List-Alerts` | 🟢 reads | List the caller's alerts. |
| `List-Stream-Subscriptions` | 🟢 reads | List currently active streams (flow / quote / exposure / quote). |
| `Preview-Alert` | 🟢 reads | Dry-run an alert spec without persisting or DMing. |
| `Update-Alert` | 🔴 acts | Patch an existing alert's fields without recreating. ``updates`` accepts the same keys Create-Alert exposes (name, symbol, alert_type, stream_type, conditions… |

## Guides

| Tool | | What it does |
|---|---|---|
| `Atlas-Agent-Guide` | 🟢 reads | READ THIS FIRST, BEFORE YOU USE ANY OTHER ATLAS TOOL. |
| `Atlas-Guide-Index` | 🟢 reads | The Atlas guide's table of contents — every topic, grouped, with the id and link for each. |
| `Atlas-Guide-Read` | 🟢 reads | Read one topic of the Atlas guide in full, by its id (from Atlas-Guide-Index or Atlas-Guide-Search). |
| `Atlas-Guide-Search` | 🟢 reads | Search the Atlas guide for a word or phrase and get back the topics that mention it, each with a snippet and a link. |

## Other

| Tool | | What it does |
|---|---|---|
| `List-Tool-Safety` | 🟢 reads | List every Atlas tool by its exact name, with what it says about its own safety: whether it only reads, whether it can change or remove something, whether it reaches… |
| `Phone-Button` | 🟢 reads | Was the button pressed on a notification you sent with Phone-Notify? |
| `Phone-Notify` | 🟡 adds | Send a notification to the signed-in person's own phone (the MindVest Atlas app), from a script, a local project, the CLI or a chat. |
