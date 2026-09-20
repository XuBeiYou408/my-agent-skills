# engineering-delivery-pipeline — 深度工程交付流水线编排技能

> 版本：v1.0 · 部署：Antigravity 技能目录（`~/.gemini/config/skills/engineering-delivery-pipeline/`）
> 面向：完整软件功能/需求的**全生命周期自动推进**，替代"每走一步手动叫下一个技能"。

## 它解决什么

当用户提出一次**交付级开发需求**（完整功能、全栈应用、数据库演进、复杂重构、生产级排障），本技能被自动激活后，作为**流水线驱动者**依序调度既有 26 个工程技能，自动把上一阶段产出作为下一阶段输入，全程链式推进；仅在**两个方向卡点**停下让用户拍板。纯咨询、命令查询、单行脚本与微调**不触发**。

## 工作方式（零常驻规则）

- **门卫即 description**：技能清单里该技能的 `description` 充当入口判定（高置信触发特征 + 硬排除），日常咨询零打扰，全文契约按需加载。
- **状态靠产物锚定**：不依赖对话记忆判断进度，以 `docs/superpowers/specs|plans/` 下的落盘产物为准，上下文压缩也不丢状态。
- **中枢增强**：`using-superpowers` 中枢新增一行映射，命中交付级需求时优先路由至此技能（未改动其既有触发铁律）。

## 流水线（7 阶段 · 两处确认）

| 阶段 | 内容 | 关键技能 | 确认点 |
| :--- | :--- | :--- | :--- |
| S1 | 需求审讯 | grill-me / brainstorming | 🔴 **确认①**（需求摘要拍板） |
| S2 | 开源调研 + 极简架构 | github_homework_researcher / ponytail | — |
| S3 | 实施计划 | writing-plans | 🔴 **确认②**（计划批准） |
| S4 | TDD 编码（领域伴随） | test-driven-development / database-migrations / docker-patterns / security-review | — |
| S5 | 根因排错 | systematic-debugging / safe_code_repair | 仅 S4 遇错进入 |
| S6 | 客观核验 + 脱敏 | verification-before-completion / repo-security-sanitizer | — |
| S7 | 分支收尾交付 | finishing-a-development-branch | 用户验收 |

> 确认①/② 是**内容拍板**（卡方向），批准后自动续跑，**无需用户叫下一步**；merge/push/删文件等危险动作不静默执行，交平台权限确认。

## 口令

| 意图 | 表述示例 | 效果 |
| :--- | :--- | :--- |
| 强制进入 | "深度交付 X / 完整流程 / 全流程开发 X" | 无条件启用流水线 |
| 退出/作废 | "退出完整流程 / 取消当前方案 / 不需要那么重" | 立即停流回到普通交互 |
| 中途降级 | "只要思路别走流程" | 跳轻量实现，产物保留 |

## 部署与生效

1. 目录 `~/.gemini/config/skills/engineering-delivery-pipeline/SKILL.md` 已就位；如会话未识别，重启 agy 会话即可。
2. 中枢映射已加至 `using-superpowers/SKILL.md`（Skill Priority 段，新增一行）。
3. 无需创建 `GEMINI.md` 或任何常驻全局规则——自动触发完全依赖 Antigravity 原生技能发现（description 门卫）。

## 自检验证（四场景）

在 agy 会话中逐一验证：

1. **完整需求自动进流**：提出"帮我开发一个待办清单 Web 应用" → 期望：先给 3 行流程摘要 → S1 审讯 → 确认① → S2/S3 → 确认② → S4 起自动推进。
2. **纯咨询不误触发**：问"什么是 Redis 缓存穿透？" → 期望：直答，不出现任何流程宣告。
3. **口令强制进入**：说"用完整流程开发登录模块" → 期望：无条件进入流水线。
4. **退出词降级**：流程中插一句"这个先简单做，别走流程" → 期望：停流，跳轻量实现。

## 已知边界

- 自动推进依赖执行模型遵循契约（纯规则方案的上限）；如某阶段未自动衔接，可用口令或明示"继续 S<N>"推进。
- 模型可能低置信漏激活：此时用进入口令一句话兜底。
