#!/usr/bin/env python
"""
修复客户数据，为缺少customer_number的记录添加值
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
import uuid

def fix_customer_numbers():
    print("开始修复客户数据...")
    
    # 获取所有客户
    customers = Customer.objects.all()
    print(f"共找到 {customers.count()} 个客户记录")
    
    for customer in customers:
        print(f"检查客户: ID='{customer.id}', Name='{customer.name}'")
        
        # 如果customer_number为空，则设置为与id相同的值
        if not customer.customer_number or customer.customer_number.strip() == '':
            print(f"  -> 为客户 {customer.name} 设置 customer_number 为 {customer.id}")
            customer.customer_number = customer.id if customer.id and customer.id.strip() != '' else f"CUST_{uuid.uuid4().hex[:8].upper()}"
            customer.save()
            print(f"  -> 保存成功")
        else:
            print(f"  -> customer_number 已存在: {customer.customer_number}")

if __name__ == "__main__":
    fix_customer_numbers()