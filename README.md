# 🐉 幼麟的 Agent 技能库与全局人设规范 (My Agent Skills)

本仓库包含了幼麟专属的通用 Agent 技能 (Skills) 规范、全局架构师人设规范与工具。一次托管在 GitHub，全 Agent 生态自动加载复用。

---

## 🎭 全局人设规范 (Global Persona & Specs)

- **核心规范文件**: [`GEMINI.md`](GEMINI.md) (Antigravity 全栈专家研发与执行规范 v2.0)
- **角色定位**: 拥有大厂 (Google / 阿里) L7+ 级别的全栈资深架构师水平与极致代码美学
- **称呼约定**: 尊称 user 为 **"幼麟"**
- **思维与交互**: **中文深度思考 (Thinking in Chinese)** + **中文专业交互 (Chinese Interaction)**
- **核心准则**: 
  - **单步追问与 95% 置信度原则**: 在给出最终实施方案前，一次仅提一个核心问题持续递进追问，达到 95% 置信度后再出方案。
  - **大厂生产级规范**: 防御性编程、强类型契约、零控制台金蝉脱壳机制、闭环交付与零死角日志。

---

## 📦 技能清单 (Skills List - 共 23 个)

| 序号 | 技能名称 | 核心能力与适用场景 |
| :---: | :--- | :--- |
| 1 | **`agent_architecture_explainer`** | 仅在用户要求对具体的 Agent 架构项目、开源 Agent 仓库、Agent 代码实现或系统工程进行深度分析、代码解构、架构走查与工程评估时触发。严格基于【Agent 4 步固定主循环（输入→分析→调用工具→反思容灾）】进行 4 维工程优化与安全防御拆解，并配合【Demo 开发者做法 vs 专业架构师做法】进行深度剖析。 |
| 2 | **`agy-customizations`** | Antigravity 自定义与扩展体系全景指南。当需要了解、配置或编写 Skills、Rules、Plugins、Hooks、MCP Servers 及其加载优先级与发现机制时触发。 |
| 3 | **`archify`** | 当用户需要对代码仓库进行架构全景分析、生成高保真交互式系统地图（System Map）、绘制复杂时序调用链（Sequence）、评估重构影响面（Blast Radius/Reach Tracing）、或准备发布项目并在自述文档（README.md）中嵌入高颜值架构封面图时触发。 |
| 4 | **`brainstorming`** | 在进行任何创意构思、新功能原型设计、行为变更或组件规划前必须触发。用于在动手写代码前深入探索用户真实意图、明确需求边界与架构方案。 |
| 5 | **`claude_code_agent_design_guide`** | 当用户准备设计、架构或构建新的 Agent 系统时，主动对比并推荐 Claude Code 垂直一体化架构、Pi Agent 极简微核架构以及企业私有模型 A+B 融合架构，根据需求给出推荐理据，待用户确认后引导一步步拆解构建。 |
| 6 | **`dispatching-parallel-agents`** | 当面临 2 个及以上没有状态共享或时序依赖的独立任务时触发，用于并行分发多个子 Agent 协同加速执行。 |
| 7 | **`executing-plans`** | 当已有编写完备的实施计划（Implementation Plan）且需要在会话中按检查点逐步执行和复核时触发。 |
| 8 | **`finishing-a-development-branch`** | 当代码实现已完成、所有测试均已通过，需要收尾、合并开发分支、清理工作区或决定如何集成代码时触发。 |
| 9 | **`github_homework_researcher`** | “写代码前，先去 GitHub 抄作业”——前置尽职调查与开源对标 Skill。杜绝 AI 闭门造车和盲目自创“方形轮子”。当用户提出新项目开发、新功能构想、技术选型、架构设计，或表达“我要做个...”、“帮我开发...”、“先调研一下”、“去 GitHub 看看”、“抄作业”、“找开源参考”时自动激活。强制在编写任何一行代码前，先通过 GitHub/开源调研提炼真实验证过的方案、踩坑历史与设计取舍，输出【选型、架构、MVP范围、开发顺序】四件套并等待确认。 |
| 10 | **`impeccable_taste_frontend`** | 当用户提出任何前端开发、UI/UX 设计、页面编写、界面重构、视觉样式走查、细节打磨、品牌看板/生图提示词生成、参考图复刻或口语化设计需求时触发。深度融合 Taste-Skill（反劣质模板审美注入、风格预设、生图提示词、旋钮参数）与 Impeccable（设计语义工程与 59 条反模式防御）。无需用户记忆任何斜杠命令，自动将口语化自然语言精准映射到底层 23 维设计工程指令与审美参数，输出工业级高审美前端代码。 |
| 11 | **`obsidian_archive`** | 当用户（幼麟）表达将当前对话/研讨内容总结保存或归档到 Obsidian 的意愿时触发（例如：“总结到 Obsidian”、“保存到知识库”、“归档当前会话”等）。自动提取上下文，执行支持任意 N 级深度目录树的递归审查与复用算法，强制在模块子目录下创建全景索引卡片（中英双语专业术语 + 口语化双解构），带 YAML Frontmatter 写入 D:\obsidian-knows\ 目录。 |
| 12 | **`ponytail`** | 极简资深架构师（Ponytail·懒人架构）思维注入 Skill。杜绝 AI 过度设计、画蛇添足、滥装三方依赖与样板代码膨胀。严格执行 7 阶极简决策天梯（YAGNI -> 现有代码复用 -> 标准库 -> 平台原生特性 -> 现有依赖 -> 单行代码 -> 最小可用代码）。在用户提出编码、重构、修Bug、选型或表达“写简单点”、“别过度设计”、“YAGNI”、“最简实现”、“不要引新包”、“单行解决”时自动激活。 |
| 13 | **`receiving-code-review`** | 当收到代码审查（Code Review）反馈时触发。在实施修改建议前进行技术严谨性与合理性验证，坚决杜绝盲目迎合或无脑修改。 |
| 14 | **`requesting-code-review`** | 当完成重大功能开发、核心任务交付或准备合并分支前触发。用于发起严格的代码审查，验证代码是否完全符合设计规范与质量要求。 |
| 15 | **`safe_code_repair`** | 当需要修改项目中代码、排查与修复 Bug、或进行缺陷诊断修复时触发。强制执行“工作区状态与安全前置、纯读诊断复现、三因分析范围锁死、用户确认最小改动、双轨回归与可回滚验证”的高可靠闭环流程。 |
| 16 | **`subagent-driven-development`** | 当执行包含多个独立任务的复杂实施计划时触发。通过在当前会话中驱动专属子 Agent 分工协作完成开发。 |
| 17 | **`systematic-debugging`** | 当遇到任何 Bug、测试失败或异常非预期行为时触发。在提出任何修复方案前，强制执行系统化四阶段根因诊断，杜绝盲目修补。 |
| 18 | **`test-driven-development`** | 在实现任何新功能、重构或修复 Bug 时触发。严格执行 TDD 测试驱动开发（先写失败测试，再写最小通过代码，最后重构）。 |
| 19 | **`using-git-worktrees`** | 当开启需要与当前工作区分离的独立功能开发，或在执行实施计划前触发。通过 Git Worktree 创建物理隔离的工作目录，避免代码污染。 |
| 20 | **`using-superpowers`** | 在开始任何对话或任务时触发。建立技能优先调度机制，强制在执行任何操作或回答前优先检索并激活匹配的专业 Skill。 |
| 21 | **`verification-before-completion`** | 在宣称任务完成、修复成功或提交 PR 之前触发。强制运行验证命令并核验确凿证据，坚决杜绝无证据的主观臆断。 |
| 22 | **`writing-plans`** | 当面对多步骤复杂任务且已有明确规范或需求时触发。在触碰任何代码前，编写结构化、可执行的高质量实施计划。 |
| 23 | **`writing-skills`** | 当需要创建新 Skill、修改现有 Skill 或在部署前验证 Skill 有效性时触发。提供专业的 Skill 架构规范与最佳实践。 |

---

## ⚡ 极速加载指南 (How to Load)

### 1. 对 Antigravity 或其他具备终端能力 Agent 的极简口令

在对话中直接发送以下这句口令给 Agent：

> 🗣️ **“请帮我拉取并配置我的 GitHub 技能库：`https://github.com/XuBeiYou408/my-agent-skills`”**

Agent 接收到链接后，会**全自动**执行：
```bash
git clone https://github.com/XuBeiYou408/my-agent-skills.git
python my-agent-skills/setup.py
```
无需任何手动复制，全局人设与全部 Skill 将自动完成加载并全局生效！

---

### 2. 在 Kimi 桌面端使用

- **方法 A (Prompt 快速模式)**：直接打开 `GEMINI.md` 或 `skills/` 目录下对应 Skill 的 `SKILL.md`，复制代码内容粘贴到 Kimi 桌面端的“自定义角色 / Agent 提示词”中。
- **方法 B (MCP 自动化模式)**：在 Kimi 桌面端的 MCP 插件设置中，添加本仓库提供的本地 MCP 写盘工具服务，即可在 Kimi 桌面端实现自动写入 Obsidian。

---

### 3. 在 Claude Code 等命令行 Agent 中使用

直接引用本仓库中的 `GEMINI.md` 作为项目/全局指导规范（如软链或复制至 `CLAUDE.md`），或通过 `setup.py` 自动部署技能。

---

## 🛠️ 本地安装 (Manual Installation)

如果您希望在本地手动安装：
```bash
git clone https://github.com/XuBeiYou408/my-agent-skills.git
cd my-agent-skills
python setup.py
```
