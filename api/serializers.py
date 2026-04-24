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
    customer_type_display = serializers.CharField(source='customer_type', read_only=True)
    brand_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Customer
        fields = ['id', 'name', 'customer_type', 'customer_type_display', 'brand', 'brand_name', 'open_date', 
                  'last_delivery_date', 'phone', 'address', 'remark', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # 确保 customer_type 显示为中文描述
        data['customer_type_display'] = instance.customer_type_display
        return data

    def get_brand_name(self, obj):
        """获取品牌名称"""
        return obj.brand.name if obj.brand else None

    def validate_name(self, value):
        """验证姓名地址不为空"""
        if not value or value.strip() == '':
            raise serializers.ValidationError("姓名地址不能为空")
        return value.strip()
    
    def validate_phone(self, value):
        """验证联系电话不为空"""
        if not value or value.strip() == '':
            raise serializers.ValidationError("联系电话不能为空")
        return value.strip()
    
    def validate_address(self, value):
        """验证地址不为空"""
        if not value or value.strip() == '':
            raise serializers.ValidationError("详细地址不能为空")
        return value.strip()
    
    def validate_open_date(self, value):
        """验证开户日期"""
        from django.utils import timezone
        if value and value > timezone.now().date():
            raise serializers.ValidationError("开户日期不能是未来日期")
        return value
