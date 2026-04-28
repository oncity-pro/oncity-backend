<script lang="ts" setup>
import type { Customer } from '#/api/customer';

import { computed } from 'vue';

import { useVbenModal } from '@vben/common-ui';

import { Descriptions, DescriptionsItem, Tag } from 'ant-design-vue';

const props = defineProps<{
  customerData?: Customer | null;
  brandName?: string;
}>();

const customer = computed(() => props.customerData);

const [Modal, modalApi] = useVbenModal({
  onOpenChange(isOpen: boolean) {
    if (isOpen) {
      modalApi.setState({ title: '客户详情' });
    }
  },
});

function getCustomerTypeColor(type?: string) {
  switch (type) {
    case 'vip':
      return 'gold';
    case 'normal':
      return 'blue';
    case 'pickup':
      return 'cyan';
    case 'closed':
      return 'default';
    case 'slow_pay':
      return 'orange';
    case 'blacklist':
      return 'red';
    default:
      return 'default';
  }
}

function getCustomerTypeLabel(type?: string) {
  switch (type) {
    case 'vip':
      return 'VIP客户';
    case 'normal':
      return '普通客户';
    case 'pickup':
      return '自提客户';
    case 'closed':
      return '已注销';
    case 'slow_pay':
      return '收款慢';
    case 'blacklist':
      return '黑名单';
    default:
      return type || '-';
  }
}
</script>

<template>
  <Modal :footer="false" class="w-[800px]">
    <Descriptions
      v-if="customer"
      :column="3"
      bordered
      :label-style="{ width: '80px', whiteSpace: 'nowrap' }"
    >
      <DescriptionsItem label="客户编号">
        {{ customer.id }}
      </DescriptionsItem>
      <DescriptionsItem label="姓名地址">
        {{ customer.name }}
      </DescriptionsItem>
      <DescriptionsItem label="客户类型">
        <Tag :color="getCustomerTypeColor(customer.customer_type)">
          {{ getCustomerTypeLabel(customer.customer_type) }}
        </Tag>
      </DescriptionsItem>
      <DescriptionsItem label="品牌">
        {{ brandName || customer.brand_name || '-' }}
      </DescriptionsItem>
      <DescriptionsItem label="联系电话">
        {{ customer.phone || '-' }}
      </DescriptionsItem>
      <DescriptionsItem label="开户日期">
        {{ customer.openDate || customer.open_date || '-' }}
      </DescriptionsItem>
      <DescriptionsItem label="最后送水日期">
        {{ customer.lastDeliveryDate || customer.last_delivery_date || '-' }}
      </DescriptionsItem>
      <DescriptionsItem label="存水量">
        {{ customer.storage_amount ?? '-' }}
      </DescriptionsItem>
      <DescriptionsItem label="欠空桶">
        {{ customer.owed_empty_bucket ?? '-' }}
      </DescriptionsItem>
      <DescriptionsItem label="总用水量">
        {{ customer.total_water_usage ?? customer.totalWaterUsage ?? '-' }}
      </DescriptionsItem>
      <DescriptionsItem label="备注">
        {{ customer.remark || '-' }}
      </DescriptionsItem>
    </Descriptions>
  </Modal>
</template>
