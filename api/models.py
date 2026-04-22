from django.db import models


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


class Customer(models.Model):
    """
    客户模型
    """
    id = models.CharField(max_length=20, primary_key=True, verbose_name='客户编号')
    name = models.CharField(max_length=200, verbose_name='姓名地址')
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
    phone = models.CharField(max_length=20, blank=True, verbose_name='联系电话')
    address = models.TextField(blank=True, verbose_name='详细地址')
    remark = models.TextField(blank=True, verbose_name='备注')
    is_active = models.BooleanField(default=True, verbose_name='是否活跃')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        ordering = ['-created_at']
        verbose_name = '客户'
        verbose_name_plural = '客户列表'

    def __str__(self):
        return f"{self.id} - {self.name}"
