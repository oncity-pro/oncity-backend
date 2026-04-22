# ONCITY API 文档

## 基础信息

- **Base URL**: `http://localhost:8000/api/v1/`
- **格式**: JSON
- **认证**: 暂未启用（后续可添加 JWT）

---

## 客户类型字段说明

从2026-04-22起，客户管理API新增了`customer_type`字段，用于区分客户类型。

### 客户类型选项
- `vip`: VIP客户
- `normal`: 普通客户（默认值）
- `pickup`: 自提客户

### API返回示例
```json
{
  "id": "0001",
  "name": "张三",
  "customer_type": "vip",
  "customer_type_display": "VIP客户",
  "brand": 1,
  "brand_name": "怡宝",
  "open_date": "2024-01-15",
  "last_delivery_date": "2024-04-20",
  "phone": "13800138001",
  "address": "北京市朝阳区xxx小区1号楼101",
  "remark": "老客户",
  "is_active": true,
  "created_at": "2024-01-15T00:00:00Z",
  "updated_at": "2024-01-15T00:00:00Z"
}
```

**字段说明：**
- `customer_type`: 客户类型代码，用于提交和存储
- `customer_type_display`: 客户类型的中文显示名称，由后端自动生成，只读

---

## API 端点列表

### 1. 健康检查

**GET** `/api/health/`

检查 API 服务是否正常运行。

**响应示例：**
```json
{
  "status": "healthy",
  "message": "ONCITY API is running"
}
```

---

### 2. 水品牌管理 (WaterBrand)

#### 2.1 获取启用的品牌列表

**GET** `/api/v1/water-brands/`

返回所有启用的水品牌（is_active=true）。

**响应示例：**
```json
[
  {
    "id": 1,
    "name": "怡宝",
    "description": "华润怡宝纯净水",
    "is_active": true,
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z"
  },
  {
    "id": 2,
    "name": "农夫山泉",
    "description": "农夫山泉天然水",
    "is_active": true,
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z"
  }
]
```

#### 2.2 获取所有品牌（包括禁用的）

**GET** `/api/v1/water-brands/all/`

返回所有水品牌，包括已禁用的。

#### 2.3 创建新品牌

**POST** `/api/v1/water-brands/all/`

**请求体：**
```json
{
  "name": "百岁山",
  "description": "百岁山天然矿泉水",
  "is_active": true
}
```

#### 2.4 获取品牌详情

**GET** `/api/v1/water-brands/{id}/`

#### 2.5 更新品牌

**PUT** `/api/v1/water-brands/{id}/`

**PATCH** `/api/v1/water-brands/{id}/`

#### 2.6 删除品牌

**DELETE** `/api/v1/water-brands/{id}/`

---

### 3. 客户管理 (Customer)

#### 3.1 获取客户列表（支持搜索）

**GET** `/api/v1/customers/`

**查询参数：**
- `keyword` (可选): 搜索关键词，支持客户编号或姓名模糊匹配

**示例：**
```
GET /api/v1/customers/?keyword=张三
GET /api/v1/customers/?keyword=0001
```

**响应示例：**
```json
[
  {
    "id": "0001",
    "name": "张三 - 北京市朝阳区xxx小区1号楼101",
    "customer_type": "normal",
    "customer_type_display": "普通客户",
    "brand": 1,
    "brand_name": "怡宝",
    "open_date": "2024-01-15",
    "last_delivery_date": "2024-04-20",
    "phone": "13800138001",
    "address": "北京市朝阳区xxx小区1号楼101",
    "remark": "老客户",
    "is_active": true,
    "created_at": "2024-01-15T00:00:00Z",
    "updated_at": "2024-01-15T00:00:00Z"
  }
]
```

#### 3.2 获取所有客户（包括搜索）

**GET** `/api/v1/customers/all/`

与 `/api/v1/customers/` 功能相同，但语义更明确。

#### 3.3 创建新客户

**POST** `/api/v1/customers/all/`

**请求体：**
```json
{
  "id": "0006",
  "name": "周八 - 北京市昌平区ccc小区6号楼606",
  "customer_type": "normal",
  "brand": 1,
  "open_date": "2024-04-21",
  "last_delivery_date": null,
  "phone": "13800138006",
  "address": "北京市昌平区ccc小区6号楼606",
  "remark": "新客户",
  "is_active": true
}
```

**字段说明：**
- `id`: 客户编号（必填，字符串类型）
- `name`: 姓名地址（必填）
- `customer_type`: 客户类型（可选，默认'normal'），可选值：'vip'(VIP客户), 'normal'(普通客户), 'pickup'(自提客户)
- `brand`: 品牌ID（可选）
- `open_date`: 开户日期（必填，格式：YYYY-MM-DD）
- `last_delivery_date`: 最后送水日期（可选）
- `phone`: 联系电话（可选）
- `address`: 详细地址（可选）
- `remark`: 备注（可选）
- `is_active`: 是否活跃（可选，默认true）

**返回字段补充：**
- `customer_type`: 客户类型代码（'vip', 'normal', 'pickup'）
- `customer_type_display`: 客户类型中文显示名称（'VIP客户', '普通客户', '自提客户'）

#### 3.4 获取客户详情

**GET** `/api/v1/customers/{id}/`

**示例：**
```
GET /api/v1/customers/0001/
```

#### 3.5 更新客户

**PUT** `/api/v1/customers/{id}/`

完整更新客户信息。

**PATCH** `/api/v1/customers/{id}/`

部分更新客户信息。

**示例：**
```json
{
  "last_delivery_date": "2024-04-21",
  "remark": "已更新送水日期"
}
```

#### 3.6 删除客户

**DELETE** `/api/v1/customers/{id}/`

---

## 错误响应

所有 API 错误都会返回统一的错误格式：

```json
{
  "detail": "错误描述信息"
}
```

或者字段验证错误：

```json
{
  "id": ["客户编号不能为空"],
  "open_date": ["开户日期不能是未来日期"]
}
```

---

## HTTP 状态码

- `200 OK`: 请求成功
- `201 Created`: 资源创建成功
- `204 No Content`: 资源删除成功
- `400 Bad Request`: 请求参数错误
- `404 Not Found`: 资源不存在
- `500 Internal Server Error`: 服务器内部错误

---

## 前端集成示例

### Vue 3 + Axios

```typescript
import axios from 'axios'

const apiClient = axios.create({
  baseURL: 'http://localhost:8000/api/v1/',
  timeout: 10000,
})

// 获取客户列表
export async function getCustomerListApi(keyword?: string) {
  const params = keyword ? { keyword } : {}
  const response = await apiClient.get('/customers/', { params })
  return response.data
}

// 获取品牌列表
export async function getWaterBrandListApi() {
  const response = await apiClient.get('/water-brands/')
  return response.data
}

// 创建客户
export async function createCustomerApi(data: any) {
  const response = await apiClient.post('/customers/all/', data)
  return response.data
}

// 更新客户
export async function updateCustomerApi(id: string, data: any) {
  const response = await apiClient.patch(`/customers/${id}/`, data)
  return response.data
}

// 删除客户
export async function deleteCustomerApi(id: string) {
  await apiClient.delete(`/customers/${id}/`)
}
```

---

## 测试工具

你可以使用以下工具测试 API：

1. **浏览器**: 直接访问 GET 接口
2. **Postman**: 导入 API 集合进行测试
3. **curl**: 命令行测试
4. **Django Browsable API**: 访问 `http://localhost:8000/api/v1/customers/` 查看可视化界面

---

## 注意事项

1. **跨域配置**: 确保 `.env` 中的 `CORS_ALLOWED_ORIGINS` 包含前端地址
2. **数据库**: 使用前需要配置 MySQL 并执行迁移
3. **客户编号**: 建议使用固定长度格式（如：0001, 0002）
4. **日期格式**: 使用 ISO 8601 格式（YYYY-MM-DD）
5. **搜索功能**: 支持客户编号和姓名的模糊匹配

---

## 下一步计划

- [ ] 添加 JWT 认证
- [ ] 添加分页支持
- [ ] 添加数据导出功能
- [ ] 添加批量操作
- [ ] 添加操作日志
