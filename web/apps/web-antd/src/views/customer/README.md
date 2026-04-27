# 客户管理页面

## 功能说明
这是一个使用 **Vben Vxe Table** 的客户管理页面，带有实时搜索功能和新增客户功能，数据来自后端 Nitro Mock。

## 主要特性
- ✅ 使用 Vben Vxe Table 高级表格组件
- ✅ **实时搜索功能**（输入时立即显示结果，支持客户编号和姓名搜索）
- ✅ **新增客户功能**（弹窗表单，数据持久化）
- ✅ **客户编号自动格式化**（从 0001 开始，4位数字）
- ✅ **开户日期和最后送水日期管理**
- ✅ **桶装水品牌管理**（从基础设置调用品牌数据）
- ✅ 支持分页功能
- ✅ 支持表格缩放、自定义列
- ✅ 支持刷新数据
- ✅ 响应式布局

## 文件结构

### 1. Mock API
#### 数据存储模块
- **位置**: `apps/backend-mock/utils/customer-data.ts`
- **功能**: 模拟数据库，存储客户数据
- **数据结构**:
  ```typescript
  interface Customer {
    id: number;                    // 内部ID（数字）
    name: string;                  // 客户姓名
    openDate?: string;             // 开户日期（可选，格式：YYYY-MM-DD）
    lastDeliveryDate?: string;     // 最后送水日期（可选，格式：YYYY-MM-DD）
    brandId?: number;              // 品牌ID（关联到基础设置的品牌）
  }
  ```
- **方法**:
  - `formatCustomerId(id)`: 格式化客户编号为4位数字（如：0001, 0002）
  - `getCustomers()`: 获取所有客户
  - `createCustomer(name, openDate, lastDeliveryDate, brandId)`: 创建新客户
  - `updateCustomer(id, name, openDate, lastDeliveryDate, brandId)`: 更新客户
  - `deleteCustomer(id)`: 删除客户

#### 列表接口
- **位置**: `apps/backend-mock/api/customer/list.ts`
- **接口**: `GET /api/customer/list`
- **功能**: 从数据存储中读取所有客户，并格式化客户编号
- **返回示例**:
  ```json
  {
    "code": 0,
    "data": [
      { 
        "id": "0001", 
        "name": "张三",
        "openDate": "2024-01-15",
        "lastDeliveryDate": "2024-12-20",
        "brandId": 1
      },
      { 
        "id": "0002", 
        "name": "李四",
        "openDate": "2024-03-20",
        "lastDeliveryDate": "2024-12-18",
        "brandId": 2
      },
      { 
        "id": "0003", 
        "name": "王五",
        "openDate": "2024-06-10",
        "lastDeliveryDate": "2024-12-19",
        "brandId": 3
      }
    ],
    "message": "ok"
  }
  ```

#### 创建接口
- **位置**: `apps/backend-mock/api/customer/create.ts`
- **接口**: `POST /api/customer/create`
- **请求体**: 
  ```json
  { 
    "name": "赵六",
    "openDate": "2024-12-01",
    "lastDeliveryDate": "2024-12-20",
    "brandId": 1
  }
  ```
- **功能**: 创建新客户并保存到数据存储，返回格式化的客户编号
- **返回示例**:
  ```json
  {
    "code": 0,
    "data": { 
      "id": "0004", 
      "name": "赵六",
      "openDate": "2024-12-01",
      "lastDeliveryDate": "2024-12-20",
      "brandId": 1
    },
    "message": "ok"
  }
  ```

### 2. 前端 API
- **位置**: `apps/web-antd/src/api/customer.ts`
- **类型定义**:
  ```typescript
  interface Customer {
    id: string;                      // 格式化后的客户编号（如：0001）
    name: string;                    // 客户姓名
    openDate?: string;               // 开户日期
    lastDeliveryDate?: string;       // 最后送水日期
    brandId?: number;                // 品牌ID
  }
  ```
- **方法**:
  - `getCustomerListApi()`: 获取客户列表
  - `createCustomerApi(data)`: 创建新客户

### 3. 页面组件
- **主页面**: `apps/web-antd/src/views/customer/index.vue`
- **表单组件**: `apps/web-antd/src/views/customer/modules/form.vue`
- **技术栈**: 
  - Vben Vxe Table（基于 vxe-table）
  - Vben Form（搜索表单和新增表单）
  - Vben Modal（弹窗）
  - Ant Design Vue
- **功能**:
  - **搜索表单**：姓名地址（实时搜索，支持客户编号和姓名）
  - **表格显示**：序号、客户编号、姓名地址、**品牌**、开户日期、最后送水日期
  - 分页：每页10条，可选10/20/50/100
  - 工具栏：搜索、刷新、缩放、自定义列、**新增客户**
  - **新增客户弹窗**：包含客户姓名（必填）、**品牌选择**、开户日期、最后送水日期，带表单验证，调用真实API

### 4. 路由配置
- **位置**: `apps/web-antd/src/router/routes/modules/customer.ts`
- **功能**: 配置客户管理页面的路由和菜单
- **菜单位置**: 左侧菜单栏独立显示
- **图标**: lucide:users

## 使用说明

### 启动开发服务器
```bash
pnpm dev:antd
```

### 访问页面
1. 浏览器访问：http://localhost:5667
2. 登录后，在左侧菜单栏找到 **"客户管理"** 菜单项
3. 点击即可看到客户列表

### 🔍 实时搜索功能
- **即时响应**：输入内容后立即显示匹配结果，无需点击查询按钮
- **智能匹配**：同时支持客户编号和客户姓名的模糊搜索
- **搜索示例**：
  - 输入 `00` → 显示所有编号以"00"开头的客户（0001, 0002, 0003...）
  - 输入 `0001` → 精确匹配编号为"0001"的客户
  - 输入 `张` → 显示姓名包含"张"的客户
  - 输入 `李` → 显示姓名包含"李"的客户
- **清空搜索**：点击输入框右侧的清除按钮或手动删除内容，恢复显示全部客户

### 新增客户
1. 点击工具栏右侧的 **"新增客户"** 按钮（蓝色按钮，带加号图标）
2. 弹出新增客户对话框
3. 填写表单：
   - **客户姓名**（必填）
   - **品牌**（选填，从下拉列表选择，数据来自基础设置）
   - **开户日期**（选填，使用日期选择器）
   - **最后送水日期**（选填，使用日期选择器）
4. 点击 **确定** 按钮提交
5. 成功后会：
   - ✅ 显示成功提示
   - ✅ 自动关闭弹窗
   - ✅ **自动刷新表格，显示新增的客户（含自动生成的000X格式编号和品牌名称）**

### 表格功能
- **分页**: 底部分页器可切换页码和每页显示数量
- **刷新**: 点击工具栏刷新按钮重新加载数据
- **缩放**: 点击工具栏缩放按钮可全屏显示
- **自定义列**: 点击工具栏自定义按钮可显示/隐藏列

## 技术实现

### 数据结构 (customer-data.ts)
```typescript
interface Customer {
  id: number;
  name: string;
  openDate?: string;         // 开户日期
  lastDeliveryDate?: string; // 最后送水日期
  brandId?: number;          // 品牌ID
}

const customers: Customer[] = [
  { 
    id: 1, 
    name: '张三',
    openDate: '2024-01-15',
    lastDeliveryDate: '2024-12-20',
    brandId: 1  // 农夫山泉
  },
  { 
    id: 2, 
    name: '李四',
    openDate: '2024-03-20',
    lastDeliveryDate: '2024-12-18',
    brandId: 2  // 怡宝
  },
  { 
    id: 3, 
    name: '王五',
    openDate: '2024-06-10',
    lastDeliveryDate: '2024-12-19',
    brandId: 3  // 娃哈哈
  },
];

// 创建新客户
export function createCustomer(
  name: string, 
  openDate?: string, 
  lastDeliveryDate?: string,
  brandId?: number
): Customer {
  const newId = customers.length > 0 
    ? Math.max(...customers.map((c) => c.id)) + 1 
    : 1;
  const newCustomer: Customer = { 
    id: newId, 
    name, 
    openDate, 
    lastDeliveryDate,
    brandId
  };
  customers.push(newCustomer);
  return newCustomer;
}
```

### 创建 API (create.ts)
```typescript
export default eventHandler(async (event) => {
  const body = await readBody(event);
  const { name, openDate, lastDeliveryDate, brandId } = body;

  if (!name) {
    return { code: -1, message: '客户姓名不能为空', data: null };
  }

  // 调用数据存储模块创建客户
  const newCustomer = createCustomer(name, openDate, lastDeliveryDate, brandId);
  
  // 格式化客户编号后返回
  const formattedCustomer = {
    ...newCustomer,
    id: formatCustomerId(newCustomer.id),
  };
  
  return useResponseSuccess(formattedCustomer);
});
```

### 前端 API 调用 (customer.ts)
```typescript
export interface Customer {
  brandId?: number;
  id: string;
  lastDeliveryDate?: string;
  name: string;
  openDate?: string;
}

export async function createCustomerApi(data: { 
  brandId?: number;
  lastDeliveryDate?: string; 
  name: string; 
  openDate?: string 
}) {
  return requestClient.post<Customer>('/customer/create', data);
}
```

### 品牌数据加载与显示 (index.vue)
```typescript
import { getWaterBrandListApi, type WaterBrand } from '#/api/water-brand';

// 品牌映射表（ID -> 名称）
const brandMap = ref<Map<number, string>>(new Map());

// 加载品牌数据
async function loadBrands() {
  try {
    const brands = await getWaterBrandListApi();
    const map = new Map<number, string>();
    brands.forEach((brand: WaterBrand) => {
      map.set(brand.id, brand.name);
    });
    brandMap.value = map;
  } catch (error) {
    console.error('加载品牌数据失败:', error);
  }
}

// 组件挂载时加载品牌数据
onMounted(() => {
  loadBrands();
});
```

### 实时搜索配置 (index.vue)
```typescript
const formOptions: VbenFormProps = {
  schema: [
    { 
      fieldName: 'keyword',
      label: '姓名地址',
      component: 'Input',
      componentProps: {
        placeholder: '输入编号或姓名地址搜索',
        allowClear: true,  // 显示清除按钮
      },
    },
  ],
  submitOnChange: true,  // ⭐ 关键字段改变时立即触发搜索
  submitOnEnter: true,   // 回车也触发搜索
};
```

### 搜索逻辑 (index.vue)
```typescript
proxyConfig: {
  ajax: {
    query: async ({ page }, formValues) => {
      const data = await getCustomerListApi();
      
      let filteredData = data;
      if (formValues.keyword) {
        const keyword = formValues.keyword.trim().toLowerCase();
        // 同时匹配客户编号和姓名
        filteredData = filteredData.filter((item: Customer) => {
          const idMatch = item.id.toLowerCase().includes(keyword);   // 匹配编号
          const nameMatch = item.name?.toLowerCase().includes(keyword); // 匹配姓名
          return idMatch || nameMatch;  // 任一匹配即可
        });
      }
      
      // 分页处理...
      return { items, total };
    },
  },
}
```

### 表格列配置 (index.vue)
```typescript
const gridOptions: VxeTableGridOptions<Customer> = {
  columns: [
    { title: '序号', type: 'seq', width: 60 },
    { field: 'id', title: '客户编号', width: 100 },
    { field: 'name', title: '姓名地址', minWidth: 200 },
    { 
      field: 'brandId', 
      title: '品牌', 
      width: 120,
      slots: { default: 'brand' },  // 使用自定义插槽显示品牌名称
    },
    { field: 'openDate', title: '开户日期', width: 120 },
    { field: 'lastDeliveryDate', title: '最后送水日期', width: 130 },
  ],
  // ...
};
```

### 品牌列自定义渲染 (index.vue)
```vue
<template #brand="{ row }">
  {{ row.brandId ? brandMap.get(row.brandId) : '-' }}
</template>
```

### 表单组件配置 (modules/form.vue)
```typescript
import { getWaterBrandListApi, type WaterBrand } from '#/api/water-brand';

// 品牌选项列表
const brandOptions = ref<Array<{ label: string; value: number }>>([]);

// 加载品牌数据
async function loadBrands() {
  try {
    const brands = await getWaterBrandListApi();
    brandOptions.value = brands.map((brand: WaterBrand) => ({
      label: brand.name,
      value: brand.id,
    }));
  } catch (error) {
    console.error('加载品牌数据失败:', error);
  }
}

const [Form, formApi] = useVbenForm({
  layout: 'vertical',
  schema: [
    {
      fieldName: 'name',
      label: '客户姓名',
      component: 'Input',
      rules: 'required',  // 必填
    },
    {
      fieldName: 'brandId',
      label: '品牌',
      component: 'Select',  // 下拉选择器
      componentProps: {
        placeholder: '请选择品牌',
        options: brandOptions,
        allowClear: true,
      },
    },
    {
      fieldName: 'openDate',
      label: '开户日期',
      component: 'DatePicker',
      componentProps: {
        placeholder: '请选择开户日期',
        style: { width: '100%' },
      },
    },
    {
      fieldName: 'lastDeliveryDate',
      label: '最后送水日期',
      component: 'DatePicker',
      componentProps: {
        placeholder: '请选择最后送水日期',
        style: { width: '100%' },
      },
    },
  ],
});

async onConfirm() {
  const { valid } = await formApi.validate();
  if (valid) {
    const values = await formApi.getValues();
    
    // 调用真实的创建API
    await createCustomerApi({ 
      brandId: values.brandId,
      lastDeliveryDate: values.lastDeliveryDate,
      name: values.name,
      openDate: values.openDate,
    });
    
    message.success('新增成功');
    modalApi.close();
    emit('success');
  }
}

// 组件挂载时加载品牌数据
onMounted(() => {
  loadBrands();
});
```

## 数据流程

### 实时搜索流程
1. 用户在"姓名地址"搜索框输入内容
2. **每次输入都会触发 `submitOnChange`**
3. 触发 `proxyConfig.ajax.query` 方法
4. 调用 `getCustomerListApi()` 从 Nitro Mock 获取数据
5. **前端根据关键词同时匹配客户编号和姓名**
6. 分页处理后返回给表格显示
7. **表格实时更新显示匹配结果**

### 品牌数据加载流程
1. 页面加载时（`onMounted`）调用 `loadBrands()`
2. 调用 `getWaterBrandListApi()` 从基础设置获取品牌列表
3. 将品牌数据转换为 Map 结构（ID -> 名称）存储在 `brandMap`
4. 表格渲染时，通过 `brandMap.get(row.brandId)` 获取品牌名称并显示

### 新增流程
1. 用户点击"新增客户"按钮
2. 打开弹窗，显示空表单
3. 表单组件加载时调用 `loadBrands()` 获取品牌选项
4. 用户填写：
   - 客户姓名（必填）
   - **品牌**（选填，从下拉列表选择）
   - **开户日期**（选填，使用日期选择器）
   - **最后送水日期**（选填，使用日期选择器）
5. 点击确定，触发表单验证
6. 验证通过后调用 `createCustomerApi()` 
7. **后端接收请求，调用 `createCustomer()` 保存到数据存储**
8. **自动生成新ID（如：4），并格式化为 "0004"**
9. **返回新创建的客户数据（包含所有字段）**
10. 前端显示成功提示，关闭弹窗
11. 触发 `success` 事件
12. 主页面监听到事件，调用 `gridApi.query()` **重新从后端获取数据**
13. **表格显示包含新增客户的完整列表（品牌列显示品牌名称）**

## ⚠️ 重要说明

### 客户编号规则
- ✅ **起始编号**: 从 0001 开始
- ✅ **格式**: 4位数字，不足补零（0001, 0002, ..., 0010, 0100, 1000...）
- ✅ **自动生成**: 系统自动分配递增的编号
- ✅ **唯一性**: 每个客户编号唯一
- 📝 **实现方式**: 使用 `String(id).padStart(4, '0')` 进行格式化

### 品牌字段说明
- **数据来源**: 品牌数据来自"基础设置"页面的桶装水品牌管理
- **存储方式**: 客户表中存储 `brandId`（品牌ID），不直接存储品牌名称
- **显示方式**: 表格中通过品牌ID查找品牌名称并显示
- **选择方式**: 新增客户时使用 Select 下拉选择器，从品牌API动态加载选项
- **可选字段**: 品牌是选填字段，可以不留
- **关联关系**: 如果删除了某个品牌，已关联该品牌的客户仍保留 brandId，但显示为"-"

### 实时搜索特性
- **即时响应**: 输入时立即显示结果，无需点击查询按钮
- **智能匹配**: 同时支持客户编号和客户姓名的模糊搜索
- **大小写不敏感**: 搜索时自动转换为小写进行比较
- **前后空格处理**: 自动去除输入内容的前后空格
- **一键清空**: 提供清除按钮，快速恢复显示全部数据
- **性能优化**: 本地数据过滤，响应速度快

### 搜索示例
| 输入内容 | 匹配结果 | 说明 |
|---------|---------|------|
| `00` | 0001, 0002, 0003... | 所有编号以"00"开头的客户 |
| `0001` | 0001 | 精确匹配编号 |
| `张` | 张三 | 姓名包含"张"的客户 |
| `李` | 李四 | 姓名包含"李"的客户 |
| `三` | 张三 | 姓名包含"三"的客户 |

### 日期字段说明
- **开户日期**: 记录客户开通服务的日期，格式为 YYYY-MM-DD（如：2024-01-15）
- **最后送水日期**: 记录最后一次送水的日期，格式为 YYYY-MM-DD（如：2024-12-20）
- 两个日期字段都是**选填**，可以不填写
- 使用 Ant Design Vue 的 **DatePicker** 组件进行选择
- 日期以字符串形式存储和传输

### 数据持久化
- ✅ **会话内持久化**：新增的客户数据保存在内存中，在当前服务器运行期间有效
- ⚠️ **重启后丢失**：由于是 Mock 数据，重启后端服务器后数据会恢复为初始的3条
- 💡 **生产环境**：需要对接真实数据库（MySQL、PostgreSQL等）

### 字段说明
- **客户编号**: 系统自动生成，4位数字格式（0001, 0002...），不可编辑，**可搜索**
- **客户姓名**: 必填字段，用于标识客户，**可搜索**
- **品牌**: 选填字段，从基础设置的品牌列表中选择，显示品牌名称
- **开户日期**: 选填字段，记录客户开户时间
- **最后送水日期**: 选填字段，记录最后送水时间，便于跟踪服务状态
- **姓名地址搜索**: 统一搜索框，支持实时模糊匹配客户编号或姓名

## 扩展示例

### 如果需要修改编号位数
修改 `formatCustomerId` 函数中的参数：
```typescript
// 改为5位数字（00001, 00002...）
export function formatCustomerId(id: number): string {
  return String(id).padStart(5, '0');
}
```

### 如果需要添加前缀
```typescript
// 添加前缀（C0001, C0002...）
export function formatCustomerId(id: number): string {
  return 'C' + String(id).padStart(4, '0');
}
```

### 如果需要按品牌筛选客户
可以在搜索表单中添加品牌筛选器：
```typescript
{
  component: 'Select',
  fieldName: 'brandId',
  label: '品牌',
  componentProps: {
    placeholder: '请选择品牌',
    options: brandOptions,
    allowClear: true,
  },
}

// 在搜索逻辑中添加品牌过滤
if (formValues.brandId) {
  filteredData = filteredData.filter((item: Customer) => 
    item.brandId === formValues.brandId
  );
}
```

### 如果需要防抖优化（避免频繁搜索）
可以添加防抖功能：
```typescript
import { debounce } from 'lodash-es';

const debouncedQuery = debounce(() => {
  gridApi.query();
}, 300);  // 300ms 防抖

// 在表单配置中使用
watchEffect(() => {
  if (formApi.values.keyword !== undefined) {
    debouncedQuery();
  }
});
```

### 如果需要日期范围搜索
可以在搜索表单中添加日期范围选择器：
```typescript
{
  component: 'RangePicker',
  fieldName: 'dateRange',
  label: '开户日期范围',
}
```

## 扩展建议
- ✅ 已实现：新增客户功能（数据持久化）
- ✅ 已实现：客户编号格式化（0001开始）
- ✅ 已实现：开户日期和最后送水日期
- ✅ 已实现：实时搜索功能（支持编号和姓名）
- ✅ 已实现：桶装水品牌管理（从基础设置调用）
- 🔲 可以添加：编辑客户功能（在表格操作列添加编辑按钮）
- 🔲 可以添加：删除客户功能（在表格操作列添加删除按钮）
- 🔲 可以添加：更多字段（如：手机号、邮箱、公司名称等）
- 🔲 可以添加：批量操作（多选后批量删除）
- 🔲 可以添加：按品牌筛选功能
- 🔲 可以添加：日期范围搜索功能
- 🔲 可以添加：搜索防抖优化
- 🔲 可以对接真实后端API（替换 Mock 数据）
