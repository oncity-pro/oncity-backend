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
    """生成客户编号：格式为4位数字，从0001开始，但要避开现有的CUS ID数值"""
    from django.apps import apps
    from django.db import connection
    
    # 延迟获取 Customer 模型，避免循环导入或定义顺序问题
    Customer = apps.get_model('api', 'Customer')
    
    # 获取当前最大的纯数字ID
    with connection.cursor() as cursor:
        # 查询所有纯数字ID的最大值
        cursor.execute("""
            SELECT MAX(CAST(id AS UNSIGNED)) 
            FROM api_customer 
            WHERE id REGEXP '^[0-9]+$'
        """)
        max_numeric_id_tuple = cursor.fetchone()
        max_numeric_id = max_numeric_id_tuple[0] if max_numeric_id_tuple[0] is not None else 0
        
        # 查询所有CUS前缀ID的最大值
        cursor.execute("""
            SELECT MAX(CAST(SUBSTRING(id, 4) AS UNSIGNED)) 
            FROM api_customer 
            WHERE id LIKE 'CUS%'
        """)
        max_cus_numeric_part_tuple = cursor.fetchone()
        max_cus_numeric_part = max_cus_numeric_part_tuple[0] if max_cus_numeric_part_tuple[0] is not None else 0
    
    # 新的ID应该是两者中的最大值加1
    new_number = max(max_numeric_id, max_cus_numeric_part) + 1
    
    return f'{new_number:04d}'


class Customer(models.Model):
    """
    客户模型
    """
    # 客户类型选择
    CUSTOMER_TYPE_CHOICES = [
        ('vip', 'VIP客户'),
        ('normal', '普通客户'),
        ('pickup', '自提客户'),
        ('closed', '已注销'),
        ('slow_pay', '收款慢'),
        ('blacklist', '黑名单'),
    ]
    
    id = models.CharField(max_length=20, primary_key=True, default=generate_customer_id, verbose_name='客户编号')
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
    open_date = models.DateField(verbose_name='开户日期', default=timezone.now)  # 设置默认值为当前日期
    last_delivery_date = models.DateField(verbose_name='最后送水日期', null=True, blank=True)  # 允许为空，便于过渡
    close_date = models.DateField(verbose_name='注销日期', null=True, blank=True)
    phone = models.CharField(max_length=20, verbose_name='联系电话', blank=True, null=True)  # 设为可选
    remark = models.TextField(blank=True, verbose_name='备注')
    is_active = models.BooleanField(default=True, verbose_name='是否活跃')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    # 新增字段：存水量
    storage_amount = models.IntegerField(default=0, verbose_name='存水量')  # 默认值为0
    # 新增字段：欠空桶
    owed_empty_bucket = models.IntegerField(default=0, verbose_name='欠空桶')  # 设置默认值为0
    # 新增字段：总用水量
    total_water_usage = models.IntegerField(default=0, verbose_name='总用水量')  # 设置默认值为0

    class Meta:
        db_table = 'api_customer'  # 确保使用正确的表名
        ordering = ['-created_at']
        verbose_name = '客户'
        verbose_name_plural = '客户列表'

    def __str__(self):
        return f"{self.id} - {self.name}"

    @property
    def customer_type_display(self):
        return dict(self.CUSTOMER_TYPE_CHOICES).get(self.customer_type, self.customer_type)
        
    @property
    def brand_name(self):
        return self.brand.name if self.brand else None


class BucketDepositConfig(models.Model):
    """
    空桶押金配置
    全局单例配置，始终只使用 id=1 的记录
    """
    amount_per_bucket = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=30.00,
        verbose_name='每桶押金金额'
    )
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '空桶押金配置'
        verbose_name_plural = '空桶押金配置'

    def __str__(self):
        return f'每桶押金: {self.amount_per_bucket}元'