# 图片搜索项目

这是一个基于语义搜索的图片搜索系统，使用FAISS向量索引和Sentence Transformers模型。

## 项目结构

```
image-search/
├── src/                    # 源代码文件
│   ├── app.py             # Flask Web应用主文件
│   ├── example_usage.py   # 使用示例
│   ├── test_api.py        # API测试文件
│   ├── search_cli.py      # 命令行搜索工具
│   ├── prepare_data.py    # 数据预处理脚本
│   └── build_index.py     # 构建FAISS索引脚本
├── scripts/               # 脚本文件
│   ├── start_server.sh    # 启动服务器脚本
│   ├── docker-build.sh    # Docker构建脚本
│   ├── docker-entrypoint.sh # Docker入口点脚本
│   └── test-docker.sh     # Docker测试脚本
├── config/                # 配置文件
│   ├── requirements.txt   # Python依赖
│   ├── Dockerfile         # Docker配置
│   └── docker-compose.yml # Docker Compose配置
├── data/                  # 数据文件
│   ├── photos.csv000      # 原始图片数据
│   ├── data.csv           # 处理后的数据
│   ├── data_indexed.csv   # 索引数据
│   ├── index.faiss        # FAISS索引文件
│   └── embeddings.npy     # 向量嵌入文件
├── docs/                  # 文档
│   └── README.md          # 详细文档
├── venv/                  # Python虚拟环境
├── .gitignore            # Git忽略文件
└── .dockerignore         # Docker忽略文件
```

## 功能特性

- 语义图片搜索
- RESTful API接口
- JSON格式响应
- 支持GET和POST请求
- 健康检查接口
- 错误处理和日志记录

**注意：** 由于数据集为英文，请使用英文进行搜索查询。

## 安装依赖

```bash
pip install -r requirements.txt
```

## 创建索引

如果你有 `photos.csv000` 数据文件，可以按照以下步骤创建搜索索引：

### 获取数据文件

`photos.csv000` 数据文件可以从 [Unsplash Dataset](https://unsplash.com/data) 下载：

1. 访问 [Unsplash Dataset 页面](https://unsplash.com/data)
2. 选择 **Lite** 版本（免费，包含25,000张图片）或 **Full** 版本（需要联系团队获取访问权限，包含480万+张图片）
3. 下载数据集，其中包含 `photos.csv000` 文件

### 1. 准备数据

首先运行数据预处理脚本，将原始数据转换为标准格式：

```bash
python prepare_data.py
```

这个脚本会：
- 读取 `photos.csv000` 文件
- 提取图片描述、ID、URL等信息
- 清理空描述数据
- 生成 `data.csv` 文件

### 2. 构建索引

然后运行索引构建脚本，创建FAISS向量索引：

```bash
python build_index.py
```

这个脚本会：
- 使用 Sentence Transformers 模型生成文本嵌入向量
- 构建FAISS索引用于快速相似度搜索
- 生成以下文件：
  - `index.faiss` - FAISS索引文件
  - `data_indexed.csv` - 索引后的图片数据
  - `embeddings.npy` - 图片描述嵌入向量

### 数据文件格式要求

`photos.csv000` 文件应包含以下列（用制表符分隔）：
- `photo_id` - 图片ID
- `ai_description` 或 `photo_description` - 图片描述
- `photo_image_url` - 图片URL
- `photo_width` - 图片宽度
- `photo_height` - 图片高度

## 启动服务

### 方法一：直接运行（开发环境）

确保以下文件存在于项目目录中：
- `index.faiss` - FAISS索引文件
- `data_indexed.csv` - 图片数据文件
- `embeddings.npy` - 图片嵌入向量文件

然后启动服务：

```bash
python app.py
```

服务将在 `http://localhost:5000` 启动。

### 方法二：使用启动脚本

```bash
chmod +x start_server.sh
./start_server.sh
```

### 方法三：Docker容器运行（推荐生产环境）

#### 构建Docker镜像

```bash
chmod +x docker-build.sh
./docker-build.sh
```

#### 运行容器

**使用docker run命令：**
```bash
docker run -d -p 5000:5000 --name image-search-container image-search:latest
```

**使用docker-compose（推荐）：**
```bash
docker-compose up -d
```

#### 容器管理

```bash
# 查看容器状态
docker ps

# 查看容器日志
docker logs image-search-container

# 停止容器
docker stop image-search-container

# 重启容器
docker restart image-search-container

# 删除容器
docker rm image-search-container
```

**Docker容器特性：**
- 自动启动HTTP服务
- 健康检查机制
- 容器重启时自动恢复服务
- 端口映射：容器内5000端口映射到主机5000端口

## API接口

### 1. 健康检查

**GET** `/health`

检查服务状态和数据加载情况。

**响应示例：**
```json
{
  "status": "healthy",
  "message": "图片搜索服务运行正常",
  "data_loaded": true
}
```

### 2. 图片搜索 (POST)

**POST** `/search`

使用POST方法进行图片搜索。

**请求体：**
```json
{
  "query": "a cute cat",
  "k": 5
}
```

**参数说明：**
- `query` (必需): 搜索查询文本
- `k` (可选): 返回结果数量，默认5，最大100

**响应示例：**
```json
{
  "query": "a cute cat",
  "total_results": 5,
  "results": [
    {
      "rank": 1,
      "image_id": "12345",
      "description": "An orange cat sitting on the windowsill",
      "similarity_score": 0.85,
      "photo_url": "https://example.com/image1.jpg",
      "width": 800,
      "height": 600
    }
  ]
}
```

### 3. 图片搜索 (GET)

**GET** `/search?q=查询文本&k=5`

使用GET方法进行图片搜索（便于测试）。

**参数说明：**
- `q` (必需): 搜索查询文本
- `k` (可选): 返回结果数量，默认5

## 使用示例

### 使用curl测试

```bash
# 健康检查
curl http://localhost:5000/health

# POST搜索
curl -X POST http://localhost:5000/search \
  -H "Content-Type: application/json" \
  -d '{"query": "a cute cat", "k": 3}'

# GET搜索
curl "http://localhost:5000/search?q=a+cute+cat&k=3"
```

### 使用Python requests

```python
import requests

# 搜索图片
response = requests.post('http://localhost:5000/search', 
                        json={'query': 'a cute cat', 'k': 5})

if response.status_code == 200:
    results = response.json()
    for result in results['results']:
        print(f"Rank: {result['rank']}")
        print(f"Image ID: {result['image_id']}")
        print(f"Description: {result['description']}")
        print(f"Similarity: {result['similarity_score']:.2f}")
        print(f"Photo URL: {result['photo_url']}")
        print("---")
```

## 错误处理

服务会返回适当的HTTP状态码和错误信息：

- `400`: 请求参数错误
- `404`: 接口不存在
- `500`: 服务器内部错误
- `503`: 服务未完全初始化

## 注意事项

1. 首次启动时，服务需要加载模型和索引数据，可能需要一些时间
2. 确保有足够的内存来加载模型和索引
3. 建议在生产环境中使用gunicorn或uwsgi等WSGI服务器 