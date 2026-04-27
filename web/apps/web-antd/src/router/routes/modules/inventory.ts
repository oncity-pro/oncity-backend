import type { RouteRecordRaw } from 'vue-router';

const inventoryRoutes: RouteRecordRaw[] = [
  {
    path: '/inventory',
    name: 'inventory',
    component: () => import('#/views/inventory/index.vue'),
    meta: {
      title: 'page.inventory.title',
      requiresAuth: true,
      icon: 'mdi:package-variant-closed',
      order: 3,
    },
  },
];

export default inventoryRoutes;