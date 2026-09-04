# repo链接 · 本仓库 GitHub 地址与验证

## 仓库地址（公开）

```
https://github.com/a976xw7td/c5-git-repo-stats
```

## 验证方式

```bash
# 1) 确认仓库公开可访问
git ls-remote https://github.com/a976xw7td/c5-git-repo-stats.git HEAD

# 2) 克隆到本地
git clone https://github.com/a976xw7td/c5-git-repo-stats.git

# 3) 查看提交历史（5 组 Conventional Commits）
cd c5-git-repo-stats && git log --oneline

# 4) 运行测试（9 passed）
python3 -m pytest tests/ -q
```

## 说明

- 仓库为 C5 挑战（ch-20260717031503-ihozqu）的交付载体：**git-repo-stats v0.1** —— 一个只读的 Git 仓库统计 CLI（Python，table/json 输出，可 pip 安装）。
- 公开时间：2026-09-04；main 分支由本地 5 组语义化提交推送建立，CI（py3.9/3.11/3.13）已通过。
