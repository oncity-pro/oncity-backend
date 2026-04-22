from rest_framework.authentication import TokenAuthentication


class BearerTokenAuthentication(TokenAuthentication):
    """
    支持 Bearer 和 Token 两种格式的 Token 认证
    """
    keyword = 'Bearer'  # 默认使用 Bearer
    
    def authenticate(self, request):
        auth = request.META.get('HTTP_AUTHORIZATION', '').split()
        
        if not auth:
            return None
        
        if len(auth) == 1:
            # 没有指定前缀，尝试两种方式
            token = auth[0]
            return self.authenticate_credentials(token)
        elif len(auth) == 2:
            # 有前缀，检查是否是 Bearer 或 Token
            if auth[0].lower() in ['bearer', 'token']:
                return self.authenticate_credentials(auth[1])
        
        return None
