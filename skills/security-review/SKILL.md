---
name: security-review
description: >-
  编写或审查涉及用户认证与鉴权、敏感数据处理、外部用户输入、API 接口暴露、第三方调用或支付交易等功能时触发。提供全面的 OWASP Top 10 防御范式与安全走查清单。
---

# 软件工程安全审查规范 (Security Review Protocol)

> **“安全不是交付前的打补丁，而是架构与编码时的肌肉记忆。”**  
> 任何涉及认证鉴权、输入输出、敏感数据和接口暴露的代码，必须经过防御性安全审查。

---

## 零、 核心铁律 (The Iron Laws of Security)

1. **绝对禁止硬编码凭据**：严禁在代码、注释或配置文件中留有真实 API Key、私钥或测试账密。
2. **所有输入皆不可信**：SQL 查询、系统命令、文件路径、HTML 渲染必须经过严格参数化与消毒。
3. **默认拒绝（Default Deny）**：所有接口默认必须鉴权，未明确声明公开的路由一律禁止匿名访问。
4. **水平与垂直越权必防（IDOR 防御）**：操作任何资源时，不仅要查 `id`，必须强制校验属于当前登录用户的 `user_id`。

---

## 一、 OWASP 核心漏洞防御规范

### 1. 注入防御 (SQL & Command Injection)
* **SQL 注入**：
  ```typescript
  // ❌ 极危：直接拼接 SQL
  const sql = `SELECT * FROM users WHERE username = '${username}'`;
  
  // ✅ 安全：参数化绑定 / ORM
  const sql = `SELECT * FROM users WHERE username = $1`;
  await db.query(sql, [username]);
  ```
* **命令执行注入**：
  ```typescript
  // ❌ 极危：使用 child_process.exec 拼接用户输入
  exec(`ping -c 1 ${userInput}`);
  
  // ✅ 安全：使用 execFile 并传入固定参数数组，或完全避免 shell 执行
  execFile('/bin/ping', ['-c', '1', validatedIp]);
  ```

### 2. 身份认证与凭据保护
* **密码哈希**：绝对禁止 MD5 / SHA256 加盐，必须使用 **Argon2id** 或 **Bcrypt**（Cost factor >= 12）。
* **JWT 规范**：
  - 必须显式限定算法（如 `algorithms: ['HS256']`），严禁允许 `none` 算法；
  - 敏感 Token 必须通过 `HttpOnly, Secure, SameSite=Lax/Strict` Cookie 传输，防止 XSS 窃取。

### 3. 对象级别越权 (BOLA / IDOR)
```typescript
// ❌ 极危：仅根据路由参数 id 更新文档，用户可以随意改其他人的数据
router.post('/documents/:id', async (req, res) => {
  await Document.update(req.body, { where: { id: req.params.id } });
});

// ✅ 安全：强制将资源归属与当前登录用户绑定
router.post('/documents/:id', async (req, res) => {
  const count = await Document.update(req.body, {
    where: { 
      id: req.params.id, 
      ownerId: req.user.id // 强制用户所有权校验
    }
  });
  if (count === 0) return res.status(404).json({ error: "资源不存在或无权访问" });
});
```

### 4. 敏感信息泄露与日志审计
* 日志打印前必须脱敏（脱敏字段：`password`, `token`, `authorization`, `creditCard`, `phone`）。
* API 响应统一收敛，严禁将数据库原始报错（Stack Trace）或内部架构信息直接抛给前端客户端。

---

## 二、 接口暴露与防暴破规范

1. **频率限制（Rate Limiting）**：
   - 登录、注册、密码找回、短信验证码、LLM 代理接口必须挂载限流中间件（例如每个 IP 每分钟不超过 5 次）。
2. **请求体大小限制**：
   - 明确限制 JSON 请求体大小（如 `express.json({ limit: '1mb' })`），防止巨型 Payload 导致内存耗尽（DoS）。
3. **CORS 策略**：
   - 生产环境严禁配置 `Access-Control-Allow-Origin: *`，必须配置确定的白名单域名。

---

## 三、 安全走查清单 (Security Review Checklist)

- [ ] **鉴权与权限**：每个新增的端点是否都有明确的身份认证与角色/权限校验？
- [ ] **数据所有权**：数据库增删改查是否都有 `WHERE user_id = current_user.id` 约束？
- [ ] **参数校验**：所有外部输入是否使用了强类型验证器（如 Zod, Joi, Pydantic）？
- [ ] **XSS / 内容渲染**：动态渲染富文本或 HTML 时是否使用了 DOMPurify 清洗？
- [ ] **日志脱敏**：控制台与持久化日志中是否排除了密钥、Token、手机号等 PII 数据？
- [ ] **依赖安全**：本次引入的新第三方包是否已经过可信度与安全性审查？
