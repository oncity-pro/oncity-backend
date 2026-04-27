# ONCITY-Django 快速配置指南

## 📌 前置要求

1. **Python 3.13+** - 已安装并添加到系统 PATH
2. **MySQL 5.7+** 或 **MariaDB 10.3+** - 数据库服务正在运行
3. **Git** - 版本控制（可选）

---

## 🚀 5 分钟快速启动

### 步骤 1: 创建 MySQL 数据库

打开 MySQL 命令行或工具（如 phpMyAdmin、MySQL Workbench），执行：

```sql
CREATE DATABASE oncity_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 步骤 2: 配置环境变量

在项目根目录，复制并重命名配置文件：

**Windows:**
```cmd
copy .env.example .env
```

**Linux/Mac:**
```bash
cp .env.example .env
```

编辑 `.env` 文件，修改以下关键配置：

```env
# Django 密钥（生产环境必须更改）
SECRET_KEY=django-insecure-change-this-in-production

# 数据库配置
DB_NAME=oncity_db
DB_USER=root              # 你的 MySQL 用户名
DB_PASSWORD=your_password # 你的 MySQL 密码
DB_HOST=localhost
DB_PORT=3306

# CORS 配置（前端地址）
CORS_ALLOWED_ORIGINS=http://localhost:5173,http://localhost:5174
```

### 步骤 3: 一键启动（推荐）

**Windows:**
```cmd
start.bat
```

**Linux/Mac:**
```bash
chmod +x start.sh
./start.sh
```

脚本会自动：
- ✅ 创建虚拟环境（如果不存在）
- ✅ 安装依赖包
- ✅ 执行数据库迁移
- ✅ 启动开发服务器

### 步骤 4: 验证安装

浏览器访问以下地址：

- **API 健康检查**: http://127.0.0.1:8000/api/health/
- **Django Admin**: http://127.0.0.1:8000/admin/
- **API 示例列表**: http://127.0.0.1:8000/api/v1/samples/

看到 JSON 响应表示成功！

---

## 🔧 手动配置（可选）

如果不想使用启动脚本，可以手动执行：

### 1. 激活虚拟环境

**Windows:**
```cmd
.\venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 数据库迁移

```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. 创建超级用户（访问 Admin）

```bash
python manage.py createsuperuser
```

按提示输入用户名、邮箱和密码。

### 5. 启动服务器

```bash
python manage.py runserver
```

---

## 🎯 与前端对接

在 **ONCITY-PRO** 前端项目中配置 API 地址：

编辑 `apps/web-antd/.env.development`：

```env
VITE_GLOB_API_URL=http://127.0.0.1:8000/api
```

然后重启前端开发服务器：

```bash
cd c:\Users\tanwe\ONCITY-PRO
pnpm dev:antd
```

---

## 📝 测试 API

### 使用 curl 测试

```bash
# 健康检查
curl http://127.0.0.1:8000/api/health/

# 获取样本列表
curl http://127.0.0.1:8000/api/v1/samples/

# 创建样本
curl -X POST http://127.0.0.1:8000/api/v1/samples/ \
  -H "Content-Type: application/json" \
  -d '{"title":"测试标题","description":"测试描述"}'
```

### 使用 Postman/Apifox

导入以下集合测试 API：

1. **GET** `/api/health/` - 健康检查
2. **GET** `/api/v1/samples/` - 获取列表
3. **POST** `/api/v1/samples/` - 创建
4. **GET** `/api/v1/samples/{id}/` - 获取详情
5. **PUT** `/api/v1/samples/{id}/` - 更新
6. **DELETE** `/api/v1/samples/{id}/` - 删除

---

## ❓ 常见问题

### Q1: 提示 `mysqlclient` 安装失败

**解决方案:**

**Windows:**
```bash
# 确保安装了 MySQL Connector/C 或使用预编译版本
pip install mysqlclient
```

如果仍然失败，可以临时使用 SQLite（修改 `.env`）：
```env
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=db.sqlite3
```

### Q2: 跨域错误 (CORS)

确保 `.env` 中配置了正确的前端地址：
```env
CORS_ALLOWED_ORIGINS=http://localhost:5173,http://localhost:5174
```

### Q3: 数据库连接失败

检查：
1. MySQL 服务是否运行
2. `.env` 中的数据库名、用户名、密码是否正确
3. 数据库是否已创建

### Q4: 端口被占用

更改启动端口：
```bash
python manage.py runserver 8080
```

---

## 🎓 下一步

- 📖 阅读 [Django 官方文档](https://docs.djangoproject.com/)
- 📚 学习 [Django REST Framework](https://www.django-rest-framework.org/)
- 🔨 创建你自己的模型和 API
- 🔐 添加 JWT 认证（推荐 `djangorestframework-simplejwt`）
- 📊 集成 Swagger 文档（推荐 `drf-spectacular`）

---

## 💡 开发建议

1. **不要提交 `.env` 文件到 Git** - 已添加到 `.gitignore`
2. **定期备份数据库** - 使用 `mysqldump` 工具
3. **使用 Django Admin** - 快速管理数据
4. **编写单元测试** - 保证代码质量
5. **查看日志文件** - `logs/debug.log` 记录详细信息

---

## 🆘 需要帮助？

- 📧 提交 Issue
- 📖 查看 README.md
- 🔍 搜索 Django 官方文档

祝开发愉快！🎉
