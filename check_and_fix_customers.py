#!/usr/bin/env python
"""
检查并修复数据库中的客户数据
"""

import os
import sys
import django
from django.conf import settings

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'oncity_backend.settings')

django.setup()

from api.models import Customer

def check_and_fix_customers():
    print("开始检查客户数据...")
    
    # 获取所有客户
    customers = Customer.objects.all()
    print(f"共找到 {customers.count()} 个客户记录")
    
    for customer in customers:
        print(f"客户ID: '{customer.id}', 姓名: '{customer.name}'")
        
        # 检查是否有空ID的客户
        if not customer.id or customer.id.strip() == '':
            print(f"  -> 发现空ID客户: {customer.name}")
    
    # 检查是否有ID为'row_38'的客户
    try:
        target_customer = Customer.objects.get(id='row_38')
        print(f"  -> 找到ID为'row_38'的客户: {target_customer.name}")
    except Customer.DoesNotExist:
        print("  -> 未找到ID为'row_38'的客户")

if __name__ == "__main__":
    check_and_fix_customers()