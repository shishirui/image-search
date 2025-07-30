#!/bin/bash

# Docker容器入口点脚本
# 用于启动图片搜索HTTP服务

set -e

echo "=== 图片搜索HTTP服务启动中 ==="

# 检查必要文件是否存在
required_files=("data/index.faiss" "data/data_indexed.csv" "data/embeddings.npy" "src/app.py")
for file in "${required_files[@]}"; do
    if [ ! -f "$file" ]; then
        echo "错误: 缺少必要文件 $file"
        exit 1
    fi
done

echo "✓ 所有必要文件已找到"

# 设置环境变量
export PYTHONUNBUFFERED=1
export FLASK_ENV=production

echo "启动Flask服务..."
echo "服务将在 http://0.0.0.0:5000 启动"
echo ""

# 启动Flask应用
exec python src/app.py 