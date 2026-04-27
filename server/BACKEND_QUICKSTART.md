# ONCITY 后端快速启动指南

## 📋 前置条件

1. ✅ Python 3.13+
2. ✅ MySQL 5.7+ 或 MariaDB
3. ✅ Git

---

## 🚀 快速开始

### 1. 配置数据库

#### 步骤 1: 创建数据库

在 MySQL 中执行：

```sql
CREATE DATABASE oncity_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

#### 步骤 2: 配置 .env 文件

编辑 `.env` 文件，设置你的 MySQL 密码：

```env
DB_PASSWORD=your_mysql_password
```

其他配置保持默认即可。

---

### 2. 安装依赖

```bash
# Windows
.\venv\Scripts\activate
pip install -r requirements.txt

# Linux/Mac
source venv/bin/activate
pip install -r requirements.txt
```

---

### 3. 执行数据库迁移

```bash
# 创建迁移文件（如果还没有）
python manage.py makemigrations

# 执行迁移
python manage.py migrate
```

这会自动创建以下表：
- `api_sample` - 示例数据
- `api_waterbrand` - 水品牌
- `api_customer` - 客户

并插入测试数据：
- 3 个水品牌（怡宝、农夫山泉、百岁山）
- 5 个测试客户

---

### 4. 创建超级用户（可选）

```bash
python manage.py createsuperuser
```

按提示输入用户名、邮箱和密码。

---

### 5. 启动开发服务器

```bash
python manage.py runserver
```

服务将在 `http://localhost:8000` 启动。

---

## ✅ 验证安装

### 1. 健康检查

访问：http://localhost:8000/api/health/

应该看到：
```json
{
  "status": "healthy",
  "message": "ONCITY API is running"
}
```

### 2. 查看客户列表

访问：http://localhost:8000/api/v1/customers/

应该看到 5 个测试客户的数据。

### 3. 查看品牌列表

访问：http://localhost:8000/api/v1/water-brands/

应该看到 3 个水品牌。

### 4. Django Admin

访问：http://localhost:8000/admin/

使用超级用户账号登录，可以管理所有数据。

---

## 🔧 常用命令

```bash
# 启动开发服务器
python manage.py runserver

# 创建新的迁移文件
python manage.py makemigrations

# 执行迁移
python manage.py migrate

# 创建超级用户
python manage.py createsuperuser

# 收集静态文件
python manage.py collectstatic --noinput

# 运行测试
python manage.py test

# 打开 Django Shell
python manage.py shell

# 查看所有路由
python manage.py show_urls
```

---

## 📊 API 端点

### 客户管理
- `GET /api/v1/customers/` - 获取客户列表（支持搜索）
- `POST /api/v1/customers/all/` - 创建客户
- `GET /api/v1/customers/{id}/` - 获取客户详情
- `PUT/PATCH /api/v1/customers/{id}/` - 更新客户
- `DELETE /api/v1/customers/{id}/` - 删除客户

### 水品牌管理
- `GET /api/v1/water-brands/` - 获取启用的品牌列表
- `GET /api/v1/water-brands/all/` - 获取所有品牌
- `POST /api/v1/water-brands/all/` - 创建品牌
- `GET /api/v1/water-brands/{id}/` - 获取品牌详情
- `PUT/PATCH /api/v1/water-brands/{id}/` - 更新品牌
- `DELETE /api/v1/water-brands/{id}/` - 删除品牌

详细文档请查看：[API_DOCUMENTATION.md](./API_DOCUMENTATION.md)

---

## 🐛 常见问题

### 问题 1: 数据库连接失败

**错误信息：**
```
Access denied for user 'root'@'localhost'
```

**解决方案：**
检查 `.env` 文件中的 `DB_PASSWORD` 是否正确。

### 问题 2: 端口被占用

**错误信息：**
```
That port is already in use.
```

**解决方案：**
使用其他端口：
```bash
python manage.py runserver 8001
```

### 问题 3: 迁移失败

**解决方案：**
删除迁移文件后重新创建：
```bash
# 删除 api/migrations/ 下除了 __init__.py 的所有文件
python manage.py makemigrations
python manage.py migrate
```

### 问题 4: CORS 错误

**解决方案：**
确保 `.env` 中的 `CORS_ALLOWED_ORIGINS` 包含前端地址：
```env
CORS_ALLOWED_ORIGINS=http://localhost:5173,http://localhost:5174
```

---

## 🔗 相关资源

- [Django 官方文档](https://docs.djangoproject.com/)
- [Django REST Framework 文档](https://www.django-rest-framework.org/)
- [API 文档](./API_DOCUMENTATION.md)
- [项目架构](./ARCHITECTURE.md)

---

## 📝 下一步

1. ✅ 后端 API 已就绪
2. ⏳ 配置前端连接到后端 API
3. ⏳ 添加 JWT 认证
4. ⏳ 部署到生产环境

祝开发顺利！🎉
