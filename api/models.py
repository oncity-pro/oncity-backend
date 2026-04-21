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
