# WarmLabel 部署清单（Railway + Vercel）

本项目推荐采用：
- 前端（uni-app H5）：Vercel
- 后端（Flask API）：Railway
- 模型服务：独立部署（云服务器或容器平台）

## 1. 部署前改造（已在代码中落地）

- 前端 API 地址改为按环境切换：`uniapp_vue_main/common/config.js`
- 后端 CORS 改为白名单：`python_flask/main.py`
- 后端生产依赖补齐：`python_flask/pyproject.toml`
- Git 忽略规则补齐：`.gitignore`
- 环境变量模板：`python_flask/.env.example`、`uniapp_vue_main/.env.production.example`

## 2. 上传 GitHub 前检查

1. 确认未上传大模型文件与本地资源
2. 确认未上传虚拟环境与构建产物
3. 确认 `.gitignore` 已生效

建议命令：

```powershell
git status
git add .
git commit -m "chore: prepare deployment for railway and vercel"
git push
```

## 3. Railway 部署后端

## 3.1 创建服务

1. 登录 Railway
2. 新建 Project，选择从 GitHub 导入
3. 选择本仓库
4. Root Directory 设为 `python_flask`

## 3.2 配置运行命令

在 Railway 服务设置中配置：

- Start Command：

```bash
gunicorn main:app --bind 0.0.0.0:$PORT
```

## 3.3 配置环境变量

按 `python_flask/.env.example` 填写至少以下变量：

- `DATABASE_URL`
- `SECRET_KEY`
- `JWT_SECRET_KEY`
- `MODEL_SERVICE_URL`
- `MODEL_ANALYZE_URL`
- `FFMPEG_PATH`
- `CORS_ALLOWED_ORIGINS`

说明：
- `CORS_ALLOWED_ORIGINS` 需要包含你的 Vercel 域名。
- `DATABASE_URL` 推荐使用 Railway PostgreSQL 插件提供的连接串。

## 3.4 健康检查

部署成功后访问：

- `/api/health`

返回 `status=healthy` 即表示后端可用。

## 4. Vercel 部署前端（uni-app H5）

说明：uni-app 需要先产出 H5 静态文件，再交给 Vercel 托管。

1. 在前端工程中执行 H5 构建（使用你当前 uni-app 的构建方式）
2. 确认生产环境变量 `VUE_APP_API_BASE_URL` 指向 Railway 后端域名
3. 在 Vercel 中导入仓库并设置：
   - Root Directory：`uniapp_vue_main`（或你的 H5 构建产物目录）
   - Build Command：按你的前端构建命令配置
   - Output Directory：按 H5 产物目录配置

## 5. 联调顺序（推荐）

1. 先确认 Railway 后端健康检查通过
2. 再部署 Vercel 前端
3. 打开前端页面测试注册、登录、数据请求
4. 若接口报跨域，优先检查 `CORS_ALLOWED_ORIGINS`

## 6. 常见问题

### 6.1 前端请求仍然打到 localhost

检查：
- `uniapp_vue_main/common/config.js` 的生产地址是否配置正确
- Vercel 环境变量 `VUE_APP_API_BASE_URL` 是否设置
- 前端是否重新构建并触发部署

### 6.2 Railway 后端启动失败

检查：
- `gunicorn` 是否在依赖中
- `Start Command` 是否为 `gunicorn main:app --bind 0.0.0.0:$PORT`
- 必要环境变量是否缺失

### 6.3 上传文件丢失

Railway 本地文件系统不是持久存储。生产环境建议迁移上传文件到对象存储（S3/R2/OSS）。
