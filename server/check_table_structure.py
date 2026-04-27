#!/usr/bin/env python
"""
检查数据库表结构
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

def check_table_structure():
    print("开始检查数据库表结构...")
    
    with connection.cursor() as cursor:
        # 检查api_customer表结构
        cursor.execute('DESCRIBE api_customer')
        rows = cursor.fetchall()
        
        print('api_customer表结构:')
        for row in rows:
            print(f"  {row[0]}: {row[1]} (NULL: {row[2]}, Key: {row[3]}, Default: {row[4]}, Extra: {row[5]})")

if __name__ == "__main__":
    check_table_structure()