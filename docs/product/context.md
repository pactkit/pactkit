# Project Context (Auto-generated)
> Last updated: 2026-02-13T23:30:00+08:00 by /project-done

## Sprint Status
- **Backlog**: 0 stories
- **In Progress**: 0 stories
- **Done**: 11 stories (STORY-001 through STORY-004, STORY-007 through STORY-013)

## Recent Completions
- STORY-013: Draw.io MCP Integration — pactkit-draw 接入官方 @drawio/mcp 实现即时预览
- STORY-012: Docs Sync — 同步文档站和 GitHub 元数据至 PDCA Slim 架构
- STORY-011: PDCA Slim — 辅助命令降级为 Skill，精简用户界面 (14→8 commands, 3→9 skills)

## Active Branches
None

## Key Decisions
| Date | Lesson | Context |
|------|--------|---------|
| 2026-02 | Integrating an external MCP server is a prompt-only change — conditional instructions to rules, skills, agents, and workflows; the IF tool available pattern is proven across 6 MCP integrations | STORY-013 |
| 2026-02 | Multi-repo docs sync is cheap via gh CLI + git clone/push — but tests reading deployed files can hide regressions until redeployment | STORY-012 |
| 2026-02 | Demoting commands to skills is a prompt-only refactor — but updating 25+ test files with hardcoded counts is the real cost; prefer data-driven assertions | STORY-011 |
| 2025-02 | Release prep is a good time to catch stale numbers in docs — embed counts as tests to prevent future drift | STORY-010 |
| 2025-02 | Auto-merge new components via separate function (not load_config) preserves existing contract | STORY-009 |

## Next Recommended Action
`/project-design` or `/project-plan` — board is empty, ready for next iteration.
