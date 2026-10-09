# Atlas MCP — Cursor

Connect Atlas to the Cursor IDE.

## 1. Get your access key

Sign in at https://www.mind-vest.io/atlas, open the **Dashboard**, and copy the key under **Profile → API / CLI / MCP Key**.

## 2. Edit Cursor's MCP config

Cursor reads MCP server configs from `~/.cursor/mcp.json` (user-scope) or `<project>/.cursor/mcp.json` (project-scope).

```json
{
  "mcpServers": {
    "atlas": {
      "url": "https://atlasmcp.finmanagerai.com/mcp",
      "headers": {
        "Authorization": "Bearer YOUR_ATLAS_ACCESS_KEY"
      }
    }
  }
}
```

Cursor auto-detects HTTP transport from the `url` field; no `type` needed.

## 3. Restart Cursor

**Settings → MCP** should show `atlas` with a green status dot. Click it to see the discovered tools.

## 4. Test prompt

In Composer (Cmd/Ctrl-I):

> "Use Atlas to compare NVDA and AMD: quote, top-volume options today, and analyst price targets."

## Required env / inputs

| Name | Required | Notes |
|---|---|---|
| `Authorization` header | yes | `Bearer YOUR_ATLAS_ACCESS_KEY`, inline in config |

## Troubleshooting

- **`atlas` shows red in Settings → MCP.** Hover for the error message. Most common: bad JSON, wrong URL, or `Bearer` typo.
- **Tool calls succeed but show no output.** Cursor sometimes truncates large JSON. Ask the model to summarize rather than dump the raw payload.
- **`401`.** The key is wrong or was replaced. Copy it again from the dashboard.
- **"Your plan's requests are used up."** `Subscription-Status` shows what is left this month.

## Capabilities & permissions

- Same as every other client: server-side reads + (with explicit approval) writes for orders, triggers, and workflows. No local FS or shell access.

See [security.md](security.md) and [tools.md](tools.md).
