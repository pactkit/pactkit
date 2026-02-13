
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
