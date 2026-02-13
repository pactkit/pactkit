# Sprint Board

## 📋 Backlog

### [STORY-008] Constitution Sharpening — 删除伪优势强化治理规则
> Spec: docs/specs/STORY-008.md

- [ ] Remove pseudo-advantages from 01-core-protocol
- [ ] Add Session Context rule to core protocol
- [ ] Strengthen Hierarchy of Truth wording
- [ ] Update tests for changed rule content
- [ ] Verify token reduction >= 30%

## 🔄 In Progress

## ✅ Done

### STORY-004: Project Visibility — GitHub/PyPI/README/Website 曝光度优化
- [x] Set GitHub topics for pactkit/pactkit (12 topics)
- [x] Update GitHub description for pactkit/pactkit
- [x] Set GitHub metadata for pactkit/pactkit.dev (homepage + topics)
- [x] Update README.md (tagline, remove --mode common, add downloads badge)
- [x] Update pyproject.toml (keywords + classifier)
- [x] Optimize website Hero sub-headline

### STORY-003: Init Guard — project-plan / project-doctor 自动检测初始化状态
- [x] Add Phase 0.5 Init Guard to `project-plan.md` prompt template
- [x] Add Phase 0.5 Init Guard to `project-doctor.md` prompt template
- [x] Write unit tests verifying Init Guard text in command templates
- [x] Verify all existing tests pass (787 passed, 0 failed)

### STORY-002: Selective Deployment — Deployer 按 Config 过滤部署
- [x] Modify `deploy()` to accept and use config parameter
- [x] Implement selective agent deployment with cleanup
- [x] Implement selective command deployment with cleanup
- [x] Implement selective skill deployment
- [x] Implement selective rule deployment and dynamic CLAUDE.md generation
- [x] Generate `pactkit.yaml` on first `pactkit init`
- [x] Update `cli.py` to load config and pass to deployer
- [x] Add deployment summary output
- [x] Write unit tests for selective deployment
- [x] Integration test: partial config end-to-end

### STORY-001: Config Schema — pactkit.yaml 加载、验证、默认值
- [x] Create `src/pactkit/config.py` with load/validate/default/generate functions
- [x] Add `pyyaml` dependency to `pyproject.toml`
- [x] Delete `src/pactkit/common_user.py` and `tests/unit/test_common_user.py`
- [x] Remove `--mode` argument and common_user branch from `cli.py`
- [x] Write unit tests for config module
- [x] Verify all existing tests still pass (747 passed, 0 failed)

