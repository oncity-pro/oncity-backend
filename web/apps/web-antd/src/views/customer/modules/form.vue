<script lang="ts" setup>

import type { 
  Customer, 
  CustomerCreateData,
  CustomerUpdateData,
} from '#/api/customer';
import type { WaterBrand } from '#/api/water-brand';

import { ref } from 'vue';

import { useVbenModal } from '@vben/common-ui';

import { message } from 'ant-design-vue';

import { useVbenForm } from '#/adapter/form';
import { 
  createCustomerApi, 
  CUSTOMER_TYPE_OPTIONS, 
  updateCustomerApi,
} from '#/api/customer';
import { getBucketDepositConfigApi } from '#/api/settings';
import { 
  getWaterBrandListApi, 
} from '#/api/water-brand';

// 定义 props 接收客户数据（作为备用方案）
const props = defineProps<{
  customerData?: Customer | null;
}>();

const emit = defineEmits<{ success: [] }>();

// 每桶押金金额（从全局配置获取）
const depositPerBucket = ref<number>(30);

// 品牌列表 - 现在由ApiSelect组件内部处理
// const brandOptions = ref<Array<{ label: string; value: number }>>([]);
// const allBrands = ref<WaterBrand[]>([]); // 存储完整品牌信息

// 加载品牌选项 - 现在由ApiSelect组件内部处理
// async function loadBrandOptions() {
//   try {
//     const brands = await getWaterBrandListApi();
//     console.log('加载的品牌数据:', brands); // 添加调试信息
//     allBrands.value = brands;
//     brandOptions.value = brands.map((brand: WaterBrand) => ({
//       label: brand.name,
//       value: brand.id,
//     }));
//     console.log('转换后的品牌选项:', brandOptions.value); // 添加调试信息
//   } catch (error) {
//     console.error('加载品牌选项失败:', error);
//   }
// }

// 表单配置
const [Form, formApi] = useVbenForm({
  schema: [
    {
      component: 'Input',
      componentProps: {
        placeholder: '请输入客户编号',
      },
      fieldName: 'id',
      label: '客户编号',
      rules: 'required',
    },
    {
      component: 'Input',
      componentProps: {
        placeholder: '请输入姓名和地址',
      },
      fieldName: 'name',
      label: '姓名地址',
      rules: 'required',
    },
    {
      component: 'Select',
      componentProps: {
        placeholder: '请选择客户类型',
        options: CUSTOMER_TYPE_OPTIONS,
      },
      fieldName: 'customer_type',
      label: '客户类型',
      defaultValue: 'normal',
    },
    {
      component: 'InputNumber',
      componentProps: {
        placeholder: '请输入存水量',
        min: 0,
      },
      fieldName: 'storage_amount',
      label: '存水量',
      rules: 'required',  // 设置为必填
      defaultValue: 0,  // 设置默认值为0
    },
    {
      component: 'InputNumber',
      componentProps: {
        placeholder: '请输入欠空桶数',
        min: 0,
        onChange: (value: number | null) => {
          const owed = value || 0;
          formApi.setValues({
            empty_bucket_deposit: Number((owed * depositPerBucket.value).toFixed(2)),
          });
        },
      },
      fieldName: 'owed_empty_bucket',
      label: '欠空桶',
      rules: 'required',  // 设置为必填
    },
    {
      component: 'InputNumber',
      componentProps: {
        disabled: true,
        placeholder: '自动计算',
        addonAfter: '元',
      },
      fieldName: 'empty_bucket_deposit',
      label: '空桶押金',
    },
    {
      component: 'ApiSelect',
      fieldName: 'brand',
      label: '水品牌',
      componentProps: {
        api: getWaterBrandListApi,
        labelField: 'name',
        valueField: 'id',
        placeholder: '请选择品牌',
        allowClear: true,
        popupMatchSelectWidth: false, // 下拉框不与选择框宽度匹配
        dropdownStyle: { minWidth: '200px' }, // 设置下拉框最小宽度
      },
    },
    {
      component: 'DatePicker',
      componentProps: {
        placeholder: '请选择开户日期',
        format: 'YYYY-MM-DD',
        valueFormat: 'YYYY-MM-DD',
      },
      fieldName: 'open_date',
      label: '开户日期',
      // 移除必填规则，因为将设置默认值
    },
    {
      component: 'DatePicker',
      componentProps: {
        placeholder: '请选择最后送水日期',
        format: 'YYYY-MM-DD',
        valueFormat: 'YYYY-MM-DD',
        allowClear: true,
      },
      fieldName: 'last_delivery_date',
      label: '最后送水日期',
      rules: 'required',  // 设置为必填
    },
    {
      component: 'Input',
      componentProps: {
        placeholder: '请输入联系电话',
      },
      fieldName: 'phone',
      label: '联系电话',
      // 移除必填规则
    },
    // 删除详细地址字段
    {
      component: 'Textarea',
      componentProps: {
        placeholder: '请输入备注信息',
        rows: 2,
      },
      fieldName: 'remark',
      label: '备注',
    },
  ],
  layout: 'horizontal',
  showDefaultActions: false,  // 隐藏表单自带的提交和重置按钮
});

// 弹窗配置
const [Modal, modalApi] = useVbenModal({
  async onConfirm() {
    const { valid } = await formApi.validate();
    if (!valid) return;

    // 禁用确认按钮，防止重复提交
    modalApi.setState({ confirmLoading: true });

    const values = await formApi.getValues();
    
    // 只使用 props 传递的数据
    const customerData = props.customerData;
    const isEdit = !!(customerData && Object.keys(customerData).length > 0);
    
    try {
      if (isEdit) {
        // 编辑模式：剔除 id，防止尝试修改主键
        if (customerData) {
          const { id: _id, ...updateValues } = values;
          await updateCustomerApi(customerData.id, updateValues as CustomerUpdateData);
          message.success('更新成功');
        }
      } else {
        // 新增模式
        await createCustomerApi(values as CustomerCreateData);
        message.success('创建成功');
      }
      
      modalApi.close();
      emit('success');
    } catch (error: any) {
      console.error('保存失败:', error);
      console.error('错误对象详情:', { 
        errorInstance: error.constructor.name, 
        hasResponse: !!error.response, 
        responseStatus: error.response?.status,
        responseData: error.response?.data,
        hasRequest: !!error.request,
        message: error.message
      });
      
      // 检查错误响应结构并显示相应消息
      // RequestClient 在 HTTP 错误时直接抛出 error.response.data，
      // 因此 error 本身可能就是响应体，需要兼容处理
      const isRawResponseData =
        error &&
        typeof error === 'object' &&
        !error.response &&
        !error.request &&
        Object.keys(error).length > 0;

      if (error.response || isRawResponseData) {
        const responseData = error.response?.data ?? error;
        
        // 检查是否包含 detail 字段（一般错误）
        if (responseData && typeof responseData === 'object' && responseData.detail) {
          message.error(responseData.detail);
        } 
        // 处理字段验证错误对象，例如：{'id': [ErrorDetail], 'customer_number': [ErrorDetail]}
        else if (Array.isArray(responseData)) {
          // 处理数组形式的错误
          responseData.forEach(_error => {
            const errorMessage = typeof _error === 'object' 
              ? (_error.string || _error.message || _error.msg || _error.detail || String(_error))
              : String(_error);
            message.error(errorMessage);
          });
        }
        else if (responseData && typeof responseData === 'object') {
          let hasFieldErrors = false;
          
          // 遍历所有可能的字段错误
          for (const [field, messages] of Object.entries(responseData)) {
            // 检查是否是非字段错误（如non_field_errors）
            if (Array.isArray(messages) && messages.length > 0) {
              hasFieldErrors = true;  // 仅在数组有内容时才标记有字段错误
              
              // 处理ErrorDetail对象数组
              for (const msg of messages) {
                // 尝试不同的可能属性名称，合并声明和赋值
                const errorMessage = typeof msg === 'object' ? (msg.string || msg.message || msg.msg || msg.detail || String(msg)) : String(msg);
                
                // 针对唯一性错误提供更友好的提示
                const isUniqueError = errorMessage.includes('已存在') || errorMessage.toLowerCase().includes('unique');
                const displayMessage = isUniqueError && field === 'id'
                  ? '客户编号已存在，请重新输入'
                  : `${field}: ${errorMessage}`;
                
                message.error(displayMessage);
              }
            } else if (typeof messages === 'string') {
              // 处理直接的字符串错误
              hasFieldErrors = true;
              message.error(`${field}: ${messages}`);
            } else if (typeof messages === 'object' && messages !== null) {
              // 处理嵌套对象
              hasFieldErrors = true;
              message.error(`${field}: ${JSON.stringify(messages)}`);
            }
          }
          
          // 如果没有处理过任何字段错误，显示通用消息
          if (!hasFieldErrors) {
            message.error('数据验证失败');
          }
        } 
        // 如果响应数据是字符串
        else if (typeof responseData === 'string') {
          message.error(responseData);
        } 
        // 其他情况
        else {
          message.error(`数据验证失败：${JSON.stringify(responseData)}`);
        }
      } else {
        // 网络错误或请求配置错误
        if (error.request) {
          // 请求已发出但没有收到响应（网络错误）
          message.error('网络连接错误或服务器无响应');
        } else {
          // 其他错误（如请求配置错误）
          message.error(`请求配置错误: ${error.message}`);
        }
      }
    } finally {
      // 确保无论成功或失败都要重新启用确认按钮
      modalApi.setState({ confirmLoading: false });
    }
  },
  async onOpenChange(isOpen: boolean) {
    if (isOpen) {
      // 优先使用 props 传递的数据
      const data = props.customerData;
      console.warn('=== 表单组件 onOpenChange ===');
      console.warn('onOpenChange - props.customerData:', props.customerData);
      console.warn('onOpenChange - data:', data);
      console.warn('onOpenChange - data 是否为空对象:', data && Object.keys(data).length === 0);
      console.warn('onOpenChange - data 所有键名:', data ? Object.keys(data) : []);
      console.warn('===========================');

      // 加载空桶押金配置
      try {
        const config = await getBucketDepositConfigApi();
        depositPerBucket.value = config.amount_per_bucket;
      } catch (error) {
        console.error('加载空桶押金配置失败:', error);
      }
      
      if (data && Object.keys(data).length > 0) {
        // 编辑模式：填充表单数据
        console.warn('进入编辑模式，准备设置表单值');
        await formApi.setValues(data);
        // 计算空桶押金
        const owed = data.owed_empty_bucket || 0;
        await formApi.setValues({
          empty_bucket_deposit: Number((owed * depositPerBucket.value).toFixed(2)),
        });
        modalApi.setState({ title: '编辑客户' });
      } else {
        // 新增模式：重置表单并设置默认值
        console.warn('进入新增模式，重置表单');
        await formApi.resetForm();
        
        // 设置默认值
        const today = new Date().toISOString().split('T')[0]; // 获取今天的日期，格式为 YYYY-MM-DD
        await formApi.setValues({ 
          open_date: today, // 设置开户日期为今天
          empty_bucket_deposit: 0,
          
          // 设置怡宝为默认品牌
          brand: 2  // 假设怡宝的ID是2
        });
        
        modalApi.setState({ title: '新增客户' });
      }
    }
  },
});
</script>

<template>
  <Modal :footer="true">
    <Form />
  </Modal>
</template>