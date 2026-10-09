# Atlas MCP — Claude Desktop

Connect Atlas to Anthropic's Claude Desktop app (macOS / Windows).

## The short way: sign in

In Claude (the desktop app or the web): **Settings → Connectors → Add custom
connector**, name it Atlas, and paste `https://atlasmcp.finmanagerai.com/mcp`.
Claude opens Atlas's sign-in page; sign in and approve. No key is needed.

## The other way: your access key

## 1. Get your access key

Sign in at https://www.mind-vest.io/atlas, open the **Dashboard**, and copy the key under **Profile → API / CLI / MCP Key**. Copy the value; you won't see it again.

## 2. Edit the Claude Desktop config

| OS | Path |
|---|---|
| macOS | `~/Library/Application Support/Claude/claude_desktop_config.json` |
| Windows | `%APPDATA%\Claude\claude_desktop_config.json` |

Add an `atlas` entry under `mcpServers`:

```json
{
  "mcpServers": {
    "atlas": {
      "type": "streamable-http",
      "url": "https://atlasmcp.finmanagerai.com/mcp",
      "headers": {
        "Authorization": "Bearer YOUR_ATLAS_ACCESS_KEY"
      }
    }
  }
}
```

If `mcpServers` already exists, add the `atlas` key alongside your other servers.

## 3. Restart Claude Desktop

Quit fully (⌘Q on macOS — closing the window doesn't reload config) and reopen.

## 4. Test prompt

> "Use Atlas to get a stock quote for SPY."

Claude should show the `Stock-Quote` tool call and return price, change %, volume, and timestamp.

## Required env / inputs

| Name | Required | Notes |
|---|---|---|
| `Authorization` header | yes | `Bearer YOUR_ATLAS_ACCESS_KEY` — pasted directly in the config |

No environment variables on the host are required.

## Troubleshooting

- **No Atlas tools listed.** Config has a JSON syntax error or Claude wasn't fully quit. Validate with `python3 -m json.tool < claude_desktop_config.json`.
- **`401`/`403`.** Key is wrong, revoked, or has a stray space. Regenerate from the dashboard.
- **"Server disconnected"** after a few seconds. Network/proxy is blocking long-lived HTTP. Switch to the [Docker stdio bridge](docker.md).
- **A tool says your plan's requests are used up.** `Subscription-Status` shows what is left this month.

## Capabilities & permissions

- **Reads:** market data, your broker balances/positions, your strategies/workflows.
- **Writes (with explicit user approval):** order previews, trigger creation/edits, workflow CRUD, and `Place-Order` for submitting trades.
- **Local file access:** none.
- **Shell execution:** none.

See [security.md](security.md) for the full safety model and [tools.md](tools.md) for the per-tool capability matrix.
