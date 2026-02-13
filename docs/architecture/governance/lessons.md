# Lessons Learned

| Date | Lesson | Context |
|------|--------|---------|
| 2025-01 | Brand rename (ScafPy -> PactKit) touched 306 references — automate with `replace_all` | Migration |
| 2025-02 | Selective deployment needs cleanup of stale files when config changes | STORY-002 |
| 2025-02 | `pactkit.yaml` must be generated on first `init` with sensible defaults | STORY-001 |
| 2025-02 | Cross-session value comes from persistent artifacts (context.md, lessons.md), not from more rules — prompt changes are the cheapest high-impact mechanism | STORY-006 |
| 2025-02 | Adding a new command touches 3 files (config.py, commands.py, rules.py) plus count assertions in existing tests — keep count tests data-driven to reduce churn | STORY-007 |
| 2025-02 | Removing rules that overlap with LLM native behavior (55% token reduction) improves signal-to-noise — fewer rules = higher compliance on the ones that matter | STORY-008 |
| 2025-02 | Auto-merge new components via separate function (not load_config) preserves existing contract — exclude section in yaml handles user opt-out without version diffing | STORY-009 |
| 2025-02 | Release prep is a good time to catch stale numbers in docs — embed counts as tests to prevent future drift | STORY-010 |
| 2026-02 | Demoting commands to skills is a prompt-only refactor (no Python scripts needed for prompt-only skills) — but updating 25+ test files with hardcoded counts is the real cost; prefer data-driven assertions | STORY-011 |
| 2026-02 | Multi-repo docs sync is cheap via gh CLI + git clone/push — but tests reading deployed files (not source) can hide regressions until redeployment | STORY-012 |
