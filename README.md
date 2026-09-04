# git-repo-stats

![CI](https://github.com/a976xw7td/c5-git-repo-stats/actions/workflows/ci.yml/badge.svg)
![Python](https://img.shields.io/badge/python-3.9%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Version](https://img.shields.io/badge/version-0.1.0-orange)

> 一条命令，洞察任意 Git 仓库：提交总数、贡献者、分支、文件结构与工作区状态。
> **纯 Python 标准库实现，零第三方依赖**，table / JSON 双输出，可人读、可进脚本。

`git-repo-stats` 是一个为"快速读懂一个陌生仓库"而生的命令行小工具。它把最常用的
仓库体检信息——提交了多少次、谁在贡献、当前在哪个分支、有没有未提交改动、代码以
什么文件类型为主——压缩成一条命令。设计目标：**只读、零依赖、随处可跑**。

## ✨ 特性

- **仓库体检**：提交总数、贡献者总数、当前分支、跟踪文件数、工作区是否干净
- **贡献者 Top N**：按提交数排序（自动忽略 merge commit）
- **文件类型分布**：跟踪文件按扩展名统计 Top 10
- **最近提交**：短 hash / 作者 / 相对时间 / 主题，一眼看出项目最近在忙什么
- **双输出格式**：`table`（人读，对齐友好）与 `json`（机器读，可管道给脚本）
- **可空仓运行**：还没有任何提交的空仓库返回零值统计，不崩溃
- **纯只读**：只调用 git 查询命令，绝不修改目标仓库；非仓库路径返回明确错误
- **零依赖**：只要 Python 3.9+ 和系统 git，无任何第三方包

## 📦 安装

```bash
# 方式一：源码安装（本仓库当前推荐方式）
git clone https://github.com/a976xw7td/c5-git-repo-stats.git
cd c5-git-repo-stats
pip install .

# 方式二：不安装，直接用模块运行（同样可用）
cd c5-git-repo-stats
PYTHONPATH=src python3 -m git_repo_stats.cli --help
```

> PyPI 发布计划见 [Roadmap](#-roadmap)；发布后可直接 `pip install git-repo-stats`。

## 🚀 快速开始

```bash
# 分析当前目录所在仓库
git-repo-stats .

# 分析任意仓库，输出 JSON（供脚本消费）
git-repo-stats --format json /path/to/repo

# 只看 Top 5 贡献者、最近 3 条提交
git-repo-stats --limit 5 --recent 3 /path/to/repo
```

### 输出示例（table）

在 [c5a-github-fundamentals](https://github.com/a976xw7td/c5a-github-fundamentals)
仓库上实测输出：

```
Git Repository Stats
=====================
仓库顶层   : /path/to/c5a-github-fundamentals
当前分支   : main
提交总数   : 6
贡献者总数 : 1
跟踪文件数 : 6
工作区状态 : 干净

贡献者 Top
-----------
    5  张浩

文件类型 Top
-------------
    4  md
    1  (none)
    1  sh

最近提交
--------
ed62dc8  10 hours ago 张浩  docs: 提交前复审——交付物移至根目录对齐平台 glob 校验
```

### 输出示例（JSON）

```json
{
  "repo": "/path/to/c5a-github-fundamentals",
  "branch": "main",
  "commits": 6,
  "authors": 1,
  "files": 6,
  "dirty": false,
  "contributors": [{"name": "张浩", "commits": 5}],
  "extensions": [{"extension": "md", "count": 4}],
  "recent_commits": [],
  "generated_at": "2026-09-04T12:00:00+08:00"
}
```

## ⚙️ 命令行参数

| 参数 | 说明 | 默认 |
|---|---|---|
| `path` | 目标 Git 仓库路径 | `.`（当前目录） |
| `-f, --format` | 输出格式：`table` / `json` | `table` |
| `--limit` | 贡献者 / 文件类型 Top N | `10` |
| `--recent` | 最近提交显示条数 | `5` |
| `-V, --version` | 显示版本号 | — |

## 🧩 设计原则与已知限制

1. **只读**：工具绝不执行任何会修改仓库的命令（无 checkout / reset / gc 等）。
2. **可空仓**：`git init` 后未提交的空仓库也能给出零值统计，便于 CI 里先行体检。
3. **中文友好**：文件名、作者名的非 ASCII 字符原样保留，不做 C 风格转义
   （`core.quotePath=false`），中文扩展名统计正确。
4. **已知限制（v0.1）**：
   - 浅克隆（shallow clone）的仓库无法统计完整历史；
   - 未跟踪文件（untracked）不计入文件数，但会让 `dirty=true`；
   - 统计的是**当前分支**的历史；如需全部分支统计，可先 `git fetch` 后检出新分支。

## 🛠️ 开发指南

```bash
git clone https://github.com/a976xw7td/c5-git-repo-stats.git
cd c5-git-repo-stats
pip install -e .          # 开发模式安装
python -m unittest discover -s tests -v   # 跑全部测试
```

- 提交信息遵循 [Conventional Commits](https://www.conventionalcommits.org/)；
- 新功能必须带测试；修 bug 请先写一个能复现的失败用例；
- 更多协作规范见 [CONTRIBUTING.md](CONTRIBUTING.md)。

## 🗺️ Roadmap

**v0.2（欢迎提 issue / PR）**
- [ ] 按作者聚合的行数变更统计（`--lines`）
- [ ] 支持 `--since/--until` 时间窗
- [ ] 子命令拆分：`git-repo-stats commits` / `contributors` / `files`
- [ ] 发布到 PyPI

## 📄 License

[MIT](LICENSE) © 2026 Zhang Hao

> 本工具源自课程挑战 C5A 中的一个 Bash 原型脚本（`git-repo-stats.sh`），
> 在此重写为零依赖 Python CLI 并开源，作为对"读懂仓库"方法论的工程化沉淀。
