import pandas as pd
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

# 加载数据
df = pd.read_csv("data.csv")
descriptions = df['description'].tolist()
image_ids = df['image_id'].tolist()

# 使用 sentence-transformers 生成向量
model = SentenceTransformer("all-MiniLM-L6-v2")
embeddings = model.encode(descriptions, convert_to_numpy=True)

# 保存 image_ids 对应顺序
np.save("embeddings.npy", embeddings)
df.to_csv("data_indexed.csv", index=False)

# 构建 faiss 索引
dim = embeddings.shape[1]
index = faiss.IndexFlatL2(dim)
index.add(embeddings)
faiss.write_index(index, "index.faiss")

print("索引构建完成！共索引：", len(image_ids), "条描述。")
