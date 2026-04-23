from rest_framework import serializers
from .models import Sample, WaterBrand, Customer


class SampleSerializer(serializers.ModelSerializer):
    """
    示例模型序列化器
    """
    class Meta:
        model = Sample
        fields = ['id', 'title', 'description', 'created_at', 'updated_at', 'is_active']
        read_only_fields = ['id', 'created_at', 'updated_at']


class WaterBrandSerializer(serializers.ModelSerializer):
    """
    水品牌序列化器
    """
    class Meta:
        model = WaterBrand
        fields = ['id', 'name', 'description', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class CustomerSerializer(serializers.ModelSerializer):
    """
    客户序列化器
    """
    brand_name = serializers.CharField(source='brand.name', read_only=True)
    customer_type_display = serializers.CharField(source='get_customer_type_display', read_only=True)
    
    class Meta:
        model = Customer
        fields = [
            'id', 'customer_number', 'name', 'customer_type', 'customer_type_display', 'brand', 'brand_name', 'open_date', 
            'last_delivery_date', 'phone', 'address', 'remark',
            'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']
    
    def validate_id(self, value):
        """验证客户编号格式"""
        if not value or value.strip() == '':
            raise serializers.ValidationError("客户编号不能为空")
        return value
    
    def validate_customer_number(self, value):
        """验证客户号码格式"""
        if not value or value.strip() == '':
            raise serializers.ValidationError("客户号码不能为空")
        return value
    
    def validate_open_date(self, value):
        """验证开户日期"""
        from django.utils import timezone
        if value > timezone.now().date():
            raise serializers.ValidationError("开户日期不能是未来日期")
        return value
