"""Tests for STORY-012: Agent frontmatter compliance with Claude Code native schema.

Based on reverse-engineering Claude Code v2.1.38 binary Zod schema (Og_):
  description, tools, disallowedTools, prompt, model, effort,
  permissionMode, mcpServers, hooks, maxTurns, skills, memory

Plus frontmatter parser fields: name, color, forkContext
"""
import pytest
import re
from pathlib import Path

AGENTS_DIR = Path.home() / '.claude' / 'agents'

# All fields confirmed as natively supported by Claude Code v2.1.38
NATIVE_FIELDS = {
    'name', 'description', 'tools', 'model',
    'permissionMode', 'disallowedTools', 'maxTurns',
    'skills', 'memory', 'effort', 'hooks', 'mcpServers',
    'color', 'forkContext',
}


def _parse_frontmatter(filepath):
    """Extract frontmatter keys from an agent markdown file."""
    text = filepath.read_text(encoding='utf-8')
    match = re.match(r'^---\n(.*?)\n---', text, re.DOTALL)
    if not match:
        return {}
    keys = set()
    for line in match.group(1).splitlines():
        if ':' in line:
            key = line.split(':')[0].strip()
            if key:
                keys.add(key)
    return keys


# ==============================================================================
# Scenario 1: core fields preserved in all agents
# ==============================================================================
class TestCoreFieldsPreserved:
    CORE_FIELDS = {'name', 'description', 'tools', 'model'}

    def test_all_agents_have_core_fields(self):
        for agent_file in sorted(AGENTS_DIR.glob('*.md')):
            keys = _parse_frontmatter(agent_file)
            for field in self.CORE_FIELDS:
                assert field in keys, f"{agent_file.name} missing '{field}'"


# ==============================================================================
# Scenario 2: no unknown fields in any agent (whitelist check)
# ==============================================================================
class TestNoUnknownFields:
    def test_all_fields_in_native_whitelist(self):
        for agent_file in sorted(AGENTS_DIR.glob('*.md')):
            keys = _parse_frontmatter(agent_file)
            unknown = keys - NATIVE_FIELDS
            assert not unknown, f"{agent_file.name} has non-native fields: {unknown}"


# ==============================================================================
# Scenario 3: skills field present on key agents
# ==============================================================================
class TestSkillsFieldPresent:
    def test_system_architect_has_skills(self):
        keys = _parse_frontmatter(AGENTS_DIR / 'system-architect.md')
        assert 'skills' in keys

    def test_senior_developer_has_skills(self):
        keys = _parse_frontmatter(AGENTS_DIR / 'senior-developer.md')
        assert 'skills' in keys


# ==============================================================================
# Scenario 4: memory field present on code-explorer
# ==============================================================================
class TestMemoryFieldPresent:
    def test_code_explorer_has_memory(self):
        keys = _parse_frontmatter(AGENTS_DIR / 'code-explorer.md')
        assert 'memory' in keys


# ==============================================================================
# Scenario 5: source templates consistency
# ==============================================================================
class TestSourceTemplates:
    def test_architects_have_skills(self):
        from pactkit.prompts import AGENTS_EXPERT
        assert 'skills' in AGENTS_EXPERT['system-architect']
        assert 'skills' in AGENTS_EXPERT['senior-developer']

    def test_explorer_has_memory(self):
        from pactkit.prompts import AGENTS_EXPERT
        assert AGENTS_EXPERT['code-explorer'].get('memory') == 'user'
