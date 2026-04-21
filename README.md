# ONCITY-Django Backend

基于 Django + MySQL 的后端 API 服务，为 ONCITY-PRO (Vue Vben Admin) 前端应用提供数据支持。

## 📋 技术栈

- **Python**: 3.13+
- **Django**: 6.0+
- **Django REST Framework**: 构建 RESTful API
- **MySQL**: 关系型数据库
- **django-cors-headers**: 跨域支持
- **python-dotenv**: 环境变量管理

## 🚀 快速开始

### 1. 环境准备

确保已安装：
- Python 3.13 或更高版本
- MySQL 5.7 或更高版本（或 MariaDB）

### 2. 安装依赖

```bash
# 激活虚拟环境
.\venv\Scripts\activate

# 安装依赖包
pip install -r requirements.txt
```

### 3. 配置环境变量

复制 `.env.example` 为 `.env` 并修改配置：

```bash
copy .env.example .env
```

编辑 `.env` 文件，至少修改以下配置：

```env
SECRET_KEY=your-secret-key-here
DB_NAME=oncity_db
DB_USER=root
DB_PASSWORD=your_mysql_password
```

### 4. 创建数据库

在 MySQL 中创建数据库：

```sql
CREATE DATABASE oncity_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 5. 数据库迁移

```bash
# 生成迁移文件
python manage.py makemigrations

# 执行迁移
python manage.py migrate

# 创建超级用户（可选，用于访问 Admin）
python manage.py createsuperuser
```

### 6. 启动开发服务器

```bash
python manage.py runserver
```

服务将在 `http://127.0.0.1:8000` 启动

## 📡 API 接口

### 健康检查
```
GET /api/health/
```

### 示例资源 CRUD
```
GET    /api/v1/samples/          # 获取列表
POST   /api/v1/samples/          # 创建
GET    /api/v1/samples/{id}/     # 获取详情
PUT    /api/v1/samples/{id}/     # 更新
DELETE /api/v1/samples/{id}/     # 删除
```

### Django Admin
```
http://127.0.0.1:8000/admin/
```

## 🔗 与前端对接

在 ONCITY-PRO 前端项目中配置 API 地址：

编辑 `apps/web-antd/.env` 或 `.env.development`：

```env
VITE_GLOB_API_URL=http://127.0.0.1:8000/api
```

## 📁 项目结构

```
ONCITY-Django/
├── api/                    # API 应用
│   ├── migrations/        # 数据库迁移文件
│   ├── admin.py           # Admin 配置
│   ├── models.py          # 数据模型
│   ├── serializers.py     # 序列化器
│   ├── urls.py            # URL 路由
│   └── views.py           # 视图函数
├── oncity_backend/        # 项目配置
│   ├── settings.py        # 配置文件
│   ├── urls.py            # 主 URL 配置
│   └── wsgi.py            # WSGI 入口
├── venv/                  # Python 虚拟环境
├── .env                   # 环境变量（不提交到 Git）
├── .env.example           # 环境变量示例
├── .gitignore
├── manage.py              # Django 管理脚本
├── requirements.txt       # Python 依赖
└── README.md              # 本文档
```

## 🛠️ 常用命令

```bash
# 激活虚拟环境
.\venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 生成迁移文件
python manage.py makemigrations

# 执行迁移
python manage.py migrate

# 创建超级用户
python manage.py createsuperuser

# 启动开发服务器
python manage.py runserver

# 收集静态文件（生产环境）
python manage.py collectstatic

# 运行测试
python manage.py test

# 打开 Django Shell
python manage.py shell
```

## 🔐 安全建议

生产环境部署前：

1. 修改 `SECRET_KEY` 为强随机字符串
2. 设置 `DEBUG=False`
3. 配置正确的 `ALLOWED_HOSTS`
4. 使用 HTTPS
5. 配置数据库连接池
6. 启用日志记录
7. 定期备份数据库

## 📝 开发规范

- 遵循 PEP 8 Python 代码规范
- 使用 Type Hints 进行类型标注
- 编写必要的单元测试
- API 遵循 RESTful 设计规范
- 使用 Swagger/OpenAPI 文档化 API（可选）

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License
