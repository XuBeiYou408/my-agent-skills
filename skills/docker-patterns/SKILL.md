---
name: docker-patterns
description: >-
  涉及编写、优化或审查 Dockerfile、Docker Compose 编排、多阶段构建（Multi-stage Build）、容器安全加固与本地微服务环境联调时触发。规范最小化镜像、非 root 权限、依赖缓存加速与跨平台兼容。
---

# Docker 与容器化标准工程规范 (Docker Patterns Protocol)

> **“开发环境跑得通不叫通，容器环境秒起、安全无漏洞、轻量高效才叫生产就绪。”**  
> 规范容器构建与服务编排，避免臃肿镜像、权限过大与跨平台换行/权限陷阱。

---

## 零、 核心铁律 (The Iron Laws of Containerization)

1. **生产镜像必须使用多阶段构建（Multi-stage Build）**：绝对禁止将编译工具链（gcc, npm/yarn cache, go toolchain）遗留在运行时镜像中。
2. **禁止以 root 用户运行生产容器**：必须显式创建并指定非特权用户（如 `USER node` 或 `USER nonroot`）。
3. **禁止把敏感配置/私钥打包进镜像**：任何 Token、API Key、私钥必须通过环境变量或运行时 Secret 挂载。
4. **.dockerignore 必须首发配置**：杜绝将本地 `node_modules`, `.git`, `.env`, `dist` 无脑复制进构建上下文。

---

## 一、 多阶段构建黄金模板

### 1. Node.js (TypeScript / Next.js) 模板
```dockerfile
# syntax=docker/dockerfile:1
# 1. 依赖安装阶段
FROM node:20-alpine AS deps
WORKDIR /app
RUN apk add --no-cache libc6-compat
COPY package.json package-lock.json ./
RUN npm ci

# 2. 编译阶段
FROM node:20-alpine AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN npm run build && npm prune --production

# 3. 生产最小运行阶段
FROM node:20-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production
# 安全加固：创建非 root 运行身份
RUN addgroup --system --gid 1001 nodejs && \
    adduser --system --uid 1001 appuser
COPY --from=builder --chown=appuser:nodejs /app/node_modules ./node_modules
COPY --from=builder --chown=appuser:nodejs /app/dist ./dist
COPY --from=builder --chown=appuser:nodejs /app/package.json ./

USER appuser
EXPOSE 3000
CMD ["node", "dist/main.js"]
```

### 2. Go 静态二进制极简模板 (Scratch / Distroless)
```dockerfile
# 构建环境
FROM golang:1.22-alpine AS builder
WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -ldflags="-w -s" -o server .

# 生产环境：无 Shell、零多余文件的超安全镜像
FROM gcr.io/distroless/static-debian12:nonroot
WORKDIR /
COPY --from=builder /app/server /server
USER nonroot:nonroot
EXPOSE 8080
ENTRYPOINT ["/server"]
```

---

## 二、 Docker Compose 本地微服务联调范式

```yaml
version: '3.8'

services:
  app:
    build:
      context: .
      target: builder # 开发时挂载代码实时热重载
    ports:
      - "3000:3000"
    volumes:
      - .:/app
      - /app/node_modules # 保护容器内依赖，防止宿主机覆盖
    environment:
      - DATABASE_URL=postgres://user:password@db:5432/mydb
    depends_on:
      db:
        condition: service_healthy # 必须等待数据库健康探针通过

  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
      POSTGRES_DB: mydb
    ports:
      - "5432:5432"
    volumes:
      - pgdata:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user -d mydb"]
      interval: 5s
      timeout: 5s
      retries: 5

volumes:
  pgdata:
```

---

## 三、 Windows / 跨平台兼容防坑指南

1. **脚本换行符问题（CRLF vs LF）**：
   - 痛点：Windows 下检出的 `entrypoint.sh` 常常带 `

`，导致 Linux 容器报错 `exec /entrypoint.sh: no such file or directory`。
   - 解法：在项目根目录 `.gitattributes` 强制声明：
     ```gitattributes
     *.sh text eol=lf
     Dockerfile text eol=lf
     ```
2. **挂载卷权限与性能**：
   - Windows WSL2 下，尽量将工程存放在 Linux 子系统目录中（如 `~/projects/`），跨盘挂载（`/mnt/c/...`）会导致 I/O 极其缓慢。

---

## 四、 容器交付审查清单 (Docker Checklist)

- [ ] 是否具备 `.dockerignore`？（排除 `.git`, `.env`, `node_modules`）
- [ ] 是否利用了 Docker 构建缓存？（先 `COPY package*.json`，再 `RUN install`，最后 `COPY . .`）
- [ ] 容器内是否以非 root 用户执行？
- [ ] 是否有明确的 `HEALTHCHECK` 或配合 Compose 设置了依赖探针？
- [ ] 生产容器中是否移除了所有构建依赖与测试代码？
