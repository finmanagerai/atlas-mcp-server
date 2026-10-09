# Atlas MCP — OpenClaw

Connect Atlas to OpenClaw.

> OpenClaw configuration paths and command names vary by build. The instructions below use the conventional MCP layout — adjust the file path to match your install if needed.

## 1. Get your access key

Sign in at https://www.mind-vest.io/atlas, open the **Dashboard**, and copy the key under **Profile → API / CLI / MCP Key**.

## 2. Edit your OpenClaw MCP config

Add `atlas` under `mcpServers`:

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

Common config locations:

- macOS / Linux: `~/.openclaw/config.json` or `~/.config/openclaw/config.json`
- Windows: `%APPDATA%\openclaw\config.json`

## 3. Reload / restart OpenClaw

Once restarted, OpenClaw should list the Atlas tools in its tool palette.

## 4. Test prompt

> "Atlas: top-volume QQQ options today, then preview a 1-contract long call at the highest-volume strike — do NOT submit."

Expect a `Top-Volume-and-OI-Contracts` call followed by a `Preview-Order` (no `Place-Order`).

## Required env / inputs

| Name | Required | Notes |
|---|---|---|
| `Authorization` header | yes | Inline in config |

## Troubleshooting

- **No tools listed.** OpenClaw build may only support stdio servers — switch to the [Docker stdio bridge](docker.md).
- **Auth header stripped.** A few proxies eat custom headers; verify with `curl -H "Authorization: Bearer YOUR_KEY" https://atlasmcp.finmanagerai.com/mcp` and confirm you don't get `401`.
- **`401`.** The key is wrong or was replaced. Copy it again from the dashboard.

## Capabilities & permissions

Same as every Atlas client: server-side read + opt-in writes for orders, triggers, workflows. No local FS, no shell.

See [security.md](security.md) and [tools.md](tools.md).
