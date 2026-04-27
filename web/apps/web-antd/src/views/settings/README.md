# 基础设置页面

## 功能说明
这是一个桶装水品牌管理页面，用于管理系统中使用的桶装水品牌信息。品牌数据会被持久化存储，方便在其他页面调用。

## 主要特性
- ✅ 使用 Vben Vxe Table 高级表格组件
- ✅ **新增品牌功能**（弹窗表单，数据持久化）
- ✅ **删除品牌功能**（带确认提示）
- ✅ **品牌名称唯一性验证**（防止重复添加）
- ✅ 支持分页功能
- ✅ 支持表格缩放、自定义列
- ✅ 支持刷新数据
- ✅ 响应式布局

## 文件结构

### 1. Mock API
#### 数据存储模块
- **位置**: `apps/backend-mock/utils/water-brand-data.ts`
- **功能**: 模拟数据库，存储桶装水品牌数据
- **数据结构**:
  ```typescript
  interface WaterBrand {
    id: number;      // 品牌ID（自增）
    name: string;    // 品牌名称
  }
  ```
- **方法**:
  - `getBrands()`: 获取所有品牌
  - `createBrand(name)`: 创建新品牌
  - `updateBrand(id, name)`: 更新品牌
  - `deleteBrand(id)`: 删除品牌

#### 列表接口
- **位置**: `apps/backend-mock/api/water-brand/list.ts`
- **接口**: `GET /api/water-brand/list`
- **功能**: 从数据存储中读取所有品牌
- **返回示例**:
  ```json
  {
    "code": 0,
    "data": [
      { "id": 1, "name": "农夫山泉" },
      { "id": 2, "name": "怡宝" },
      { "id": 3, "name": "娃哈哈" }
    ],
    "message": "ok"
  }
  ```

#### 创建接口
- **位置**: `apps/backend-mock/api/water-brand/create.ts`
- **接口**: `POST /api/water-brand/create`
- **请求体**: `{ "name": "百岁山" }`
- **功能**: 创建新品牌并保存到数据存储
- **验证**: 
  - 品牌名称不能为空
  - 品牌名称不能重复
- **返回示例**:
  ```json
  {
    "code": 0,
    "data": { "id": 4, "name": "百岁山" },
    "message": "ok"
  }
  ```

#### 删除接口
- **位置**: `apps/backend-mock/api/water-brand/delete.ts`
- **接口**: `POST /api/water-brand/delete`
- **请求体**: `{ "id": 4 }`
- **功能**: 根据ID删除品牌
- **返回示例**:
  ```json
  {
    "code": 0,
    "data": { "success": true },
    "message": "ok"
  }
  ```

### 2. 前端 API
- **位置**: `apps/web-antd/src/api/water-brand.ts`
- **类型定义**:
  ```typescript
  interface WaterBrand {
    id: number;
    name: string;
  }
  ```
- **方法**:
  - `getWaterBrandListApi()`: 获取品牌列表
  - `createWaterBrandApi(data)`: 创建新品牌
  - `deleteWaterBrandApi(data)`: 删除品牌

### 3. 页面组件
- **主页面**: `apps/web-antd/src/views/settings/index.vue`
- **表单组件**: `apps/web-antd/src/views/settings/modules/brand-form.vue`
- **技术栈**: 
  - Vben Vxe Table（基于 vxe-table）
  - Vben Form（新增表单）
  - Vben Modal（弹窗）
  - Ant Design Vue
- **功能**:
  - **表格显示**：序号、品牌ID、品牌名称、操作列
  - 分页：每页10条，可选10/20/50/100
  - 工具栏：刷新、缩放、自定义列、**新增品牌**
  - **操作列**：删除按钮（带确认提示）
  - **新增品牌弹窗**：包含品牌名称输入框（必填），带表单验证和重复检查

### 4. 路由配置
- **位置**: `apps/web-antd/src/router/routes/modules/settings.ts`
- **功能**: 配置基础设置页面的路由和菜单
- **菜单位置**: 左侧菜单栏独立显示（一级菜单）
- **图标**: lucide:settings

## 使用说明

### 启动开发服务器
```bash
pnpm dev:antd
```

### 访问页面
1. 浏览器访问：http://localhost:5667
2. 登录后，在左侧菜单栏找到 **"基础设置"** 菜单项
3. 点击即可看到桶装水品牌管理页面

### 新增品牌
1. 点击工具栏右侧的 **"新增品牌"** 按钮（蓝色按钮，带加号图标）
2. 弹出新增品牌对话框
3. 填写表单：
   - **品牌名称**（必填，最多50个字符）
4. 点击 **确定** 按钮提交
5. 成功后会：
   - ✅ 显示成功提示
   - ✅ 自动关闭弹窗
   - ✅ **自动刷新表格，显示新增的品牌**

### 删除品牌
1. 在表格操作列点击 **"删除"** 按钮
2. 弹出确认对话框
3. 点击 **确定** 确认删除
4. 成功后会：
   - ✅ 显示成功提示
   - ✅ 自动刷新表格，移除已删除的品牌

### 表格功能
- **分页**: 底部分页器可切换页码和每页显示数量
- **刷新**: 点击工具栏刷新按钮重新加载数据
- **缩放**: 点击工具栏缩放按钮可全屏显示
- **自定义列**: 点击工具栏自定义按钮可显示/隐藏列

## 技术实现

### 数据结构 (water-brand-data.ts)
```typescript
interface WaterBrand {
  id: number;
  name: string;
}

const brands: WaterBrand[] = [
  { id: 1, name: '农夫山泉' },
  { id: 2, name: '怡宝' },
  { id: 3, name: '娃哈哈' },
];

// 创建新品牌
export function createBrand(name: string): WaterBrand {
  const newId = brands.length > 0 
    ? Math.max(...brands.map((b) => b.id)) + 1 
    : 1;
  const newBrand: WaterBrand = { id: newId, name };
  brands.push(newBrand);
  return newBrand;
}
```

### 创建 API (create.ts)
```typescript
export default eventHandler(async (event) => {
  const body = await readBody(event);
  const { name } = body;

  if (!name || !name.trim()) {
    return { code: -1, message: '品牌名称不能为空', data: null };
  }

  // 检查品牌是否已存在
  const brands = await import('~/utils/water-brand-data').then((m) => m.getBrands());
  const exists = brands.some((b) => b.name === name.trim());
  
  if (exists) {
    return { code: -1, message: '该品牌已存在', data: null };
  }

  // 创建新品牌
  const newBrand = createBrand(name.trim());
  return useResponseSuccess(newBrand);
});
```

### 前端 API 调用 (water-brand.ts)
```typescript
export interface WaterBrand {
  id: number;
  name: string;
}

export async function getWaterBrandListApi() {
  return requestClient.get<WaterBrand[]>('/water-brand/list');
}

export async function createWaterBrandApi(data: { name: string }) {
  return requestClient.post<WaterBrand>('/water-brand/create', data);
}

export async function deleteWaterBrandApi(data: { id: number }) {
  return requestClient.post<{ success: boolean }>('/water-brand/delete', data);
}
```

### 表格配置 (index.vue)
```typescript
const gridOptions: VxeTableGridOptions<WaterBrand> = {
  columns: [
    { title: '序号', type: 'seq', width: 80 },
    { field: 'id', title: '品牌ID', width: 120 },
    { field: 'name', title: '品牌名称', minWidth: 200 },
    {
      title: '操作',
      width: 120,
      fixed: 'right',
      slots: { default: 'action' },
    },
  ],
  // ...
};
```

### 表单组件配置 (modules/brand-form.vue)
```typescript
const [Form, formApi] = useVbenForm({
  layout: 'vertical',
  schema: [
    {
      fieldName: 'name',
      label: '品牌名称',
      component: 'Input',
      componentProps: {
        placeholder: '请输入品牌名称',
        maxlength: 50,
      },
      rules: 'required',  // 必填
    },
  ],
});

async onConfirm() {
  const { valid } = await formApi.validate();
  if (valid) {
    const values = await formApi.getValues();
    
    try {
      // 调用真实的创建API
      await createWaterBrandApi({ name: values.name });
      
      message.success('新增成功');
      modalApi.close();
      emit('success');
    } catch (error: any) {
      // 显示后端返回的错误信息
      message.error(error?.message || '操作失败');
    }
  }
}
```

### 删除功能 (index.vue)
```typescript
function onDelete(row: WaterBrand) {
  AntdModal.confirm({
    title: '确认删除',
    content: `确定要删除品牌"${row.name}"吗？`,
    okText: '确定',
    cancelText: '取消',
    onOk: async () => {
      try {
        await deleteWaterBrandApi({ id: row.id });
        message.success('删除成功');
        refreshGrid();
      } catch (error) {
        message.error('删除失败');
      }
    },
  });
}
```

## 数据流程

### 查询流程
1. 页面加载或点击刷新按钮
2. 触发 `proxyConfig.ajax.query` 方法
3. 调用 `getWaterBrandListApi()` 从 Nitro Mock 获取数据
4. 分页处理后返回给表格显示

### 新增流程
1. 用户点击"新增品牌"按钮
2. 打开弹窗，显示空表单
3. 用户填写品牌名称（必填）
4. 点击确定，触发表单验证
5. 验证通过后调用 `createWaterBrandApi()` 
6. **后端接收请求，进行验证**：
   - 检查品牌名称是否为空
   - 检查品牌名称是否已存在
7. **验证通过后，调用 `createBrand()` 保存到数据存储**
8. **返回新创建的品牌数据（包含自动生成的ID）**
9. 前端显示成功提示，关闭弹窗
10. 触发 `success` 事件
11. 主页面监听到事件，调用 `gridApi.query()` **重新从后端获取数据**
12. **表格显示包含新增品牌的完整列表**

### 删除流程
1. 用户点击操作列的"删除"按钮
2. 弹出确认对话框
3. 用户确认后调用 `deleteWaterBrandApi()`
4. **后端接收请求，调用 `deleteBrand()` 从数据存储中删除**
5. 返回删除成功标识
6. 前端显示成功提示
7. 刷新表格，移除已删除的品牌

## ⚠️ 重要说明

### 品牌名称规则
- ✅ **必填字段**: 品牌名称不能为空
- ✅ **唯一性**: 品牌名称不能重复，系统会自动检查
- ✅ **长度限制**: 最多50个字符
- ✅ **自动去空格**: 提交时会自动去除前后空格
- 📝 **初始数据**: 系统预置了3个品牌（农夫山泉、怡宝、娃哈哈）

### 数据持久化
- ✅ **会话内持久化**：新增的品牌数据保存在内存中，在当前服务器运行期间有效
- ⚠️ **重启后丢失**：由于是 Mock 数据，重启后端服务器后数据会恢复为初始的3条
- 💡 **生产环境**：需要对接真实数据库（MySQL、PostgreSQL等）

### 在其他页面调用品牌数据
品牌数据存储在后端，可以在其他页面通过以下方式调用：

```typescript
import { getWaterBrandListApi } from '#/api/water-brand';

// 在任何组件中使用
const brands = await getWaterBrandListApi();
console.log(brands); // [{ id: 1, name: '农夫山泉' }, ...]
```

**使用场景示例**：
- 在客户管理页面选择桶装水品牌
- 在订单页面选择品牌
- 在统计页面按品牌分组

## 扩展示例

### 在其他页面使用品牌下拉选择
```vue
<script lang="ts" setup>
import { ref, onMounted } from 'vue';
import { getWaterBrandListApi } from '#/api/water-brand';

const brandOptions = ref([]);

onMounted(async () => {
  const brands = await getWaterBrandListApi();
  brandOptions.value = brands.map(b => ({
    label: b.name,
    value: b.id,
  }));
});
</script>

<template>
  <Select :options="brandOptions" placeholder="请选择品牌" />
</template>
```

### 如果需要编辑品牌功能
可以添加编辑按钮和编辑表单：
```typescript
// 在表格操作列添加编辑按钮
<Button type="link" size="small" @click="onEdit(row)">
  编辑
</Button>

// 编辑函数
function onEdit(row: WaterBrand) {
  brandFormModalApi.setData(row).open();
}
```

### 如果需要批量导入品牌
可以添加Excel导入功能：
```typescript
// 上传Excel文件，解析后批量创建品牌
```

## 扩展建议
- ✅ 已实现：新增品牌功能（数据持久化）
- ✅ 已实现：删除品牌功能（带确认提示）
- ✅ 已实现：品牌名称唯一性验证
- 🔲 可以添加：编辑品牌功能
- 🔲 可以添加：批量删除功能
- 🔲 可以添加：品牌启用/禁用状态
- 🔲 可以添加：品牌Logo上传
- 🔲 可以添加：品牌描述信息
- 🔲 可以对接真实后端API（替换 Mock 数据）
