# Project Context (Auto-generated)
> Last updated: 2026-02-14T01:30:00+08:00 by /project-done

## Sprint Status
- **Backlog**: 0 stories
- **In Progress**: 0 stories
- **Done**: 13 stories (STORY-001 through STORY-004, STORY-007 through STORY-013, BUG-001, BUG-002)

## Recent Completions
- BUG-002: Plugin Mode Deploys Hardcoded Paths — deploy-time path rewriting for plugin/marketplace modes
- BUG-001: Scripted Skill Prompts Use Wrong Script Path — fixed absolute paths in SKILL.md templates
- STORY-013: Draw.io MCP Integration — pactkit-draw instant preview via @drawio/mcp

## Active Branches
None

## Key Decisions
| Date | Lesson | Context |
|------|--------|---------|
| 2026-02 | Deploy-time path rewriting (template stays canonical, deployer rewrites at write time) is the correct pattern for multi-mode deployment | BUG-002 |
| 2026-02 | Skill SKILL.md prompts must use absolute paths for script invocations — the LLM runs bash from project cwd, not the skill base directory | BUG-001 |
| 2026-02 | Integrating an external MCP server is a prompt-only change — the IF tool available pattern is proven across 6 MCP integrations | STORY-013 |
| 2026-02 | Multi-repo docs sync is cheap via gh CLI + git clone/push — but tests reading deployed files can hide regressions until redeployment | STORY-012 |
| 2026-02 | Demoting commands to skills is a prompt-only refactor — but updating 25+ test files with hardcoded counts is the real cost; prefer data-driven assertions | STORY-011 |

## Next Recommended Action
Board is empty. Run `/project-design` to define new product features.
