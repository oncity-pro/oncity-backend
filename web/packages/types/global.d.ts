import type { RouteMeta as IRouteMeta } from '@vben-core/typings';

import 'vue-router';

declare module 'lucide-vue-next' {
  import type { Component } from 'vue';
  export const Check: Component;
  export const ChevronDown: Component;
  export const ChevronLeft: Component;
  export const ChevronRight: Component;
  export const ChevronUp: Component;
  export const ChevronsLeft: Component;
  export const ChevronsRight: Component;
  export const Circle: Component;
  export const Dot: Component;
  export const Eye: Component;
  export const Minus: Component;
  export const MoreHorizontal: Component;
  export const Pencil: Component;
  export const Plus: Component;
  export const Trash2: Component;
  export const X: Component;
}

declare module 'vue-router' {
  // eslint-disable-next-line @typescript-eslint/no-empty-object-type
  interface RouteMeta extends IRouteMeta {}
}

export interface VbenAdminProAppConfigRaw {
  VITE_GLOB_API_URL: string;
  VITE_GLOB_AUTH_DINGDING_CLIENT_ID: string;
  VITE_GLOB_AUTH_DINGDING_CORP_ID: string;
}

interface AuthConfig {
  dingding?: {
    clientId: string;
    corpId: string;
  };
}

export interface ApplicationConfig {
  apiURL: string;
  auth: AuthConfig;
}

declare global {
  interface Window {
    _VBEN_ADMIN_PRO_APP_CONF_: VbenAdminProAppConfigRaw;
  }
}
