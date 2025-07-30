#!/bin/bash

# Docker容器测试脚本

echo "=== 测试Docker容器 ==="

# 检查容器是否运行
if ! docker ps | grep -q image-search-container; then
    echo "错误: 容器未运行，请先启动容器"
    echo "运行命令: docker-compose up -d"
    exit 1
fi

echo "✓ 容器正在运行"

# 等待服务启动
echo "等待服务启动..."
sleep 10

# 测试健康检查接口
echo "测试健康检查接口..."
response=$(curl -s http://localhost:5000/health)

if [ $? -eq 0 ]; then
    echo "✓ 健康检查通过"
    echo "响应: $response"
else
    echo "✗ 健康检查失败"
    exit 1
fi

# 测试搜索接口
echo ""
echo "测试搜索接口..."
search_response=$(curl -s "http://localhost:5000/search?q=beautiful%20landscape&k=3")

if [ $? -eq 0 ]; then
    echo "✓ 搜索接口正常"
    echo "搜索结果数量: $(echo $search_response | grep -o '"total_results":[0-9]*' | cut -d':' -f2)"
else
    echo "✗ 搜索接口失败"
    exit 1
fi

echo ""
echo "=== 所有测试通过！ ==="
echo "服务地址: http://localhost:5000"
echo "健康检查: http://localhost:5000/health"
echo "搜索接口: http://localhost:5000/search?q=your_query" 