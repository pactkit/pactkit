
### [STORY-005] Plugin Distribution — 支持 Claude Code Plugin 格式分发
> Spec: docs/specs/STORY-005.md

- [x] Add --format parameter to CLI (classic/plugin/marketplace)
- [x] Implement _deploy_plugin_json() for .claude-plugin/plugin.json
- [x] Implement _deploy_claude_md_inline() for self-contained CLAUDE.md
- [x] Implement plugin mode in deploy() — full component deployment
- [x] Implement _deploy_marketplace_json() for marketplace repo structure
- [x] Write unit tests for plugin mode deployment
- [x] Write unit tests for marketplace mode deployment
- [x] Verify classic mode unchanged — all existing tests pass
- [x] Integration test: claude --plugin-dir loads generated plugin

### [STORY-006] Session Context Protocol — 跨会话项目状态自动感知
> Spec: docs/specs/STORY-006.md

- [x] Add context.md generation to Done playbook
- [x] Add context.md generation to Plan playbook
- [x] Add context.md generation to Init playbook
- [x] Add @context.md reference to CLAUDE_MD_TEMPLATE
- [x] Add lessons.md auto-append to Done playbook
- [x] Write unit tests for prompt changes
- [x] Verify plugin mode inline CLAUDE.md unaffected

### [STORY-007] /project-status 冷启动项目状态感知命令
> Spec: docs/specs/STORY-007.md

- [x] Add project-status.md playbook to commands.py
- [x] Add to VALID_COMMANDS and routing table
- [x] Write unit tests for new command content
- [x] Verify non-initialized project fallback

### [STORY-008] Constitution Sharpening — 删除伪优势强化治理规则
> Spec: docs/specs/STORY-008.md

- [x] Remove pseudo-advantages from 01-core-protocol
- [x] Add Session Context rule to core protocol
- [x] Strengthen Hierarchy of Truth wording
- [x] Update tests for changed rule content
- [x] Verify token reduction >= 30%

### [STORY-009] Config Auto-Merge — pactkit init 自动合并新组件
> Spec: docs/specs/STORY-009.md

- [x] Modify load_config() merge logic
- [x] Add auto-append for new components
- [x] Handle user opt-out (exclude)
- [x] Add version tracking to yaml
- [x] Update tests
- [x] Backward compatibility verification

### [STORY-010] Release v1.1.0 — 文档同步 + 版本发布
> Spec: docs/specs/STORY-010.md

- [x] Sync README.md (13→14 commands, add project-status)
- [x] Sync .claude/CLAUDE.md (stale numbers)
- [x] Bump version to 1.1.0 (pyproject + __init__)
- [x] Create CHANGELOG.md
- [x] Run tests + build verification
- [x] Git tag v1.1.0

### [STORY-011] PDCA Slim — 辅助命令降级为 Skill，精简用户界面
> Spec: docs/specs/STORY-011.md

- [x] Remove 6 commands from VALID_COMMANDS and COMMANDS_CONTENT
- [x] Create 6 new SKILL_*_MD templates in skills.py
- [x] Register 6 new skills in VALID_SKILLS
- [x] Update PDCA command prompts to reference skills instead of sibling commands
- [x] Update routing table and agent skill references
- [x] Update deployer to deploy 9 skills
- [x] Add deprecation warnings for removed commands in load_config
- [x] Update all count-based tests

### [STORY-012] Docs Sync — 同步文档站和 GitHub 元数据至 PDCA Slim 架构
> Spec: docs/specs/STORY-012.md

- [x] Update pactkit/pactkit GitHub repo description
- [x] Update index.mdx (At a Glance counts + links)
- [x] Rewrite commands.mdx (8 commands, remove 6 old entries)
- [x] Update skills.mdx (add 6 new prompt-only skills)
- [x] Update installation.mdx and configuration.mdx counts
- [x] Update workflow.mdx trace reference
- [x] Regenerate claude-code-plugin with pactkit init --format marketplace

### [BUG-001] Scripted Skill Prompts Use Wrong Script Path
> Spec: docs/specs/BUG-001.md

- [x] Update SKILL_VISUALIZE_MD path references (R1)
- [x] Update SKILL_BOARD_MD path references (R1)
- [x] Update SKILL_SCAFFOLD_MD path references (R1)
- [x] Verify existing tests pass (R5)
