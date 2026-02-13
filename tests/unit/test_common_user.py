"""
STORY-039: Common User 体验版 — 独立自含零脚本 PDCA 安装器
Tests for pactkit init --mode common
"""
import subprocess
import sys
import os
from pathlib import Path

import pytest

COMMON_USER_SCRIPT = Path(__file__).resolve().parent.parent.parent / "src" / "pactkit" / "common_user.py"

FORBIDDEN_KEYWORDS = [
    "pactkit",
    "scaffold",
    "visualize",
    "board.py",
    "pactkit_tools",
    "skills/",
    "python3 ",
]


@pytest.fixture
def deploy_dir(tmp_path):
    """Run common-user.py with --target pointing to a temp directory."""
    target = tmp_path / "claude"
    result = subprocess.run(
        [sys.executable, str(COMMON_USER_SCRIPT), "--target", str(target)],
        capture_output=True,
        text=True,
        cwd=str(COMMON_USER_SCRIPT.parent.parent),
    )
    assert result.returncode == 0, f"Script failed:\n{result.stderr}"
    return target


class TestScenario1_ZeroScriptDeployment:
    """Scenario 1: 体验版零脚本部署"""

    def test_claude_md_exists(self, deploy_dir):
        assert (deploy_dir / "CLAUDE.md").is_file()

    def test_commands_exist(self, deploy_dir):
        commands_dir = deploy_dir / "commands"
        assert commands_dir.is_dir()
        expected = {"plan.md", "act.md", "check.md", "done.md"}
        actual = {f.name for f in commands_dir.iterdir() if f.is_file()}
        assert actual == expected, f"Expected {expected}, got {actual}"

    def test_no_skills_directory(self, deploy_dir):
        skills_dir = deploy_dir / "skills"
        if skills_dir.exists():
            contents = list(skills_dir.rglob("*"))
            assert len(contents) == 0, f"skills/ should be empty, found: {contents}"

    def test_no_rules_directory(self, deploy_dir):
        assert not (deploy_dir / "rules").exists()

    def test_no_agents_directory(self, deploy_dir):
        assert not (deploy_dir / "agents").exists()


class TestScenario2_ZeroScriptReferences:
    """Scenario 2: 生成内容零脚本引用"""

    def test_no_forbidden_keywords_in_any_file(self, deploy_dir):
        violations = []
        for f in deploy_dir.rglob("*.md"):
            content = f.read_text(encoding="utf-8")
            for keyword in FORBIDDEN_KEYWORDS:
                if keyword in content:
                    violations.append(f"{f.relative_to(deploy_dir)}: contains '{keyword}'")
        assert violations == [], f"Forbidden keywords found:\n" + "\n".join(violations)


class TestScenario3_InlinePDCA:
    """Scenario 3: CLAUDE.md 内嵌 PDCA 说明"""

    def test_claude_md_contains_pdca_steps(self, deploy_dir):
        content = (deploy_dir / "CLAUDE.md").read_text(encoding="utf-8")
        for step in ["Plan", "Act", "Check", "Done"]:
            assert step in content, f"CLAUDE.md missing PDCA step: {step}"

    def test_claude_md_no_cross_file_references(self, deploy_dir):
        content = (deploy_dir / "CLAUDE.md").read_text(encoding="utf-8")
        assert "@" not in content or "@~/" not in content, "CLAUDE.md contains cross-file @import references"
        for keyword in ["skills/", "rules/", "agents/"]:
            assert keyword not in content, f"CLAUDE.md references '{keyword}'"


class TestScenario4_SelfContained:
    """common-user.py must not import any devops internal modules."""

    def test_no_internal_imports(self):
        content = COMMON_USER_SCRIPT.read_text(encoding="utf-8")
        for module in ["pactkit.prompts", "pactkit.generators", "pactkit.skills"]:
            assert module not in content, f"common-user.py imports internal module: {module}"

    def test_only_stdlib_imports(self):
        content = COMMON_USER_SCRIPT.read_text(encoding="utf-8")
        lines = content.splitlines()
        import_lines = [l.strip() for l in lines if l.strip().startswith(("import ", "from "))]
        allowed_modules = {"os", "sys", "argparse", "pathlib", "textwrap"}
        for line in import_lines:
            # Extract module name
            if line.startswith("from "):
                module = line.split()[1].split(".")[0]
            else:
                module = line.split()[1].split(".")[0]
            assert module in allowed_modules, f"Unexpected import: '{line}' (module: {module})"
