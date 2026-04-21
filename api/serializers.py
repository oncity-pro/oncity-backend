from rest_framework import serializers
from .models import Sample


class SampleSerializer(serializers.ModelSerializer):
    """
    示例模型序列化器
    """
    class Meta:
        model = Sample
        fields = ['id', 'title', 'description', 'created_at', 'updated_at', 'is_active']
        read_only_fields = ['id', 'created_at', 'updated_at']
