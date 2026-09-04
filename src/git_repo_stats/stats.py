"""仓库统计采集与渲染（v0.1）。

设计原则：
- 纯只读：只调用 git 的查询类命令，绝不修改目标仓库；
- 可空仓运行：HEAD 不存在时给出零值统计而不是崩溃；
- 输出双模：table（人读）/ json（机器读），为后续接入脚本留口。
"""

from __future__ import annotations

import json
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any

from . import git_cmd


def _ext_of(name: str) -> str:
    """取文件扩展名（含点，小写）；无扩展名归为 '(none)'。"""
    base = name.rsplit("/", 1)[-1]
    if "." in base[1:]:
        return base.rsplit(".", 1)[-1].lower()
    return "(none)"


def _branch(repo: Path) -> str:
    """当前分支；detached HEAD 时返回短 hash 说明。"""
    branch = git_cmd.safe_run(repo, ["symbolic-ref", "--short", "HEAD"]).strip()
    if branch:
        return branch
    head = git_cmd.safe_run(repo, ["rev-parse", "--short", "HEAD"]).strip()
    return f"(detached @ {head})" if head else "(无提交)"


def _recent_commits(repo: Path, n: int) -> list[dict[str, str]]:
    """最近 n 条提交：短 hash / 作者 / 相对日期 / 主题。"""
    if not git_cmd.has_commits(repo):
        return []
    raw = git_cmd.safe_run(
        repo,
        [
            "log",
            "--no-merges",
            f"-{n}",
            "--pretty=format:%h%x1f%an%x1f%ar%x1f%s",
        ],
    )
    commits: list[dict[str, str]] = []
    for line in raw.splitlines():
        if not line:
            continue
        parts = line.split("\x1f")
        if len(parts) == 4:
            commits.append(
                {
                    "hash": parts[0],
                    "author": parts[1],
                    "date": parts[2],
                    "subject": parts[3],
                }
            )
    return commits


def _contributors(repo: Path, limit: int) -> list[dict[str, Any]]:
    """贡献者 top N（按提交数，忽略 merge）。"""
    raw = git_cmd.safe_run(repo, ["shortlog", "-sn", "--no-merges", "HEAD"])
    rows: list[dict[str, Any]] = []
    for line in raw.splitlines()[:limit]:
        line = line.strip()
        if not line:
            continue
        count, _, name = line.partition("\t")
        if count.isdigit() and name:
            rows.append({"name": name, "commits": int(count)})
    return rows


def _files(repo: Path) -> tuple[int, list[dict[str, Any]]]:
    """跟踪文件数 + 扩展名分布 top N（统计全部跟踪文件，不做二进制过滤）。

    用 ls-files -z 以 NUL 分隔文件名，配合 quotePath=false：
    任意文件名（中文、空格、换行）都不会破坏解析。
    """
    raw = git_cmd.safe_run(repo, ["ls-files", "-z"])
    names = [n for n in raw.split("\x00") if n]
    counter: Counter[str] = Counter()
    for name in names:
        ext = _ext_of(name)
        counter[ext if ext != "(none)" else "(none)"] += 1
    top = [
        {"extension": ext, "count": count}
        for ext, count in counter.most_common(10)
    ]
    return len(names), top


def _dirty(repo: Path) -> bool:
    status = git_cmd.safe_run(repo, ["status", "--porcelain"]).strip()
    return bool(status)


def collect(repo_path: str, limit: int = 10, recent: int = 5) -> dict[str, Any]:
    """采集一个仓库的统计快照。repo_path 为仓库顶层绝对路径。"""
    repo = Path(repo_path)
    committed = git_cmd.has_commits(repo)
    file_count, ext_top = _files(repo)
    branch = _branch(repo)
    total_commits = (
        int(git_cmd.safe_run(repo, ["rev-list", "--count", "HEAD"]).strip() or "0")
        if committed
        else 0
    )
    authors = len(_contributors(repo, limit=100000))
    return {
        "repo": repo_path,
        "branch": branch,
        "commits": total_commits,
        "authors": authors,
        "files": file_count,
        "dirty": _dirty(repo),
        "contributors": _contributors(repo, limit)[:limit],
        "extensions": ext_top,
        "recent_commits": _recent_commits(repo, recent),
        "generated_at": datetime.now().isoformat(timespec="seconds"),
    }


def render_table(data: dict[str, Any]) -> str:
    """渲染为人类可读的文本块（不依赖 CJK 宽度对齐，跨平台稳定）。"""
    lines: list[str] = []
    lines.append("Git Repository Stats")
    lines.append("=" * 21)
    lines.append(f"仓库顶层   : {data['repo']}")
    lines.append(f"当前分支   : {data['branch']}")
    lines.append(f"提交总数   : {data['commits']}")
    lines.append(f"贡献者总数 : {data['authors']}")
    lines.append(f"跟踪文件数 : {data['files']}")
    lines.append(f"工作区状态 : {'有未提交改动' if data['dirty'] else '干净'}")

    if data["contributors"]:
        lines.append("")
        lines.append("贡献者 Top")
        lines.append("-" * 11)
        for row in data["contributors"]:
            lines.append(f"{row['commits']:>5}  {row['name']}")

    if data["extensions"]:
        lines.append("")
        lines.append("文件类型 Top")
        lines.append("-" * 13)
        for row in data["extensions"]:
            lines.append(f"{row['count']:>5}  {row['extension']}")

    if data["recent_commits"]:
        lines.append("")
        lines.append("最近提交")
        lines.append("-" * 8)
        for c in data["recent_commits"]:
            lines.append(f"{c['hash']}  {c['date']:<10} {c['author']}  {c['subject']}")

    return "\n".join(lines)


def render_json(data: dict[str, Any]) -> str:
    """渲染为 JSON（机器可读，供脚本/仪表盘消费）。"""
    return json.dumps(data, ensure_ascii=False, indent=2)
