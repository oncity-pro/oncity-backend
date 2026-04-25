from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    SampleListCreateView, 
    SampleDetailView, 
    HealthCheckView,
    WaterBrandListView,
    WaterBrandListCreateView,
    WaterBrandDetailView,
    CustomerListView,
    CustomerListCreateView,
    CustomerDetailView,
    CustomerStatsView,
    LoginView,
    LogoutView,
    RefreshTokenView,
    AccessCodesView,
    UserInfoView,
    MenuView
)

# 使用路由器自动注册视图
router = DefaultRouter()
router.register(r'samples', SampleListCreateView, basename='sample')

urlpatterns = [
    # 健康检查
    path('health', HealthCheckView.as_view(), name='health-check'),
    
    # 认证路由
    path('auth/login', LoginView.as_view(), name='login'),
    path('auth/logout', LogoutView.as_view(), name='logout'),
    path('auth/refresh', RefreshTokenView.as_view(), name='refresh-token'),
    path('auth/codes', AccessCodesView.as_view(), name='access-codes'),
    
    # 用户信息路由
    path('user/info', UserInfoView.as_view(), name='user-info'),
    
    # 菜单路由
    path('menu/all', MenuView.as_view(), name='menu-all'),
    
    # API v1 路由
    path('v1/', include([
        # Sample 路由
        path('samples', SampleListCreateView.as_view(), name='sample-list-create'),
        path('samples/<int:pk>', SampleDetailView.as_view(), name='sample-detail'),
        
        # WaterBrand 路由
        path('water-brands', WaterBrandListView.as_view(), name='water-brand-list'),
        path('water-brands/all', WaterBrandListCreateView.as_view(), name='water-brand-list-create'),
        path('water-brands/<int:pk>', WaterBrandDetailView.as_view(), name='water-brand-detail'),
        
        # Customer 路由
        path('customers', CustomerListView.as_view(), name='customer-list'),
        path('customers/all', CustomerListCreateView.as_view(), name='customer-list-create'),
        path('customers/<str:pk>', CustomerDetailView.as_view(), name='customer-detail'),
        
        # Statistics 路由
        path('stats/customers', CustomerStatsView.as_view(), name='customer-stats'),
    ])),
    
    # 也可以直接使用 router（如果需要）
    # path('', include(router.urls)),
]