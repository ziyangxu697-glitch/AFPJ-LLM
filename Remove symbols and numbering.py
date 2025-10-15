import pandas as pd
import re

def clean_text(text):
    """清理文本：先根据序号分割处理末尾符号，然后去掉序号，保留换行格式"""
    if not isinstance(text, str):
        return text  # 如果不是字符串，直接返回原值

    # 分割文本为多段（基于换行符）
    paragraphs = text.split('\n')
    cleaned_paragraphs = []

    for para in paragraphs:
        if para.strip():  # 只处理非空段落
            # 先处理末尾符号（句号和分号）
            cleaned_para = re.sub(r'[。；]$', '', para.strip())
            # 再去掉开头的序号，如（一）、（二）等
            cleaned_para = re.sub(r'^（[一二三四五六七八九十]+）', '', cleaned_para)
            cleaned_paragraphs.append(cleaned_para)

    # 用换行符重新连接所有段落
    return '\n'.join(cleaned_paragraphs).strip()

def clean_excel(file_path, output_path):
    """读取 Excel 文件，清理指定列的内容，并保存到新的 Excel 文件"""
    try:
        # 读取 Excel 文件
        df = pd.read_excel(file_path)

        # 检查列是否存在
        if 'answer' not in df.columns or 'response' not in df.columns:
            print("Error: 'answer' or 'response' column not found in the Excel file.")
            return

        # 清理指定列的内容
        df['answer'] = df['answer'].apply(clean_text)
        df['response'] = df['response'].apply(clean_text)

        # 保存到新的 Excel 文件
        df.to_excel(output_path, index=False)
        print(f"Cleaned data saved to {output_path}")
    except Exception as e:
        print(f"Error occurred: {e}")



if __name__ == '__main__':
    input_file = 'E:/pythonProject1/测试多个模型/Deepseek-V3/信息抽取之定性依据1/output.xlsx'  # 输入文件路径
    output_file = 'E:/pythonProject1/测试多个模型/Deepseek-V3/信息抽取之定性依据1/output1.xlsx'  # 输出文件路径
    clean_excel(input_file, output_file)
