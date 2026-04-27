"""
测试客户类型字段
"""
import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def test_customer_type():
    """测试客户类型字段"""
    print("=" * 50)
    print("测试客户类型字段")
    print("=" * 50)
    
    # 获取客户列表
    response = requests.get(f"{BASE_URL}/api/v1/customers/all")
    if response.status_code == 200:
        data = response.json()
        if data['code'] == 0 and len(data['data']) > 0:
            customer = data['data'][0]
            print(f"\n第一个客户信息:")
            print(f"  客户编号: {customer['id']}")
            print(f"  客户姓名: {customer['name']}")
            print(f"  客户类型代码: {customer['customer_type']}")
            print(f"  客户类型显示: {customer['customer_type_display']}")
            print("\n✓ 客户类型字段测试通过!")
        else:
            print("\n✗ 没有客户数据")
    else:
        print(f"\n✗ API请求失败: {response.status_code}")
    
    print("\n" + "=" * 50)
    print("客户类型选项:")
    print("  - vip: VIP客户")
    print("  - normal: 普通客户")
    print("  - pickup: 自提客户")
    print("=" * 50)

if __name__ == "__main__":
    test_customer_type()
