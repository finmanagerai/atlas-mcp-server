# Atlas MCP — OpenAI Codex CLI

Connect Atlas to the [`codex`](https://github.com/openai/codex) CLI. Codex configures MCP servers in TOML.

> Codex's MCP schema has shifted across builds. The block below targets recent versions that support remote streamable-HTTP servers. If your build only accepts stdio servers (older Codex), use the [Docker stdio bridge](docker.md) instead.

## 1. Get your access key

Sign in at https://www.mind-vest.io/atlas, open the **Dashboard**, and copy the key under **Profile → API / CLI / MCP Key**.

## 2. Edit `~/.codex/config.toml`

Add an `[mcp_servers.atlas]` block:

```toml
[mcp_servers.atlas]
type = "streamable-http"
url  = "https://atlasmcp.finmanagerai.com/mcp"

[mcp_servers.atlas.headers]
Authorization = "Bearer YOUR_ATLAS_ACCESS_KEY"
```

If your Codex build expects a different key (e.g. `transport` instead of `type`, or wants the auth as an env var), `codex --help` and `codex mcp --help` will show the current field names — the URL and bearer header don't change.

### Stdio fallback (older Codex)

```toml
[mcp_servers.atlas]
command = "docker"
args = [
  "run", "--rm", "-i",
  "-e", "ATLAS_API_KEY",
  "ghcr.io/sparfenyuk/mcp-proxy:latest",
  "--transport", "streamablehttp",
  "--headers", "Authorization", "Bearer ${ATLAS_API_KEY}",
  "https://atlasmcp.finmanagerai.com/mcp",
]

[mcp_servers.atlas.env]
ATLAS_API_KEY = "YOUR_ATLAS_ACCESS_KEY"
```

## 3. Verify

```bash
codex mcp list
```

`atlas` should show up with status `connected` and its tool count.

## 4. Test prompt

```bash
codex "Use Atlas to fetch a quote for SPY and the next 5 option expirations."
```

Expect `Stock-Quote` and `Option-Expiration-Dates` calls.

## Required env / inputs

| Name | Required | Notes |
|---|---|---|
| `Authorization` header | yes | Inline in TOML, or via `${ATLAS_API_KEY}` if you prefer keeping secrets in env |
| `ATLAS_API_KEY` (stdio fallback only) | yes | Read by the `mcp-proxy` container |

## Troubleshooting

- **`codex mcp list` doesn't show `atlas`.** Check TOML syntax (`codex` is strict about quoting). Run `python3 -c 'import tomllib; tomllib.load(open("/path/to/config.toml","rb"))'` to validate.
- **"Unknown transport" / "Unsupported config".** Your Codex build pre-dates remote-HTTP MCP support — use the stdio fallback above.
- **`401`/`403`.** Bad key. Regenerate.
- **A tool says your plan's requests are used up.** `Subscription-Status` shows what is left this month.

## Capabilities & permissions

Same as every Atlas client: server-side reads + opt-in writes for orders, triggers, workflows. No local FS access, no shell execution from Atlas's side. See [security.md](security.md) and [tools.md](tools.md).
