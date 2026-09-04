# Contributing to git-repo-stats

感谢你愿意花时间为 git-repo-stats 做贡献！无论是修一个 bug、加一个功能、
补文档还是提一个好 issue，都欢迎。

## 目录

- [项目设计底线](#项目设计底线)
- [开发环境](#开发环境)
- [跑测试](#跑测试)
- [提 Issue](#提-issue)
- [提 Pull Request](#提-pull-request)
- [提交信息规范](#提交信息规范)
- [版本与变更日志](#版本与变更日志)

## 项目设计底线

改动之前请先确认它不违背以下三条原则（违背时请先在 issue 里讨论）：

1. **零第三方依赖**：只使用 Python 标准库与系统 `git`。任何新依赖都需要充分理由。
2. **纯只读**：绝不执行会修改目标仓库的 git 命令。
3. **跨平台**：代码不得依赖 macOS / Linux 专有行为（本项目开发在 macOS 上，
   但 CI 跑在 Ubuntu；Windows 用户在 issue 中反馈的问题同样会被认真对待）。

## 开发环境

```bash
git clone https://github.com/a976xw7td/c5-git-repo-stats.git
cd c5-git-repo-stats
python3 -m venv .venv && source .venv/bin/activate   # 可选，推荐隔离环境
pip install -e .
```

## 跑测试

测试使用标准库 `unittest`，无第三方依赖：

```bash
python -m unittest discover -s tests -v
```

提交 PR 前请确保本地全绿；CI（GitHub Actions，Python 3.9 / 3.11 / 3.13）
会在 push 后自动复跑同样的命令。

## 提 Issue

请使用仓库自带的模板（点击 New Issue 即可选择）：

- 🐛 [Bug report](.github/ISSUE_TEMPLATE/bug_report.md)：可复现的 bug，请尽量给出
  复现命令、输入与期望/实际输出，以及你的环境（操作系统、Python 版本、git 版本）。
- ✨ [Feature request](.github/ISSUE_TEMPLATE/feature_request.md)：新想法请说明
  动机与使用场景，帮助维护者判断它是否适合这个"小而锐利"的工具。

## 提 Pull Request

1. 从 `main` 拉一个分支：`git checkout -b feat/your-feature`；
2. 做改动，**新功能请附带测试**（参考 `tests/test_cli.py` 的写法）；
3. 本地全量测试通过后推送并开 PR，PR 模板会自动展开；
4. 维护者会 review，可能需要几轮修改——对事不对人，请别介意。

## 提交信息规范

使用 [Conventional Commits](https://www.conventionalcommits.org/zh-hans/)：

```
<type>(<scope>): <描述>

type: feat | fix | docs | refactor | test | chore | perf | ci
```

示例：

```
feat(cli): 新增 --since/--until 时间窗参数
fix(stats): 空仓库下 authors 计数错误
docs(readme): 补充 Windows 已知问题
```

## 版本与变更日志

- 版本遵循 [SemVer](https://semver.org/lang/zh-CN/)：`MAJOR.MINOR.PATCH`；
- 版本号维护在 `src/git_repo_stats/__init__.py` 与 `pyproject.toml` 两处，需同步修改；
- 用户可见变更记录在 [CHANGELOG.md](CHANGELOG.md)（Keep a Changelog 风格），
  发版时由维护者统一更新。
