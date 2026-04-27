import type { RouteRecordRaw } from 'vue-router';

const routes: RouteRecordRaw[] = [
  {
    name: 'Settings',
    path: '/settings',
    component: () => import('#/views/settings/index.vue'),
    meta: {
      icon: 'lucide:settings',
      order: 20,
      title: '基础设置',
    },
  },
];

export default routes;
