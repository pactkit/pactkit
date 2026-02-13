import sys
from pathlib import Path

# 确保能 import pactkit.prompts
current_dir = Path(__file__).resolve().parent
project_root = current_dir.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from pactkit import prompts
from pactkit.skills import load_script
from pactkit.utils import atomic_write


def deploy(mode="expert"):
    print("🚀 PactKit DevOps Deployment (v20.0 - EXPERT Mode)")

    # 1. 准备目录
    claude_root = Path.home() / ".claude"
    agents_dir = claude_root / "agents"
    commands_dir = claude_root / "commands"
    skills_dir = claude_root / "skills"

    for d in [claude_root, agents_dir, commands_dir, skills_dir]:
        d.mkdir(parents=True, exist_ok=True)

    # 2. 部署 Skills (v20.0 Compliant Skill Structure)
    _deploy_skills(skills_dir)

    # 3. 清理旧文件
    _cleanup_legacy(skills_dir)

    # 4. 部署 Expert 配置
    _deploy_expert(claude_root, agents_dir, commands_dir)

    print("\n🎉 Deployment Complete.")


def _deploy_skills(skills_dir):
    """部署合规的 Skill 目录结构"""
    skill_defs = [
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

    for sd in skill_defs:
        skill_dir = skills_dir / sd['name']
        scripts_dir = skill_dir / 'scripts'
        scripts_dir.mkdir(parents=True, exist_ok=True)

        atomic_write(skill_dir / 'SKILL.md', sd['skill_md'])
        atomic_write(scripts_dir / sd['script_name'], sd['script_source'])

    print(f"✅ Deployed {len(skill_defs)} Skills (Compliant Structure)")


def _cleanup_legacy(skills_dir):
    """清理旧的 pactkit_tools.py"""
    legacy = skills_dir / 'pactkit_tools.py'
    if legacy.exists():
        legacy.unlink()
        print(f"🧹 Removed legacy: {legacy}")


def _deploy_rules(claude_root):
    """部署模块化规则到 ~/.claude/rules/，保护用户自定义文件"""
    rules_dir = claude_root / "rules"
    rules_dir.mkdir(parents=True, exist_ok=True)

    # 清理受管理的文件（01-04 前缀），保留用户文件（10+）
    for f in rules_dir.glob('*.md'):
        if any(f.name.startswith(p) for p in prompts.RULES_MANAGED_PREFIXES):
            f.unlink()

    # 写入规则模块
    for key, filename in prompts.RULES_FILES.items():
        atomic_write(rules_dir / filename, prompts.RULES_MODULES[key])

    print(f"✅ Deployed {len(prompts.RULES_FILES)} Rule Modules")


def _cleanup_managed(directory, managed_names, prefix=None):
    """清理受管理文件，保留用户自定义文件。

    Args:
        directory: 目标目录
        managed_names: 受管理的文件名集合（含扩展名）
        prefix: 如果提供，按前缀匹配清理；否则按 managed_names 精确匹配
    """
    if not directory.exists():
        return
    for f in directory.glob('*.md'):
        if prefix and f.name.startswith(prefix):
            f.unlink()
        elif not prefix and f.name in managed_names:
            f.unlink()


def _deploy_expert(claude_root, agents_dir, commands_dir):
    # 部署模块化规则
    _deploy_rules(claude_root)

    # 部署精简版 CLAUDE.md（@import 引用）
    atomic_write(claude_root / "CLAUDE.md", prompts.CLAUDE_MD_TEMPLATE)
    print("✅ Constitution Updated (Modular)")

    # 清理旧的受管理 Agent 文件，保留用户自定义 Agent
    managed_agent_files = {f"{name}.md" for name in prompts.AGENTS_EXPERT}
    _cleanup_managed(agents_dir, managed_agent_files)

    # 部署 Agents (满血版 + 高级字段)
    OPTIONAL_FIELDS = ['permissionMode', 'disallowedTools', 'maxTurns', 'memory', 'skills']
    for name, cfg in prompts.AGENTS_EXPERT.items():
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
    print(f"✅ Deployed {len(prompts.AGENTS_EXPERT)} Expert Agents")

    # 清理旧的受管理 Command 文件，保留用户自定义命令
    _cleanup_managed(commands_dir, set(), prefix="project-")

    # 部署 Commands (满血版)
    for filename, content in prompts.COMMANDS_CONTENT.items():
        atomic_write(commands_dir / filename, content)
    print(f"✅ Deployed {len(prompts.COMMANDS_CONTENT)} Command Playbooks")
