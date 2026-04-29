<script lang="ts" setup>
import type { VbenFormProps } from '#/adapter/form';
import type { VxeTableGridOptions } from '#/adapter/vxe-table';
import type { Customer } from '#/api/customer';
import type { WaterBrand } from '#/api/water-brand';

import { defineComponent, h, onMounted, ref, nextTick } from 'vue';

import { Page, useVbenModal } from '@vben/common-ui';
import { Plus } from '@vben/icons';
import { Eye, MoreHorizontal, Pencil, Search, Trash2 } from 'lucide-vue-next';

import { Button, Dropdown, Menu, message, Modal } from 'ant-design-vue';

import { useVbenVxeGrid } from '#/adapter/vxe-table';
import { 
  deleteCustomerApi,
  getCustomerListApi 
} from '#/api/customer';
import { 
  getWaterBrandListApi
} from '#/api/water-brand';

import Detail from './modules/detail.vue';
import Form from './modules/form.vue';

// 品牌列表（用于显示品牌名称）
const brandMap = ref<Map<number, string>>(new Map());

// 加载状态
const loading = ref(false);

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
    message.error('加载品牌数据失败');
  }
}

// 创建弹窗
const [FormModal, formModalApi] = useVbenModal({
  connectedComponent: Form,
  destroyOnClose: true,
});

// 详情弹窗
const [DetailModal, detailModalApi] = useVbenModal({
  connectedComponent: Detail,
  destroyOnClose: true,
});

// 当前编辑的客户数据（用于替代 modalApi.setData/getData）
const currentCustomer = ref<Customer | null>(null);

// 当前查看详情的客户数据
const currentDetailCustomer = ref<Customer | null>(null);
const detailBrandName = ref<string>('');

// 新增客户
function onCreate() {
  currentCustomer.value = null;
  formModalApi.open();
}

// 查看详情
function onViewDetail(row: Customer) {
  currentDetailCustomer.value = { ...row };
  detailBrandName.value = row.brand ? (brandMap.value.get(row.brand) ?? '') : '';
  detailModalApi.open();
}

// 编辑客户
async function onEdit(row: Customer) {
  // 使用 toRaw 避免响应式代理对象问题
  const { toRaw } = await import('vue');
  currentCustomer.value = toRaw({...row}); // 使用展开运算符复制对象
  console.warn('onEdit - 设置 currentCustomer:', currentCustomer.value);
  console.warn('onEdit - currentCustomer.id:', currentCustomer.value?.id);
  console.warn('onEdit - 准备打开弹窗');
  
  // 使用 nextTick 替代 setTimeout
  await nextTick();
  formModalApi.open();
}

// 点击删除菜单项，弹出确认对话框
function handleDeleteClick(row: Customer) {
  Modal.confirm({
    title: '确定要删除这个客户吗？',
    content: '删除后无法恢复，请谨慎操作。',
    okText: '确定',
    okType: 'danger',
    cancelText: '取消',
    onOk: () => onDelete(row),
  });
}

// 删除客户
async function onDelete(row: Customer) {
  // 验证客户 ID 是否存在
  if (!row.id) {
    message.error('客户编号不存在，无法删除');
    console.error('删除失败：客户数据缺少 ID', row);
    return;
  }
  
  try {
    console.warn(`准备删除客户，ID: ${row.id}`);
    await deleteCustomerApi(row.id);
    message.success('删除成功');
    refreshGrid();
  } catch (error: any) {
    console.error('删除失败:', error);
    
    // 检查错误响应
    let errorMessage = '删除失败';
    if (error.response) {
      // 服务器响应了错误状态码
      if (error.response.status === 404) {
        errorMessage = '客户不存在，无法删除';
      } else if (error.response.data?.message) {
        errorMessage = error.response.data.message;
      } else if (error.response.data?.detail) {
        errorMessage = error.response.data.detail;
      }
    } else if (error.message) {
      errorMessage = error.message;
    }
    
    message.error(errorMessage);
  }
}

// 刷新表格
function refreshGrid() {
  gridApi.query();
}

// 搜索表单配置
const formOptions: VbenFormProps = {
  // 默认展开
  collapsed: false,
  // inline 布局 + 靠右对齐
  layout: 'inline',
  wrapperClass: 'justify-end',
  schema: [
    {
      component: 'Input',
      componentProps: {
        placeholder: '输入编号或姓名地址搜索',
        allowClear: true,
        style: { width: '240px' },
      },
      fieldName: 'keyword',
      label: (() =>
        h('span', { class: 'flex items-center gap-1' }, [
          h(Search, { class: 'size-4' }),
          '查询',
        ])) as any,
      // 移除字段默认边距，确保与表格左对齐
      formItemClass: '!mb-0',
      // label 左对齐，覆盖默认的右对齐
      labelClass: '!text-left',
    },
  ],
  // 控制表单是否显示折叠按钮
  showCollapseButton: false,
  // 隐藏默认操作按钮（实时搜索无需点击查询）
  showDefaultActions: false,
  // 是否在字段值改变时提交表单（启用实时搜索）
  submitOnChange: true,
  // 按下回车时是否提交表单
  submitOnEnter: true,
};

// 表格配置
const gridOptions: VxeTableGridOptions<Customer> = {
  rowConfig: {
    keyField: 'id',  // 使用正确的属性来指定行的唯一标识
  },
  stripe: true,  // 启用斑马纹
  columns: [
    { title: '序号', type: 'seq', width: 60 },
    { field: 'id', title: '客户编号', width: 100 },
    { 
      field: 'name', 
      title: '姓名地址', 
      minWidth: 200,
    },
    { field: 'customer_type_display', title: '客户类型', width: 100 },
    { 
      field: 'brandId', 
      title: '品牌', 
      width: 120,
      slots: { default: 'brand' },
    },
    { field: 'openDate', title: '开户日期', width: 120 },
    { field: 'lastDeliveryDate', title: '最后送水日期', width: 130 },
    { field: 'storage_amount', title: '存水量', width: 100 },
    { field: 'owed_empty_bucket', title: '欠空桶', width: 100 },
    { field: 'total_water_usage', title: '总用水量', width: 100 },
    {
      title: '操作',
      width: 80,
      fixed: 'right',
      slots: { default: 'action' },
    },
  ],
  height: 'auto',
  keepSource: true,
  pagerConfig: {
    enabled: true,
    pageSize: 12,  // ✅ 修改为每页默认显示12条
    pageSizes: [12, 13, 14, 15],  // ✅ 更新分页选项为12/13/14/15
  },
  proxyConfig: {
    ajax: {
      query: async ({ page }, formValues) => {
        
        loading.value = true;
        
        try {
          // 加载品牌数据（如果还没有加载）
          if (brandMap.value.size === 0) {
            await loadBrands();
          }
          
          // 调用真实 API 获取数据
          const params: any = {};
          if (formValues.keyword) {
            params.keyword = formValues.keyword;
          }
          
          const data = await getCustomerListApi(params);
          
          // 调试：打印第一条数据的结构
          if (data && data.length > 0) {
            console.warn('客户数据结构示例:', data[0]);
            const firstItem = data[0];
            if (firstItem) {
              console.warn('客户数据所有键名:', Object.keys(firstItem));
            }
          }
          
          // 模拟分页（后端暂未支持分页，前端处理）
          const total = data.length;
          const start = (page.currentPage - 1) * page.pageSize;
          const end = start + page.pageSize;
          const items = data.slice(start, end);
          
          return {
            items,
            total,
          };
        } catch (error) {
          console.error('获取客户列表失败:', error);
          message.error('获取客户列表失败');
          return {
            items: [],
            total: 0,
          };
        } finally {
          loading.value = false;
        }
      },
    },
  },
  toolbarConfig: {
    // 显示搜索表单控制按钮
    search: true,
    refresh: true,
    zoom: true,
    custom: true,
  },
};

const [Grid, gridApi] = useVbenVxeGrid({ formOptions, gridOptions });

// 组件挂载时加载品牌数据
onMounted(() => {
  loadBrands();
});
</script>

<template>
  <Page auto-content-height title="客户管理">
    <FormModal :customer-data="currentCustomer" @success="refreshGrid" />
    <DetailModal :customer-data="currentDetailCustomer" :brand-name="detailBrandName" />
    <Grid table-title="客户列表" :loading="loading">
      <template #toolbar-tools>
        <Button type="primary" @click="onCreate">
          <Plus class="size-5" />
          新增客户
        </Button>
      </template>
      
      <!-- 自定义品牌列的渲染 -->
      <template #brand="{ row }">
        {{ row.brand ? brandMap.get(row.brand) : '-' }}
      </template>
      
      <!-- 操作列 -->
      <template #action="{ row }">
        <Dropdown :trigger="['click']">
          <Button type="link" size="small">
            <MoreHorizontal class="size-4" />
          </Button>
          <template #overlay>
            <Menu>
              <Menu.Item @click="onViewDetail(row)">
                <span class="flex items-center gap-1">
                  <Eye class="size-3.5" />
                  详情
                </span>
              </Menu.Item>
              <Menu.Item @click="onEdit(row)">
                <span class="flex items-center gap-1">
                  <Pencil class="size-3.5" />
                  编辑
                </span>
              </Menu.Item>
              <Menu.Item danger @click="handleDeleteClick(row)">
                <span class="flex items-center gap-1">
                  <Trash2 class="size-3.5" />
                  删除
                </span>
              </Menu.Item>
            </Menu>
          </template>
        </Dropdown>
      </template>
    </Grid>
  </Page>
</template>
