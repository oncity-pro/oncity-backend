# 前端客户类型字段集成指南

本文档说明如何在ONCITY-PRO（Vben Admin）前端项目中集成客户类型字段。

## 📋 后端API支持

后端已完全支持客户类型字段，返回两个相关字段：
- `customer_type`: 类型代码（'vip', 'normal', 'pickup', 'closed', 'slow_pay', 'blacklist'）- 用于提交
- `customer_type_display`: 中文显示名称 - 用于展示

## 🔧 前端需要修改的文件

### 1. TypeScript接口定义

**文件位置**: `src/api/customer/index.ts` 或 `src/api/types/customer.ts`

```typescript
// 客户类型选项（用于下拉框）
export const CUSTOMER_TYPE_OPTIONS = [
  { label: 'VIP客户', value: 'vip' },
  { label: '普通客户', value: 'normal' },
  { label: '自提客户', value: 'pickup' },
  { label: '已注销', value: 'closed' },
  { label: '收款慢', value: 'slow_pay' },
  { label: '黑名单', value: 'blacklist' },
] as const;

export interface Customer {
  id: string;
  name: string;
  customer_type?: 'vip' | 'normal' | 'pickup' | 'closed' | 'slow_pay' | 'blacklist';
  customer_type_display?: string;
  brand?: number;
  brand_name?: string;
  open_date: string;
  last_delivery_date?: string | null;
  phone?: string;
  address?: string;
  remark?: string;
  is_active?: boolean;
  created_at?: string;
  updated_at?: string;
}

```

### 2. 表格页面组件

**文件位置**: `src/views/customer/index.vue`

#### 2.1 表格列配置

在表格的columns配置中添加客户类型列：

```typescript
const columns: VxeTableGridOptions['columns'] = [
  {
    field: 'id',
    title: '客户编号',
    width: 100,
  },
  {
    field: 'name',
    title: '姓名地址',
    minWidth: 200,
  },
  // 新增客户类型列
  {
    field: 'customer_type_display',
    title: '客户类型',
    width: 100,
  },
  {
    field: 'brand_name',
    title: '水品牌',
    width: 120,
  },
  // ... 其他列
];
```

#### 2.2 筛选功能（可选）

如果需要按客户类型筛选，在搜索表单中添加：

``vue
<template>
  <BasicForm @register="registerSearchForm">
    <template #customer_type="{ model, field }">
      <Select
        v-model:value="model[field]"
        placeholder="请选择客户类型"
        allow-clear
      >
        <SelectOption value="vip">VIP客户</SelectOption>
        <SelectOption value="normal">普通客户</SelectOption>
        <SelectOption value="pickup">自提客户</SelectOption>
      </Select>
    </template>
  </BasicForm>
</template>

<script setup lang="ts">
const searchFormSchema: FormSchema[] = [
  {
    field: 'keyword',
    label: '关键词',
    component: 'Input',
  },
  {
    field: 'customer_type',
    label: '客户类型',
    component: 'Select',
    componentProps: {
      options: CUSTOMER_TYPE_OPTIONS,
    },
  },
];
</script>
```

### 3. 表单组件（新增/编辑）

**文件位置**: `src/views/customer/modules/CustomerModal.vue` 或类似

#### 3.1 表单Schema配置

``typescript
import { CUSTOMER_TYPE_OPTIONS } from '@/api/customer';

const formSchema: FormSchema[] = [
  {
    field: 'id',
    label: '客户编号',
    component: 'Input',
    required: true,
  },
  {
    field: 'name',
    label: '姓名地址',
    component: 'Input',
    required: true,
  },
  // 新增客户类型字段
  {
    field: 'customer_type',
    label: '客户类型',
    component: 'Select',
    defaultValue: 'normal', // 默认值
    componentProps: {
      options: CUSTOMER_TYPE_OPTIONS,
    },
    rules: [{ required: true, message: '请选择客户类型' }],
  },
  {
    field: 'brand',
    label: '水品牌',
    component: 'ApiSelect',
    componentProps: {
      api: getWaterBrands,
      labelField: 'name',
      valueField: 'id',
    },
  },
  {
    field: 'open_date',
    label: '开户日期',
    component: 'DatePicker',
    required: true,
    componentProps: {
      valueFormat: 'YYYY-MM-DD',
    },
  },
  // ... 其他字段
];
```

#### 3.2 表单数据初始化

确保在打开弹窗时正确初始化customer_type字段：

``typescript
async function openModal(record?: Customer) {
  modalVisible.value = true;
  
  if (record) {
    // 编辑模式：使用后端返回的数据
    formData.value = {
      ...record,
      customer_type: record.customer_type || 'normal',
    };
  } else {
    // 新增模式：设置默认值
    formData.value = {
      id: '',
      name: '',
      customer_type: 'normal', // 默认普通客户
      brand: undefined,
      open_date: dayjs().format('YYYY-MM-DD'),
      // ... 其他字段
    };
  }
}
```

### 4. API调用

确保在创建和更新客户时包含customer_type字段：

```
// 创建客户
export function createCustomer(data: Partial<Customer>) {
  return requestClient.post('/v1/customers/all/', data);
}

// 更新客户
export function updateCustomer(id: string, data: Partial<Customer>) {
  return requestClient.put(`/v1/customers/${id}/`, data);
}
```

## ⚠️ 注意事项

1. **前端同步更新**：后端已添加新的客户类型选项（'closed', 'slow_pay', 'blacklist'），前端必须同步更新CUSTOMER_TYPE_OPTIONS常量和Customer接口定义，否则新选项不会在界面上显示。
2. **默认值处理**: 新增客户时，customer_type默认为'normal'（普通客户）
3. **编辑回填**: 编辑时必须从后端获取的customer_type值正确回填到表单
4. **必填验证**: 建议将customer_type设为必填字段
5. **类型安全**: 使用TypeScript枚举或联合类型确保类型安全
6. **Vben规范**: 遵循Vben Admin的代码规范和组件使用规范
7. **rowKey配置**: 确保表格配置中正确设置了rowKey为'id'

## 🧪 测试检查清单

- [ ] 表格中能正确显示客户类型（中文）
- [ ] 新增客户时可以选择客户类型
- [ ] 编辑客户时能正确回填客户类型
- [ ] 保存后数据库中customer_type字段正确更新
- [ ] 刷新页面后客户类型显示正确
- [ ] （可选）按客户类型筛选功能正常

## 📝 示例代码片段

### 完整的表单Schema示例

```
const formSchema: FormSchema[] = [
  {
    field: 'id',
    label: '客户编号',
    component: 'Input',
    colProps: { span: 12 },
    rules: [{ required: true, message: '请输入客户编号' }],
  },
  {
    field: 'name',
    label: '姓名地址',
    component: 'Input',
    colProps: { span: 24 },
    rules: [{ required: true, message: '请输入姓名地址' }],
  },
  {
    field: 'customer_type',
    label: '客户类型',
    component: 'Select',
    colProps: { span: 12 },
    defaultValue: 'normal',
    componentProps: {
      options: [
        { label: 'VIP客户', value: 'vip' },
        { label: '普通客户', value: 'normal' },
        { label: '自提客户', value: 'pickup' },
      ],
    },
    rules: [{ required: true, message: '请选择客户类型' }],
  },
  {
    field: 'brand',
    label: '水品牌',
    component: 'ApiSelect',
    colProps: { span: 12 },
    componentProps: {
      api: getWaterBrands,
      labelField: 'name',
      valueField: 'id',
    },
  },
  {
    field: 'open_date',
    label: '开户日期',
    component: 'DatePicker',
    colProps: { span: 12 },
    componentProps: {
      valueFormat: 'YYYY-MM-DD',
    },
    rules: [{ required: true, message: '请选择开户日期' }],
  },
  {
    field: 'phone',
    label: '联系电话',
    component: 'Input',
    colProps: { span: 12 },
  },
  {
    field: 'address',
    label: '详细地址',
    component: 'InputTextArea',
    colProps: { span: 24 },
  },
  {
    field: 'remark',
    label: '备注',
    component: 'InputTextArea',
    colProps: { span: 24 },
  },
  {
    field: 'is_active',
    label: '是否活跃',
    component: 'Switch',
    colProps: { span: 12 },
    defaultValue: true,
  },
];
```

## 🎯 快速开始

1. 在TypeScript接口中添加customer_type字段
2. 在表格columns中添加customer_type_display列
3. 在表单schema中添加customer_type选择框
4. 确保表单提交时包含customer_type字段
5. 测试新增、编辑、显示功能

完成以上步骤后，前端就能完整支持客户类型功能了！