"""git-repo-stats 命令行入口。"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from . import __version__, git_cmd
from .stats import collect, render_json, render_table


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="git-repo-stats",
        description="一条命令洞察任意 Git 仓库：提交、贡献者、分支、文件结构。",
        epilog="示例：git-repo-stats --format json .",
    )
    parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="目标 Git 仓库路径（默认当前目录）",
    )
    parser.add_argument(
        "-f",
        "--format",
        choices=["table", "json"],
        default="table",
        help="输出格式：table（默认，人读）/ json（机器读）",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=10,
        help="贡献者/文件类型 Top N（默认 10）",
    )
    parser.add_argument(
        "--recent",
        type=int,
        default=5,
        help="最近提交显示条数（默认 5）",
    )
    parser.add_argument(
        "-V",
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        path = Path(args.path).expanduser().resolve()
        repo_top = git_cmd.ensure_repo(path)
        data = collect(repo_top, limit=args.limit, recent=args.recent)
    except git_cmd.NotARepositoryError as exc:
        print(f"错误：{exc}", file=sys.stderr)
        return 2

    output = render_json(data) if args.format == "json" else render_table(data)
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
