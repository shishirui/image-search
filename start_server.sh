#!/bin/bash

# 图片搜索HTTP服务启动脚本

echo "=== 图片搜索HTTP服务启动脚本 ==="
echo "正在检查依赖..."

# 检查Python是否安装
if ! command -v python3 &> /dev/null; then
    echo "错误: 未找到Python3，请先安装Python3"
    exit 1
fi

# 检查必要文件是否存在
required_files=("index.faiss" "data_indexed.csv" "embeddings.npy")
for file in "${required_files[@]}"; do
    if [ ! -f "$file" ]; then
        echo "错误: 缺少必要文件 $file"
        echo "请确保以下文件存在于当前目录："
        printf '%s\n' "${required_files[@]}"
        exit 1
    fi
done

echo "✓ 所有必要文件已找到"

# 检查是否已安装依赖
if [ ! -d "venv" ]; then
    echo "创建虚拟环境..."
    python3 -m venv venv
fi

echo "激活虚拟环境..."
source venv/bin/activate

echo "安装依赖包..."
pip install -r requirements.txt

echo "启动Flask服务..."
echo "服务将在 http://localhost:5000 启动"
echo "按 Ctrl+C 停止服务"
echo ""

python app.py 