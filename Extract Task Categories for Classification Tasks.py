import pandas as pd

# 读取 Excel 文件
# 替换 'your_file.xlsx' 为你的 Excel 文件路径
df = pd.read_excel('E:/pythonProject1/deepseek蒸馏qwen7b原始基座测试/审计问题分类/output1 - 副本.xlsx')

# 定义关键词列表
keywords = ['财政审计', '企业审计', '农业农村审计', '公共工程审计', '海关审计', '金融审计', '经济责任审计', '民生审计', '税收审计', '自然资源资产审计', '审计共性问题']

# 定义提取函数
def extract_keywords(text):
    if not isinstance(text, str):  # 处理非字符串情况
        return text
    # 统计关键词出现次数
    count = sum(1 for keyword in keywords if keyword in text)
    # 如果没有关键词或有多个关键词，保留原文
    if count != 1:
        return text
    # 如果只有一个关键词，返回该关键词
    for keyword in keywords:
        if keyword in text:
            return keyword
    return text

# 应用函数创建新列
df['extracted_response'] = df['response_new'].apply(extract_keywords)

# 保存处理后的 Excel 文件
# 替换 'output_file.xlsx' 为输出文件路径
df.to_excel('E:/pythonProject1/deepseek蒸馏qwen7b原始基座测试/审计问题分类/output2.xlsx', index=False)

print("处理完成，已保存到 E:/pythonProject1/deepseek蒸馏qwen7b原始基座测试/审计问题分类/output2.xlsx")