#!/usr/bin/env python
"""
修复客户ID和客户号码
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

def update_customer_ids():
    print("开始更新客户ID...")
    
    # 获取所有客户
    customers = Customer.objects.all()
    print(f"共找到 {customers.count()} 个客户记录")
    
    for customer in customers:
        print(f"检查客户: ID='{customer.id}', Name='{customer.name}', Number='{customer.customer_number}'")
        
        # 如果ID为空，则生成一个新的ID
        if not customer.id or customer.id.strip() == '':
            new_id = f"CUST_{uuid.uuid4().hex[:8].upper()}"
            print(f"  -> 为客户 {customer.name} 设置新ID为 {new_id}")
            
            # 需要特别处理空ID的更新
            old_id = customer.id
            customer.id = new_id
            customer.customer_number = new_id
            customer.save(force_update=True)
            print(f"  -> 保存成功，新ID: {customer.id}, 新号码: {customer.customer_number}")

if __name__ == "__main__":
    update_customer_ids()