#!/bin/bash

# Docker构建脚本

echo "=== 构建图片搜索Docker镜像 ==="

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "错误: 未找到Docker，请先安装Docker"
    exit 1
fi

# 构建镜像
echo "正在构建Docker镜像..."
docker build -t image-search:latest .

if [ $? -eq 0 ]; then
    echo "✓ Docker镜像构建成功！"
    echo ""
    echo "运行容器命令："
    echo "  docker run -d -p 5000:5000 --name image-search-container image-search:latest"
    echo ""
    echo "或者使用docker-compose："
    echo "  docker-compose up -d"
else
    echo "✗ Docker镜像构建失败"
    exit 1
fi 