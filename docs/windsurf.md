# Atlas MCP — Windsurf (Codeium)

Connect Atlas to the Windsurf IDE.

## 1. Get your access key

Sign in at https://www.mind-vest.io/atlas, open the **Dashboard**, and copy the key under **Profile → API / CLI / MCP Key**.

## 2. Edit Windsurf's MCP config

Windsurf reads `~/.codeium/windsurf/mcp_config.json`.

```json
{
  "mcpServers": {
    "atlas": {
      "serverUrl": "https://atlasmcp.finmanagerai.com/mcp",
      "headers": {
        "Authorization": "Bearer YOUR_ATLAS_ACCESS_KEY"
      }
    }
  }
}
```

> Windsurf uses `serverUrl` (not `url`) for remote HTTP MCP servers. Older Windsurf builds only accepted stdio servers — if your build doesn't show the `serverUrl` option, update to the latest, or use the [Docker stdio bridge](docker.md).

## 3. Reload Windsurf

**Cascade panel → MCP servers → Refresh** (or fully restart). `atlas` should appear with its tools listed.

## 4. Test prompt

In Cascade:

> "Atlas: pull SPY's options chain for the next expiration and show me the highest-gamma strikes."

## Required env / inputs

| Name | Required | Notes |
|---|---|---|
| `Authorization` header | yes | Inline in config |

## Troubleshooting

- **`atlas` not showing up.** Confirm config path; some Windsurf builds also read from `~/.windsurf/mcp_config.json`. Try both.
- **"Tool call timed out".** Streaming responses can exceed Windsurf's default tool timeout for big options chains. Ask for fewer expirations or a single strike range.
- **`401`.** The key is wrong or was replaced. Copy it again from the dashboard.

## Capabilities & permissions

- Server-side data only; no local FS, no shell. Mutating tools (`Place-Order`, `Workflow-Run`, trigger CRUD) need explicit user confirmation in chat.

See [security.md](security.md).
