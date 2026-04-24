from django.db import models
from django.utils import timezone
import uuid


class Sample(models.Model):
    """
    示例模型 - 用于测试 API 功能
    """
    title = models.CharField(max_length=200, verbose_name='标题')
    description = models.TextField(blank=True, verbose_name='描述')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    is_active = models.BooleanField(default=True, verbose_name='是否激活')

    class Meta:
        ordering = ['-created_at']
        verbose_name = '示例'
        verbose_name_plural = '示例列表'

    def __str__(self):
        return self.title


class WaterBrand(models.Model):
    """
    水品牌模型
    """
    name = models.CharField(max_length=100, verbose_name='品牌名称')
    description = models.TextField(blank=True, verbose_name='品牌描述')
    is_active = models.BooleanField(default=True, verbose_name='是否启用')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        ordering = ['id']
        verbose_name = '水品牌'
        verbose_name_plural = '水品牌列表'

    def __str__(self):
        return self.name


def generate_customer_id():
    """生成客户编号：从1开始的递增数字，格式为4位数字，不足前面补0"""
    from django.db import connection
    with connection.cursor() as cursor:
        # 查询当前最大客户编号
        cursor.execute("SELECT MAX(CAST(id AS UNSIGNED)) FROM api_customer WHERE id REGEXP '^[0-9]+$'")
        result = cursor.fetchone()[0]
        
        # 如果没有现有记录，则从1开始
        next_id = 1 if result is None else int(result) + 1
        
        # 格式化为4位数字，前面补0
        return f"{next_id:04d}"


def generate_customer_number():
    """生成客户号码：从1开始的递增数字，格式为CUS+4位数字"""
    from django.db import connection
    with connection.cursor() as cursor:
        # 查询当前最大客户号码
        cursor.execute("SELECT MAX(CAST(SUBSTRING(customer_number, 4) AS UNSIGNED)) FROM api_customer WHERE customer_number LIKE 'CUS%' AND SUBSTRING(customer_number, 4) REGEXP '^[0-9]+$'")
        result = cursor.fetchone()[0]
        
        # 如果没有现有记录，则从1开始
        next_num = 1 if result is None else int(result) + 1
        
        # 格式化为CUS+4位数字
        return f"CUS{next_num:04d}"


class Customer(models.Model):
    """
    客户模型
    """
    # 客户类型选择
    CUSTOMER_TYPE_CHOICES = [
        ('vip', 'VIP客户'),
        ('normal', '普通客户'),
        ('pickup', '自提客户'),
    ]
    
    id = models.CharField(max_length=20, primary_key=True, default=generate_customer_id, verbose_name='客户编号')
    customer_number = models.CharField(max_length=20, unique=True, default=generate_customer_number, verbose_name='客户号码')
    name = models.CharField(max_length=200, verbose_name='姓名地址')
    customer_type = models.CharField(
        max_length=10,
        choices=CUSTOMER_TYPE_CHOICES,
        default='normal',
        verbose_name='客户类型'
    )
    brand = models.ForeignKey(
        WaterBrand, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='customers',
        verbose_name='水品牌'
    )
    open_date = models.DateField(verbose_name='开户日期')
    last_delivery_date = models.DateField(blank=True, null=True, verbose_name='最后送水日期')
    phone = models.CharField(max_length=20, verbose_name='联系电话')
    address = models.TextField(verbose_name='详细地址')
    remark = models.TextField(blank=True, verbose_name='备注')
    is_active = models.BooleanField(default=True, verbose_name='是否活跃')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'api_customer'  # 确保使用正确的表名
        ordering = ['-created_at']
        verbose_name = '客户'
        verbose_name_plural = '客户列表'

    def __str__(self):
        return f"{self.id} - {self.name}"