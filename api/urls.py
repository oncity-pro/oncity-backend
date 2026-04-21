from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SampleListCreateView, SampleDetailView, HealthCheckView

# 使用路由器自动注册视图
router = DefaultRouter()
router.register(r'samples', SampleListCreateView, basename='sample')

urlpatterns = [
    # 健康检查
    path('health/', HealthCheckView.as_view(), name='health-check'),
    
    # API v1 路由
    path('v1/', include([
        path('samples/', SampleListCreateView.as_view(), name='sample-list-create'),
        path('samples/<int:pk>/', SampleDetailView.as_view(), name='sample-detail'),
    ])),
    
    # 也可以直接使用 router（如果需要）
    # path('', include(router.urls)),
]
