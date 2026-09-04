# Changelog

本项目的所有用户可见变更都记录在此文件中。

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/)，
版本遵循 [Semantic Versioning](https://semver.org/lang/zh-CN/)。

## [Unreleased]

（暂无）

## [0.1.0] - 2026-09-04

### Added

- 首次发布：`git-repo-stats` 命令行工具，一条命令输出仓库体检信息
  - 提交总数、贡献者总数、当前分支、跟踪文件数、工作区是否干净
  - 贡献者 Top N（按提交数，忽略 merge）
  - 文件类型分布 Top N（扩展名统计）
  - 最近提交列表（短 hash / 作者 / 相对时间 / 主题）
- `table`（人读）与 `json`（机器读）双输出格式
- 可空仓运行：无提交的仓库返回零值统计，不崩溃
- 中文文件名友好：非 ASCII 文件名不做 C 风格转义，扩展名统计正确
- 零第三方依赖：仅使用 Python 标准库（3.9+）与系统 git
- MIT License；配套 GitHub Actions CI（Python 3.9 / 3.11 / 3.13）
