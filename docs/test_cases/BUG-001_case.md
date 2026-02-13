# Test Cases: BUG-001 — Scripted Skill Prompts Use Wrong Script Path

## TC-1: Visualize skill prompt contains base directory instruction

**Given** the `SKILL_VISUALIZE_MD` template in `src/pactkit/prompts/skills.py`
**When** inspecting the prompt text
**Then** it MUST NOT contain bare `scripts/visualize.py` without a base directory reference
**And** it MUST contain an instruction to use the skill base directory for path resolution

## TC-2: Board skill prompt contains base directory instruction

**Given** the `SKILL_BOARD_MD` template in `src/pactkit/prompts/skills.py`
**When** inspecting the prompt text
**Then** it MUST NOT contain bare `scripts/board.py` without a base directory reference
**And** it MUST contain an instruction to use the skill base directory for path resolution

## TC-3: Scaffold skill prompt contains base directory instruction

**Given** the `SKILL_SCAFFOLD_MD` template in `src/pactkit/prompts/skills.py`
**When** inspecting the prompt text
**Then** it MUST NOT contain bare `scripts/scaffold.py` without a base directory reference
**And** it MUST contain an instruction to use the skill base directory for path resolution

## TC-4: Deployed SKILL.md matches template

**Given** PactKit is deployed via `pactkit init -t /tmp/bug001-verify`
**When** reading `skills/pactkit-visualize/SKILL.md`
**Then** the content matches `SKILL_VISUALIZE_MD` and contains the base directory instruction

## TC-5: Existing tests remain passing

**Given** the fix is applied to `src/pactkit/prompts/skills.py`
**When** running `pytest tests/ -q`
**Then** all pre-existing tests pass with 0 failures
