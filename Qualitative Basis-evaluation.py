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
    return text.split('\n')  # 按换行符分割文本并返回列表

def extract_sections(text):
    """提取【法律当中应当做的行为】和【法律禁止做的行为】的内容"""
    sections = {'应当做的行为': [], '禁止做的行为': []}
    current_section = None

    lines = preprocess_text(text)
    for line in lines:
        if "【法律当中应当做的行为】" in line:
            current_section = '应当做的行为'
        elif "【法律禁止做的行为】" in line:
            current_section = '禁止做的行为'
        elif current_section:
            sections[current_section].append(line.strip())

    return sections

def calculate_metrics(df):
    """计算评估指标，分别比较应当做的行为和禁止做的行为，然后累加结果"""
    if df is None or df.empty:
        print("No data to process.")
        return None

    if 'answer' not in df.columns or 'response' not in df.columns:
        print("Excel file must contain 'answer' and 'response' columns.")
        return None

    metrics = {
        'true_positives': 0,
        'false_positives': 0,
        'false_negatives': 0
    }

    for _, row in df.iterrows():
        answer_sections = extract_sections(row['answer'])
        response_sections = extract_sections(row['response'])

        # 分别比较“应当做的行为”
        answer_should = set(answer_sections['应当做的行为'])
        response_should = set(response_sections['应当做的行为'])
        metrics['true_positives'] += len(answer_should.intersection(response_should))
        metrics['false_positives'] += len(response_should.difference(answer_should))
        metrics['false_negatives'] += len(answer_should.difference(response_should))

        # 分别比较“禁止做的行为”
        answer_forbid = set(answer_sections['禁止做的行为'])
        response_forbid = set(response_sections['禁止做的行为'])
        metrics['true_positives'] += len(answer_forbid.intersection(response_forbid))
        metrics['false_positives'] += len(response_forbid.difference(answer_forbid))
        metrics['false_negatives'] += len(answer_forbid.difference(response_forbid))

    tp = metrics['true_positives']
    fp = metrics['false_positives']
    fn = metrics['false_negatives']

    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0

    missing_rate = fn / (tp + fn) if (tp + fn) > 0 else 0
    redundancy = fp / (tp + fp) if (tp + fp) > 0 else 0

    f1 = (2 * precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

    return {
        "Precision": precision,
        "Recall": recall,
        "F1": f1,
        "Missing Rate": missing_rate,
        "Redundancy": redundancy
    }


def main():
    file_path = "E:/pythonProject1/测试多个模型/Deepseek-V3/信息抽取之定性依据1/output1.xlsx"  # 替换为你的 Excel 文件路径
    df = load_excel_data(file_path)
    metrics = calculate_metrics(df)
    if metrics:
        print("Evaluation Metrics:")
        for metric, value in metrics.items():
            print(f"{metric}: {value:.4f}")

if __name__ == "__main__":
    main()