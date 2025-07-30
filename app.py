from flask import Flask, request, jsonify
import faiss
import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# 全局变量存储模型和数据
index = None
df = None
embeddings = None
image_ids = None
descriptions = None
model = None

def load_model_and_data():
    """加载模型和索引数据"""
    global index, df, embeddings, image_ids, descriptions, model
    
    try:
        logger.info("正在加载FAISS索引...")
        index = faiss.read_index("index.faiss")
        
        logger.info("正在加载数据...")
        df = pd.read_csv("data_indexed.csv")
        embeddings = np.load("embeddings.npy")
        image_ids = df['image_id'].tolist()
        descriptions = df['description'].tolist()
        
        logger.info("正在加载模型...")
        model = SentenceTransformer("all-MiniLM-L6-v2")
        
        logger.info("所有数据加载完成！")
        return True
    except Exception as e:
        logger.error(f"加载数据时出错: {e}")
        return False

@app.route('/health', methods=['GET'])
def health_check():
    """健康检查接口"""
    return jsonify({
        'status': 'healthy',
        'message': '图片搜索服务运行正常',
        'data_loaded': all([index is not None, df is not None, model is not None])
    })

@app.route('/search', methods=['POST'])
def search_images():
    """图片搜索接口"""
    try:
        # 检查数据是否已加载
        if not all([index is not None, df is not None, model is not None]):
            return jsonify({
                'error': '服务未完全初始化，请稍后重试'
            }), 503
        
        # 获取请求参数
        data = request.get_json()
        if not data or 'query' not in data:
            return jsonify({
                'error': '缺少查询参数 "query"'
            }), 400
        
        query = data['query']
        k = data.get('k', 5)  # 默认返回5个结果
        
        # 验证参数
        if not isinstance(query, str) or not query.strip():
            return jsonify({
                'error': '查询参数不能为空'
            }), 400
        
        if not isinstance(k, int) or k <= 0 or k > 100:
            return jsonify({
                'error': 'k参数必须是1-100之间的整数'
            }), 400
        
        # 执行搜索
        query_vec = model.encode([query], convert_to_numpy=True)
        D, I = index.search(query_vec, k=k)
        
        # 构建结果
        results = []
        for rank, (idx, distance) in enumerate(zip(I[0], D[0])):
            image_info = df.iloc[idx]
            
            result = {
                'rank': int(rank + 1),
                'image_id': str(image_ids[idx]),
                'description': str(descriptions[idx]),
                'similarity_score': float(1 - distance),  # 转换为相似度分数
                'photo_url': str(image_info.get('photo_image_url', 'N/A')),
                'width': int(image_info.get('photo_width', 0)) if pd.notna(image_info.get('photo_width')) else 'N/A',
                'height': int(image_info.get('photo_height', 0)) if pd.notna(image_info.get('photo_height')) else 'N/A'
            }
            results.append(result)
        
        return jsonify({
            'query': query,
            'total_results': len(results),
            'results': results
        })
        
    except Exception as e:
        logger.error(f"搜索时出错: {e}")
        return jsonify({
            'error': '搜索过程中发生错误',
            'details': str(e)
        }), 500

@app.route('/search', methods=['GET'])
def search_images_get():
    """GET方法的搜索接口（用于简单测试）"""
    try:
        # 检查数据是否已加载
        if not all([index is not None, df is not None, model is not None]):
            return jsonify({
                'error': '服务未完全初始化，请稍后重试'
            }), 503
        
        query = request.args.get('q')
        k = request.args.get('k', 5, type=int)
        
        if not query:
            return jsonify({
                'error': '缺少查询参数 "q"'
            }), 400
        
        # 验证参数
        if not isinstance(query, str) or not query.strip():
            return jsonify({
                'error': '查询参数不能为空'
            }), 400
        
        if not isinstance(k, int) or k <= 0 or k > 100:
            return jsonify({
                'error': 'k参数必须是1-100之间的整数'
            }), 400
        
        # 执行搜索
        query_vec = model.encode([query], convert_to_numpy=True)
        D, I = index.search(query_vec, k=k)
        
        # 构建结果
        results = []
        for rank, (idx, distance) in enumerate(zip(I[0], D[0])):
            image_info = df.iloc[idx]
            
            result = {
                'rank': int(rank + 1),
                'image_id': str(image_ids[idx]),
                'description': str(descriptions[idx]),
                'similarity_score': float(1 - distance),  # 转换为相似度分数
                'photo_url': str(image_info.get('photo_image_url', 'N/A')),
                'width': int(image_info.get('photo_width', 0)) if pd.notna(image_info.get('photo_width')) else 'N/A',
                'height': int(image_info.get('photo_height', 0)) if pd.notna(image_info.get('photo_height')) else 'N/A'
            }
            results.append(result)
        
        return jsonify({
            'query': query,
            'total_results': len(results),
            'results': results
        })
        
    except Exception as e:
        logger.error(f"搜索时出错: {e}")
        return jsonify({
            'error': '搜索过程中发生错误',
            'details': str(e)
        }), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'error': '接口不存在'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'error': '服务器内部错误'
    }), 500

if __name__ == '__main__':
    # 启动时加载数据
    if load_model_and_data():
        logger.info("启动Flask服务...")
        app.run(host='0.0.0.0', port=5000, debug=False)
    else:
        logger.error("数据加载失败，服务无法启动") 