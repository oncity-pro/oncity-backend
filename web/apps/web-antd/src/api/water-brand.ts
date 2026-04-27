/**
 * 水品牌管理 API
 * 与 Django 后端的水品牌接口对接
 */

import { requestClient } from './request';

// ==================== 类型定义 ====================

export interface WaterBrand {
  id: number;
  name: string;
  description?: string;
  is_active?: boolean;
  created_at?: string;
  updated_at?: string;
}

// ==================== API 函数 ====================

/**
 * 获取启用的水品牌列表
 */
export async function getWaterBrandListApi(): Promise<WaterBrand[]> {
  return requestClient.get<WaterBrand[]>('/v1/water-brands/all');
}

/**
 * 获取所有水品牌(包括禁用的)
 */
export async function getAllWaterBrandsApi(): Promise<WaterBrand[]> {
  return requestClient.get<WaterBrand[]>('/v1/water-brands/all');
}

/**
 * 获取水品牌详情
 * @param id 品牌ID
 */
export async function getWaterBrandDetailApi(id: number): Promise<WaterBrand> {
  return requestClient.get<WaterBrand>(`/v1/water-brands/${id}`);
}

/**
 * 创建水品牌
 * @param data 品牌数据
 */
export async function createWaterBrandApi(data: Partial<WaterBrand>): Promise<WaterBrand> {
  return requestClient.post<WaterBrand>('/v1/water-brands/all', data);
}

/**
 * 更新水品牌(完整更新)
 * @param id 品牌ID
 * @param data 品牌数据
 */
export async function updateWaterBrandApi(id: number, data: Partial<WaterBrand>): Promise<WaterBrand> {
  return requestClient.put<WaterBrand>(`/v1/water-brands/${id}`, data);
}

/**
 * 更新水品牌(部分更新)
 * @param id 品牌ID
 * @param data 品牌数据
 */
export async function patchWaterBrandApi(id: number, data: Partial<WaterBrand>): Promise<WaterBrand> {
  // Vben RequestClient 可能不支持 patch，使用 put 替代
  return requestClient.put<WaterBrand>(`/v1/water-brands/${id}`, data);
}

/**
 * 删除水品牌
 * @param id 品牌ID
 */
export async function deleteWaterBrandApi(id: number): Promise<void> {
  return requestClient.delete(`/v1/water-brands/${id}`);
}
