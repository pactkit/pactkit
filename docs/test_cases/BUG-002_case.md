# Test Cases: BUG-002 — Plugin Mode Deploys Hardcoded Paths

## TC-1: Classic deployment preserves ~/.claude/skills/ paths

**Given** PactKit is deployed via `pactkit init -t /tmp/test`
**When** reading deployed SKILL.md and command files
**Then** all script paths use `~/.claude/skills/` prefix

## TC-2: Plugin deployment uses ${CLAUDE_PLUGIN_ROOT}/skills/ paths

**Given** PactKit is deployed via `pactkit init --format plugin -t /tmp/test`
**When** reading deployed SKILL.md files
**Then** all script paths use `${CLAUDE_PLUGIN_ROOT}/skills/` prefix
**And** zero occurrences of `~/.claude/skills/` in any deployed file

## TC-3: Plugin commands use ${CLAUDE_PLUGIN_ROOT}/skills/ paths

**Given** PactKit is deployed via `pactkit init --format plugin -t /tmp/test`
**When** reading deployed command playbooks
**Then** all `python3 ` script invocations use `${CLAUDE_PLUGIN_ROOT}/skills/` prefix

## TC-4: Marketplace inherits plugin path behavior

**Given** PactKit is deployed via `pactkit init --format marketplace -t /tmp/test`
**When** reading deployed plugin subdirectory SKILL.md files
**Then** paths use `${CLAUDE_PLUGIN_ROOT}/skills/` (same as plugin mode)

## TC-5: Regression — existing tests pass

**Given** the fix is applied
**When** running `pytest tests/ -q`
**Then** all pre-existing tests pass with 0 failures
