# ONCITY-PRO 前后端分离架构说明

## 📊 项目概览

本项目采用**前后端完全分离**的架构设计：

```
┌─────────────────────────────────────────┐
│         ONCITY-PRO (前端)               │
│  Vue Vben Admin + TypeScript + Vite     │
│  位置: c:\Users\tanwe\ONCITY-PRO        │
└──────────────┬──────────────────────────┘
               │ HTTP/REST API
               │ (Axios Request)
               ▼
┌─────────────────────────────────────────┐
│      ONCITY-Django (后端)               │
│  Django + DRF + MySQL                   │
│  位置: c:\Users\tanwe\ONCITY-Django     │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│         MySQL Database                  │
│  数据存储层                              │
└─────────────────────────────────────────┘
```

---

## 🗂️ 项目结构

### 前端项目 (ONCITY-PRO)
```
c:\Users\tanwe\ONCITY-PRO\
├── apps/
│   ├── web-antd/              # Vue 3 + Ant Design Vue 应用
│   └── backend-mock/          # Mock 数据服务（开发用）
├── packages/                  # 共享包
├── internal/                  # 内部配置
└── ...
```

### 后端项目 (ONCITY-Django)
```
c:\Users\tanwe\ONCITY-Django\
├── api/                       # API 应用
│   ├── models.py             # 数据模型
│   ├── serializers.py        # 序列化器
│   ├── views.py              # 视图
│   └── urls.py               # URL 路由
├── oncity_backend/           # Django 项目配置
│   ├── settings.py           # 配置文件
│   └── urls.py               # 主路由
├── venv/                     # Python 虚拟环境
├── .env                      # 环境变量（不提交 Git）
├── manage.py                 # Django 管理脚本
└── requirements.txt          # Python 依赖
```

---

## 🔗 前后端对接配置

### 1. 后端 CORS 配置

在 `ONCITY-Django/.env` 中配置允许的前端地址：

```env
CORS_ALLOWED_ORIGINS=http://localhost:5173,http://localhost:5174
```

### 2. 前端 API 地址配置

在 `ONCITY-PRO/apps/web-antd/.env.development` 中：

```env
VITE_GLOB_API_URL=http://127.0.0.1:8000/api
```

生产环境 `.env.production`：

```env
VITE_GLOB_API_URL=https://api.yourdomain.com/api
```

### 3. 请求适配器

Vben Admin 已内置请求适配器，位于：
- `packages/effects/request/src/request-client/`

无需额外配置，只需设置环境变量即可。

---

## 🚀 开发工作流

### 启动后端

```bash
cd c:\Users\tanwe\ONCITY-Django
.\venv\Scripts\activate
python manage.py runserver
```

或使用一键脚本：
```bash
start.bat
```

### 启动前端

```bash
cd c:\Users\tanwe\ONCITY-PRO
pnpm dev:antd
```

### 访问地址

- **前端**: http://localhost:5173
- **后端 API**: http://127.0.0.1:8000/api
- **Django Admin**: http://127.0.0.1:8000/admin/
- **API 健康检查**: http://127.0.0.1:8000/api/health/

---

## 📡 API 设计规范

### RESTful 风格

```
GET    /api/v1/resources/          # 获取列表
POST   /api/v1/resources/          # 创建资源
GET    /api/v1/resources/{id}/     # 获取详情
PUT    /api/v1/resources/{id}/     # 完整更新
PATCH  /api/v1/resources/{id}/     # 部分更新
DELETE /api/v1/resources/{id}/     # 删除资源
```

### 响应格式

**成功响应:**
```json
{
  "count": 100,
  "next": "http://127.0.0.1:8000/api/v1/resources/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "示例",
      "created_at": "2026-04-21T08:00:00Z"
    }
  ]
}
```

**错误响应:**
```json
{
  "detail": "错误信息描述",
  "status_code": 400
}
```

### 状态码规范

- `200 OK` - 成功
- `201 Created` - 创建成功
- `204 No Content` - 删除成功
- `400 Bad Request` - 请求参数错误
- `401 Unauthorized` - 未认证
- `403 Forbidden` - 无权限
- `404 Not Found` - 资源不存在
- `500 Internal Server Error` - 服务器错误

---

## 🔐 认证与授权

### 当前配置（开发阶段）

- **权限**: `AllowAny` - 允许匿名访问
- **认证**: Session + Token

### 生产环境建议

1. **JWT 认证** (推荐)
   ```bash
   pip install djangorestframework-simplejwt
   ```

2. **权限控制**
   - `IsAuthenticated` - 需登录
   - `IsAdminUser` - 仅管理员
   - 自定义权限类

3. **跨域配置**
   - 限制 `CORS_ALLOWED_ORIGINS` 为生产域名
   - 启用 HTTPS

---

## 📦 数据库设计

### 当前模型示例

**Sample 模型** (`api/models.py`):
```python
class Sample(models.Model):
    title = CharField(max_length=200)
    description = TextField(blank=True)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    is_active = BooleanField(default=True)
```

### 创建新模型步骤

1. 在 `api/models.py` 中定义模型
2. 在 `api/serializers.py` 中创建序列化器
3. 在 `api/views.py` 中创建视图
4. 在 `api/urls.py` 中注册路由
5. 执行迁移:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

---

## 🧪 测试策略

### 后端测试

```bash
# 运行所有测试
python manage.py test

# 运行特定应用测试
python manage.py test api

# 带覆盖率报告
coverage run manage.py test
coverage report
```

### 前端测试

```bash
# 单元测试
pnpm test:unit

# E2E 测试
pnpm test:e2e
```

### API 手动测试

使用提供的 `API_TEST_EXAMPLES.http` 文件，配合：
- **VSCode REST Client** 插件
- **Postman**
- **Apifox**
- **curl/httpie** 命令行工具

---

## 🔄 开发 Mock 切换

### 使用 Mock 数据（前端独立开发）

前端默认连接 `backend-mock`：
```env
VITE_GLOB_API_URL=/api  # 相对路径，由 Vite 代理到 mock
```

### 切换到真实后端

修改环境变量：
```env
VITE_GLOB_API_URL=http://127.0.0.1:8000/api
```

重启前端开发服务器即可。

---

## 🚢 部署方案

### 方案 A: 独立部署（推荐）

**前端部署:**
- 构建静态文件: `pnpm build:antd`
- 部署到 Nginx / CDN / Vercel / Netlify

**后端部署:**
- 使用 Gunicorn + Nginx
- 或使用 Docker Compose
- 数据库: MySQL / PostgreSQL

### 方案 B: Docker Compose 一键部署

在 `ONCITY-Django` 目录：
```bash
docker-compose up -d
```

自动启动：
- MySQL 数据库
- Django 后端
- 静态文件服务

---

## 📝 开发最佳实践

### 后端

1. ✅ 使用虚拟环境隔离依赖
2. ✅ 环境变量管理敏感信息
3. ✅ 编写单元测试
4. ✅ 使用 Django Admin 快速管理数据
5. ✅ API 版本控制 (`/api/v1/`)
6. ✅ 日志记录关键操作
7. ❌ 不要提交 `.env` 文件
8. ❌ 不要在生产环境开启 DEBUG

### 前端

1. ✅ 使用 TypeScript 类型安全
2. ✅ 组件化开发
3. ✅ 统一的请求封装
4. ✅ 错误边界处理
5. ✅ 响应式设计
6. ❌ 避免硬编码 API 地址
7. ❌ 避免在前端存储敏感信息

---

## 🆘 常见问题排查

### 1. 跨域错误

**症状**: 浏览器控制台显示 CORS 错误

**解决**:
- 检查后端 `.env` 中的 `CORS_ALLOWED_ORIGINS`
- 确保包含前端地址
- 重启 Django 服务

### 2. 404 错误

**症状**: API 返回 404

**解决**:
- 检查 URL 路径是否正确
- 确认 `api/urls.py` 和 `oncity_backend/urls.py` 配置
- 查看 Django 控制台输出

### 3. 数据库连接失败

**症状**: `OperationalError: Can't connect to MySQL server`

**解决**:
- 确认 MySQL 服务运行
- 检查 `.env` 中的数据库配置
- 确认数据库已创建
- 测试命令行连接: `mysql -u root -p`

### 4. 前端无法连接后端

**症状**: 网络请求失败

**解决**:
- 确认后端服务正在运行
- 检查 `VITE_GLOB_API_URL` 配置
- 浏览器开发者工具查看 Network 标签
- 测试后端健康检查接口

---

## 📚 相关文档

- [Django 官方文档](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Vue Vben Admin 文档](https://doc.vben.pro/)
- [MySQL 文档](https://dev.mysql.com/doc/)

---

## 🎯 下一步计划

1. ✅ ~~基础项目搭建~~
2. ✅ ~~API 示例实现~~
3. ⬜ 用户认证系统 (JWT)
4. ⬜ 业务模块开发
5. ⬜ 权限管理系统
6. ⬜ API 文档生成 (Swagger)
7. ⬜ 单元测试覆盖
8. ⬜ 生产环境部署

---

**祝开发顺利！** 🎉

如有问题，请查阅文档或提交 Issue。
