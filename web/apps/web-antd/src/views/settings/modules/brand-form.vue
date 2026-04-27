<script lang="ts" setup>
import { computed, ref } from 'vue';

import { useVbenModal } from '@vben/common-ui';

import { message } from 'ant-design-vue';

import { useVbenForm } from '#/adapter/form';
import { createWaterBrandApi, type WaterBrand } from '#/api/water-brand';

const emit = defineEmits(['success']);

const formData = ref<null | WaterBrand>(null);

const getTitle = computed(() => {
  return formData.value?.id ? '编辑品牌' : '新增品牌';
});

// 表单配置
const [Form, formApi] = useVbenForm({
  layout: 'vertical',
  schema: [
    {
      component: 'Input',
      componentProps: {
        placeholder: '请输入品牌名称',
        maxlength: 50,
      },
      fieldName: 'name',
      label: '品牌名称',
      rules: 'required',
    },
  ],
  showDefaultActions: false,
});

// 弹窗配置
const [Modal, modalApi] = useVbenModal({
  async onConfirm() {
    const { valid } = await formApi.validate();
    if (valid) {
      modalApi.lock();
      const values = await formApi.getValues();
      
      try {
        // 调用真实的创建API
        await createWaterBrandApi({ 
          name: values.name,
        });
        
        message.success('新增成功');
        modalApi.close();
        emit('success');
      } catch (error: any) {
        console.error('操作失败:', error);
        // 显示后端返回的错误信息
        const errorMsg = error.response?.data?.detail || 
                        Object.values(error.response?.data || {})[0] || 
                        '操作失败';
        message.error(typeof errorMsg === 'string' ? errorMsg : '操作失败');
      } finally {
        modalApi.lock(false);
      }
    }
  },
  onOpenChange(isOpen) {
    if (isOpen) {
      const data = modalApi.getData<WaterBrand>();
      formData.value = data || null;
      
      if (data) {
        formApi.setValues(data);
      } else {
        formApi.resetForm();
      }
    }
  },
});
</script>

<template>
  <Modal :title="getTitle">
    <Form class="mx-4" />
  </Modal>
</template>
