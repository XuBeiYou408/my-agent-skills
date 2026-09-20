---
name: repo-security-sanitizer
description: >-
  代码提交、开源发布、合并主分支或对现有代码库进行安全尽职调查时触发。执行敏感凭据脱敏扫描（API Key、Token、私钥）、依赖 CVE 漏洞体检与危险系统调用审查。
---

# 代码库脱敏与静态安全扫描规范 (Repo Security Sanitizer)

> **“一次不经意的 git push，可能让你的云账号在 5 分钟内被盗刷上万美元。”**  
> 在代码推送到远端或开源发布前，必须进行地毯式脱敏扫描与合规清理。

---

## 零、 核心铁律 (The Iron Laws of Sanitization)

1. **绝对禁止将已泄露的凭据“仅做删除提交”**：Git 提交历史中包含的凭据等同于完全公开泄露，必须彻底重写提交历史或立即吊销轮换。
2. **提交前必跑本地扫描**：必须确保 `.env`、证书、私钥完全处于 `.gitignore` 规则之下。
3. **一旦泄露立即吊销**：发现凭据推送到公网，第一优先级是到云平台控制台**吊销/轮换密钥**，而不是花时间争论如何删 Git。

---

## 一、 敏感凭据高危特征检索清单

在发布或合并前，运行以下关键字与正则检测：

| 凭据类型 | 常见特征 / 正则模式 | 处置要求 |
| :--- | :--- | :--- |
| **OpenAI / LLM API Key** | `sk-[a-zA-Z0-9]{20,}` / `sk-proj-` | 必须移入环境变量或本地 `.env` |
| **Anthropic API Key** | `sk-ant-[a-zA-Z0-9]{32,}` | 严禁出现在任何示例文件代码块中 |
| **AWS 访问密钥** | `AKIA[0-9A-Z]{16}` | 严重告警，立即移入 AWS Secret Manager |
| **GitHub Personal Token** | `ghp_[a-zA-Z0-9]{36}` / `github_pat_` | 立即吊销 |
| **私钥文件** | `-----BEGIN (RSA|EC|OPENSSH) PRIVATE KEY-----` | 绝对禁止提交到 Git |
| **内网 IP / 测试域名** | `10\.\d{1,3}\.\d{1,3}\.\d{1,3}` / `192\.168\.` | 开源前替换为 `example.com` 或环境变量 |

---

## 二、 依赖合规与漏洞扫描 (SCA)

在项目构建前，针对对应技术栈执行本地依赖审计：

### 1. Node.js 生态
```bash
# 检查已知高危 CVE
npm audit --audit-level=high
# 或 pnpm 审计
pnpm audit --prod
```

### 2. Python 生态
```bash
# 使用 pip-audit 扫描虚拟环境依赖
pip install pip-audit
pip-audit
```

### 3. Go 生态
```bash
# 官方漏洞扫描工具
go install golang.org/x/vuln/cmd/govulncheck@latest
govulncheck ./...
```

---

## 三、 危险函数与高危模式审查

走查代码中是否存在以下危险原型：
1. **动态执行代码**：
   - JavaScript: `eval()`, `new Function(...)`, `vm.runInContext(...)`
   - Python: `exec()`, `eval()`, `__import__(...)`, `pickle.loads(...)`（反序列化 RCE 风险）
2. **直接系统调用拼接**：
   - 检查所有 `child_process`, `subprocess`, `os.system` 调用，确认未拼接不可信输入。
3. **禁用 SSL 证书校验**：
   - 严禁出现 `rejectUnauthorized: false` 或 `verify=False`，测试环境也不允许带入生产。

---

## 四、 紧急补救指南：历史提交已泄露密钥怎么办？

如果敏感信息已经 commit 到了本地甚至 remote，单写一个 `git rm` 毫无意义。必须按如下流程处置：

```bash
# 1. 立即在服务商后台吊销该 Key 并重新生成！(最重要)

# 2. 从 Git 历史中彻底擦除该文件（推荐使用 git-filter-repo）
# 安装：pip install git-filter-repo
git filter-repo --path sensitive-config.json --invert-paths --force

# 3. 强制推送到远端（需团队沟通一致）
git push origin --force --all
```

---

## 五、 脱敏发布自查清单 (Sanitizer Checklist)

- [ ] 根目录与子目录是否配置了完善的 `.gitignore`（包含 `.env`, `*.pem`, `*.key`）？
- [ ] 全局搜索代码库，确认无任何真实的 `sk-`, `AKIA`, `password=` 等硬编码？
- [ ] 示例配置文件是否统一命名为 `.env.example`，并且其中的值全为占位符？
- [ ] 文档与测试用例中出现的 IP、邮箱、域名是否均为保留测试地址（如 `test@example.com`）？
- [ ] 依赖扫描工具输出为 0 高危/严重漏洞？
