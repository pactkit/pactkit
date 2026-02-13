"""Tests for STORY-003: Init Guard in project-plan and project-doctor."""
from pactkit.prompts import COMMANDS_CONTENT


# ==============================================================================
# Scenario 1: project-plan Init Guard exists
# ==============================================================================
class TestPlanInitGuard:
    """STORY-003 R1: project-plan MUST include Phase 0.5 Init Guard."""

    def test_plan_has_init_guard_phase(self):
        """Phase 0.5 section header must be present."""
        content = COMMANDS_CONTENT["project-plan.md"]
        assert "Phase 0.5" in content
        assert "Init Guard" in content

    def test_plan_checks_pactkit_yaml(self):
        """Guard must check .claude/pactkit.yaml."""
        content = COMMANDS_CONTENT["project-plan.md"]
        assert ".claude/pactkit.yaml" in content

    def test_plan_checks_sprint_board(self):
        """Guard must check docs/product/sprint_board.md."""
        content = COMMANDS_CONTENT["project-plan.md"]
        assert "docs/product/sprint_board.md" in content

    def test_plan_checks_architecture_graphs(self):
        """Guard must check docs/architecture/graphs/."""
        content = COMMANDS_CONTENT["project-plan.md"]
        assert "docs/architecture/graphs/" in content

    def test_plan_triggers_project_init(self):
        """Guard must reference running /project-init when markers missing."""
        content = COMMANDS_CONTENT["project-plan.md"]
        assert "/project-init" in content

    def test_plan_warning_message(self):
        """Guard must print a warning when not initialized."""
        content = COMMANDS_CONTENT["project-plan.md"]
        assert "not initialized" in content.lower() or "Not initialized" in content

    def test_plan_guard_before_phase1(self):
        """Phase 0.5 must appear before Phase 1."""
        content = COMMANDS_CONTENT["project-plan.md"]
        guard_pos = content.index("Phase 0.5")
        phase1_pos = content.index("Phase 1")
        assert guard_pos < phase1_pos


# ==============================================================================
# Scenario 2: project-plan on initialized project (silent skip)
# ==============================================================================
class TestPlanInitGuardSilentSkip:
    """STORY-003 R1: Init Guard SHOULD silently skip when all markers exist."""

    def test_plan_mentions_all_exist_skip(self):
        """Guard should mention proceeding if all markers exist."""
        content = COMMANDS_CONTENT["project-plan.md"]
        # Should mention skipping / proceeding when everything is fine
        lower = content.lower()
        assert "all" in lower and ("exist" in lower or "present" in lower or "skip" in lower)


# ==============================================================================
# Scenario 3: project-doctor Init Guard exists
# ==============================================================================
class TestDoctorInitGuard:
    """STORY-003 R2: project-doctor MUST include Phase 0.5 Init Guard."""

    def test_doctor_has_init_guard_phase(self):
        """Phase 0.5 section header must be present."""
        content = COMMANDS_CONTENT["project-doctor.md"]
        assert "Phase 0.5" in content
        assert "Init Guard" in content

    def test_doctor_checks_pactkit_yaml(self):
        """Guard must check .claude/pactkit.yaml."""
        content = COMMANDS_CONTENT["project-doctor.md"]
        assert ".claude/pactkit.yaml" in content

    def test_doctor_checks_sprint_board(self):
        """Guard must check docs/product/sprint_board.md."""
        content = COMMANDS_CONTENT["project-doctor.md"]
        assert "docs/product/sprint_board.md" in content

    def test_doctor_checks_architecture_graphs(self):
        """Guard must check docs/architecture/graphs/."""
        content = COMMANDS_CONTENT["project-doctor.md"]
        assert "docs/architecture/graphs/" in content

    def test_doctor_offers_choice(self):
        """Doctor guard must offer choice: auto-fix or continue diagnosis."""
        content = COMMANDS_CONTENT["project-doctor.md"]
        lower = content.lower()
        # Doctor should give user a choice, not auto-run
        assert "choice" in lower or "ask" in lower or "offer" in lower

    def test_doctor_guard_before_phase1(self):
        """Phase 0.5 must appear before Phase 1."""
        content = COMMANDS_CONTENT["project-doctor.md"]
        guard_pos = content.index("Phase 0.5")
        phase1_pos = content.index("Phase 1")
        assert guard_pos < phase1_pos
