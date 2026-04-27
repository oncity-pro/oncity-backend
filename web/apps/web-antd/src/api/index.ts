/**
 * API 模块统一导出
 */

// 认证管理
export * from './core/auth';

// 菜单管理
export * from './core/menu';

// 用户管理
export * from './core/user';

// 客户管理
export * from './customer';

// 请求客户端
export { baseRequestClient, requestClient } from './request';

// 水品牌管理
export * from './water-brand';