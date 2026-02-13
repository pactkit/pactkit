
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
