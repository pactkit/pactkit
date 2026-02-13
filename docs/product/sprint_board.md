# Sprint Board

## 📋 Backlog

### STORY-002: Selective Deployment — Deployer 按 Config 过滤部署
- [ ] Modify `deploy()` to accept and use config parameter
- [ ] Implement selective agent deployment with cleanup
- [ ] Implement selective command deployment with cleanup
- [ ] Implement selective skill deployment
- [ ] Implement selective rule deployment and dynamic CLAUDE.md generation
- [ ] Generate `pactkit.yaml` on first `pactkit init`
- [ ] Update `cli.py` to load config and pass to deployer
- [ ] Add deployment summary output
- [ ] Write unit tests for selective deployment
- [ ] Integration test: partial config end-to-end

## 🔄 In Progress

## ✅ Done

### STORY-001: Config Schema — pactkit.yaml 加载、验证、默认值
- [x] Create `src/pactkit/config.py` with load/validate/default/generate functions
- [x] Add `pyyaml` dependency to `pyproject.toml`
- [x] Delete `src/pactkit/common_user.py` and `tests/unit/test_common_user.py`
- [x] Remove `--mode` argument and common_user branch from `cli.py`
- [x] Write unit tests for config module
- [x] Verify all existing tests still pass (747 passed, 0 failed)
