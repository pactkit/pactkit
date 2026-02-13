"""Tests for STORY-010: Commands must reference visualize multi-mode."""
import pytest
from pathlib import Path

CLAUDE_DIR = Path.home() / '.claude'
COMMANDS = CLAUDE_DIR / 'commands'
AGENTS = CLAUDE_DIR / 'agents'


# ==============================================================================
# Scenario 1: project-trace uses call graph
# ==============================================================================
class TestProjectTrace:
    def test_trace_has_call_mode(self):
        content = (COMMANDS / 'project-trace.md').read_text()
        assert '--mode call' in content

    def test_trace_has_entry_param(self):
        content = (COMMANDS / 'project-trace.md').read_text()
        assert '--entry' in content

    def test_trace_references_call_graph_mmd(self):
        content = (COMMANDS / 'project-trace.md').read_text()
        assert 'call_graph.mmd' in content


# ==============================================================================
# Scenario 2: project-plan mode selection guidance
# ==============================================================================
class TestProjectPlan:
    def test_plan_has_mode_class(self):
        content = (COMMANDS / 'project-plan.md').read_text()
        assert '--mode class' in content

    def test_plan_has_mode_call(self):
        content = (COMMANDS / 'project-plan.md').read_text()
        assert '--mode call' in content

    def test_plan_has_mode_selection_guidance(self):
        content = (COMMANDS / 'project-plan.md').read_text()
        # Should mention at least two modes to guide selection
        assert 'class' in content and 'call' in content


# ==============================================================================
# Scenario 3: project-act full graph update
# ==============================================================================
class TestProjectAct:
    def test_act_has_call_entry(self):
        content = (COMMANDS / 'project-act.md').read_text()
        assert '--mode call' in content or '--entry' in content

    def test_act_phase4_updates_class_graph(self):
        content = (COMMANDS / 'project-act.md').read_text()
        assert '--mode class' in content


# ==============================================================================
# Scenario 4: project-doctor class health check
# ==============================================================================
class TestProjectDoctor:
    def test_doctor_has_class_mode(self):
        content = (COMMANDS / 'project-doctor.md').read_text()
        assert '--mode class' in content


# ==============================================================================
# Scenario 5: project-init full mode discovery
# ==============================================================================
class TestProjectInit:
    def test_init_has_class_mode(self):
        content = (COMMANDS / 'project-init.md').read_text()
        assert '--mode class' in content


# ==============================================================================
# Scenario 6: Agents know about new modes
# ==============================================================================
class TestAgents:
    def test_system_architect_knows_class_mode(self):
        content = (AGENTS / 'system-architect.md').read_text()
        assert '--mode class' in content or 'class' in content.lower()

    def test_senior_developer_knows_call_mode(self):
        content = (AGENTS / 'senior-developer.md').read_text()
        assert '--mode call' in content or '--entry' in content
