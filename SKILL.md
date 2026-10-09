---
name: atlas-mcp
description: Connect MindVest Atlas to the assistant the person is using, and check that it works. Atlas is a hosted MCP server with tools to scan options flow, analyze real-time stock market data, build investing and trading workflows, set alerts, and preview and place orders in the person's own broker account. Use when the person asks to install or connect Atlas.
---

# Connecting Atlas

Atlas is hosted. There is nothing to run: an assistant needs the address, and
the person signs in.

- **Address:** `https://atlasmcp.finmanagerai.com/mcp` (streamable HTTP)
- **Account:** https://www.mind-vest.io/atlas

## How to connect

1. **Find out which assistant this is** and open its page under `docs/`:

   | Assistant | Page |
   |---|---|
   | Claude Desktop | [docs/claude-desktop.md](docs/claude-desktop.md) |
   | Claude Code | [docs/claude-code.md](docs/claude-code.md) |
   | Cursor | [docs/cursor.md](docs/cursor.md) |
   | Windsurf | [docs/windsurf.md](docs/windsurf.md) |
   | OpenAI Codex CLI | [docs/codex.md](docs/codex.md) |
   | OpenClaw | [docs/openclaw.md](docs/openclaw.md) |
   | Anything that only speaks stdio | [docs/docker.md](docs/docker.md) |

   ChatGPT and Codex can also install the plugin (the server plus its skills):
   see the readme.

2. **Prefer sign-in to a key.** An assistant that can open a sign-in page
   needs only the address. The person signs in to Atlas in their own browser;
   you never see or handle their password.

3. **When the assistant cannot open a sign-in page**, it needs the person's
   access key in a header: `Authorization: Bearer <key>`. The key is on their
   dashboard under Profile → API / CLI / MCP Key. Never type a made-up key
   into a config file: leave `YOUR_ATLAS_ACCESS_KEY` there and ask the person
   to put theirs in. Never repeat a key back to them.

4. **Check it works**: call `Stock-Quote` for `SPY`. A price means the
   connection, the sign-in and the tools are all in place.

## When something is wrong

| What you see | What it means | What to do |
|---|---|---|
| The tools do not appear | The assistant has not re-read its settings | Quit it fully and open it again |
| 401 | Not signed in, or the key is wrong or was replaced | Sign in again, or copy the key again from the dashboard |
| An answer saying the plan's requests are used up | The month's requests are spent | `Subscription-Status` shows what is left and links to the dashboard |
| It connects and then hangs | The assistant cannot speak streamable HTTP | Use the bridge in [docs/docker.md](docs/docker.md) |

## Using it once it is connected

- The full list of tools, with what each one can do: [docs/tools.md](docs/tools.md).
- What is possible with workflows, alerts, plays and orders, with every field
  and templates: the skills under [plugin/skills](plugin/skills).
- Looking something up uses one request of the person's plan. Working on their
  own setups does not.
- A tool that can send or change an order says so. Preview first, show the
  person, and place only when they say to.
- With more than one broker account connected, ask which. Never choose.
