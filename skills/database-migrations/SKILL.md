---
name: database-migrations
description: >-
  涉及数据库表结构变更、字段增删、索引调整、数据平滑迁移或实施零停机（Zero-Downtime）部署时触发。指导无锁变更、双写迁移、展开-收缩模式及主流 ORM（Prisma, TypeORM, Drizzle, Django, golang-migrate）最佳实践。
---

# 数据库安全平滑迁移规范 (Database Migration Protocol)

> **“代码可以随时回滚，数据库一旦被锁死或破坏，就是灾难事故。”**  
> 线上数据库的变更原则永远是：**不锁死业务表、不破坏向后兼容、永远具备回滚方案、分步平滑演进**。

---

## 零、 核心铁律 (The Iron Laws of Migrations)

1. **绝对禁止一次性做破坏性变更**：字段重命名、删除列、修改字段类型必须分多阶段进行（展开-收缩模式）。
2. **大表 DDL 必须无锁（Zero-Lock）**：严禁在生产高峰对高频大表执行全表阻塞锁操作。
3. **数据迁移必须分批执行（Batching/Chunking）**：严禁单条 SQL 更新数万行以上数据，必须限制每次更新批次并休眠释放锁。
4. **所有变更必须具备回滚策略（Down Migration / Rollback Plan）**：无法平滑回滚的脚本严禁上线。

---

## 一、 核心范式：展开与收缩模式 (Expand and Contract Pattern)

当需要重命名字段、拆分表或更改字段类型时，必须跨越至少两个发布周期，严禁一步到位：

```text
[Phase 1: 展开 (Expand)]
1. 新增目标字段（允许为 Null）
2. 业务代码双写（Dual-write）：读取旧字段，同时向新旧字段写入
3. 离线/后台分批将历史数据回填（Backfill）到新字段

[Phase 2: 切换 (Switch)]
1. 验证新旧字段数据一致性
2. 业务代码切换为读取新字段，写入仍保留双写或仅写新字段

[Phase 3: 收缩 (Contract)]
1. 停用旧字段的读取与写入
2. 执行最终迁移脚本：删除旧字段/旧约束
```

---

## 二、 危险 DDL 与安全替代对照表

| 目标操作 | 危险做法（高危锁表） | 安全无锁做法 |
| :--- | :--- | :--- |
| **创建索引** | `CREATE INDEX idx_user ON users(email);`<br>*(阻塞全表写入)* | **PostgreSQL**: `CREATE INDEX CONCURRENTLY idx_user ON users(email);`<br>**MySQL**: `ALTER TABLE users ADD INDEX idx_user(email), ALGORITHM=INPLACE, LOCK=NONE;` |
| **添加非空字段** | `ALTER TABLE orders ADD COLUMN status VARCHAR(20) NOT NULL DEFAULT 'pending';`<br>*(全表重写与元数据长锁)* | **分三步走**：<br>1. 先添加允许为空的列：`ADD COLUMN status VARCHAR(20);`<br>2. 增加默认值：`ALTER TABLE orders ALTER COLUMN status SET DEFAULT 'pending';`<br>3. 分批回填历史数据后，再添加非空约束（Postgres 使用 `NOT VALID` 然后 `VALIDATE CONSTRAINT`）。 |
| **重命名字段** | `ALTER TABLE users RENAME COLUMN phone TO mobile;`<br>*(导致旧版本应用崩溃)* | 采用**展开-收缩模式**：新建 `mobile` 字段 ➔ 双写 ➔ 回填 ➔ 切换读 ➔ 弃用 `phone`。 |
| **删除字段** | `ALTER TABLE users DROP COLUMN unused_field;`<br>*(旧应用实例缓存该列时报错)* | 1. 先在代码层面去除所有对该字段的引用并上线发布；<br>2. 观察一个版本周期确认无调用后，再执行 `DROP COLUMN`。 |

---

## 三、 主流 ORM 工程化指南

### 1. Prisma
* **本地开发**：使用 `npx prisma migrate dev --name <migration_name>` 生成版本化 SQL 迁移文件。
* **生产部署**：**严禁**在生产环境执行 `migrate dev`，必须使用 `npx prisma migrate deploy`，仅执行已审查的变更。
* **审查生成的 SQL**：Prisma 生成的迁移文件必须手动走查，若包含无锁不兼容的 `CREATE INDEX`，需手动修改为 `CREATE INDEX CONCURRENTLY`（并加上 `-- prisma-migration-no-atomic` 注释）。

### 2. Drizzle ORM / TypeORM
* 始终将 Schema 结构变更与数据回填（Data Migration）脚本分离。
* 数据填充脚本单独放在 scripts 目录，通过分批循环更新：
```typescript
// 安全的数据回填示例
let hasMore = true;
let lastId = 0;
const BATCH_SIZE = 500;

while (hasMore) {
  const records = await db.query(
    'SELECT id, old_col FROM orders WHERE id > $1 ORDER BY id ASC LIMIT $2',
    [lastId, BATCH_SIZE]
  );
  if (records.length === 0) break;
  
  for (const r of records) {
    await db.query('UPDATE orders SET new_col = $1 WHERE id = $2', [transform(r.old_col), r.id]);
    lastId = r.id;
  }
  // 释放连接与 CPU 锁，让业务查询优先
  await sleep(100);
}
```

---

## 四、 迁移发布前审查清单 (Pre-Migration Checklist)

- [ ] **向后兼容性**：该变更上线后，尚未更新的旧版本代码是否会报错？
- [ ] **DDL 锁审查**：大表操作是否加上了 `CONCURRENTLY` 或 `ALGORITHM=INPLACE`？
- [ ] **超时保护**：是否在迁移会话中设置了锁等待超时（如 `SET lock_timeout = '5s';`），防止 DDL 挂起阻塞全站查询？
- [ ] **外键约束**：添加外键时是否会造成全表检查锁？（建议先加无约束检查，后异步验证）
- [ ] **回滚脚本**：是否已在本地或预发环境完整验证了对应的回滚（Down）逻辑？
