# Repo: OpenBox-Marketing

## .cursor/skills/gke-full-deploy/SKILL.md
```markdown
---
name: gke-full-deploy
description: Full GKE deployment of OpenBox from scratch. Use when setting up a new GKE cluster, doing a fresh deployment, or migrating OpenBox to a new environment.
---

# GKE 全新部署

从零将 OpenBox 部署到 GKE 集群的完整流程。

## 架构概览

```
同一个 GKE 集群
├── Namespace: openbox              ← 应用层
│   ├── Backend Deployment (FastAPI)
│   ├── Frontend Deployment (Nginx)
│   ├── Ingress (对外入口 + HTTPS)
│   └── Secret (凭证)
└── Namespace: openbox-sandbox      ← 沙箱层
    ├── Pod sandbox-{user_id}       ← 动态创建
    ├── Service sandbox-{user_id}
    └── PVC workspace-{user_id}     ← 持久化存储
```

## 前置条件

- [ ] `gcloud` CLI 已安装并认证
- [ ] `kubectl` 已安装
- [ ] Docker 已安装
- [ ] 拥有域名 DNS 管理权限
- [ ] 准备好以下凭证（不要写入代码或 skill）：
  - PostgreSQL 连接串
  - Redis URL（密码中特殊字符需 URL 编码）
  - Blob Storage 连接串
  - JWT Secret
  - LLM API Key
  - Search API Key（如 Tavily）

## 部署步骤

### Step 1: 创建 GKE 集群

```bash
gcloud container clusters create <CLUSTER_NAME> \
  --region=<REGION> \
  --num-nodes=1 \
  --machine-type=e2-standard-2 \
  --disk-size=50 \
  --workload-pool=<PROJECT_ID>.svc.id.goog \
  --enable-ip-alias \
  --release-channel=regular \
  --project=<PROJECT_ID>
```

验证连接：`kubectl get nodes`

### Step 2: 创建 Namespace

```bash
kubectl create namespace openbox
kubectl create namespace openbox-sandbox
```

### Step 3: 创建 PostgreSQL 数据库

如果数据库在 GKE 内网，通过集群内 Pod 连接：

```bash
kubectl run pg-client --rm -i --tty --restart=Never --namespace=openbox \
  --image=postgres:16-alpine \
  --command -- psql "<POSTGRES_URL>" -c "CREATE DATABASE openbox;"
```

### Step 4: 构建并推送 Docker 镜像

**必须使用 `--platform linux/amd64`**（GKE 节点是 amd64）。

```bash
gcloud auth configure-docker gcr.io --quiet

# 三个镜像并行构建
docker build --platform linux/amd64 -t gcr.io/<PROJECT_ID>/openbox-sandbox:latest ./container
docker build --platform linux/amd64 -t gcr.io/<PROJECT_ID>/openbox-backend:latest ./backend
docker build --platform linux/amd64 -t gcr.io/<PROJECT_ID>/openbox-frontend:latest ./frontend

# 推送
docker push gcr.io/<PROJECT_ID>/openbox-sandbox:latest
docker push gcr.io/<PROJECT_ID>/openbox-backend:latest
docker push gcr.io/<PROJECT_ID>/openbox-frontend:latest
```

### Step 5: 创建 K8s Secret

**重要**：Redis 密码中的特殊字符 `!@#$%` 等必须 URL 编码。

```bash
kubectl create secret generic openbox-secrets -n openbox \
  --from-literal=DATABASE_URL='<ASYNCPG_URL>' \
  --from-literal=REDIS_URL='<REDIS_URL_ENCODED>' \
  --from-literal=JWT_SECRET='<JWT_SECRET>' \
  --from-literal=SANDBOX_IMAGE='gcr.io/<PROJECT_ID>/openbox-sandbox:latest' \
  --from-literal=OPENBOX_API_KEY='<API_KEY>' \
  --from-literal=BLOB_AZURE_CONNECTION_STRING='<BLOB_CONN>' \
  --from-literal=BLOB_AZURE_CONTAINER='<CONTAINER_NAME>' \
  --from-literal=TAVILY_API_KEY='<TAVILY_KEY>' \
  --from-literal=OPENAI_API_KEY='<OPENAI_KEY>'
```

### Step 6: 创建镜像拉取凭证

```bash
ACCESS_TOKEN=$(gcloud auth print-access-token)
for NS in openbox openbox-sandbox; do
  kubectl create secret docker-registry gcr-pull-secret -n $NS \
    --docker-server=gcr.io --docker-username=oauth2accesstoken \
    --docker-password="$ACCESS_TOKEN" --docker-email=<EMAIL>
done

# 绑定到 ServiceAccount
kubectl patch serviceaccount default -n openbox \
  -p '{"imagePullSecrets": [{"name": "gcr-pull-secret"}]}'
```

### Step 7: 部署 K8s 资源

`k8s/base.yaml` 包含所有资源定义。部署前需：

1. 确认 `BLOB_PROVIDER` 值（azure 或 gcs）
2. 确认环境变量与 Secret key 匹配

```bash
sed "s/PROJECT_ID/<PROJECT_ID>/g" k8s/base.yaml | kubectl apply -f -
```

部署后绑定 imagePullSecret 到创建的 ServiceAccount：

```bash
kubectl patch serviceaccount openbox-backend -n openbox \
  -p '{"imagePullSecrets": [{"name": "gcr-pull-secret"}]}'
kubectl patch serviceaccount sandbox-pods -n openbox-sandbox \
  -p '{"imagePullSecrets": [{"name": "gcr-pull-secret"}]}'
```

### Step 8: 运行数据库 Migration

```bash
kubectl exec -n openbox deployment/openbox-backend -- uv run alembic upgrade head
```

**注意**：检查 migration 中的列长度是否与 ORM 模型一致（常见问题：`VARCHAR(26)` vs `String(64)`）。如不一致需手动 ALTER。

### Step 9: 配置外部访问（Ingress + HTTPS）

#### 预留静态 IP

```bash
gcloud compute addresses create <APP>-static-ip --global --project=<PROJECT_ID>
gcloud compute addresses describe <APP>-static-ip --global --format='get(address)'
```

#### 创建 ManagedCertificate + Ingress

参考 `.claude/gke-ingress-setup/SKILL.md` 中的完整流程。关键资源：

- ManagedCertificate（域名 SSL 证书，签发需 15-60 分钟）
- FrontendConfig（HTTP → HTTPS 跳转）
- Ingress（路由规则：`/api` `/ws` → backend，`/` → frontend）

#### 配置 DNS

在域名管理后台添加 A 记录：`<DOMAIN> → <STATIC_IP>`

### Step 10: 验证

```bash
# Pod 状态
kubectl get pods -n openbox

# 健康检查
curl -s https://<DOMAIN>/health

# 证书状态
kubectl get managedcertificate -n openbox

# Backend 日志
kubectl logs -f deployment/openbox-backend -n openbox
```

## 凭证管理

部署完成后，将所有凭证保存到本地文件（如 `gke-credentials.md`），并加入 `.gitignore`：

```bash
echo "gke-credentials.md" >> .gitignore
```

## 关键注意事项

### Redis URL 编码
密码中的 `!@#$%` 必须 URL 编码，否则 URL 解析器会把 `@` 当作主机分隔符。

### 交叉编译 .venv 问题
在 ARM Mac 上用 `--platform linux/amd64` 构建时，`uv sync` 创建的 `.venv` 在 amd64 容器中不可用。Backend Dockerfile 应使用 `pip install` 而非 `uv sync`。

### Sandbox Pod 权限
Sandbox Pod 默认以 root 运行。如需限制权限，在 `kubernetes.py` 的 pod spec 中添加 `securityContext`，并确保 PVC 目录权限正确（通过 `fsGroup` 或 `initContainer`）。

### imagePullSecret 过期
使用 `gcloud auth print-access-token` 生成的 token 约 1 小时过期。每次部署前需刷新。长期方案是配置 Workload Identity（需要 `iam.serviceAccountAdmin` 权限）。

### 集群费用
GKE Standard 集群管理费免费，按节点 VM 计费。3 个 `e2-standard-2` 节点约 $145/月。不用时记得删除集群。

```

## .cursor/skills/gke-ingress-setup/SKILL.md
```markdown
---
name: gke-ingress-setup
description: Set up GKE Ingress with Google Managed Certificate for HTTPS access. Use when creating Ingress, configuring SSL certificates, setting up domain proxy, or troubleshooting GKE Ingress and certificate issues.
---

# GKE Ingress Setup with Google Managed Certificate

## Overview

在 GKE Autopilot 集群上，通过 Ingress + Google Managed Certificate 为服务配置 HTTPS 域名访问。

## Prerequisites

- 已安装 `gcloud` 和 `kubectl`
- 已连接到目标 GKE 集群（`kubectl config get-contexts` 确认）
- 拥有域名的 DNS 管理权限

## 完整流程

### Step 1: 创建 ClusterIP Service

为目标应用创建 ClusterIP Service，暴露应用端口：

```yaml
apiVersion: v1
kind: Service
metadata:
  name: <app>-service
  namespace: default
spec:
  selector:
    app: <app>
  ports:
    - protocol: TCP
      port: <app-port>
      targetPort: <app-port>
  type: ClusterIP
```

> **注意**：Service 端口使用应用实际端口（如 4000），无需改为 80。GCP 负载均衡器会自动在 80/443 上监听并转发到 Service 端口。

### Step 2: 预留全球静态 IP

```bash
gcloud compute addresses create <app>-static-ip \
  --global \
  --project=<project-id>
```

获取分配的 IP：

```bash
gcloud compute addresses describe <app>-static-ip \
  --global \
  --project=<project-id> \
  --format='get(address)'
```

### Step 3: 创建 ManagedCertificate + FrontendConfig + Ingress

一次性创建三个资源：

```yaml
apiVersion: networking.gke.io/v1
kind: ManagedCertificate
metadata:
  name: <app>-certificate
  namespace: default
spec:
  domains:
    - <your-domain>
---
apiVersion: networking.gke.io/v1beta1
kind: FrontendConfig
metadata:
  name: <app>-frontend-config
  namespace: default
spec:
  redirectToHttps:
    enabled: true
    responseCodeName: MOVED_PERMANENTLY_DEFAULT
---
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: <app>-ingress
  namespace: default
  annotations:
    kubernetes.io/ingress.global-static-ip-name: <app>-static-ip
    networking.gke.io/managed-certificates: <app>-certificate
    networking.gke.io/v1beta1.FrontendConfig: <app>-frontend-config
spec:
  rules:
    - host: <your-domain>
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: <app>-service
                port:
                  number: <app-port>
```

### Step 4: 配置 DNS

在域名 DNS 管理后台添加 A 记录：

```
<your-domain>  →  A  →  <static-ip>
```

### Step 5: 等待证书签发

Google Managed Certificate 签发通常需要 **15-60 分钟**。

检查状态：

```bash
kubectl get managedcertificate <app>-certificate
kubectl describe managedcertificate <app>-certificate
```

证书状态说明：

| 状态 | 含义 |
|------|------|
| `Provisioning` | 正在签发，正常等待 |
| `Active` | 签发完成，HTTPS 可用 |
| `ProvisioningFailed` | 签发失败，检查 DNS |
| `ProvisioningFailedPermanently` | 永久失败，需删除重建 |

域名状态说明：

| 状态 | 含义 |
|------|------|
| `Provisioning` | 正在验证域名 |
| `Active` | 域名验证通过 |
| `FailedNotVisible` | DNS 未正确指向静态 IP |

GCP 侧证书详情：

```bash
gcloud compute ssl-certificates describe <cert-name> \
  --project=<project-id>
```

## 流量链路

```
用户浏览器
  ↓ HTTPS (443) / HTTP (80 → 301 重定向 HTTPS)
GCP 负载均衡器 (静态 IP)
  ↓ 应用端口
ClusterIP Service
  ↓ 应用端口
Pod (容器)
```

## 常见问题排查

### 证书签发失败 (ProvisioningFailedPermanently)

1. 确认 DNS A 记录正确指向 Ingress 静态 IP
2. 删除失败的 ManagedCertificate 并重新创建
3. 如果之前有同域名证书残留，需先清理

### Ingress 删除卡住 (Finalizer)

Ingress 有 GKE finalizer 用于清理 GCP 负载均衡器资源，如果卡住可强制移除：

```bash
kubectl patch ingress <ingress-name> \
  -p '{"metadata":{"finalizers":[]}}' --type=merge
```

> **警告**：强制移除 finalizer 后需到 GCP Console 手动检查并清理残留的负载均衡器资源。

### 健康检查协议错误

如果出现 `Protocol "TCP" is not valid` 错误，需确保 Service 使用 HTTP 协议。可通过 BackendConfig 自定义健康检查：

```yaml
apiVersion: cloud.google.com/v1
kind: BackendConfig
metadata:
  name: <app>-backend-config
spec:
  healthCheck:
    type: HTTP
    port: <app-port>
    requestPath: /
```

然后在 Service 上添加注解：

```yaml
metadata:
  annotations:
    cloud.google.com/backend-config: '{"default":"<app>-backend-config"}'
```

### HTTPS 返回 500 或连接终止

证书还在签发中时，HTTPS 无法正常工作，会出现 500 或连接终止。等证书状态变为 `Active` 即可。

### ClusterIP 无法从外部访问

ClusterIP 只在集群内部可达，这是正常的。外部访问通过 Ingress 的公网 IP。

## 验证清单

```
- [ ] Service 创建成功，Endpoints 不为空
- [ ] 静态 IP 已预留
- [ ] ManagedCertificate 已创建
- [ ] FrontendConfig 已创建
- [ ] Ingress 已创建，Address 已分配
- [ ] DNS A 记录已配置
- [ ] Ingress 后端状态为 HEALTHY
- [ ] 证书状态为 Active
- [ ] HTTP 访问返回 301 重定向
- [ ] HTTPS 访问正常
```

## 有用的命令

```bash
# 查看集群所有 Ingress
kubectl get ingress --all-namespaces

# 查看所有证书
kubectl get managedcertificates --all-namespaces

# 查看 Ingress 详情（含后端健康状态和事件）
kubectl describe ingress <ingress-name>

# 验证 DNS 解析
dig <your-domain> +short

# 测试 HTTP 访问
curl -s -o /dev/null -w "%{http_code}" http://<your-domain>/

# 测试 HTTPS 访问（跳过证书验证）
curl -sk -o /dev/null -w "%{http_code}" https://<your-domain>/

# 列出 GCP 静态 IP
gcloud compute addresses list --global --project=<project-id>

# 列出 GCP SSL 证书
gcloud compute ssl-certificates list --project=<project-id>
```

```

## .cursor/skills/gke-update-deploy/SKILL.md
```markdown
---
name: gke-update-deploy
description: Update and redeploy OpenBox to GKE after code changes. Use when the user wants to deploy updates, push new images, restart pods, or apply config changes to the running GKE cluster.
---

# GKE 更新部署

代码变更后，将 OpenBox 更新部署到 GKE 集群。

## 前置条件

- kubectl 已连接到 openbox 集群
- gcloud 已认证
- Docker 已登录 GCR（`gcloud auth configure-docker gcr.io --quiet`）

## 连接集群

```bash
gcloud container clusters get-credentials openbox --region=us-central1 --project=<PROJECT_ID>
```

## 更新流程

### 1. 判断需要更新的组件

| 变更内容 | 需要重建的镜像 |
|---------|--------------|
| `backend/` 代码变更 | openbox-backend |
| `frontend/` 代码变更 | openbox-frontend |
| `container/` 代码变更 | openbox-sandbox |
| `k8s/base.yaml` 变更 | 无需重建镜像，直接 apply |
| K8s Secret 变更 | 无需重建镜像，更新 secret 后 restart |

### 2. 重建并推送镜像

**注意**：必须使用 `--platform linux/amd64`，因为 GKE 节点是 amd64。

```bash
cd <项目根目录>

# Backend
docker build --platform linux/amd64 -t gcr.io/<PROJECT_ID>/openbox-backend:latest ./backend
docker push gcr.io/<PROJECT_ID>/openbox-backend:latest

# Frontend
docker build --platform linux/amd64 -t gcr.io/<PROJECT_ID>/openbox-frontend:latest ./frontend
docker push gcr.io/<PROJECT_ID>/openbox-frontend:latest

# Sandbox（仅 container/ 目录变更时）
docker build --platform linux/amd64 -t gcr.io/<PROJECT_ID>/openbox-sandbox:latest ./container
docker push gcr.io/<PROJECT_ID>/openbox-sandbox:latest
```

### 3. 刷新镜像拉取凭证

imagePullSecret 使用临时 token，约 1 小时过期，部署前必须刷新：

```bash
ACCESS_TOKEN=$(gcloud auth print-access-token)
for NS in openbox openbox-sandbox; do
  kubectl delete secret gcr-pull-secret -n $NS 2>/dev/null
  kubectl create secret docker-registry gcr-pull-secret -n $NS \
    --docker-server=gcr.io --docker-username=oauth2accesstoken \
    --docker-password="$ACCESS_TOKEN" --docker-email=<EMAIL>
done
```

### 4. 重启 Deployment

```bash
# 重启 backend（推完 backend 镜像后）
kubectl rollout restart deployment openbox-backend -n openbox

# 重启 frontend（推完 frontend 镜像后）
kubectl rollout restart deployment openbox-frontend -n openbox
```

Sandbox Pod 不需要手动重启，下次用户创建会话时自动使用新镜像。如需立即更新现有 sandbox：

```bash
kubectl delete pods -n openbox-sandbox --all
```

### 5. 应用 K8s 配置变更

```bash
sed "s/PROJECT_ID/<PROJECT_ID>/g" k8s/base.yaml | kubectl apply -f -
```

### 6. 运行数据库 Migration（如有）

```bash
kubectl exec -n openbox deployment/openbox-backend -- uv run alembic upgrade head
```

### 7. 验证

```bash
# Pod 状态
kubectl get pods -n openbox
kubectl get pods -n openbox-sandbox

# Backend 日志
kubectl logs deployment/openbox-backend -n openbox --tail=20

# 健康检查
curl -s https://<DOMAIN>/health
```

## 常见问题

### ImagePullBackOff
imagePullSecret 过期，执行 Step 3 刷新。

### Pod 启动慢
检查 Dockerfile CMD 是否使用了 `uv run`（会重建 venv）。应使用 `pip install` + 直接调用 `uvicorn`。

### 前端 TypeScript 编译失败
先本地 `cd frontend && npx tsc --noEmit` 检查错误，修复后再构建镜像。

### 数据库字段长度不匹配
ORM 模型和数据库 migration 列长度需一致，检查是否需要 ALTER TABLE。

```
