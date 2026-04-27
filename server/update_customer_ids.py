#!/usr/bin/env python
"""
修复客户ID
"""

import os
import sys
import django

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'oncity_backend.settings')
django.setup()

from api.models import Customer, generate_customer_id

def update_customer_ids():
    """
    更新客户ID，确保它们不是空字符串
    """
    print("正在获取所有客户...")
    
    customers = Customer.objects.all()
    
    print(f"找到 {customers.count()} 个客户")
    
    for customer in customers:
        print(f"检查客户: ID='{customer.id}', Name='{customer.name}'")
        
        # 检查ID是否为空或None
        if not customer.id or customer.id.strip() == '':
            # 生成新ID
            new_id = generate_customer_id()
            customer.id = new_id
            
            print(f"  -> 更新客户 {customer.name} 的ID为 {new_id}")
            
            # 保存更改
            customer.save()
            print(f"  -> 保存成功，新ID: {customer.id}")
        else:
            print(f"  -> ID已存在: {customer.id}")

if __name__ == '__main__':
    update_customer_ids()