"""PactKit configuration — load, validate, and generate pactkit.yaml."""
import warnings
from pathlib import Path

import yaml

# ---------------------------------------------------------------------------
# Valid identifiers (the registry of all known components)
# ---------------------------------------------------------------------------

VALID_AGENTS = frozenset({
    'system-architect',
    'senior-developer',
    'qa-engineer',
    'repo-maintainer',
    'system-medic',
    'security-auditor',
    'visual-architect',
    'code-explorer',
    'product-designer',
})

VALID_COMMANDS = frozenset({
    'project-plan',
    'project-act',
    'project-check',
    'project-done',
    'project-init',
    'project-doctor',
    'project-draw',
    'project-trace',
    'project-sprint',
    'project-review',
    'project-hotfix',
    'project-design',
    'project-release',
    'project-status',
})

VALID_SKILLS = frozenset({
    'pactkit-visualize',
    'pactkit-board',
    'pactkit-scaffold',
})

VALID_RULES = frozenset({
    '01-core-protocol',
    '02-hierarchy-of-truth',
    '03-file-atlas',
    '04-routing-table',
    '05-workflow-conventions',
    '06-mcp-integration',
})

VALID_STACKS = frozenset({'auto', 'python', 'node', 'go', 'java'})


# ---------------------------------------------------------------------------
# Default config
# ---------------------------------------------------------------------------

def get_default_config() -> dict:
    """Return the default config with all components enabled."""
    return {
        'version': '0.0.1',
        'stack': 'auto',
        'root': '.',
        'agents': sorted(VALID_AGENTS),
        'commands': sorted(VALID_COMMANDS),
        'skills': sorted(VALID_SKILLS),
        'rules': sorted(VALID_RULES),
    }


# ---------------------------------------------------------------------------
# Load config
# ---------------------------------------------------------------------------

def load_config(path: Path | str | None = None) -> dict:
    """Load pactkit.yaml from *path*, merging with defaults.

    If *path* is ``None``, uses ``~/.claude/pactkit.yaml``.
    If the file does not exist, returns the full default config.
    Missing keys in the user file inherit from defaults.
    """
    if path is None:
        path = Path.home() / '.claude' / 'pactkit.yaml'
    else:
        path = Path(path)

    default = get_default_config()

    if not path.exists():
        return default

    raw = path.read_text(encoding='utf-8')
    user_data = yaml.safe_load(raw)

    # Empty file or YAML that parses to None
    if not isinstance(user_data, dict):
        return default

    # Merge: user keys override defaults; missing keys inherit
    merged = dict(default)
    for key, value in user_data.items():
        if key in merged:
            merged[key] = value

    return merged


# ---------------------------------------------------------------------------
# Validate config
# ---------------------------------------------------------------------------

_REGISTRY = {
    'agents': VALID_AGENTS,
    'commands': VALID_COMMANDS,
    'skills': VALID_SKILLS,
    'rules': VALID_RULES,
}


def validate_config(config: dict) -> None:
    """Warn (never raise) about unknown component names or invalid values."""
    # Validate stack
    stack = config.get('stack', 'auto')
    if stack not in VALID_STACKS:
        warnings.warn(f"Unknown stack: {stack}. Valid: {', '.join(sorted(VALID_STACKS))}")

    # Validate component lists
    for key, valid_set in _REGISTRY.items():
        user_list = config.get(key, [])
        if not isinstance(user_list, list):
            warnings.warn(f"Config key '{key}' should be a list, got {type(user_list).__name__}")
            continue
        for name in user_list:
            if not isinstance(name, str):
                warnings.warn(f"Config key '{key}' contains non-string value: {name!r}")
            elif name not in valid_set:
                warnings.warn(f"Unknown {key.rstrip('s')}: {name}")


# ---------------------------------------------------------------------------
# YAML generation
# ---------------------------------------------------------------------------

def generate_default_yaml() -> str:
    """Return the default config as a commented YAML string."""
    cfg = get_default_config()
    lines = [
        '# PactKit Configuration',
        '# Edit this file to customize which components are deployed.',
        '# Remove items from a list to disable them. Default: all enabled.',
        '',
        f'version: "{cfg["version"]}"',
        f'stack: {cfg["stack"]}',
        f'root: {cfg["root"]}',
        '',
        '# Agents — AI role definitions deployed to ~/.claude/agents/',
        'agents:',
    ]
    for a in cfg['agents']:
        lines.append(f'  - {a}')

    lines.extend(['', '# Commands — PDCA playbooks deployed to ~/.claude/commands/'])
    lines.append('commands:')
    for c in cfg['commands']:
        lines.append(f'  - {c}')

    lines.extend(['', '# Skills — tool scripts deployed to ~/.claude/skills/'])
    lines.append('skills:')
    for s in cfg['skills']:
        lines.append(f'  - {s}')

    lines.extend(['', '# Rules — constitution modules deployed to ~/.claude/rules/'])
    lines.append('rules:')
    for r in cfg['rules']:
        lines.append(f'  - {r}')

    lines.append('')  # trailing newline
    return '\n'.join(lines)
