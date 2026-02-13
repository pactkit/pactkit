# PactKit

[![PyPI version](https://img.shields.io/pypi/v/pactkit)](https://pypi.org/project/pactkit/)
[![Downloads](https://img.shields.io/pypi/dm/pactkit)](https://pypi.org/project/pactkit/)
[![Python](https://img.shields.io/pypi/pyversions/pactkit)](https://pypi.org/project/pactkit/)
[![CI](https://github.com/pactkit/pactkit/actions/workflows/ci.yml/badge.svg)](https://github.com/pactkit/pactkit/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

**Ship features with AI agents that follow specs, not vibes.**

> PactKit gives Claude Code a structured operating system — 9 specialized agents, 13 commands, and a full Plan-Act-Check-Done lifecycle. One `pip install` and your AI assistant writes specs before code, runs TDD, and never commits without passing tests.

### What it looks like

```
You:  /project-sprint "Add OAuth2 login"

 Plan   System Architect scans codebase, writes Spec, updates Board
 Act    Senior Developer writes tests first (RED), then code (GREEN)
 Check  QA Engineer runs 6-phase audit (security + quality + spec alignment)
 Done   Repo Maintainer gates regression, archives story, commits
```

## Why PactKit?

AI coding assistants are powerful but unpredictable without structure. PactKit adds a **spec-driven governance layer**:

- **Spec is the Law** — Specifications are the single source of truth (Spec > Tests > Code)
- **Multi-Agent Ensemble** — 9 specialized agents collaborate, each with defined roles
- **Full PDCA Lifecycle** — Plan → Act → Check → Done, with quality gates at every stage
- **Safe by Design** — TDD-first development, safe regression testing, pre-existing test protection

## Installation

```bash
pip install pactkit
```

Requires Python 3.10+ and [Claude Code](https://docs.anthropic.com/en/docs/claude-code).

## Quick Start

```bash
# Deploy full toolkit (13 commands + 9 agents + 3 skills)
pactkit init

# Update to latest playbooks (preserves your config)
pactkit update

# Check installed version
pactkit version
```

Then in any project with Claude Code:

```bash
# Plan — Analyze requirements, create Spec
/project-plan "Add user authentication"

# Act — Implement with strict TDD
/project-act STORY-001

# Check — Security scan + quality audit (P0-P3 severity)
/project-check

# Done — Safe regression gate + conventional commit
/project-done
```

Or run the full cycle in one command:

```bash
/project-sprint "Add user authentication"
```

## PDCA+ Workflow

| Phase | Command | Agent | What Happens |
|-------|---------|-------|-------------|
| **Plan** | `/project-plan` | System Architect | Codebase scan → Spec generation → Board entry |
| **Act** | `/project-act` | Senior Developer | Visual scan → TDD loop → Regression check |
| **Check** | `/project-check` | QA + Security | 6-phase deep audit (Security/Quality/Spec alignment) |
| **Done** | `/project-done` | Repo Maintainer | Safe regression gate → Archive → Conventional commit |
| **Trace** | `/project-trace` | Code Explorer | Call graph tracing → Sequence diagram |
| **Draw** | `/project-draw` | Visual Architect | Generate Draw.io XML architecture diagrams |
| **Doctor** | `/project-doctor` | System Medic | Configuration drift detection → Health report |
| **Review** | `/project-review` | QA Engineer | PR review with SOLID/Security/Quality checklists |
| **Sprint** | `/project-sprint` | Team Lead | One-command automated PDCA orchestration |
| **Hotfix** | `/project-hotfix` | Senior Developer | Fast-track fix bypassing PDCA (with traceability) |
| **Release** | `/project-release` | Repo Maintainer | Version bump → Archive → Git tag → Changelog |
| **Design** | `/project-design` | Product Designer | PRD generation → Story decomposition → Board setup |

## Agent Ensemble

PactKit deploys 9 specialized agents, each with constrained tools and focused responsibilities:

| Agent | Role | Core Capability |
|-------|------|----------------|
| System Architect | Architecture design | Maintain Intent Graph, write Specs |
| Senior Developer | Full-stack development | TDD loop, call chain analysis, hotfix |
| QA Engineer | Quality gates | Deep check (P0-P3), PR review |
| Security Auditor | Security audit | OWASP scanning, threat modeling |
| Repo Maintainer | Repository ops | Cleanup, archiving, Git conventions, releases |
| System Medic | System diagnostics | Configuration drift repair |
| Visual Architect | Architecture visualization | Draw.io XML generation |
| Code Explorer | Code tracing | Call graph + sequence diagram |
| Product Designer | Product design | PRD, story decomposition, board init |

## Skills

Three atomic skills are deployed as standalone scripts:

- **pactkit-visualize** — Code dependency graph (Mermaid): file-level, class-level, call-level
- **pactkit-board** — Sprint board operations: add story, update task, archive
- **pactkit-scaffold** — File scaffolding: create spec, test files, git branches, skills

## Safe Regression

PactKit's safe regression system prevents agents from blindly modifying pre-existing tests:

- **TDD Loop** — Only iterates on tests created in the current story
- **Regression Check** — Read-only gate; pre-existing test failure = STOP and report
- **Done Gate** — Full regression by default; incremental only when ALL safety conditions are met

## Hierarchy of Truth

```
Tier 1: Specs (docs/specs/*.md)     — The Law
Tier 2: Tests                        — The Verification
Tier 3: Implementation               — The Mutable Reality
```

When conflicts arise: Spec wins. Always.

## Configuration

PactKit deploys to `~/.claude/`:

```
~/.claude/
├── CLAUDE.md                 ← Modular constitution (entry point)
├── rules/                    ← 6 rule modules
├── commands/                 ← 13 command playbooks
├── agents/                   ← 9 agent definitions
└── skills/                   ← 3 skill packages
    ├── pactkit-visualize/
    ├── pactkit-board/
    └── pactkit-scaffold/
```

## MCP Integration

PactKit conditionally integrates with MCP servers when available:

| MCP Server | Purpose | PDCA Phase |
|------------|---------|------------|
| Context7 | Library documentation lookup | Act |
| shadcn | UI component search/install | Design |
| Playwright | Browser automation testing | Check |
| Chrome DevTools | Performance/console/network | Check |
| Memory | Cross-session knowledge graph | Plan/Act/Done |

All MCP instructions are conditional — gracefully skipped when unavailable.

## Upgrading

```bash
pip install --upgrade pactkit
pactkit update
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

[MIT](LICENSE)
