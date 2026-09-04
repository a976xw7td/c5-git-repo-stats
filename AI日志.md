# AI日志 · C5 GitHub Repository（git-repo-stats v0.1）

> 学生：张浩（2023108600001）｜ 挑战：C5 GitHub Repository（ch-20260717031503-ihozqu）｜ 日期：2026-09-04
> 本文件记录本次"公开、可验证技术能力仓库"构建的 AI 协作全过程：每轮的目标、人的决策、AI 的动作与可复核证据（commit / 文件 / 测试输出）。原则：**涉及外部副作用（建仓、推送、平台提交）之前，一律停下等人工确认。**

## 0. 分工原则

- **人（学生）负责**：定目标、选主题、拍板取舍、审阅产物、授权（GitHub OAuth）与确认提交；
- **AI 负责**：执行构建（代码 / 文档 / 脚本）、给出可核验证据、主动发现风险（如 OAuth scope 缺失）；
- **一条红线**：不替人做对外决策；每次发布 / 授权前先说明并等待。

## 1. 协作时间线

### R1 主题定稿 —— 决策在人
| 项 | 内容 |
|---|---|
| 输入 | C5 要求"建立公开、可验证的技术能力"；上一挑战（C5A）已交付过 shell 统计脚本 `git-repo-stats.sh` |
| 人的决策 | 把它升级为**可安装、可测试、带 CI 的 Python CLI 开源仓库**（git-repo-stats v0.1），复用 C5A 资产并体现增量能力，而非另起一个空壳 |
| AI 动作 | 对照 shell 版功能（统计提交/作者/文件等），给出 Python 化方案：src layout + pyproject + 只读 CLI（table/json 输出），明确**不做任何写操作** |
| 证据 | 本仓库根目录结构、`pyproject.toml` |

### R2 骨架与核心实现
- **AI 实现**：`src/git_repo_stats/{cli,git_cmd,stats}.py` + 控制台入口（entry_points），`git` 通过 subprocess 调用并处理非零退出码；输出支持表格与 JSON 两种格式。
- **人**：审阅功能范围（只读统计），确认命名与边界。
- **证据**：commit `d238a90` chore(packaging)、`bbe165e` feat(read-only CLI, table/json)。

### R3 测试
- **AI 写测试**：pytest 用例覆盖 CLI 输出与 git 调用边界。
- **证据**：`tests/test_cli.py`；本地运行 `9 passed`（1.10s）。

### R4 AI 主动自查清理
- **AI 复查**发现 `stats.py` 残留未使用常量 `_BINARY_EXTS`、docstring 表述误导（暗示做了二进制过滤，实际无此逻辑），主动删除并重写 docstring，**无行为变更**，回归通过。
- **证据**：`stats.py` 当前内容（sha256 608c4bb…）、清理提交记录。

### R5 开源要素补齐
- **AI 起草**：README（定位/安装/用法/输出示例）、MIT LICENSE、CONTRIBUTING、CHANGELOG（Keep a Changelog 风格）、`.github` 的 issue 模板 ×2（bug/feature）、PR 模板、CI（py3.9 / 3.11 / 3.13 矩阵）。
- **人**：审阅 README，核对安装与用法部分与实现一致。
- **证据**：commit `848b875` ci、`11135f4` docs；GitHub Actions 首次运行 **success**。

### R6 Git 规范化与发布（外部副作用 → 人工授权）
- **AI**：`git init -b main`；按 Conventional Commits 语义分组提交（chore→feat→test→ci→docs，共 5 组）；`gh repo create --public` 建公开仓。
- **卡点**：首次 `git push` 被 GitHub 拒绝——OAuth token 缺 `workflow` scope（仓库含 CI 文件）。AI 定位根因并给出最小修复路径（`gh auth refresh -s workflow` 设备码授权）。
- **人**：完成设备码授权（一次性码 827A-E9E2，https://github.com/login/device）。
- **结果**：重推成功 `origin/main`；远程 CI 排队并 **success**。
- **证据**：`git log --oneline`（5 组提交）、远程 `https://github.com/a976xw7td/c5-git-repo-stats`、`gh run list`。

### R7 交付文档（本文件所在轮）
起草 `AI日志.md` / `拿来说明.md` / `repo链接.md` / `docs/AAR.md` 四份课程交付物，与开源仓库文档并存，提交前再次人工确认。

## 2. 纠错记录

| 问题 | 根因 | 处理 | 证据 |
|---|---|---|---|
| push 被 GitHub 拒绝 | OAuth token 缺 `workflow` scope（推送含 CI 的仓库必需） | 人工设备码授权补 scope 后重推 | 推送成功、CI success |
| `stats.py` 含死代码与误导 docstring | 初版冗余，自查遗漏 | 删除 `_BINARY_EXTS`、重写 docstring | `stats.py` 当前内容 |
| C5 详情直连接口 404 | 平台接口形态为 query 参数而非路径 | 改用 `/api/challenges?challengeId=…` 取到交付物与 rubric | 交付物字段 `README.md,*repo链接*,*AI日志*,*拿来说明*` |

## 3. 局限与诚实声明

1. 仓库功能范围为**只读 git 统计**，不含任何写/破坏性 git 操作，这是有意的边界而非缺陷；
2. CI 覆盖 Python 3.9 / 3.11 / 3.13 三版本矩阵，全部绿；
3. 所有 AI 产物均经人审阅后才入库；建仓、推送、平台提交等外部动作前均先征得同意并记录于此。
