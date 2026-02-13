"""
STORY-007: /project-status — 冷启动项目状态感知命令
"""
import importlib

import pytest


def _prompts():
    import pactkit.prompts as p
    importlib.reload(p)
    return p


def _config():
    from pactkit import config
    return config


# ===========================================================================
# Scenario 1: Playbook exists and is registered
# ===========================================================================

class TestStatusPlaybookExists:
    """project-status.md must exist in COMMANDS_CONTENT."""

    def test_registered_in_commands_content(self):
        p = _prompts()
        assert 'project-status.md' in p.COMMANDS_CONTENT

    def test_non_empty(self):
        p = _prompts()
        content = p.COMMANDS_CONTENT['project-status.md']
        assert isinstance(content, str)
        assert len(content) > 100

    def test_has_frontmatter(self):
        p = _prompts()
        content = p.COMMANDS_CONTENT['project-status.md']
        assert content.strip().startswith('---')

    def test_has_description_in_frontmatter(self):
        p = _prompts()
        content = p.COMMANDS_CONTENT['project-status.md']
        assert 'description:' in content


# ===========================================================================
# Scenario 2: Routing table includes Status
# ===========================================================================

class TestRoutingTableIncludesStatus:
    """Routing table must have a Status entry."""

    def test_status_in_routing(self):
        p = _prompts()
        routing = p.RULES_MODULES['routing']
        assert 'project-status' in routing

    def test_has_role(self):
        p = _prompts()
        routing = p.RULES_MODULES['routing']
        assert 'System Medic' in routing

    def test_has_playbook_reference(self):
        p = _prompts()
        routing = p.RULES_MODULES['routing']
        assert 'project-status.md' in routing

    def test_has_goal(self):
        p = _prompts()
        routing = p.RULES_MODULES['routing']
        # Find the Status section and check it has a Goal line
        lines = routing.split('\n')
        in_status_section = False
        has_goal = False
        for line in lines:
            if 'Status' in line and 'project-status' in line:
                in_status_section = True
            elif in_status_section and line.startswith('###'):
                break  # next section
            elif in_status_section and '**Goal**' in line:
                has_goal = True
        assert has_goal, "Status routing entry must have a Goal line"


# ===========================================================================
# Scenario 3: VALID_COMMANDS includes project-status
# ===========================================================================

class TestValidCommandsIncludesStatus:
    """config.VALID_COMMANDS must include 'project-status'."""

    def test_in_valid_commands(self):
        cfg = _config()
        assert 'project-status' in cfg.VALID_COMMANDS

    def test_default_config_includes_status(self):
        cfg = _config()
        default = cfg.get_default_config()
        assert 'project-status' in default['commands']


# ===========================================================================
# Scenario 4: Playbook content — R1 structured report
# ===========================================================================

class TestPlaybookContentReport:
    """Playbook must instruct the agent to output a structured report."""

    def test_has_sprint_board_section(self):
        p = _prompts()
        content = p.COMMANDS_CONTENT['project-status.md']
        assert 'Sprint Board' in content

    def test_has_git_state_section(self):
        p = _prompts()
        content = p.COMMANDS_CONTENT['project-status.md']
        assert 'Git State' in content

    def test_has_health_indicators_section(self):
        p = _prompts()
        content = p.COMMANDS_CONTENT['project-status.md']
        assert 'Health Indicators' in content

    def test_has_recommended_next_action(self):
        p = _prompts()
        content = p.COMMANDS_CONTENT['project-status.md']
        assert 'Recommended Next Action' in content or 'Next Action' in content


# ===========================================================================
# Scenario 5: Read-only constraint — R2
# ===========================================================================

class TestReadOnlyConstraint:
    """Playbook must be read-only — no Write/Edit in allowed-tools."""

    def test_allowed_tools_no_write(self):
        p = _prompts()
        content = p.COMMANDS_CONTENT['project-status.md']
        lines = content.split('\n')
        for line in lines:
            if 'allowed-tools' in line:
                assert 'Write' not in line, \
                    "project-status is read-only, must not have Write tool"
                assert 'Edit' not in line, \
                    "project-status is read-only, must not have Edit tool"
                break

    def test_mentions_read_only(self):
        p = _prompts()
        content = p.COMMANDS_CONTENT['project-status.md'].lower()
        assert 'read-only' in content or 'read only' in content or \
            'must not modify' in content or 'does not modify' in content


# ===========================================================================
# Scenario 6: Non-initialized project fallback — R4
# ===========================================================================

class TestNonInitializedFallback:
    """Playbook must handle projects without sprint_board.md."""

    def test_mentions_uninitialized_handling(self):
        p = _prompts()
        content = p.COMMANDS_CONTENT['project-status.md'].lower()
        assert 'not initialized' in content or 'uninitialized' in content or \
            'no sprint' in content or 'missing' in content or \
            'project-init' in content

    def test_suggests_project_init(self):
        p = _prompts()
        content = p.COMMANDS_CONTENT['project-status.md']
        assert '/project-init' in content


# ===========================================================================
# Scenario 7: Context refresh — R5
# ===========================================================================

class TestContextRefresh:
    """Playbook should mention context.md refresh."""

    def test_mentions_context_refresh(self):
        p = _prompts()
        content = p.COMMANDS_CONTENT['project-status.md']
        assert 'context.md' in content


# ===========================================================================
# Scenario 8: Backward compatibility
# ===========================================================================

class TestBackwardCompatibility:
    """Adding project-status must not break existing commands."""

    def test_existing_commands_still_present(self):
        p = _prompts()
        expected = [
            'project-plan.md', 'project-act.md', 'project-check.md',
            'project-done.md', 'project-init.md', 'project-doctor.md',
            'project-draw.md', 'project-trace.md', 'project-release.md',
            'project-sprint.md', 'project-review.md', 'project-hotfix.md',
            'project-design.md',
        ]
        for cmd in expected:
            assert cmd in p.COMMANDS_CONTENT, f"Missing {cmd}"

    def test_total_command_count(self):
        """14 commands total after adding project-status."""
        cfg = _config()
        assert len(cfg.VALID_COMMANDS) == 14
