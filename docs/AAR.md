# AAR 复盘 · C5 git-repo-stats 开源仓库

> 复盘时间：2026-09-04 ｜ 作者：张浩（2023108600001）｜ 挑战：C5 GitHub Repository（ch-20260717031503-ihozqu）
> 框架：学到了什么 / 完成过程 / 与 AI 协作 / 卡点与突破 / 改进方向 / 归因

## 1. 学到了什么（七维）

| 维度 | 内容 |
|---|---|
| **知识** | 开源仓库专业度四件套（README 定位 + LICENSE + CONTRIBUTING + CHANGELOG）；issue 模板 / PR 模板的社区作用；GitHub OAuth token scope 体系（`repo` vs `workflow`）；src layout + pyproject 打包规范；Keep a Changelog 惯例 |
| **技能** | 独立走通"本地语义化提交 → 公开仓库 → CI 绿"全链路；`gh repo create --public`、`gh auth refresh -s workflow` 设备码授权；pytest 与 CLI 测试；table/json 双格式输出 CLI 设计 |
| **工具** | gh CLI、GitHub Actions（py3.9/3.11/3.13 矩阵）、pytest、git subprocess 封装 |
| **协作** | 与 AI 分工的新模式：**决策权明确在人**（选题/授权/确认），AI 负责执行与自查（主动清理死代码 = 超出指令的负责任行为）；"涉及外部副作用先停"原则再次验证有效 |
| **流程** | 挑战闭环复用：查详情（注意 API 形态）→ 定主题 → 本地构建 → 开源要素 → Git 规范化 → 授权推送 → 文档留证 → 预检提交 |
| **认知** | "公开可验证的技术能力"不是把代码放上去就完——评审看的是**仓库本身是否像个专业开源项目**（结构、文档、社区要素、CI），课程交付文档（AI日志/拿说明）是佐证而非主体 |
| **元认知** | 交付物 glob 与文件名必须**逐字节对齐**：C1 已踩过 `拿说明` vs `拿来说明` 的坑，这次先读接口原始字段（`*拿来说明*`）再命名，零返工——教训沉淀成了行动 |

## 2. 完成过程（时间线）

1. 定主题：把 C5A 已交付的 `git-repo-stats.sh` 升级为可安装 Python CLI（git-repo-stats v0.1）——理由：真实增量、可验证、不与 C5A 重复；
2. 搭骨架：src layout + pyproject + cli/git_cmd/stats 三模块，只读设计；
3. 测试：pytest 9 例覆盖 CLI 输出与 git 调用边界，本地全绿；
4. 自查清理：AI 发现 stats.py 死代码与误导 docstring，删除/重写，无行为变更；
5. 开源要素：README / MIT LICENSE / CONTRIBUTING / CHANGELOG / issue×2 / PR 模板 / CI；
6. Git 规范化：5 组 Conventional Commits（chore→feat→test→ci→docs）；
7. 发布：`gh repo create --public` → 首推被 GitHub 拒（缺 workflow scope）→ 设备码授权 → 重推成功 → CI success；
8. 交付文档：AI日志 / 拿说明 / repo链接 / AAR 四份，等人工确认后提交平台。

## 3. 与 AI 协作的过程评价

- **有效的模式**：AI 负责执行（编码/文档/脚本/建仓操作细节），我只做三类决策——**选什么**（主题、范围边界）、**授不授权**（OAuth、是否对外发布）、**认不认可**（审 README、确认文档）；
- **AI 的亮点**：① 主动把"二进制过滤 docstring 与实现不符"这种隐蔽问题挖出来修掉（超出字面指令的责任心）；② 推送被拒后没有绕路（没有建议降级成私有仓或删 CI），而是准确定位到 scope 并给出最小修复路径；③ 全程先核实后动手（先读平台接口形态再查详情）；
- **我的参与点**：主题选型、功能范围（只读边界）拍板、OAuth 设备码授权、README 与交付文档审阅。

## 4. 卡点与突破

| 卡点 | 突破 |
|---|---|
| 首推 GitHub 被拒：`refusing to allow an OAuth App to create or update workflow … without workflow scope` | 理解 GitHub token scope 模型：含 CI 的仓库需要 `workflow` 权限；用 `gh auth refresh -s workflow` 设备码授权补权，重推成功——**工具链报错不可怕，怕的是不读懂就乱试** |
| 交付物命名易错（C1 踩过 `拿说明` vs `拿来说明`） | 这次不靠猜：直接读平台 API 原始 `required_deliverables` 字段（`README.md,*repo链接*,*AI日志*,*拿来说明*`），按字节对齐命名 |
| 平台 get-challenge 直连 404 | 读客户端 runtime.js 源码发现接口形态是 query 参数（`/api/challenges?challengeId=…`），不再盲试 |

## 5. 改进方向（下次怎么做更好）

1. **推送前先查 scope**：凡仓库含 `.github/workflows/`，建仓前先 `gh auth status` 确认含 `workflow`，省一次被拒往返；
2. **交付物命名前置核对**：定稿前直接从 API 拉 `required_deliverables` 原文逐字节对齐，把 C1/C5 两次教训固化为固定第一步；
3. **README 与实现同步审**：这次 README 由人核对了安装命令，下次让 AI 顺带跑一遍 README 里的每条命令再入库（文档即测试）；
4. **更早引入 CI**：CI 矩阵在 docs 提交后才首跑，若早于功能提交建立，能第一时间抓平台差异问题。

## 6. 归因（为什么这次能完成）

| 因素 | 权重 | 说明 |
|---|---|---|
| 主题复用 | 30% | 基于 C5A 真实脚本升级，素材与方向天然清晰，避免"从零选题"摇摆 |
| 流程成熟 | 25% | C1/C5A 两轮沉淀的挑战闭环（查→定→建→验→授权→推→证）直接复用 |
| AI 执行质量 | 25% | 编码/自查/文档高质高效，卡点定位准确 |
| 元认知沉淀 | 20% | 上次教训（glob 对齐、查分用 submissionId）本轮直接生效，零返工 |

**一句话总结**：C5 让我把"会做的东西"做成了**专业开源仓库的样子**——最大的收获不是代码，而是理解了 GitHub 的权限模型与开源社区要素的评审视角；最大的教训是——**报错即文档，先读懂 scope 与接口，再动手。**
