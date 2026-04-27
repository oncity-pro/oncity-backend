#!/usr/bin/env python
"""
使用SQL更新客户ID
"""

import os
import sys
import django

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'oncity_backend.settings')

django.setup()

from django.db import connection

def update_customer_id_sql():
    print("开始使用SQL更新客户ID...")
    
    with connection.cursor() as cursor:
        # 查询ID为空或NULL的客户记录
        cursor.execute("SELECT id, name FROM api_customer WHERE id = '' OR id IS NULL")
        rows = cursor.fetchall()
        
        if not rows:
            print("没有找到ID为空的客户记录")
            return
        
        print(f"找到 {len(rows)} 条ID为空的记录")
        
        for i, row in enumerate(rows):
            old_id = row[0]
            name = row[1]
            
            # 生成新的唯一ID
            new_id = f"CUS{1000 + i + 1:04d}"  # CUS1001, CUS1002, ...
            
            print(f"处理客户: Name='{name}', Current ID='{old_id}' -> New ID='{new_id}'")
            
            # 更新记录
            cursor.execute(
                "UPDATE api_customer SET id = %s WHERE name = %s AND (id = '' OR id IS NULL)",
                [new_id, name]
            )
    
    print("客户ID更新完成")

if __name__ == "__main__":
    update_customer_id_sql()