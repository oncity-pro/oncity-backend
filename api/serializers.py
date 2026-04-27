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
    # 驼峰命名字段在 to_representation 中手动处理

    class Meta:
        model = Customer
        fields = ['id', 'name', 'customer_type', 'customer_type_display', 'brand', 'brand_name',
                  'open_date', 'last_delivery_date',
                  'phone', 'remark', 'is_active', 'created_at', 'updated_at', 'storage_amount', 'owed_empty_bucket', 'total_water_usage']
        read_only_fields = ['created_at', 'updated_at']

    def validate_id(self, value):
        """验证客户编号唯一性"""
        if not value:
            return value
        if self.instance is not None and value == self.instance.id:
            # 更新模式且编号未变，无需校验
            return value
        if Customer.objects.filter(id=value).exists():
            raise serializers.ValidationError("客户编号已存在，请重新输入")
        return value

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # 确保 customer_type 显示为中文描述
        data['customer_type_display'] = instance.customer_type_display
        # 同时保留驼峰命名字段
        data['openDate'] = instance.open_date.isoformat() if instance.open_date else None
        data['lastDeliveryDate'] = instance.last_delivery_date.isoformat() if instance.last_delivery_date else None
        # 处理 brand 字段（可能是 WaterBrand 对象或 None）
        data['brandId'] = instance.brand_id if instance.brand else None
        # 添加驼峰命名的storage_amount字段
        data['storageAmount'] = instance.storage_amount
        # 添加驼峰命名的owed_empty_bucket字段
        data['owedEmptyBucket'] = instance.owed_empty_bucket
        # 添加驼峰命名的total_water_usage字段
        data['totalWaterUsage'] = instance.total_water_usage
        return data

    def get_brand_name(self, obj):
        """获取品牌名称"""
        return obj.brand.name if obj.brand else None

    def validate_name(self, value):
        """验证姓名地址不为空"""
        if not value or value.strip() == '':
            raise serializers.ValidationError("姓名地址不能为空")
        return value.strip()
    
    # 删除对phone字段的验证函数，使其成为可选字段
    def validate_open_date(self, value):
        """验证开户日期"""
        from django.utils import timezone
        if value and value > timezone.now().date():
            raise serializers.ValidationError("开户日期不能是未来日期")
        return value
