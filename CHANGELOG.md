# Changelog

All notable changes to the public Atlas MCP registry artifacts in this repository. The hosted server itself is versioned separately at https://atlasmcp.finmanagerai.com.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Plugin 1.1.0 — 2026-10-09

### Added
- `atlas-agent-run-workflows`: a workflow your own assistant runs. It registers the workflow, asks Atlas what runs are waiting, and hands in what it decided; Atlas checks it, holds it for review or places it, sends it to followers and logs it. With a step-by-step account of what Atlas does with a run.
- `atlas-triggers-and-trades` covers linked trades: either/or pairs and one-starts-the-other, with templates.

### Changed
- `docs/tools.md`: 160 tools. The marketplace tools and two collaborator tools are gone; three were added for workflows an assistant runs.

## Plugin 1.0.3 — 2026-10-09

### Changed
- The short description is "Automate finance and investing".

## Plugin 1.0.2 — 2026-10-09

### Changed
- The short description is "Finance, investing workflows".

## Plugin 1.0.1 — 2026-10-09

### Changed
- The plugin's listing: the short description is "Investing, trading workflows", and the category is written the way OpenAI's dashboard lists it (`finance`).

## [1.1.0] — 2026-10-09

### Changed
- What Atlas is, said plainly everywhere: tools for AI agents to scan options flow, analyze real-time stock market data, and build investing and trading workflows that Atlas carries out in your own broker account. The registry description, the readme and the install skill were written when Atlas was mostly market data.
- `docs/tools.md` is now written from the live server (157 tools; it listed 85, several under names that no longer exist) and marks each tool as reads, adds, changes or acts.
- Signing in through the browser comes first on every install page. The access key is for clients that cannot open a sign-in page, and the pages say where it actually is (Profile, API / CLI / MCP Key).
- Removed claims that were not true: alerts by SMS and Telegram, and fixed request limits.

### Added
- `plugin/`: the MindVest Atlas plugin. The server plus six skills (`atlas-get-started`, `atlas-market-data`, `atlas-workflows`, `atlas-alerts`, `atlas-signals`, `atlas-triggers-and-trades`) that say what is possible, list every field, and carry templates. The field lists under each skill's `references/` are written from the live server.
- `scripts/build-plugin.py`: builds the archives to upload. `mindvest-atlas-chatgpt.zip` for ChatGPT and Codex, `mindvest-atlas-claude-code.zip` for Claude Code, and one zip per skill for Claude's skill upload. Each release carries them.
- `.claude-plugin/marketplace.json`, so Claude Code can install the plugin from this repository.

## [1.0.1] — docs

### Added
- Per-client install recipes under `docs/`: Claude Desktop, Claude Code, Cursor, Windsurf, OpenAI Codex CLI, OpenClaw, Docker stdio bridge.
- `SKILL.md` so AI agents can install and use Atlas MCP end-to-end.
- Reference docs: `docs/tools.md` (catalog with read/write classification), `docs/security.md` (auth, rate limits, permissions), `docs/examples.md` (prompt → tool mapping), `docs/ci.md` (smoke-test pattern).
- `examples/mcp.json` and `examples/smoke-test.sh`.

## [1.0.0] — initial registry submission

### Added
- `server.json` — registry manifest pointing to the hosted Atlas MCP endpoint at `https://atlasmcp.finmanagerai.com/mcp` (streamable-HTTP, Bearer auth).
- `.github/workflows/publish.yml` — tag-driven publish via `mcp-publisher` + GitHub OIDC.
- `README.md` — install + capability overview.
- `.gitignore` — ignore `mcp-publisher` local auth state.
