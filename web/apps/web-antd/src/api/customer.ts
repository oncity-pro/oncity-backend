/**
 * 客户管理 API
 * 与 Django 后端的客户接口对接
 */

import { requestClient } from './request';

// ==================== 常量定义 ====================

/**
 * 客户类型选项
 */
export const CUSTOMER_TYPE_OPTIONS = [
  { label: 'VIP客户', value: 'vip' },
  { label: '普通客户', value: 'normal' },
  { label: '自提客户', value: 'pickup' },
  { label: '已注销', value: 'closed' },
  { label: '收款慢', value: 'slow_pay' },
  { label: '黑名单', value: 'blacklist' },
] as const;

// ==================== 类型定义 ====================

export interface Customer {
  customer_type?:
    | 'normal'
    | 'pickup'
    | 'vip'
    | 'closed'
    | 'slow_pay'
    | 'blacklist';
  customer_type_display?: string;
  id: string;
  name: string;
  brand?: number;
  brandId?: number; // 驼峰命名（供前端使用）
  brand_name?: string;
  open_date: string;
  openDate?: string; // 驼峰命名（供前端使用）
  last_delivery_date?: null | string;
  lastDeliveryDate?: string; // 驼峰命名（供前端使用）
  close_date?: null | string;
  closeDate?: string; // 驼峰命名（供前端使用）
  phone?: string;
  remark?: string;
  is_active?: boolean;
  created_at?: string;
  updated_at?: string;
  // 新增字段：存水量
  storage_amount?: number;
  // 新增字段：欠空桶
  owed_empty_bucket?: number;
  // 新增字段：总用水量
  total_water_usage?: number;
  totalWaterUsage?: number; // 驼峰命名（供前端使用）
}

export interface CustomerListParams {
  keyword?: string;
  page?: number;
  pageSize?: number;
}

export interface CustomerCreateData {
  customer_type?:
    | 'normal'
    | 'pickup'
    | 'vip'
    | 'closed'
    | 'slow_pay'
    | 'blacklist';
  id: string;
  name: string;
  brand?: number;
  open_date: string;
  last_delivery_date: string;  // 改为必填
  phone?: string;  // 改为可选
  remark?: string;
  is_active?: boolean;
  // 新增字段：存水量
  storage_amount: number;  // 改为必填
  // 新增字段：欠空桶
  owed_empty_bucket: number;  // 改为必填
}

export interface CustomerUpdateData {
  customer_type?:
    | 'normal'
    | 'pickup'
    | 'vip'
    | 'closed'
    | 'slow_pay'
    | 'blacklist';
  name?: string;
  brand?: number;
  open_date?: string;
  last_delivery_date?: null | string;
  phone?: string;
  remark?: string;
  is_active?: boolean;
  // 新增字段：存水量
  storage_amount?: number;
  // 新增字段：欠空桶
  owed_empty_bucket?: number;
}

// ==================== API 函数 ====================

/**
 * 获取客户列表
 * @param params 查询参数(支持 keyword 搜索)
 */
export async function getCustomerListApi(
  params?: CustomerListParams,
): Promise<Customer[]> {
  return requestClient.get<Customer[]>('/v1/customers/all', { params });
}

/**
 * 获取所有客户(包括搜索)
 * @param params 查询参数
 */
export async function getAllCustomersApi(
  params?: CustomerListParams,
): Promise<Customer[]> {
  return requestClient.get<Customer[]>('/v1/customers/all', { params });
}

/**
 * 获取客户详情
 * @param id 客户编号
 */
export async function getCustomerDetailApi(id: string): Promise<Customer> {
  return requestClient.get<Customer>(`/v1/customers/${id}`);
}

/**
 * 创建客户
 * @param data 客户数据
 */
export async function createCustomerApi(
  data: CustomerCreateData,
): Promise<Customer> {
  return requestClient.post<Customer>('/v1/customers/all', data);
}

/**
 * 更新客户(完整更新)
 * @param id 客户编号
 * @param data 客户数据
 */
export async function updateCustomerApi(
  id: string,
  data: CustomerUpdateData,
): Promise<Customer> {
  return requestClient.put<Customer>(`/v1/customers/${id}`, data);
}

/**
 * 更新客户(部分更新)
 * @param id 客户编号
 * @param data 客户数据
 */
export async function patchCustomerApi(
  id: string,
  data: Partial<CustomerUpdateData>,
): Promise<Customer> {
  // Vben RequestClient 可能不支持 patch，使用 put 替代
  return requestClient.put<Customer>(`/v1/customers/${id}`, data);
}

/**
 * 删除客户
 * @param id 客户编号
 */
export async function deleteCustomerApi(id: string): Promise<void> {
  return requestClient.delete(`/v1/customers/${id}`);
}