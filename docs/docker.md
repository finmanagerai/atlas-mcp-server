# Atlas MCP — Docker (stdio bridge)

For MCP clients that **only speak stdio** (don't yet support `streamable-http`), run a small Docker container that bridges stdio ↔ Atlas's remote HTTP endpoint via [`mcp-proxy`](https://github.com/sparfenyuk/mcp-proxy).

You don't need this for Claude Desktop, Claude Code, Cursor, or recent Windsurf builds — those speak streamable-HTTP natively.

## 1. Get your access key

Sign in at https://www.mind-vest.io/atlas, open the **Dashboard**, and copy the key under **Profile → API / CLI / MCP Key**.

## 2. Pull the bridge image

```bash
docker pull ghcr.io/sparfenyuk/mcp-proxy:latest
```

(Or build from source — see the `mcp-proxy` repo.)

## 3. Wire it into your client's config

```json
{
  "mcpServers": {
    "atlas": {
      "command": "docker",
      "args": [
        "run", "--rm", "-i",
        "-e", "ATLAS_API_KEY",
        "ghcr.io/sparfenyuk/mcp-proxy:latest",
        "--transport", "streamablehttp",
        "--headers", "Authorization", "Bearer ${ATLAS_API_KEY}",
        "https://atlasmcp.finmanagerai.com/mcp"
      ],
      "env": {
        "ATLAS_API_KEY": "YOUR_ATLAS_ACCESS_KEY"
      }
    }
  }
}
```

The client launches the container per session, the container speaks stdio to the client and HTTPS to Atlas.

## 4. Test it from a shell first

```bash
docker run --rm -i \
  ghcr.io/sparfenyuk/mcp-proxy:latest \
  --transport streamablehttp \
  --headers Authorization "Bearer YOUR_ATLAS_ACCESS_KEY" \
  https://atlasmcp.finmanagerai.com/mcp <<'EOF'
{"jsonrpc":"2.0","id":1,"method":"tools/list"}
EOF
```

You should see a JSON-RPC response listing all Atlas tools.

## Required env / inputs

| Name | Required | Notes |
|---|---|---|
| `ATLAS_API_KEY` | yes | Passed into the container as an env var; injected into the `Authorization` header |
| Docker | yes | `docker --version` ≥ 20.10 |
| Outbound 443 | yes | Container must reach `atlasmcp.finmanagerai.com` |

## Troubleshooting

- **`docker: command not found`.** Install Docker Desktop or your distro's `docker` package.
- **Bridge connects but no tools listed.** The bridge launched but the upstream returned an error — check `ATLAS_API_KEY`. Re-run the shell test above and inspect the response.
- **Slow first response.** The image pull happens on first use. Pre-pull or warm with `docker pull`.
- **`401`/`403`.** Bad key. Regenerate.
- **A tool says your plan's requests are used up.** `Subscription-Status` shows what is left this month.

## Capabilities & permissions

- Container is a transparent proxy — same Atlas capabilities, same safety model. No local FS access (we don't bind-mount anything), no shell access from Atlas's side.
- The container has outbound network only; it doesn't accept inbound connections.

See [security.md](security.md).
