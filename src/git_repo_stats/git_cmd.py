"""Git 命令封装：统一 subprocess 调用与错误处理。

只依赖标准库与系统 git 可执行文件，保持零第三方依赖。
"""

from __future__ import annotations

import subprocess
from pathlib import Path

_TIMEOUT_SECONDS = 30


class NotARepositoryError(Exception):
    """目标路径不是 Git 仓库，或 git 命令不可用。"""


def _run(repo: Path, args: list[str]) -> str:
    """在 repo 目录下执行 git 命令，返回 stdout。

    统一带 -c core.quotePath=false：让 ls-files 等对中文/非 ASCII
    文件名原样输出，避免被转义为 "AI\\346\\227\\245.md" 形式的 C 串。
    """
    try:
        proc = subprocess.run(
            [
                "git",
                "-C",
                str(repo),
                "-c",
                "core.quotePath=false",
                *args,
            ],
            capture_output=True,
            text=True,
            timeout=_TIMEOUT_SECONDS,
        )
    except FileNotFoundError:
        raise NotARepositoryError("未找到 git 可执行文件，请先安装 Git。")
    except subprocess.TimeoutExpired:
        raise NotARepositoryError(f"git 命令超时：git {' '.join(args)}")

    if proc.returncode != 0:
        raise NotARepositoryError(
            proc.stderr.strip() or f"git 命令失败：git {' '.join(args)}"
        )
    return proc.stdout


def ensure_repo(path: Path) -> str:
    """确认 path 是 Git 仓库，返回其顶层目录绝对路径。"""
    try:
        top = _run(path, ["rev-parse", "--show-toplevel"]).strip()
    except NotARepositoryError as exc:
        raise NotARepositoryError(
            f"'{path}' 不是有效的 Git 仓库（{exc}）"
        ) from exc
    if not top:
        raise NotARepositoryError(f"'{path}' 不是有效的 Git 仓库")
    return top


def has_commits(repo: Path) -> bool:
    """仓库是否已有至少一次提交（HEAD 是否存在）。"""
    try:
        proc = subprocess.run(
            ["git", "-C", str(repo), "rev-parse", "--verify", "HEAD"],
            capture_output=True,
            text=True,
            timeout=_TIMEOUT_SECONDS,
        )
        return proc.returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False


def safe_run(repo: Path, args: list[str], default: str = "") -> str:
    """执行可能失败的 git 命令，失败时返回 default 而非抛异常。"""
    try:
        return _run(repo, args)
    except NotARepositoryError:
        return default
