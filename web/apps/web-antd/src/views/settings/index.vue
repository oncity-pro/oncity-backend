<script lang="ts" setup>
import type { VxeTableGridOptions } from '#/adapter/vxe-table';

import { Page, useVbenModal } from '@vben/common-ui';
import { Plus } from '@vben/icons';

import { Modal as AntdModal, Button, message } from 'ant-design-vue';

import { useVbenVxeGrid } from '#/adapter/vxe-table';
import { deleteWaterBrandApi, getWaterBrandListApi, type WaterBrand } from '#/api/water-brand';

import BrandForm from './modules/brand-form.vue';

// 创建弹窗
const [BrandFormModal, brandFormModalApi] = useVbenModal({
  connectedComponent: BrandForm,
  destroyOnClose: true,
});

// 新增品牌
function onCreate() {
  brandFormModalApi.setData(null).open();
}

// 删除品牌
function onDelete(row: WaterBrand) {
  AntdModal.confirm({
    title: '确认删除',
    content: `确定要删除品牌"${row.name}"吗？`,
    okText: '确定',
    cancelText: '取消',
    onOk: async () => {
      try {
        await deleteWaterBrandApi(row.id);
        message.success('删除成功');
        refreshGrid();
      } catch (error) {
        console.error('删除失败:', error);
        message.error('删除失败');
      }
    },
  });
}

// 刷新表格
function refreshGrid() {
  gridApi.query();
}

// 表格配置
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
  height: 'auto',
  keepSource: true,
  pagerConfig: {
    enabled: true,
    pageSize: 10,
    pageSizes: [10, 20, 50, 100],
  },
  proxyConfig: {
    ajax: {
      query: async ({ page }) => {
        console.log('查询参数:', { page });
        // 调用API获取数据
        const data = await getWaterBrandListApi();
        
        // 模拟分页
        const total = data.length;
        const start = (page.currentPage - 1) * page.pageSize;
        const end = start + page.pageSize;
        const items = data.slice(start, end);
        
        return {
          items,
          total,
        };
      },
    },
  },
  toolbarConfig: {
    refresh: true,
    zoom: true,
    custom: true,
  },
};

const [Grid, gridApi] = useVbenVxeGrid({ gridOptions });
</script>

<template>
  <Page auto-content-height title="基础设置">
    <BrandFormModal @success="refreshGrid" />
    <Grid table-title="桶装水品牌管理">
      <template #toolbar-tools>
        <Button type="primary" @click="onCreate">
          <Plus class="size-5" />
          新增品牌
        </Button>
      </template>
      
      <!-- 操作列 -->
      <template #action="{ row }">
        <Button type="link" danger size="small" @click="onDelete(row)">
          删除
        </Button>
      </template>
    </Grid>
  </Page>
</template>
