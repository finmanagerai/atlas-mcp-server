<p align="center">
  <img src="https://readme-typing-svg.demolab.com?font=Inter&weight=700&size=28&duration=3000&pause=700&center=true&vCenter=true&width=900&lines=MindVest+Atlas;Scan+options+flow+and+real-time+market+data;Build+investing+and+trading+workflows;You+set+the+strategy.+Atlas+carries+it+out." alt="MindVest Atlas" />
</p>

<p align="center">
  <strong>Atlas gives your AI agent the tools to scan options flow, analyze real-time stock market data, and build investing and trading workflows, so you don't have to build this yourself.</strong>
</p>

<p align="center">
  <a href="#install">Install</a>
  ·
  <a href="#the-plugin">Plugin</a>
  ·
  <a href="#what-you-can-ask-for">What you can ask for</a>
  ·
  <a href="#tools">Tools</a>
  ·
  <a href="#safety">Safety</a>
</p>

<p align="center">
  <img alt="MCP" src="https://img.shields.io/badge/MCP-Compatible-blue" />
  <img alt="Works with" src="https://img.shields.io/badge/Works%20with-ChatGPT%20%7C%20Claude%20%7C%20Codex%20%7C%20Cursor-purple" />
  <img alt="Market data" src="https://img.shields.io/badge/Data-Options%20flow%20%7C%20Quotes%20%7C%20Charts-orange" />
  <img alt="Orders" src="https://img.shields.io/badge/Orders-In%20your%20own%20broker%20account-green" />
</p>

---

# MindVest Atlas

**You focus on the strategy. Atlas automates it and handles the execution, in
your own broker account, by the rules you set.**

Most assistants can talk about the market. Few can look at it, and fewer can
act on what they find. Atlas is a hosted MCP server that gives an assistant
both halves:

```text
Scan the market  →  Decide with your plan  →  Preview  →  You approve  →  Atlas carries it out
```

<img width="1128" height="946" alt="Atlas workflow" src="https://github.com/user-attachments/assets/9a98410e-1cfd-49d3-a2dd-95d5346af1fa" />

This repository holds what you need to connect: the install pages, the tool
list, and the plugin. The server itself is hosted for you at
`https://atlasmcp.finmanagerai.com/mcp`. There is nothing to run.

---

## Install

### 1. Have an Atlas account

Create one, or sign in, at **https://www.mind-vest.io/atlas**.

### 2. Add Atlas to your assistant

**The address is all most assistants need.** Give them
`https://atlasmcp.finmanagerai.com/mcp` and they open Atlas's sign-in page in
your browser the first time. You sign in there; the assistant never sees your
password.

- **ChatGPT and Codex**: install the plugin. See [The plugin](#the-plugin).
- **Claude (web and desktop)**: Settings → Connectors → Add custom connector,
  and paste the address.
- **Claude Code**:

  ```bash
  claude mcp add --transport http atlas https://atlasmcp.finmanagerai.com/mcp
  ```

  then `/mcp` inside a session to sign in. Or install the plugin, which adds
  the skills too:

  ```bash
  /plugin marketplace add finmanagerai/atlas-mcp-server
  /plugin install mindvest-atlas@mindvest
  ```

- **Anything that reads the MCP registry**: `io.github.finmanagerai/atlas-mcp-server`

**For an assistant that cannot open a sign-in page**, use your access key
instead. It is on your dashboard under **Profile → API / CLI / MCP Key**.
Treat it like a password.

```json
{
  "mcpServers": {
    "atlas": {
      "type": "streamable-http",
      "url": "https://atlasmcp.finmanagerai.com/mcp",
      "headers": { "Authorization": "Bearer YOUR_ATLAS_ACCESS_KEY" }
    }
  }
}
```

### 3. Try it

Ask: "Show me a quote for SPY." If a price comes back, you are connected.

### A page for each assistant

[Claude Desktop](docs/claude-desktop.md) ·
[Claude Code](docs/claude-code.md) ·
[Cursor](docs/cursor.md) ·
[Windsurf](docs/windsurf.md) ·
[OpenAI Codex CLI](docs/codex.md) ·
[OpenClaw](docs/openclaw.md) ·
[Docker (for assistants that only speak stdio)](docs/docker.md)

---

## The plugin

A plugin is the server plus **skills**: short guides that tell an assistant
what is possible with Atlas and show it templates to start from. Nine come
with it:

| Skill | What it covers |
|---|---|
| `atlas-get-started` | Check the connection, your plan and your broker accounts |
| `atlas-market-data` | Scanning options flow and analyzing real-time stock market data |
| `atlas-workflows` | Building a plan Atlas runs for you: every field, with templates |
| `atlas-alerts` | Being told when something happens, and starting a workflow when it does |
| `atlas-signals` | Posting, reading and taking plays |
| `atlas-triggers-and-trades` | Direct triggers, linked trades (either/or and one-starts-the-other), orders, and managing an open trade |
| `atlas-agent-run-workflows` | A workflow your own assistant runs: it registers it, picks up the runs that are waiting, and hands in what it decided |
| `atlas-agent-run-loop` | The loop that wakes your assistant by itself: the wake-up, a check that costs nothing when no run is waiting, and the stages of one run |
| `atlas-agent-run-loop-test` | Proving that loop works with a workflow that cannot trade: the tools, the assistant waking by itself, and a run started by a schedule or an alert |

To have your own assistant wake itself on a timer, see
[docs/agent-run-loop.md](docs/agent-run-loop.md).

Each skill says what is possible, not what you must do. The lists of fields
inside them are written from the live server, so they match it.

**Download** the archives from the
[latest release](https://github.com/finmanagerai/atlas-mcp-server/releases/latest):

| File | For |
|---|---|
| `mindvest-atlas-chatgpt.zip` | ChatGPT and Codex. Upload it on the OpenAI platform's Plugins page |
| `mindvest-atlas-claude-code.zip` | Claude Code |
| `mindvest-atlas-claude-skills.zip` | Claude's "upload a skill": unzip it, then upload the skills one at a time |

Or build them yourself: `python3 scripts/build-plugin.py` writes `dist/`.

No key is inside any of them. They carry the server's address, and you sign
in when the plugin first connects.

---

## What you can ask for

**Scan the options market**

```text
What are the biggest options trades in the market today?
```

```text
Which has more call buying right now: NVDA, AMD or AVGO?
```

**Analyze a stock**

```text
Give me the picture on AAPL: the trend, the options flow, and when it next reports.
```

```text
Where is the largest gamma level on SPY today, and is price above or below it?
```

**Build a workflow**

```text
Every weekday at 9:30, send me a brief on SPY and the five names on my list.
```

```text
When SPY breaks above 600, buy the nearest call with $500, take half off at
+30%, and show me the trade before it goes in.
```

**Set an alert**

```text
Tell me when a call sweep over $250k prints on NVDA.
```

**Post or take a play**

```text
Post it to my group: SPY 780 calls at 2.10, out at +50% and +100%, stop 30%.
```

**Place and manage a trade**

```text
Preview buying 10 NVDA at 900 with a stop at 880 and a target at 940.
```

```text
Move the stop on my SPY trade to breakeven.
```

More, with the tools each one uses: [docs/examples.md](docs/examples.md).

---

## Tools

Every tool the server has, with what each one can do at its worst (only
reads, adds something, changes something, or can send an order):
**[docs/tools.md](docs/tools.md)**. That page is written from the live server.

In short:

- **Market data**: options flow, quotes, price history, charts, options
  chains, dealer exposure, earnings, financials, filings, web search.
- **Workflows**: a plan in plain words that Atlas runs on a schedule, when an
  alert goes off, or when you press Run.
- **Alerts**: a price level, a large options trade, a volume spike, a
  technical cross, a move in dealer exposure, or your own trades.
- **Plays**: one trade idea, written down in full, shared with a board or a
  group.
- **Orders and trades**: preview, place, cancel, and manage a trade that is
  open, in your own connected broker account.
- **Strategies and memory**: your written playbooks, and what Atlas remembers
  about how you work.

---

## Safety

- **An order is placed or changed only when you say so**, or by a workflow
  you switched on. Every tool states whether it only reads, changes something,
  or can send an order, and your assistant asks you first.
- **Preview first.** An order can be staged and shown to you before anything
  reaches your broker, and a workflow can hold each run for your approval.
- **Your broker sign-in stays with your broker.** You connect an account on
  the Atlas dashboard; an assistant never sees those details.
- **Atlas runs on its own servers.** It does not read files on your computer
  or run commands there.
- **Atlas does not give investment advice.** Trading involves risk, including
  the loss of what you put in.

More: [docs/security.md](docs/security.md) ·
[Privacy](https://www.mind-vest.io/privacy) ·
[Terms](https://www.mind-vest.io/terms)

---

> This repository holds only what is needed to find and install Atlas. The
> server, the broker connections and the data pipelines are not open source.
