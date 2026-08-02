# 🐉 幼麟的 Agent 技能库 (My Agent Skills)

本仓库包含了幼麟专属的通用 Agent 技能 (Skills) 规范与工具。一次托管在 GitHub，全 Agent 生态自动加载复用。

---

## 📦 技能清单 (Skills List)

| 技能名称 | 核心触发表达 | 核心功能说明 |
| :--- | :--- | :--- |
| **`obsidian_archive`** | “总结到 Obsidian”、“保存到知识库” | 自动提取当前对话，基于任意 N 级深度递归审查算法，生成“三位一体”极速认知卡片并写入 `D:\obsidian-knows\` 目录 |
| **`agent_architecture_explainer`** | 剖析/讲解任何 Agent 架构时 | 基于 Agent 4 步固定主循环（输入→分析→调用工具→反思容灾）进行 4 维解构，并对比 Demo 做法与工业级架构师做法 |
| **`claude_code_agent_design_guide`** | 构思/设计/开发新 Agent 时 | 提供 Claude Code 范式、Pi Agent 极简微核范式与企业私有模型 A+B 融合范式的选型及阶梯式构建指南 |

---

## ⚡ 极速加载指南 (How to Load)

### 1. 对 Antigravity 或其他具备终端能力 Agent 的极简口令

在对话中直接发送以下这句口令给 Agent：

> 🗣️ **“请帮我拉取并配置我的 GitHub 技能库：`https://github.com/[您的GitHub用户名]/my-agent-skills`”**

Agent 接收到链接后，会**全自动**执行：
```bash
git clone https://github.com/[您的GitHub用户名]/my-agent-skills.git
python my-agent-skills/setup.py
```
无需任何手动复制，技能将自动完成加载并全局生效！

---

### 2. 在 Kimi 桌面端使用

- **方法 A (Prompt 快速模式)**：直接打开 `skills/` 目录下对应 Skill 的 `SKILL.md`，复制代码内容粘贴到 Kimi 桌面端的“自定义角色 / Agent 提示词”中。
- **方法 B (MCP 自动化模式)**：在 Kimi 桌面端的 MCP 插件设置中，添加本仓库提供的本地 MCP 写盘工具服务，即可在 Kimi 桌面端实现自动写入 Obsidian。

---

## 🛠️ 本地安装 (Manual Installation)

如果您希望在本地手动安装：
```bash
git clone https://github.com/[您的GitHub用户名]/my-agent-skills.git
cd my-agent-skills
python setup.py
```
