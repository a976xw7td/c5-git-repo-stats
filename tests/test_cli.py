"""git-repo-stats 端到端 CLI 测试。

策略：在临时目录用真实 git 命令造最小仓库，再调用 cli.main()
断言退出码、stdout/stderr。测试本身也验证了"克隆后零依赖可跑"。
"""

from __future__ import annotations

import io
import json
import os
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

# 允许在未安装（未 pip install -e .）时直接从源码目录运行测试
SRC = Path(__file__).resolve().parents[1] / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from git_repo_stats.cli import main  # noqa: E402


def _git(repo: Path, *args: str) -> None:
    subprocess.run(
        ["git", "-C", str(repo), *args],
        check=True,
        capture_output=True,
        text=True,
    )


def make_repo(root: Path, name: str = "repo") -> Path:
    """创建一个含两次提交、两个作者的最小仓库。"""
    repo = root / name
    repo.mkdir()
    _git(repo, "init", "-q")
    _git(repo, "config", "user.email", "alice@example.com")
    _git(repo, "config", "user.name", "Alice")
    (repo / "app.py").write_text("print('hello')\n", encoding="utf-8")
    (repo / "README.md").write_text("# demo\n", encoding="utf-8")
    _git(repo, "add", ".")
    _git(repo, "commit", "-q", "-m", "feat: initial skeleton")
    _git(repo, "config", "user.email", "bob@example.com")
    _git(repo, "config", "user.name", "Bob")
    (repo / "app.py").write_text("print('hello v2')\n", encoding="utf-8")
    _git(repo, "add", ".")
    _git(repo, "commit", "-q", "-m", "fix: bump greeting")
    return repo


def run_cli(argv: list[str]) -> tuple[int, str, str]:
    out, err = io.StringIO(), io.StringIO()
    with redirect_stdout(out), redirect_stderr(err):
        code = main(argv)
    return code, out.getvalue(), err.getvalue()


class CliTest(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def test_non_repository_returns_error(self) -> None:
        code, out, err = run_cli([str(self.root)])
        self.assertEqual(code, 2)
        self.assertIn("不是有效的 Git 仓库", err)

    def test_nonexistent_path_returns_error(self) -> None:
        code, _, err = run_cli([str(self.root / "nope")])
        self.assertEqual(code, 2)
        self.assertIn("不是有效的 Git 仓库", err)

    def test_json_shape_on_real_repo(self) -> None:
        repo = make_repo(self.root)
        code, out, _ = run_cli(["--format", "json", str(repo)])
        self.assertEqual(code, 0)
        data = json.loads(out)
        self.assertEqual(data["commits"], 2)
        self.assertEqual(data["authors"], 2)
        self.assertGreaterEqual(data["files"], 2)
        self.assertIn("repo", data)
        self.assertIn("branch", data)
        self.assertIn("contributors", data)
        self.assertIn("extensions", data)
        self.assertIn("recent_commits", data)
        self.assertEqual(len(data["recent_commits"]), 2)

    def test_table_output_readable(self) -> None:
        repo = make_repo(self.root)
        code, out, _ = run_cli([str(repo)])
        self.assertEqual(code, 0)
        self.assertIn("提交总数   : 2", out)
        self.assertIn("Alice", out)
        self.assertIn("Bob", out)

    def test_contributors_sorted_desc(self) -> None:
        repo = make_repo(self.root)
        repo2 = repo
        # 再给 Alice 加一次提交，制造 2:1 的提交分布
        _git(repo2, "commit", "-q", "--allow-empty", "-m", "docs: note")
        _, out, _ = run_cli(["--format", "json", str(repo2)])
        data = json.loads(out)
        self.assertEqual(data["commits"], 3)
        names = [c["name"] for c in data["contributors"]]
        counts = [c["commits"] for c in data["contributors"]]
        self.assertEqual(counts, sorted(counts, reverse=True))
        # make_repo：Alice 1 次、Bob 2 次（第 2 次 + docs），Bob 应居首
        self.assertEqual(names[0], "Bob")

    def test_empty_repo_no_crash(self) -> None:
        repo = self.root / "empty"
        repo.mkdir()
        _git(repo, "init", "-q")
        code, out, _ = run_cli(["--format", "json", str(repo)])
        self.assertEqual(code, 0)
        data = json.loads(out)
        self.assertEqual(data["commits"], 0)
        self.assertEqual(data["authors"], 0)
        self.assertEqual(data["recent_commits"], [])

    def test_limit_and_recent_flags(self) -> None:
        repo = make_repo(self.root)
        code, out, _ = run_cli(
            ["--format", "json", "--limit", "1", "--recent", "1", str(repo)]
        )
        self.assertEqual(code, 0)
        data = json.loads(out)
        self.assertEqual(len(data["contributors"]), 1)
        self.assertEqual(len(data["recent_commits"]), 1)

    def test_extensions_detected(self) -> None:
        repo = make_repo(self.root)
        _, out, _ = run_cli(["--format", "json", str(repo)])
        data = json.loads(out)
        exts = {e["extension"]: e["count"] for e in data["extensions"]}
        self.assertEqual(exts.get("py"), 1)
        self.assertEqual(exts.get("md"), 1)

    def test_chinese_filenames_not_garbled(self) -> None:
        """中文文件名必须按 .md 统计一次，而不是被转义成 'md\"' 之类畸形扩展名。

        回归背景：git 默认 core.quotePath=true 会把中文文件名转义为
        C 风格引号串，导致扩展名解析出 'md\"' 条目。
        """
        repo = make_repo(self.root)
        (repo / "说明.md").write_text("使用说明\n", encoding="utf-8")
        (repo / "AI日志.md").write_text("协作记录\n", encoding="utf-8")
        _git(repo, "add", ".")
        _git(repo, "commit", "-q", "-m", "docs: 中文说明与日志")
        _, out, _ = run_cli(["--format", "json", str(repo)])
        data = json.loads(out)
        exts = {e["extension"]: e["count"] for e in data["extensions"]}
        self.assertEqual(exts.get("md"), 3)  # README + 说明 + AI日志
        self.assertNotIn("md\"", exts)
        # make_repo 基线 2 个文件（app.py/README.md）+ 新增 2 个中文名文件
        self.assertEqual(data["files"], 4)


if __name__ == "__main__":
    unittest.main()
