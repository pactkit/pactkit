"""Tests for STORY-028: Add Regression Gate and Deploy Verification to /project-done."""
import pytest


def _prompts():
    import importlib
    import pactkit.prompts as p
    importlib.reload(p)
    return p


# ==============================================================================
# Scenario 1: Done Playbook Has Regression Gate
# ==============================================================================
class TestDoneRegressionGate:
    """STORY-028 Scenario 1: project-done.md has a regression testing phase."""

    def test_done_has_regression_keyword(self):
        p = _prompts()
        done = p.COMMANDS_CONTENT['project-done.md']
        lower = done.lower()
        assert 'regression' in lower or 'test suite' in lower

    def test_done_has_full_test_run(self):
        """Should instruct running the full test suite."""
        p = _prompts()
        done = p.COMMANDS_CONTENT['project-done.md']
        lower = done.lower()
        assert 'pytest' in lower or 'test suite' in lower or 'test runner' in lower

    def test_regression_before_commit(self):
        """Regression gate must appear before the Git Commit phase heading."""
        p = _prompts()
        done = p.COMMANDS_CONTENT['project-done.md']
        # Find regression gate phase
        regression_idx = max(
            done.lower().find('regression'),
            done.lower().find('test suite'),
        )
        # Find the Phase 4 heading (Git Commit phase)
        commit_phase_idx = done.find('Phase 4')
        assert regression_idx > 0, "No regression gate found"
        assert commit_phase_idx > 0, "No git commit phase found"
        assert regression_idx < commit_phase_idx, "Regression gate must come before Phase 4"


# ==============================================================================
# Scenario 2: Done Playbook Has Deploy Step
# ==============================================================================
class TestDoneDeployVerify:
    """STORY-028 Scenario 2: project-done.md has a deploy & verify phase."""

    def test_done_has_deploy_keyword(self):
        p = _prompts()
        done = p.COMMANDS_CONTENT['project-done.md']
        lower = done.lower()
        assert 'deploy' in lower

    def test_done_has_verify_keyword(self):
        p = _prompts()
        done = p.COMMANDS_CONTENT['project-done.md']
        lower = done.lower()
        assert 'verify' in lower or 'smoke' in lower or 'spot-check' in lower

    def test_deploy_before_commit(self):
        """Deploy & verify must appear before the Git Commit phase heading."""
        p = _prompts()
        done = p.COMMANDS_CONTENT['project-done.md']
        deploy_idx = done.lower().find('deploy')
        commit_phase_idx = done.find('Phase 4')
        assert deploy_idx > 0, "No deploy step found"
        assert commit_phase_idx > 0, "No git commit phase found"
        assert deploy_idx < commit_phase_idx, "Deploy must come before Phase 4"

    def test_deploy_mentions_deployer(self):
        """Should reference the deployer mechanism."""
        p = _prompts()
        done = p.COMMANDS_CONTENT['project-done.md']
        assert 'pactkit init' in done or 'pactkit.yaml' in done or 'deployer' in done.lower()


# ==============================================================================
# Scenario 3: Done Playbook Stops on Failure
# ==============================================================================
class TestDoneStopsOnFailure:
    """STORY-028 Scenario 3: project-done.md stops if tests fail."""

    def test_done_has_stop_instruction(self):
        p = _prompts()
        done = p.COMMANDS_CONTENT['project-done.md']
        lower = done.lower()
        assert 'stop' in lower or 'abort' in lower or 'do not commit' in lower or 'must not' in lower

    def test_done_has_fail_handling(self):
        p = _prompts()
        done = p.COMMANDS_CONTENT['project-done.md']
        lower = done.lower()
        assert 'fail' in lower or 'red' in lower or 'error' in lower


# ==============================================================================
# Scenario 4: Repo Maintainer Agent Mentions Gates
# ==============================================================================
class TestRepoMaintainerGates:
    """STORY-028 Scenario 4: repo-maintainer agent mentions regression + deploy."""

    def test_maintainer_mentions_regression(self):
        p = _prompts()
        prompt = p.AGENTS_EXPERT['repo-maintainer']['prompt']
        lower = prompt.lower()
        assert 'regression' in lower or 'test suite' in lower

    def test_maintainer_mentions_deploy(self):
        p = _prompts()
        prompt = p.AGENTS_EXPERT['repo-maintainer']['prompt']
        lower = prompt.lower()
        assert 'deploy' in lower or 'verify' in lower


# ==============================================================================
# Scenario 5: Backward Compatibility
# ==============================================================================
class TestBackwardCompatibility:
    """STORY-028 Scenario 5: All existing commands and agents still present."""

    def test_existing_commands_present(self):
        p = _prompts()
        expected = [
            'project-plan.md', 'project-act.md', 'project-check.md',
            'project-done.md', 'project-init.md', 'project-doctor.md',
            'project-draw.md', 'project-trace.md', 'project-release.md',
            'project-sprint.md', 'project-review.md', 'project-hotfix.md',
        ]
        for cmd in expected:
            assert cmd in p.COMMANDS_CONTENT, f"Missing {cmd}"

    def test_agents_unchanged(self):
        p = _prompts()
        expected_agents = [
            'system-architect', 'senior-developer', 'qa-engineer',
            'repo-maintainer', 'system-medic', 'security-auditor',
            'visual-architect', 'code-explorer',
        ]
        for agent in expected_agents:
            assert agent in p.AGENTS_EXPERT, f"Missing agent {agent}"
