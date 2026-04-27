#!/usr/bin/env python
"""
修复数据库中的空ID客户记录
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

def fix_empty_customer_ids():
    print("开始修复空ID的客户记录...")
    
    # 获取所有ID为空的客户
    empty_id_customers = Customer.objects.filter(id__exact='')
    
    print(f"找到 {empty_id_customers.count()} 个ID为空的客户记录")
    
    for customer in empty_id_customers:
        # 生成一个新的唯一ID，例如使用UUID的一部分
        new_id = str(uuid.uuid4())[:10]  # 取UUID的前10个字符
        
        print(f"将客户 '{customer.name}' 的空ID更新为: {new_id}")
        
        # 更新客户ID
        customer.id = new_id
        customer.save()
        print(f"  -> 更新成功")
    
    print("修复完成！")

if __name__ == "__main__":
    fix_empty_customer_ids()