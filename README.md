# 图片搜索HTTP API服务

这是一个基于Flask的图片搜索HTTP API服务，使用FAISS向量索引和Sentence Transformers进行语义搜索。

## 功能特性

- 语义图片搜索
- RESTful API接口
- JSON格式响应
- 支持GET和POST请求
- 健康检查接口
- 错误处理和日志记录

## 安装依赖

```bash
pip install -r requirements.txt
```

## 启动服务

确保以下文件存在于项目目录中：
- `index.faiss` - FAISS索引文件
- `data_indexed.csv` - 图片数据文件
- `embeddings.npy` - 图片嵌入向量文件

然后启动服务：

```bash
python app.py
```

服务将在 `http://localhost:5000` 启动。

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
  "query": "一只可爱的小猫",
  "k": 5
}
```

**参数说明：**
- `query` (必需): 搜索查询文本
- `k` (可选): 返回结果数量，默认5，最大100

**响应示例：**
```json
{
  "query": "一只可爱的小猫",
  "total_results": 5,
  "results": [
    {
      "rank": 1,
      "image_id": "12345",
      "description": "一只橘色的小猫坐在窗台上",
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
  -d '{"query": "一只可爱的小猫", "k": 3}'

# GET搜索
curl "http://localhost:5000/search?q=一只可爱的小猫&k=3"
```

### 使用Python requests

```python
import requests

# 搜索图片
response = requests.post('http://localhost:5000/search', 
                        json={'query': '一只可爱的小猫', 'k': 5})

if response.status_code == 200:
    results = response.json()
    for result in results['results']:
        print(f"排名: {result['rank']}")
        print(f"图片ID: {result['image_id']}")
        print(f"描述: {result['description']}")
        print(f"相似度: {result['similarity_score']:.2f}")
        print(f"图片URL: {result['photo_url']}")
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