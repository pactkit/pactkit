import sys
from pathlib import Path

# 确保能 import pactkit.prompts
current_dir = Path(__file__).resolve().parent
project_root = current_dir.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from pactkit import prompts
from pactkit.config import (
    VALID_AGENTS,
    VALID_COMMANDS,
    VALID_RULES,
    VALID_SKILLS,
    generate_default_yaml,
    get_default_config,
    load_config,
    validate_config,
)
from pactkit.skills import load_script
from pactkit.utils import atomic_write


def deploy(config=None, target=None, **_kwargs):
    """Deploy PactKit configuration.

    Args:
        config: Optional config dict. If None, loads from pactkit.yaml or defaults.
        target: Optional target directory. If None, uses ~/.claude.
    """
    # Resolve target directory
    if target is not None:
        claude_root = Path(target)
    else:
        claude_root = Path.home() / ".claude"

    # Migrate legacy scafpy remnants before anything else
    _migrate_from_scafpy(claude_root)

    # Load config if not provided
    if config is None:
        yaml_path = claude_root / "pactkit.yaml"
        config = load_config(yaml_path)

    validate_config(config)

    print("🚀 PactKit DevOps Deployment")

    # Prepare directories
    agents_dir = claude_root / "agents"
    commands_dir = claude_root / "commands"
    skills_dir = claude_root / "skills"

    for d in [claude_root, agents_dir, commands_dir, skills_dir]:
        d.mkdir(parents=True, exist_ok=True)

    # Deploy components filtered by config
    enabled_skills = config.get('skills', [])
    enabled_rules = config.get('rules', [])
    enabled_agents = config.get('agents', [])
    enabled_commands = config.get('commands', [])

    n_skills = _deploy_skills(skills_dir, enabled_skills)
    _cleanup_legacy(skills_dir)
    n_rules = _deploy_rules(claude_root, enabled_rules)
    _deploy_claude_md(claude_root, enabled_rules)
    n_agents = _deploy_agents(agents_dir, enabled_agents)
    n_commands = _deploy_commands(commands_dir, enabled_commands)

    # Generate pactkit.yaml if it doesn't exist
    _generate_config_if_missing(claude_root)

    # Summary
    total_agents = len(VALID_AGENTS)
    total_commands = len(VALID_COMMANDS)
    total_skills = len(VALID_SKILLS)
    total_rules = len(VALID_RULES)

    print(f"\n✅ Deployed: {n_agents}/{total_agents} Agents, "
          f"{n_commands}/{total_commands} Commands, "
          f"{n_skills}/{total_skills} Skills, "
          f"{n_rules}/{total_rules} Rules")


def _deploy_skills(skills_dir, enabled_skills):
    """Deploy skill directories filtered by config."""
    all_skill_defs = [
        {
            'name': 'pactkit-visualize',
            'skill_md': prompts.SKILL_VISUALIZE_MD,
            'script_name': 'visualize.py',
            'script_source': load_script('visualize.py'),
        },
        {
            'name': 'pactkit-board',
            'skill_md': prompts.SKILL_BOARD_MD,
            'script_name': 'board.py',
            'script_source': load_script('board.py'),
        },
        {
            'name': 'pactkit-scaffold',
            'skill_md': prompts.SKILL_SCAFFOLD_MD,
            'script_name': 'scaffold.py',
            'script_source': load_script('scaffold.py'),
        },
    ]

    enabled_set = set(enabled_skills)
    deployed = 0
    for sd in all_skill_defs:
        if sd['name'] not in enabled_set:
            continue
        skill_dir = skills_dir / sd['name']
        scripts_dir = skill_dir / 'scripts'
        scripts_dir.mkdir(parents=True, exist_ok=True)

        atomic_write(skill_dir / 'SKILL.md', sd['skill_md'])
        atomic_write(scripts_dir / sd['script_name'], sd['script_source'])
        deployed += 1

    return deployed


def _cleanup_legacy(skills_dir):
    """Clean up legacy pactkit_tools.py."""
    legacy = skills_dir / 'pactkit_tools.py'
    if legacy.exists():
        legacy.unlink()


def _migrate_from_scafpy(claude_root):
    """Migrate legacy scafpy-* remnants to pactkit-* naming.

    - Removes old scafpy-visualize/, scafpy-board/, scafpy-scaffold/ skill dirs
    - Renames scafpy.yaml → pactkit.yaml (or deletes if pactkit.yaml already exists)
    """
    import shutil

    # Clean up legacy skill directories
    skills_dir = claude_root / "skills"
    for old_name in ('scafpy-visualize', 'scafpy-board', 'scafpy-scaffold'):
        old_dir = skills_dir / old_name
        if old_dir.is_dir():
            shutil.rmtree(old_dir)

    # Migrate config file
    old_yaml = claude_root / "scafpy.yaml"
    new_yaml = claude_root / "pactkit.yaml"
    if old_yaml.is_file():
        if not new_yaml.exists():
            old_yaml.rename(new_yaml)
        else:
            old_yaml.unlink()


def _deploy_rules(claude_root, enabled_rules):
    """Deploy rule modules filtered by config."""
    rules_dir = claude_root / "rules"
    rules_dir.mkdir(parents=True, exist_ok=True)

    enabled_set = set(enabled_rules)

    # Build reverse map: rule identifier -> (key, filename)
    # e.g. '01-core-protocol' -> ('core', '01-core-protocol.md')
    rule_id_to_key = {}
    for key, filename in prompts.RULES_FILES.items():
        rule_id = filename.removesuffix('.md')
        rule_id_to_key[rule_id] = key

    # Clean managed rule files
    for f in rules_dir.glob('*.md'):
        if any(f.name.startswith(p) for p in prompts.RULES_MANAGED_PREFIXES):
            f.unlink()

    # Write only enabled rules
    deployed = 0
    for rule_id in enabled_rules:
        key = rule_id_to_key.get(rule_id)
        if key is None:
            continue
        filename = prompts.RULES_FILES[key]
        atomic_write(rules_dir / filename, prompts.RULES_MODULES[key])
        deployed += 1

    return deployed


def _deploy_claude_md(claude_root, enabled_rules):
    """Generate CLAUDE.md with @import only for enabled rules."""
    # Build reverse map: rule identifier -> filename
    rule_id_to_filename = {}
    for key, filename in prompts.RULES_FILES.items():
        rule_id = filename.removesuffix('.md')
        rule_id_to_filename[rule_id] = filename

    lines = ["# PactKit Global Constitution (v23.0 Modular)", ""]
    for rule_id in sorted(enabled_rules):
        filename = rule_id_to_filename.get(rule_id)
        if filename:
            lines.append(f"@~/.claude/rules/{filename}")

    lines.append("")  # trailing newline
    atomic_write(claude_root / "CLAUDE.md", "\n".join(lines))


def _deploy_agents(agents_dir, enabled_agents):
    """Deploy agent definitions filtered by config."""
    enabled_set = set(enabled_agents)

    # Clean up managed agent files not in enabled set
    managed_agent_files = {f"{name}.md" for name in prompts.AGENTS_EXPERT}
    if agents_dir.exists():
        for f in agents_dir.glob('*.md'):
            if f.name in managed_agent_files and f.stem not in enabled_set:
                f.unlink()

    # Deploy enabled agents
    OPTIONAL_FIELDS = ['permissionMode', 'disallowedTools', 'maxTurns', 'memory', 'skills']
    deployed = 0
    for name, cfg in prompts.AGENTS_EXPERT.items():
        if name not in enabled_set:
            continue
        agent_path = agents_dir / f"{name}.md"
        content = [
            "---",
            f"name: {name}",
            f"description: {cfg['desc']}",
            f"tools: {cfg['tools']}",
            f"model: {cfg.get('model', 'sonnet')}",
        ]
        for field in OPTIONAL_FIELDS:
            if field in cfg:
                content.append(f"{field}: {cfg[field]}")
        content.extend([
            "---",
            "",
            cfg['prompt'],
            "",
            "Please refer to ~/.claude/CLAUDE.md for routing."
        ])
        atomic_write(agent_path, "\n".join(content))
        deployed += 1

    return deployed


def _deploy_commands(commands_dir, enabled_commands):
    """Deploy command playbooks filtered by config."""
    enabled_set = set(enabled_commands)

    # Build map: command name -> filename
    # e.g. 'project-plan' -> 'project-plan.md'
    enabled_filenames = {f"{cmd}.md" for cmd in enabled_commands}

    # Clean managed command files not in enabled set
    if commands_dir.exists():
        for f in commands_dir.glob('*.md'):
            if f.name.startswith("project-") and f.name not in enabled_filenames:
                f.unlink()

    # Deploy enabled commands
    deployed = 0
    for filename, content in prompts.COMMANDS_CONTENT.items():
        cmd_name = filename.removesuffix('.md')
        if cmd_name not in enabled_set:
            continue
        atomic_write(commands_dir / filename, content)
        deployed += 1

    return deployed


def _generate_config_if_missing(claude_root):
    """Generate pactkit.yaml with defaults if it doesn't exist."""
    yaml_path = claude_root / "pactkit.yaml"
    if not yaml_path.exists():
        atomic_write(yaml_path, generate_default_yaml())
