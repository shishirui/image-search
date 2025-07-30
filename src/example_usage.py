#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
图片搜索API使用示例
演示如何在实际应用中使用图片搜索HTTP服务
"""

import requests
import json
import time

class ImageSearchClient:
    """图片搜索客户端"""
    
    def __init__(self, base_url="http://localhost:5000"):
        self.base_url = base_url
        self.session = requests.Session()
    
    def health_check(self):
        """检查服务健康状态"""
        try:
            response = self.session.get(f"{self.base_url}/health")
            return response.json() if response.status_code == 200 else None
        except Exception as e:
            print(f"健康检查失败: {e}")
            return None
    
    def search_images(self, query, k=5):
        """搜索图片"""
        try:
            data = {
                "query": query,
                "k": k
            }
            response = self.session.post(
                f"{self.base_url}/search",
                json=data,
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"搜索失败: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            print(f"搜索出错: {e}")
            return None
    
    def search_images_get(self, query, k=5):
        """使用GET方法搜索图片"""
        try:
            params = {
                "q": query,
                "k": k
            }
            response = self.session.get(f"{self.base_url}/search", params=params)
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"搜索失败: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            print(f"搜索出错: {e}")
            return None

def print_search_results(results):
    """打印搜索结果"""
    if not results:
        print("没有搜索结果")
        return
    
    print(f"\n查询: {results['query']}")
    print(f"找到 {results['total_results']} 个结果:")
    print("-" * 80)
    
    for result in results['results']:
        print(f"排名: {result['rank']}")
        print(f"图片ID: {result['image_id']}")
        print(f"描述: {result['description']}")
        print(f"相似度: {result['similarity_score']:.3f}")
        print(f"图片URL: {result['photo_url']}")
        print(f"尺寸: {result['width']} x {result['height']}")
        print("-" * 40)

def main():
    """主函数 - 演示API使用"""
    print("=== 图片搜索API使用示例 ===")
    
    # 创建客户端
    client = ImageSearchClient()
    
    # 检查服务状态
    print("1. 检查服务状态...")
    health = client.health_check()
    if health:
        print(f"✓ 服务状态: {health['status']}")
        print(f"✓ 数据加载: {health['data_loaded']}")
    else:
        print("✗ 服务不可用")
        return
    
    # 示例搜索查询
    search_queries = [
        "一只可爱的小猫",
        "美丽的风景",
        "美食",
        "建筑",
        "动物"
    ]
    
    print(f"\n2. 执行搜索测试...")
    for i, query in enumerate(search_queries, 1):
        print(f"\n--- 搜索 {i}: {query} ---")
        
        # 使用POST方法搜索
        results = client.search_images(query, k=3)
        if results:
            print_search_results(results)
        
        # 避免请求过于频繁
        time.sleep(1)
    
    print(f"\n3. 测试GET方法搜索...")
    results = client.search_images_get("一只可爱的小猫", k=2)
    if results:
        print_search_results(results)
    
    print(f"\n=== 示例完成 ===")
    print("您可以根据需要修改搜索查询和参数")

if __name__ == '__main__':
    main() 