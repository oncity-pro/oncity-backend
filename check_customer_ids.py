import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'oncity_backend.settings')
django.setup()

from api.models import Customer

def check_customer_ids():
    # 检查所有客户
    all_customers = Customer.objects.all()
    print('所有客户的ID:')
    numeric_ids = []
    cus_ids = []
    
    for customer in all_customers:
        print('  ', customer.id, '-', customer.name)
        if customer.id.isdigit():  # 检查是否为纯数字
            numeric_ids.append(int(customer.id))
        elif customer.id.startswith('CUS'):
            cus_ids.append(int(customer.id[3:]))  # 提取CUS后面的数字
    
    print('\n纯数字ID的最大值:', max(numeric_ids) if numeric_ids else 0)
    print('CUS ID的最大数字部分:', max(cus_ids) if cus_ids else 0)

if __name__ == '__main__':
    check_customer_ids()