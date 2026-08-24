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

## 📦 技能清单 (Skills List)

| 序号 | 技能名称 | 适用领域 / 核心触发场景 | 核心功能与能力说明 |
| :---: | :--- | :--- | :--- |
| 1 | **`obsidian_archive`** | “总结到 Obsidian”、“保存到知识库” | 自动提取当前对话，基于任意 N 级深度递归审查算法，生成“三位一体”极速认知卡片并写入 `D:\obsidian-knows\` 目录 |
| 2 | **`agent_architecture_explainer`** | 剖析/讲解任何 Agent 架构时 | 基于 Agent 4 步固定主循环（输入→分析→调用工具→反思容灾）进行 4 维解构，并对比 Demo 做法与工业级架构师做法 |
| 3 | **`claude_code_agent_design_guide`** | 构思/设计/开发新 Agent 时 | 提供 Claude Code 范式、Pi Agent 极简微核范式与企业私有模型 A+B 融合范式的选型及阶梯式构建指南 |
| 4 | **`agy-customizations`** | Antigravity 定制与扩展开发 | 深度解析 Antigravity 自定义体系（Skills、Rules、Plugins、Hooks、MCP Servers 及加载优先级机制） |
| 5 | **`antigravity_guide`** | Antigravity 官方功能查阅与使用 | Google Antigravity (AGY) 综合指南、CLI / IDE / SDK 快速索引、Slash Commands 与环境配置手册 |
| 6 | **`gemini-api-dev`** | Gemini & Gemma 模型应用开发 | Gemini API 与 Gemma 4 模型开发指南（多模态音视频、函数调用、结构化输出、多语言 SDK 最佳实践） |
| 7 | **`gemini-interactions-api`** | Gemini Interactions API 开发 | Interactions API 规范（文本生成、多轮对话、流式响应、后台异步研究任务、旧版 API 迁移） |
| 8 | **`gemini-live-api-dev`** | 实时音视频流式交互应用 | Gemini Live API 实时双向音视频流式交互开发（WebSocket、VAD 语音活动检测、原生音频、实时翻译） |
| 9 | **`gemini-omni-flash-api`** | 视频生成与音视频处理工作流 | Gemini 视频编辑与生成（文本生视频、首帧动画、ffmpeg 视频预处理优化脚本与并行渲染） |
| 10 | **`google-antigravity-sdk`** | 自主多智能体系统开发 | Google Antigravity (AGY) SDK 自主智能体与多智能体系统（Multi-Agent）设计、编排与调试实战 |

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
无需任何手动复制，全局人设与全部 10 个 Skill 将自动完成加载并全局生效！

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
