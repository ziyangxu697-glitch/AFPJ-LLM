import pandas as pd


def load_excel_data(file_path):
    """加载 Excel 文件中的数据"""
    try:
        df = pd.read_excel(file_path)
        return df
    except Exception as e:
        print(f"Error loading Excel file: {e}")
        return None


def preprocess_text(text):
    """对文本进行预处理，删除多余的格式化文本和空行"""
    if not isinstance(text, str):
        return ""

    # 删除特定的格式化标记
    text = text.replace("：**", "").replace("**", "").replace("---", "").strip()

    # # 分割成行并移除空行
    # lines = text.split('\n')
    # 只保留非空行并去除首尾空格
    cleaned_lines = [line.strip() for line in lines if line.strip()]
    # 重新组合文本
    cleaned_text = '\n'.join(cleaned_lines)

    return cleaned_text


def preprocess_columns(df):
    """对指定列进行预处理"""
    if df is None or df.empty:
        print("No data to process.")
        return None

    # 检查必要的列是否存在
    if 'reasoning content' not in df.columns:
        print("Excel file must contain 'reasoning content' column.")
        return None

    # 对 'reasoning content' 列进行预处理
    df['reasoning content'] = df['reasoning content'].apply(preprocess_text)

    # 如果有 'answer1' 列，也进行处理（可选）
    if 'answer1' in df.columns:
        df['answer1'] = df['answer1'].apply(preprocess_text)

    return df


def save_excel_data(df, output_file_path):
    """保存处理后的数据到新的 Excel 文件"""
    try:
        df.to_excel(output_file_path, index=False)
        print(f"Processed data saved to {output_file_path}")
    except Exception as e:
        print(f"Error saving Excel file: {e}")


def main():
    # 输入和输出文件路径
    input_file_path = "E:/pythonProject1/数据集重构/信息抽取之处理处罚.xlsx"  # 替换为实际输入路径
    output_file_path = "E:/pythonProject1/数据集重构/信息抽取之处理处罚结果.xlsx"  # 替换为实际输出路径

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