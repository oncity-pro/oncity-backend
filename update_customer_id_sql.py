#!/usr/bin/env python
"""
使用SQL更新客户ID
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

from django.db import connection
import uuid

def update_customer_id_sql():
    print("开始使用SQL更新客户ID...")
    
    with connection.cursor() as cursor:
        # 查询所有客户
        cursor.execute("SELECT id, customer_number, name FROM api_customer WHERE id = '' OR id IS NULL")
        rows = cursor.fetchall()
        
        print(f"找到 {len(rows)} 个ID为空的客户记录")
        
        for row in rows:
            old_id = row[0]
            customer_number = row[1]
            name = row[2]
            
            print(f"处理客户: ID='{old_id}', Number='{customer_number}', Name='{name}'")
            
            # 生成新的ID
            new_id = f"CUST_{uuid.uuid4().hex[:8].upper()}"
            
            print(f"  -> 将客户 {name} 的ID从 '{old_id}' 更新为 '{new_id}'")
            
            # 更新记录
            cursor.execute(
                "UPDATE api_customer SET id = %s, customer_number = %s WHERE name = %s AND (id = '' OR id IS NULL)",
                [new_id, customer_number, name]
            )
            
            print(f"  -> 更新成功，新ID: {new_id}")

if __name__ == "__main__":
    update_customer_id_sql()