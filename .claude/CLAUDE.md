# PactKit — Project Context

## What is PactKit?

PactKit is a spec-driven agentic DevOps toolkit for AI coding assistants. It compiles development workflows, role definitions, and behavioral rules into executable "constitutions" and "playbooks" for Claude Code.

- **Name origin**: Pact (契约) + Kit — "Code by Contract"
- **Domain**: pactkit.dev
- **GitHub Org**: https://github.com/pactkit
- **PyPI**: https://pypi.org/project/pactkit/
- **License**: MIT

## Project Status

846 tests passing. Published on PyPI and GitHub.

### Distribution Modes

| Mode | Command | Output |
|------|---------|--------|
| Classic (pip) | `pactkit init` | Deploys to `~/.claude/` with `pactkit.yaml` filtering |
| Plugin | `pactkit init --format plugin` | Self-contained `.claude-plugin/` directory |
| Marketplace | `pactkit init --format marketplace` | Plugin + `marketplace.json` for GitHub repo |

Marketplace repo: https://github.com/pactkit/claude-code-plugin

### Cross-Session Memory

PactKit generates `docs/product/context.md` (via Done/Plan/Init commands) which CLAUDE.md auto-loads via `@./docs/product/context.md`. This gives new sessions automatic awareness of sprint status, recent completions, and recommended next actions.

## Architecture

```
src/pactkit/
├── cli.py              ← CLI entry: pactkit init/update/version (--format classic|plugin|marketplace)
├── config.py           ← pactkit.yaml load/validate/generate
├── utils.py            ← atomic_write() utility
├── scripts.py          ← Legacy script templates
├── generators/
│   └── deployer.py     ← Core deployment orchestrator (classic/plugin/marketplace)
├── prompts/            ← All prompt templates and constants
│   ├── agents.py       ← 9 agent definitions
│   ├── commands.py     ← 13 command playbooks
│   ├── references.py   ← Reference checklists (SOLID/Security/Quality)
│   ├── rules.py        ← 6 constitution rule modules + CLAUDE_MD_TEMPLATE
│   ├── skills.py       ← 3 skill definitions
│   └── workflows.py    ← PDCA workflow prompts + LANG_PROFILES
└── skills/             ← Skill script source files
    ├── board.py        ← Sprint board operations
    ├── scaffold.py     ← File scaffolding
    └── visualize.py    ← Code dependency graph (Mermaid)
```

## Dev Commands

```bash
# Run tests
pytest tests/ -v

# Lint
ruff check src/ tests/

# Install in dev mode
pip install -e .

# Test CLI
pactkit version
pactkit init -t /tmp/preview
pactkit init --format plugin -t /tmp/plugin-preview
```
