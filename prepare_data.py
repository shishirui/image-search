import pandas as pd

# 读取原始数据文件
print("正在读取 photos.csv000...")
df = pd.read_csv("photos.csv000", sep='\t')

print(f"原始数据包含 {len(df)} 行")

# 选择需要的列并重命名
# 使用 ai_description 作为描述，如果没有则使用 photo_description
if 'ai_description' in df.columns:
    df['description'] = df['ai_description'].fillna(df.get('photo_description', ''))
else:
    df['description'] = df.get('photo_description', '')

# 重命名 photo_id 为 image_id
df['image_id'] = df['photo_id']

# 选择最终需要的列，包括图片URL、宽度和高度
result_df = df[['image_id', 'description', 'photo_image_url', 'photo_width', 'photo_height']].copy()

# 清理数据：移除空描述
result_df = result_df.dropna(subset=['description'])
result_df = result_df[result_df['description'].str.strip() != '']

print(f"处理后数据包含 {len(result_df)} 行")

# 保存为 data.csv
result_df.to_csv("data.csv", index=False)
print("数据已保存为 data.csv")

# 显示前几行作为示例
print("\n前5行数据示例：")
print(result_df.head()) 