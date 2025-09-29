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
    """对文本进行分割处理，以换行为界限分割文本"""
    # 如果不是字符串（比如 NaN 或 float），返回空集合
    if not isinstance(text, str):
        return set()
    # 去除首尾空白后按换行符分割并转换为集合
    return set(line.strip() for line in text.strip().split('\n') if line.strip())

def calculate_metrics(df):
    """计算评估指标"""
    if df is None or df.empty:
        print("No data to process.")
        return None

    if 'answer' not in df.columns or 'response' not in df.columns:
        print("Excel file must contain 'answer' and 'response' columns.")
        return None

    true_positives = 0
    false_positives = 0
    false_negatives = 0

    for _, row in df.iterrows():
        answer = preprocess_text(row['answer'])    # 按换行符分割
        response = preprocess_text(row['response']) # 按换行符分割

        true_positives += len(answer.intersection(response))
        false_positives += len(response.difference(answer))
        false_negatives += len(answer.difference(response))

    # 计算指标，避免除以零
    total_positives = true_positives + false_positives
    total_actual = true_positives + false_negatives

    precision = true_positives / total_positives if total_positives > 0 else 0
    recall = true_positives / total_actual if total_actual > 0 else 0
    f1 = (2 * precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
    missing_rate = false_negatives / total_actual if total_actual > 0 else 0
    redundancy = false_positives / total_positives if total_positives > 0 else 0

    return {
        "Precision": precision,
        "Recall": recall,
        "F1": f1,
        "Missing Rate": missing_rate,
        "Redundancy": redundancy,
    }

def main():
    file_path = "E:/pythonProject1/测试多个模型/Deepseek-V3/信息抽取之处理处罚依据1/output1.xlsx"  # 替换为你的 Excel 文件路径
    df = load_excel_data(file_path)
    if df is not None:  # 添加检查，确保 df 不为 None
        metrics = calculate_metrics(df)
        if metrics:
            print("Evaluation Metrics:")
            for metric, value in metrics.items():
                print(f"{metric}: {value:.4f}")

if __name__ == "__main__":
    main()
