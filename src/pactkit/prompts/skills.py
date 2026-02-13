from pactkit.skills import load_script, _SHARED_HEADER

# ==============================================================================
# SKILL SOURCE CODE (loaded from pactkit/skills/)
# ==============================================================================

VISUALIZE_SOURCE = load_script('visualize.py')
BOARD_SOURCE = load_script('board.py')
SCAFFOLD_SOURCE = load_script('scaffold.py')

# --- Backward-compatible combined source (for old tests) ---
TOOLS_SOURCE = VISUALIZE_SOURCE + "\n" + BOARD_SOURCE + "\n" + SCAFFOLD_SOURCE
TOOLS_CONTENT = TOOLS_SOURCE.split('\n')

# ==============================================================================
# SKILL.md TEMPLATES (Frontmatter + Documentation)
# ==============================================================================
SKILL_VISUALIZE_MD = """---
name: pactkit-visualize
description: "Generate project code dependency graph (Mermaid), supporting file-level, class-level, and function-level call chain analysis"
---

# PactKit Visualize

Generate project code relationship graphs (Mermaid format), supporting three analysis modes.

## Prerequisites
- The project must have Python source files (`.py`) to generate meaningful graphs
- The `docs/architecture/graphs/` directory is automatically created by `init_arch`

## Command Reference

### visualize -- Generate code dependency graph
```
python3 scripts/visualize.py visualize [--mode file|class|call] [--entry <func>] [--focus <module>]
```

| Parameter | Description | Default |
|-----------|-------------|---------|
| `--mode file` | File-level dependency graph (inter-module import relationships) | Default |
| `--mode class` | Class diagram (including inheritance) | - |
| `--mode call` | Function-level call graph | - |
| `--entry <func>` | BFS transitive chain tracing from specified function (requires `--mode call`) | - |
| `--focus <module>` | Focus on call relationships of specified module (requires `--mode call`) | - |

### init_arch -- Initialize architecture directory
```
python3 scripts/visualize.py init_arch
```
- Creates `docs/architecture/graphs/` and `docs/architecture/governance/`
- Generates placeholder file `system_design.mmd`

### list_rules -- List governance rules
```
python3 scripts/visualize.py list_rules
```
- Outputs the list of rule files under `docs/architecture/governance/`

## Output Files

| Mode | Output Path | Mermaid Type |
|------|-------------|-------------|
| `--mode file` | `docs/architecture/graphs/code_graph.mmd` | graph TD |
| `--mode class` | `docs/architecture/graphs/class_graph.mmd` | classDiagram |
| `--mode call` | `docs/architecture/graphs/call_graph.mmd` | graph TD |
| `--focus` | `docs/architecture/graphs/focus_graph.mmd` | graph TD |

## Usage Scenarios
- `/project-plan`: Run `visualize` to understand current project state before making design decisions
- `/project-act`: Run `visualize --focus <module>` to understand dependencies of the modification target
- `/project-doctor`: Run `visualize` to check whether architecture graphs can be generated correctly
- `/project-trace`: Run `visualize --mode call --entry <func>` to trace call chains
"""

SKILL_BOARD_MD = """---
name: pactkit-board
description: "Sprint Board atomic operations: add Story, update Task, archive completed Stories"
---

# PactKit Board

Atomic operations tool for Sprint Board (`docs/product/sprint_board.md`).

## Prerequisites
- `docs/product/sprint_board.md` must exist (created by `/project-init`)
- `docs/product/archive/` directory is used for archiving (automatically created by the archive command)

## Command Reference

### add_story -- Add a work item (Story, Hotfix, or Bug)
```
python3 scripts/board.py add_story ITEM-ID "Title" "Task A|Task B"
```
- `ITEM-ID`: Work item identifier, e.g. `STORY-001`, `HOTFIX-001`, `BUG-001`
- `Title`: Item title
- `Task A|Task B`: Task list, use `|` as separator for multiple tasks
- Output: `✅ Story ITEM-ID added` or `❌` error message

### update_task -- Update Task status
```
python3 scripts/board.py update_task ITEM-ID "Task Name"
```
- `Task Name`: Must be an exact match with the task name in the Board
- Changes `- [ ] Task Name` to `- [x] Task Name`
- Output: `✅ Task updated` or `❌ Task not found`

### archive -- Archive completed Stories
```
python3 scripts/board.py archive
```
- Moves all Stories with every task marked `[x]` to `docs/product/archive/archive_YYYYMM.md`

### list_stories -- View current Stories
```
python3 scripts/board.py list_stories
```

### update_version -- Update version number
```
python3 scripts/board.py update_version 1.0.0
```

### snapshot -- Architecture snapshot
```
python3 scripts/board.py snapshot "v1.0.0"
```
- Saves current architecture graphs to `docs/architecture/snapshots/{version}_*.mmd`

### fix_board -- Relocate misplaced stories to correct sections
```
python3 scripts/board.py fix_board
```
- Scans for stories outside their correct section and relocates them based on task status:
  - All `[ ]` → `## 📋 Backlog`
  - Mixed `[ ]`/`[x]` → `## 🔄 In Progress`
  - All `[x]` → `## ✅ Done`
- Output: `✅ Board fixed: N stories relocated.` or `✅ No misplaced stories found.`

## Usage Scenarios
- `/project-plan`: Use `add_story` to create a Story
- `/project-act`: Use `update_task` to mark completed tasks
- `/project-done`: Use `archive` to archive completed Stories
- `/project-release`: Use `update_version` + `snapshot` to publish a release
- `/project-doctor`: Use `fix_board` to repair misplaced stories
"""

SKILL_SCAFFOLD_MD = """---
name: pactkit-scaffold
description: "File scaffolding: create Spec, test files, E2E tests, Git branches, Skills"
---

# PactKit Scaffold

Project file scaffolding tool for quickly creating standardized project files.

## Prerequisites
- `docs/specs/` directory must exist (required by `create_spec`)
- `tests/unit/` and `tests/e2e/` directories must exist (required by test scaffolding)
- Git repository must be initialized (required by `git_start`)

## Command Reference

### create_spec -- Create a Spec file
```
python3 scripts/scaffold.py create_spec ITEM-ID "Title"
```
- `ITEM-ID`: Work item identifier, e.g. `STORY-001`, `HOTFIX-001`, `BUG-001`
- `Title`: Spec title
- Output: `docs/specs/{ITEM-ID}.md` (with template structure)

### create_test_file -- Create a unit test
```
python3 scripts/scaffold.py create_test_file src/module.py
```
- Automatically generates the corresponding test file based on the source file path
- Output: `tests/unit/test_module.py`

### create_e2e_test -- Create an E2E test
```
python3 scripts/scaffold.py create_e2e_test ITEM-ID "scenario_name"
```
- Output: `tests/e2e/test_{ITEM-ID}_{scenario}.py`

### git_start -- Create a Git branch
```
python3 scripts/scaffold.py git_start ITEM-ID
```
- Branch prefix is inferred from the item type:
  - `STORY-*` → `feature/STORY-*`
  - `HOTFIX-*` → `fix/HOTFIX-*`
  - `BUG-*` → `fix/BUG-*`

### create_skill -- Create a Skill directory scaffold
```
python3 scripts/scaffold.py create_skill skill-name "Description of the skill"
```
- `skill-name`: Skill identifier (must start with lowercase letter: `^[a-z][a-z0-9]*(-[a-z0-9]+)*$`)
- `Description`: Brief description for SKILL.md frontmatter
- Output: `~/.claude/skills/{skill-name}/` with `SKILL.md`, `scripts/{clean_name}.py`, `references/.gitkeep`
- Refuses to overwrite if the skill directory already exists

## Usage Scenarios
- `/project-plan`: Use `create_spec` to create a Spec template
- `/project-act`: Use `create_test_file` to create test scaffolding
- `/project-check`: Use `create_e2e_test` to create E2E tests
- Ad-hoc: Use `create_skill` to scaffold a new reusable skill
"""

