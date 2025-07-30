#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
import time

def test_health_check():
    """测试健康检查接口"""
    print("=== 测试健康检查接口 ===")
    try:
        response = requests.get('http://localhost:5000/health')
        print(f"状态码: {response.status_code}")
        print(f"响应: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        return response.status_code == 200
    except Exception as e:
        print(f"错误: {e}")
        return False

def test_search_post():
    """测试POST搜索接口"""
    print("\n=== 测试POST搜索接口 ===")
    try:
        data = {
            "query": "一只可爱的小猫",
            "k": 3
        }
        response = requests.post('http://localhost:5000/search', 
                               json=data,
                               headers={'Content-Type': 'application/json'})
        print(f"状态码: {response.status_code}")
        print(f"请求数据: {json.dumps(data, indent=2, ensure_ascii=False)}")
        print(f"响应: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        return response.status_code == 200
    except Exception as e:
        print(f"错误: {e}")
        return False

def test_search_get():
    """测试GET搜索接口"""
    print("\n=== 测试GET搜索接口 ===")
    try:
        params = {
            "q": "一只可爱的小猫",
            "k": 3
        }
        response = requests.get('http://localhost:5000/search', params=params)
        print(f"状态码: {response.status_code}")
        print(f"请求参数: {params}")
        print(f"响应: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        return response.status_code == 200
    except Exception as e:
        print(f"错误: {e}")
        return False

def test_error_handling():
    """测试错误处理"""
    print("\n=== 测试错误处理 ===")
    
    passed = 0
    total = 2
    
    # 测试缺少查询参数
    try:
        response = requests.post('http://localhost:5000/search', 
                               json={},
                               headers={'Content-Type': 'application/json'})
        print(f"缺少查询参数 - 状态码: {response.status_code}")
        print(f"响应: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        if response.status_code == 400:
            passed += 1
    except Exception as e:
        print(f"错误: {e}")
    
    # 测试无效的k参数
    try:
        response = requests.post('http://localhost:5000/search', 
                               json={"query": "测试", "k": 0},
                               headers={'Content-Type': 'application/json'})
        print(f"无效k参数 - 状态码: {response.status_code}")
        print(f"响应: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        if response.status_code == 400:
            passed += 1
    except Exception as e:
        print(f"错误: {e}")
    
    return passed == total

def main():
    """主测试函数"""
    print("开始测试图片搜索API服务...")
    print("请确保服务已在 http://localhost:5000 启动")
    print()
    
    # 等待服务启动
    print("等待服务启动...")
    time.sleep(2)
    
    # 运行测试
    tests = [
        test_health_check,
        test_search_post,
        test_search_get,
        test_error_handling
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"测试失败: {e}")
    
    print(f"\n=== 测试结果 ===")
    print(f"通过: {passed}/{total}")
    
    if passed == total:
        print("🎉 所有测试通过！")
    else:
        print("❌ 部分测试失败")

if __name__ == '__main__':
    main() 