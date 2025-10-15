import pandas as pd
import re


def load_excel_data(file_path):
    """加载 Excel 文件中的数据"""
    try:
        df = pd.read_excel(file_path)
        return df
    except Exception as e:
        print(f"Error loading Excel file: {e}")
        return None


def preprocess_text(text):
    """对文本进行预处理，提取 </think> 之后的内容，删除格式化标记，并只删除结尾的重复空行"""
    if not isinstance(text, str):
        return ""

    # 提取 </think> 之后的内容
    match = re.search(r'</think>\s*(.*)', text, re.DOTALL)
    if match:
        text = match.group(1).strip()  # 获取 </think> 之后的非空内容
    else:
        text = text.strip()  # 如果没有 </think>，使用原始内容（去除首尾空格）

    # 删除特定的格式化标记
    text = text.replace("：**", "").replace("**", "").replace("---", "").replace("###", "")

    # 分割成行并清理
    lines = text.split('\n')
    # 移除每行首尾空格
    lines = [line.strip() for line in lines]
    # 过滤掉空行（仅包含空格或空字符串的行），但保留有意插入的空行
    cleaned_lines = []
    for i, line in enumerate(lines):
        if line or (i > 0 and lines[i-1]):  # 保留非结尾的空行
            cleaned_lines.append(line)

    # 只移除结尾的连续空行
    while cleaned_lines and not cleaned_lines[-1]:
        cleaned_lines.pop()

    # 重新组合文本，保留非结尾的空行
    cleaned_text = '\n'.join(cleaned_lines)

    return cleaned_text


def preprocess_columns(df):
    """对 response 列进行预处理"""
    if df is None or df.empty:
        print("No data to process.")
        return None

    # 检查必要的列是否存在
    if 'response' not in df.columns:
        print("Excel file must contain 'response' column.")
        return None

    # 对 'response' 列进行预处理，生成 'response_new' 列
    df['response_new'] = df['response'].apply(preprocess_text)

    return df


def save_excel_data(df, output_file_path):
    """保存处理后的数据到新的 Excel 文件"""
    try:
        df.to_excel(output_file_path, index=False, engine='openpyxl')
        print(f"Processed data saved to {output_file_path}")
    except Exception as e:
        print(f"Error saving Excel file: {e}")


def main():
    # 输入和输出文件路径
    input_file_path = "E:/pythonProject1/测试多个模型/Deepseek-V3/问题短语-表现形式1/output.xlsx"  # 替换为实际输入路径
    output_file_path = "E:/pythonProject1/测试多个模型/Deepseek-V3/问题短语-表现形式1/output1.xlsx"  # 替换为实际输出路径

    # 加载数据
    df = load_excel_data(input_file_path)
    if df is not None:
        # 预处理数据
        df = preprocess_columns(df)
        if df is not None:
            # 保存处理后的数据
            save_excel_data(df, output_file_path)


if __name__ == "__main__":
    main()