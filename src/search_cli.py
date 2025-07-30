import faiss
import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer

# 加载索引和数据
index = faiss.read_index("data/index.faiss")
df = pd.read_csv("data/data_indexed.csv")
embeddings = np.load("data/embeddings.npy")
image_ids = df['image_id'].tolist()
descriptions = df['description'].tolist()

# 加载模型
model = SentenceTransformer("all-MiniLM-L6-v2")

print("请输入要搜索的图片描述（按 Ctrl+C 退出）：")

while True:
    try:
        query = input("\n> ")
        query_vec = model.encode([query], convert_to_numpy=True)
        D, I = index.search(query_vec, k=5)

        print("\n最相关的图片：")
        for rank, idx in enumerate(I[0]):
            image_id = image_ids[idx]
            description = descriptions[idx]
            
            # 从数据框中获取图片信息
            image_info = df.iloc[idx]
            photo_url = image_info.get('photo_image_url', 'N/A')
            width = image_info.get('photo_width', 'N/A')
            height = image_info.get('photo_height', 'N/A')
            
            print(f"{rank + 1}. 图片ID: {image_id}")
            print(f"   描述: {description}")
            print(f"   图片URL: {photo_url}")
            print(f"   尺寸: {width} x {height}")
            print()
    except KeyboardInterrupt:
        print("\n再见！")
        break
