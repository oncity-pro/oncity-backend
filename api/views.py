from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Sample, WaterBrand, Customer
from .serializers import SampleSerializer, WaterBrandSerializer, CustomerSerializer
from .authentication import BearerTokenAuthentication


# ==================== Authentication Views ====================

class LoginView(APIView):
    """
    用户登录视图
    POST /api/auth/login/
    """
    permission_classes = []  # 允许未认证用户访问
    
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        if not username or not password:
            return Response({
                'code': 1,
                'message': '请提供用户名和密码'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # 验证用户
        user = authenticate(username=username, password=password)
        
        if user is not None:
            # 生成或获取 token
            token, created = Token.objects.get_or_create(user=user)
            
            return Response({
                'code': 0,
                'message': '登录成功',
                'data': {
                    'accessToken': token.key,
                    'user': {
                        'id': user.id,
                        'username': user.username,
                        'email': user.email,
                        'first_name': user.first_name,
                        'last_name': user.last_name
                    }
                }
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'code': 1,
                'message': '用户名或密码错误'
            }, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    """
    用户登出视图
    POST /api/auth/logout/
    """
    def post(self, request):
        # 删除用户的 token
        try:
            token = Token.objects.get(user=request.user)
            token.delete()
            return Response({
                'code': 0,
                'message': '退出成功'
            }, status=status.HTTP_200_OK)
        except Token.DoesNotExist:
            return Response({
                'code': 0,
                'message': '已退出'
            }, status=status.HTTP_200_OK)


class RefreshTokenView(APIView):
    """
    刷新 Token 视图
    POST /api/auth/refresh/
    """
    def post(self, request):
        # 简单实现：返回当前 token
        try:
            token = Token.objects.get(user=request.user)
            return Response({
                'code': 0,
                'data': token.key
            }, status=status.HTTP_200_OK)
        except Token.DoesNotExist:
            return Response({
                'code': 1,
                'message': '未授权'
            }, status=status.HTTP_401_UNAUTHORIZED)


class AccessCodesView(APIView):
    """
    获取用户权限码视图
    GET /api/auth/codes/
    """
    def get(self, request):
        # 简单实现：返回所有权限码
        # 实际项目中应该根据用户角色返回对应的权限码
        return Response({
            'code': 0,
            'data': [
                'AC_100100',
                'AC_100110',
                'AC_100120',
                'AC_100010',
                'AC_100020',
                'AC_100030',
            ]
        }, status=status.HTTP_200_OK)


class UserInfoView(APIView):
    """
    获取用户信息视图
    GET /api/user/info/
    """
    def get(self, request):
        # 检查用户是否已认证
        if not request.user or not request.user.is_authenticated:
            return Response({
                'code': 1,
                'message': '未授权访问'
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        user = request.user
        
        return Response({
            'code': 0,
            'data': {
                'userId': user.id,
                'username': user.username,
                'realName': f'{user.first_name} {user.last_name}'.strip() or user.username,
                'email': user.email,
                'avatar': None,  # 可以后续添加头像功能
                'desc': None,
                'homePath': '/dashboard',  # 默认首页
                'roles': ['admin'] if user.is_superuser else ['user'],
                'authBtnList': ['*']  # 所有权限
            }
        }, status=status.HTTP_200_OK)


# ==================== Sample Views (原有代码) ====================

class HealthCheckView(APIView):
    """
    健康检查视图
    """
    def get(self, request):
        return Response({
            'status': 'healthy',
            'message': 'ONCITY API is running'
        }, status=status.HTTP_200_OK)


class SampleListCreateView(generics.ListCreateAPIView):
    """
    示例列表和创建视图
    """
    queryset = Sample.objects.all()
    serializer_class = SampleSerializer


class SampleDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    示例详情、更新和删除视图
    """
    queryset = Sample.objects.all()
    serializer_class = SampleSerializer


# ==================== WaterBrand Views ====================

class WaterBrandListView(generics.ListAPIView):
    """
    水品牌列表视图
    """
    queryset = WaterBrand.objects.filter(is_active=True)
    serializer_class = WaterBrandSerializer


class WaterBrandListCreateView(generics.ListCreateAPIView):
    """
    水品牌列表和创建视图
    """
    queryset = WaterBrand.objects.all()
    serializer_class = WaterBrandSerializer
    pagination_class = None  # 禁用分页，返回完整列表
    
    def list(self, request, *args, **kwargs):
        """
        重写 list 方法，返回 Vben Admin 期望的格式
        """
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'code': 0,
            'message': 'success',
            'data': serializer.data
        })
    
    def create(self, request, *args, **kwargs):
        """
        重写 create 方法，返回 Vben Admin 期望的格式
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({
            'code': 0,
            'message': '创建成功',
            'data': serializer.data
        }, status=status.HTTP_201_CREATED)


class WaterBrandDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    水品牌详情、更新和删除视图
    """
    queryset = WaterBrand.objects.all()
    serializer_class = WaterBrandSerializer
    
    def destroy(self, request, *args, **kwargs):
        """
        重写 destroy 方法，返回 Vben Admin 期望的格式
        """
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({
            'code': 0,
            'message': '删除成功',
            'data': None
        }, status=status.HTTP_200_OK)


# ==================== Customer Views ====================

class CustomerListView(generics.ListAPIView):
    """
    客户列表视图（支持搜索）
    """
    serializer_class = CustomerSerializer
    
    def get_queryset(self):
        queryset = Customer.objects.all()
        
        # 获取搜索参数
        keyword = self.request.query_params.get('keyword', None)
        
        if keyword:
            # 支持按客户编号或姓名模糊搜索
            from django.db.models import Q
            queryset = queryset.filter(
                Q(id__icontains=keyword) | 
                Q(name__icontains=keyword)
            )
        
        return queryset


class CustomerListCreateView(generics.ListCreateAPIView):
    """
    客户列表和创建视图
    """
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    pagination_class = None  # 禁用分页，返回完整列表
    
    def get_queryset(self):
        queryset = Customer.objects.all()
        
        # 获取搜索参数
        keyword = self.request.query_params.get('keyword', None)
        
        if keyword:
            # 支持按客户编号或姓名模糊搜索
            from django.db.models import Q
            queryset = queryset.filter(
                Q(id__icontains=keyword) | 
                Q(name__icontains=keyword)
            )
        
        return queryset
    
    def list(self, request, *args, **kwargs):
        """
        重写 list 方法，返回 Vben Admin 期望的格式
        """
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'code': 0,
            'message': 'success',
            'data': serializer.data
        })
    
    def create(self, request, *args, **kwargs):
        """
        重写 create 方法，返回 Vben Admin 期望的格式
        """
        # 添加调试信息
        print(f"收到创建客户的请求数据: {request.data}")
        
        # 检查是否为JSON请求
        content_type = request.content_type if hasattr(request, 'content_type') else request.META.get('CONTENT_TYPE', '')
        print(f"请求内容类型: {content_type}")
        
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            print(f"数据验证失败: {serializer.errors}")
            # 尝试获取更具体的错误信息
            error_details = {}
            for field, errors in serializer.errors.items():
                error_details[field] = [str(error) for error in errors]
                
            return Response({
                'code': 1,
                'message': '数据验证失败',
                'errors': error_details
            }, status=status.HTTP_400_BAD_REQUEST)
            
        self.perform_create(serializer)
        print(f"客户创建成功: {serializer.data}")
        return Response({
            'code': 0,
            'message': '创建成功',
            'data': serializer.data
        }, status=status.HTTP_201_CREATED)


class CustomerDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    客户详情、更新和删除视图
    """
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    
    def update(self, request, *args, **kwargs):
        """
        重写 update 方法，返回 Vben Admin 期望的格式
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        
        if not serializer.is_valid():
            print(f"数据验证失败: {serializer.errors}")
            error_details = {}
            for field, errors in serializer.errors.items():
                error_details[field] = [str(error) for error in errors]
                
            return Response({
                'code': 1,
                'message': '数据验证失败',
                'errors': error_details
            }, status=status.HTTP_400_BAD_REQUEST)
        
        self.perform_update(serializer)
        print(f"客户更新成功: {serializer.data}")
        return Response({
            'code': 0,
            'message': '更新成功',
            'data': serializer.data
        })
    
    def destroy(self, request, *args, **kwargs):
        """
        重写 destroy 方法，返回 Vben Admin 期望的格式
        """
        instance = self.get_object()
        print(f"准备删除客户: {instance.id} - {instance.name}")
        try:
            self.perform_destroy(instance)
            print(f"客户删除成功: {instance.id}")
            return Response({
                'code': 0,
                'message': '删除成功',
                'data': None
            }, status=status.HTTP_200_OK)
        except Exception as e:
            print(f"删除客户失败: {instance.id}, 错误: {str(e)}")
            return Response({
                'code': 1,
                'message': f'删除失败: {str(e)}',
                'data': None
            }, status=status.HTTP_400_BAD_REQUEST)


# ==================== Menu Views ====================

class MenuView(APIView):
    """
    获取用户菜单视图
    GET /api/menu/all/
    
    返回 Vben Admin 期望的路由格式
    """
    def get(self, request):
        # 检查用户是否已认证
        if not request.user or not request.user.is_authenticated:
            return Response({
                'code': 1,
                'message': '未授权访问'
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        # 返回示例菜单结构
        # 实际项目中应该根据用户角色从数据库动态加载菜单
        menus = [
            {
                "name": "Dashboard",
                "path": "/dashboard",
                "component": "BasicLayout",
                "meta": {
                    "title": "仪表盘",
                    "icon": "lucide:layout-dashboard",
                    "order": -1
                },
                "children": [
                    {
                        "name": "Analytics",
                        "path": "/dashboard/analytics",
                        "component": "/dashboard/analytics/index",
                        "meta": {
                            "title": "分析页",
                            "icon": "lucide:area-chart"
                        }
                    },
                    {
                        "name": "Workspace",
                        "path": "/dashboard/workspace",
                        "component": "/dashboard/workspace/index",
                        "meta": {
                            "title": "工作台",
                            "icon": "lucide:briefcase"
                        }
                    }
                ]
            },
            {
                "name": "WaterBrand",
                "path": "/water-brand",
                "component": "BasicLayout",
                "meta": {
                    "title": "水品牌管理",
                    "icon": "lucide:droplet",
                    "order": 1
                },
                "children": [
                    {
                        "name": "WaterBrandList",
                        "path": "/water-brand/list",
                        "component": "/water-brand/list/index",
                        "meta": {
                            "title": "品牌列表",
                            "icon": "lucide:list"
                        }
                    }
                ]
            },
            {
                "name": "Customer",
                "path": "/customer",
                "component": "/customer/index",
                "meta": {
                    "title": "客户管理",
                    "icon": "lucide:users",
                    "order": 2
                }
            }
        ]
        
        return Response({
            'code': 0,
            'data': menus
        }, status=status.HTTP_200_OK)
