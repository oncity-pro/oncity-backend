# ONCITY API 测试脚本
# 用于快速验证后端 API 是否正常工作

import requests
import json

# 配置
BASE_URL = "http://localhost:8000"

def print_separator():
    print("\n" + "="*60 + "\n")

def test_health_check():
    """测试健康检查"""
    print("🔍 测试 1: 健康检查")
    try:
        response = requests.get(f"{BASE_URL}/api/health/")
        print(f"状态码: {response.status_code}")
        print(f"响应: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ 错误: {e}")
        return False

def test_water_brands():
    """测试水品牌 API"""
    print("🔍 测试 2: 获取水品牌列表")
    try:
        response = requests.get(f"{BASE_URL}/api/v1/water-brands/")
        print(f"状态码: {response.status_code}")
        brands = response.json()
        print(f"品牌数量: {len(brands)}")
        for brand in brands:
            print(f"  - ID: {brand['id']}, 名称: {brand['name']}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ 错误: {e}")
        return False

def test_customers():
    """测试客户 API"""
    print("🔍 测试 3: 获取客户列表")
    try:
        response = requests.get(f"{BASE_URL}/api/v1/customers/")
        print(f"状态码: {response.status_code}")
        customers = response.json()
        print(f"客户数量: {len(customers)}")
        for customer in customers[:3]:  # 只显示前3个
            print(f"  - 编号: {customer['id']}, 姓名: {customer['name']}, 品牌: {customer.get('brand_name', '-')}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ 错误: {e}")
        return False

def test_customer_search():
    """测试客户搜索"""
    print("🔍 测试 4: 客户搜索（keyword=张三）")
    try:
        response = requests.get(f"{BASE_URL}/api/v1/customers/", params={"keyword": "张三"})
        print(f"状态码: {response.status_code}")
        customers = response.json()
        print(f"搜索结果数量: {len(customers)}")
        for customer in customers:
            print(f"  - 编号: {customer['id']}, 姓名: {customer['name']}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ 错误: {e}")
        return False

def test_create_customer():
    """测试创建客户"""
    print("🔍 测试 5: 创建新客户")
    try:
        new_customer = {
            "id": "9999",
            "name": "测试客户 - 北京市朝阳区测试路1号",
            "brand": 1,
            "open_date": "2024-04-21",
            "phone": "13900139000",
            "address": "北京市朝阳区测试路1号",
            "remark": "API 测试创建的客戶",
            "is_active": True
        }
        response = requests.post(
            f"{BASE_URL}/api/v1/customers/all/",
            json=new_customer,
            headers={"Content-Type": "application/json"}
        )
        print(f"状态码: {response.status_code}")
        if response.status_code == 201:
            customer = response.json()
            print(f"✅ 创建成功!")
            print(f"  编号: {customer['id']}")
            print(f"  姓名: {customer['name']}")
            print(f"  品牌: {customer.get('brand_name', '-')}")
            
            # 清理测试数据
            delete_customer("9999")
            return True
        else:
            print(f"❌ 创建失败: {response.text}")
            return False
    except Exception as e:
        print(f"❌ 错误: {e}")
        return False

def delete_customer(customer_id):
    """删除测试客户"""
    try:
        response = requests.delete(f"{BASE_URL}/api/v1/customers/{customer_id}/")
        if response.status_code == 204:
            print(f"✅ 已清理测试客户 {customer_id}")
    except Exception as e:
        print(f"清理测试数据失败: {e}")

def main():
    """主函数"""
    print("\n" + "="*60)
    print("   ONCITY API 测试脚本")
    print("="*60)
    print(f"\n后端地址: {BASE_URL}")
    print("\n请确保 Django 服务器正在运行...")
    print_separator()
    
    results = []
    
    # 执行测试
    results.append(("健康检查", test_health_check()))
    print_separator()
    
    results.append(("水品牌列表", test_water_brands()))
    print_separator()
    
    results.append(("客户列表", test_customers()))
    print_separator()
    
    results.append(("客户搜索", test_customer_search()))
    print_separator()
    
    results.append(("创建客户", test_create_customer()))
    print_separator()
    
    # 汇总结果
    print("📊 测试结果汇总:")
    print("-"*60)
    passed = 0
    failed = 0
    for test_name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"  {test_name:20s} {status}")
        if result:
            passed += 1
        else:
            failed += 1
    
    print("-"*60)
    print(f"总计: {len(results)} 个测试, {passed} 通过, {failed} 失败")
    print("="*60 + "\n")
    
    if failed == 0:
        print("🎉 所有测试通过！API 工作正常！")
    else:
        print("⚠️  部分测试失败，请检查后端配置和数据库。")
    
    return failed == 0

if __name__ == "__main__":
    try:
        success = main()
        exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n测试已取消")
        exit(1)
