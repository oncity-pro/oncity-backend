# ONCITY 前端集成指南

## 📋 概述

本文档说明如何将前端项目连接到 Django 后端 API，实现真实的数据交互。

---

## ✅ 已完成的配置

### 1. API 文件结构

```
apps/web-antd/src/api/
├── request.ts          # Axios 请求客户端配置
├── customer.ts         # 客户管理 API
├── water-brand.ts      # 水品牌管理 API
└── index.ts            # 统一导出
```

### 2. 环境变量配置

创建了 `.env.development` 文件：
```env
VITE_GLOB_API_URL=http://localhost:8000
VITE_NITRO_MOCK=false
```

### 3. 更新的页面

- ✅ `src/views/customer/index.vue` - 客户列表页面
- ✅ `src/views/customer/modules/form.vue` - 客户表单组件

---

## 🚀 快速开始

### 步骤 1: 启动 Django 后端

```bash
cd C:\Users\tanwe\ONCITY-Django
.\venv\Scripts\activate
python manage.py runserver
```

后端将在 `http://localhost:8000` 运行。

### 步骤 2: 安装前端依赖（如果还没有）

```bash
cd C:\Users\tanwe\ONCITY-PRO
pnpm install
```

### 步骤 3: 启动前端开发服务器

```bash
pnpm dev
```

前端将在 `http://localhost:5173` 运行。

### 步骤 4: 验证连接

1. 打开浏览器访问 `http://localhost:5173`
2. 导航到"客户管理"页面
3. 应该能看到从 Django 后端加载的客户数据

---

## 🔧 API 使用说明

### 导入 API

```typescript
import { 
  getCustomerListApi, 
  createCustomerApi,
  updateCustomerApi,
  deleteCustomerApi 
} from '#/api/customer';

import { 
  getWaterBrandListApi 
} from '#/api/water-brand';
```

### 使用示例

#### 1. 获取客户列表

```typescript
// 获取所有客户
const customers = await getCustomerListApi();

// 带搜索条件
const customers = await getCustomerListApi({ keyword: '张三' });
```

#### 2. 创建客户

```typescript
const newCustomer = await createCustomerApi({
  id: '0006',
  name: '测试客户',
  brand: 1,
  open_date: '2024-04-21',
  phone: '13800138006',
});
```

#### 3. 更新客户

```typescript
// 部分更新
await patchCustomerApi('0001', {
  last_delivery_date: '2024-04-21',
  remark: '已更新',
});

// 完整更新
await updateCustomerApi('0001', customerData);
```

#### 4. 删除客户

```typescript
await deleteCustomerApi('0001');
```

#### 5. 获取品牌列表

```typescript
const brands = await getWaterBrandListApi();
```

---

## 🌐 跨域配置

### 后端配置（Django）

确保 `.env` 文件中包含前端地址：

```env
CORS_ALLOWED_ORIGINS=http://localhost:5173,http://localhost:5174
```

### 前端配置

已在 `request.ts` 中配置了正确的 baseURL：

```typescript
const API_BASE_URL = import.meta.env.VITE_GLOB_API_URL || 'http://localhost:8000';
```

---

## 📊 数据类型定义

### Customer

```typescript
interface Customer {
  id: string;                    // 客户编号
  name: string;                  // 姓名地址
  brand?: number;                // 品牌ID
  brand_name?: string;           // 品牌名称（只读）
  open_date: string;             // 开户日期
  last_delivery_date?: string;   // 最后送水日期
  phone?: string;                // 联系电话
  address?: string;              // 详细地址
  remark?: string;               // 备注
  is_active?: boolean;           // 是否活跃
}
```

### WaterBrand

```typescript
interface WaterBrand {
  id: number;                    // 品牌ID
  name: string;                  // 品牌名称
  description?: string;          // 品牌描述
  is_active?: boolean;           // 是否启用
}
```

---

## 🐛 常见问题

### 问题 1: CORS 错误

**错误信息：**
```
Access to XMLHttpRequest at 'http://localhost:8000/api/v1/customers/' 
from origin 'http://localhost:5173' has been blocked by CORS policy
```

**解决方案：**
1. 检查后端 `.env` 中的 `CORS_ALLOWED_ORIGINS` 是否包含前端地址
2. 重启 Django 服务器

### 问题 2: 网络连接失败

**错误信息：**
```
Network Error
```

**解决方案：**
1. 确认 Django 服务器正在运行
2. 检查 `.env.development` 中的 `VITE_GLOB_API_URL` 是否正确
3. 尝试在浏览器中直接访问 `http://localhost:8000/api/health/`

### 问题 3: 404 Not Found

**错误信息：**
```
Request failed with status code 404
```

**解决方案：**
1. 检查 API 路径是否正确
2. 确认后端 URL 配置中包含相应的路由
3. 查看 Django 控制台输出的请求日志

### 问题 4: 认证失败

**错误信息：**
```
Request failed with status code 401
```

**解决方案：**
目前 API 暂未启用认证，如果出现此错误：
1. 检查是否在 `request.ts` 中添加了不必要的 token
2. 暂时注释掉 token 相关代码

---

## 🔍 调试技巧

### 1. 查看网络请求

打开浏览器开发者工具（F12）→ Network 标签，可以看到：
- 所有 API 请求
- 请求参数
- 响应数据
- 状态码

### 2. 查看控制台日志

代码中已添加详细的 console.log：
```javascript
console.log('查询参数:', { page, formValues });
console.log('API 返回数据:', data);
console.log('品牌数据加载成功:', brands);
```

### 3. 使用 Django Browsable API

直接访问 API 端点查看数据格式：
- http://localhost:8000/api/v1/customers/
- http://localhost:8000/api/v1/water-brands/

---

## 📝 下一步优化建议

### 1. 添加 Loading 状态

已在表格中添加 loading 状态：
```vue
<Grid table-title="客户列表" :loading="loading">
```

### 2. 添加错误边界

可以在全局添加错误处理：
```typescript
// 在 main.ts 或 app.ts 中
app.config.errorHandler = (err, instance, info) => {
  console.error('Global Error:', err);
  message.error('发生错误，请刷新页面');
};
```

### 3. 添加请求缓存

对于不常变化的数据（如品牌列表），可以添加缓存：
```typescript
let brandCache: WaterBrand[] | null = null;

async function getWaterBrandListApi(forceRefresh = false) {
  if (!forceRefresh && brandCache) {
    return brandCache;
  }
  const data = await requestClient.get<WaterBrand[]>('/water-brands/');
  brandCache = data;
  return data;
}
```

### 4. 添加分页支持

后端暂未实现分页，当前在前端进行模拟分页。后续可以：
1. 在后端添加 DRF 的分页配置
2. 前端传递 page 和 pageSize 参数
3. 后端返回 paginated 数据

---

## 🔗 相关资源

- [Django REST Framework 文档](https://www.django-rest-framework.org/)
- [Axios 文档](https://axios-http.com/)
- [Vue Vben Admin 文档](https://doc.vben.pro/)
- [后端 API 文档](../../ONCITY-Django/API_DOCUMENTATION.md)

---

## ✨ 总结

现在你的前端项目已经：
- ✅ 配置了 API 请求客户端
- ✅ 创建了完整的客户管理 API
- ✅ 创建了水品牌管理 API
- ✅ 更新了客户列表页面使用真实数据
- ✅ 创建了客户表单组件支持新增/编辑
- ✅ 添加了错误处理和加载状态

前后端已经完全打通！🎉
