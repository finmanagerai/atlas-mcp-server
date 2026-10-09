# Atlas MCP — CI Tests

A minimal smoke test you can drop into your own CI to confirm the Atlas MCP endpoint is reachable, your API key is valid, and `tools/list` returns a non-empty catalog.

## Shell smoke test

The example script lives at [`examples/smoke-test.sh`](../examples/smoke-test.sh). It does three things:

1. Sends a JSON-RPC `tools/list` request via `curl`.
2. Asserts the response status is `200` and the body contains at least one tool.
3. Optionally calls `Stock-Quote` on `SPY` and checks for a non-empty `price`.

```bash
ATLAS_API_KEY=xxxxx ./examples/smoke-test.sh
```

Exit code `0` = healthy, non-zero = failed (with a diagnostic on stderr).

## GitHub Actions

```yaml
name: atlas-smoke

on:
  schedule:
    - cron: "*/30 * * * *"   # every 30 min
  workflow_dispatch:

jobs:
  smoke:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Smoke test
        env:
          ATLAS_API_KEY: ${{ secrets.ATLAS_API_KEY }}
        run: ./examples/smoke-test.sh
```

Add `ATLAS_API_KEY` as a repository secret (use a key from a dedicated CI account, not your personal dashboard key).

## What it covers

- ✅ DNS + TLS to `atlasmcp.finmanagerai.com`
- ✅ Bearer auth path (`401` if the key is bad)
- ✅ Server returns a tool catalog (`tools/list`)
- ✅ A real read-only tool call succeeds
- ❌ Order placement — intentionally not exercised; we never want CI placing live trades.

## Caveats

- The quote this test asks for uses one request of the account's plan each time it runs. Schedule it with that in mind; `Subscription-Status` shows what is left.
- The script does not test workflow / trigger writes. If you want those covered, add a "create → preview → delete" round-trip and gate it behind a `CI_FULL=1` env var.
