## 变更内容

（这个 PR 改了什么、为什么改）

## 关联 Issue

Fixes #（issue 编号，如有）

## 设计底线核对

- [ ] 零第三方依赖（仅 Python 标准库 + 系统 git）
- [ ] 纯只读：不修改被分析仓库
- [ ] 空仓库 / 无 HEAD 时不崩溃（输出零值统计）
- [ ] 中英文文件名与含特殊字符路径处理正常（`-c core.quotePath=false`）

## 测试

- [ ] 本地 `python3 -m unittest discover -s tests` 全部通过
- [ ] 本次变更已补充/更新对应测试

## 变更日志

- [ ] CHANGELOG.md 已更新
- [ ] 若涉及版本号：`src/git_repo_stats/__init__.py` 与 `pyproject.toml` 已同步
