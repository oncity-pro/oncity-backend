import type { RouteRecordRaw } from 'vue-router';

const routes: RouteRecordRaw[] = [
  {
    name: 'CustomerList',
    path: '/customer',
    component: () => import('#/views/customer/index.vue'),
    meta: {
      icon: 'lucide:users', // 保留你原来的图标
      order: 10,
      title: '客户管理',
    },
  },
];

export default routes;
