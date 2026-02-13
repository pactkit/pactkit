# Project Context (Auto-generated)
> Last updated: 2026-02-14T00:30:00+08:00 by /project-done

## Sprint Status
- **Backlog**: 0 stories
- **In Progress**: 0 stories
- **Done**: 12 stories (STORY-001 through STORY-004, STORY-007 through STORY-013, BUG-001)

## Recent Completions
- BUG-001: Scripted Skill Prompts Use Wrong Script Path — fixed absolute paths in SKILL.md templates
- STORY-013: Draw.io MCP Integration — pactkit-draw instant preview via @drawio/mcp
- STORY-012: Docs Sync — website and GitHub metadata aligned to PDCA Slim architecture

## Active Branches
None

## Key Decisions
| Date | Lesson | Context |
|------|--------|---------|
| 2026-02 | Skill SKILL.md prompts must use absolute paths for script invocations — the LLM runs bash from project cwd, not the skill base directory | BUG-001 |
| 2026-02 | Integrating an external MCP server is a prompt-only change — the IF tool available pattern is proven across 6 MCP integrations | STORY-013 |
| 2026-02 | Multi-repo docs sync is cheap via gh CLI + git clone/push — but tests reading deployed files can hide regressions until redeployment | STORY-012 |
| 2026-02 | Demoting commands to skills is a prompt-only refactor — but updating 25+ test files with hardcoded counts is the real cost; prefer data-driven assertions | STORY-011 |
| 2025-02 | Release prep is a good time to catch stale numbers in docs — embed counts as tests to prevent future drift | STORY-010 |

## Next Recommended Action
`/project-design` or `/project-plan` — board is empty, ready for next iteration.
