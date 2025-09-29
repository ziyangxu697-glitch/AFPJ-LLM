import numpy as np
import pandas as pd
from sklearn.metrics import f1_score, matthews_corrcoef
from statistics import mean
from pathlib import Path

class Classification:
    CALCULATE_MCC = True
    LOWER_CASE = True
    VERSION = 1

    def __init__(self, excel_file_path):
        """初始化并加载 Excel 文件"""
        self.excel_file_path = excel_file_path
        self.load_dataset()

    def load_dataset(self):
        """从 Excel 文件加载数据集"""
        try:
            df = pd.read_excel(self.excel_file_path)
            print(f"从 {self.excel_file_path} 加载数据集，总行数: {len(df)}")

            # 检查必要列
            required_columns = ['query', 'answer', 'response']
            if not all(col in df.columns for col in required_columns):
                raise ValueError(f"Excel 文件必须包含以下列: {required_columns}")

            # 存储数据集
            self.data = df.to_dict(orient="records")
        except Exception as e:
            print(f"加载数据集时发生错误: {e}")
            self.data = []

    def process_results(self, doc):
        """处理 Excel 中的 answer 和 response 的对比"""
        gold = doc["answer"]  # 正确答案
        if self.LOWER_CASE:
            gold = str(gold).lower()

        response = doc["response"].strip()  # Excel 中的 response 列
        if self.LOWER_CASE:
            response = str(response).lower()

        # 计算准确率：完全匹配
        acc = 1.0 if gold == response else 0.0

        # 用于 F1 和 MCC 的预测和真实值
        pred = response if response else "missing"  # 如果 response 为空，标记为 "missing"

        results = {
            "acc": acc,
            "missing": int(not response),  # 如果 response 为空，标记为 1
            "f1": (pred, gold),  # 用于计算加权 F1
            "macro_f1": (pred, gold),  # 用于计算宏 F1
        }

        if self.CALCULATE_MCC:
            results["mcc"] = (pred, gold)

        return results

    def higher_is_better(self):
        """定义指标优化方向"""
        metrics = {
            "acc": True,
            "f1": True,
            "macro_f1": True,
            "missing": False,
        }
        if self.CALCULATE_MCC:
            metrics["mcc"] = True
        return metrics

    def weighted_f1(self, items):
        """计算加权 F1 分数"""
        preds, golds = zip(*items)
        labels = list(set(golds))  # 所有唯一答案作为标签
        preds = np.array(preds)
        golds = np.array(golds)
        f1 = f1_score(golds, preds, average="weighted", labels=labels)
        return f1

    def macro_f1(self, items):
        """计算宏 F1 分数"""
        preds, golds = zip(*items)
        labels = list(set(golds))
        preds = np.array(preds)
        golds = np.array(golds)
        f1 = f1_score(golds, preds, average="macro", labels=labels)
        return f1

    def matthews_corrcoef(self, items):
        """计算 Matthews 相关系数"""
        preds, golds = zip(*items)
        labels = {label: i for i, label in enumerate(list(set(golds)))}
        preds = [labels.get(pred, -1) for pred in preds]  # 未匹配的预测用 -1
        golds = [labels.get(gold, -1) for gold in golds]
        return matthews_corrcoef(golds, preds)

    def aggregation(self):
        """定义指标聚合方式"""
        metrics = {
            "acc": mean,
            "missing": mean,
            "f1": self.weighted_f1,
            "macro_f1": self.macro_f1,
        }
        if self.CALCULATE_MCC:
            metrics["mcc"] = self.matthews_corrcoef
        return metrics

    def evaluate(self):
        """运行评估"""
        results = []
        for doc in self.data:
            result = self.process_results(doc)
            print(f"索引 {doc.get('index', '未知')}: {result}")
            results.append(result)

        # 聚合结果
        aggregated_results = {}
        for metric in self.aggregation():
            items = [r[metric] for r in results]
            aggregated_results[metric] = self.aggregation()[metric](items)
        return aggregated_results
# 示例使用
if __name__ == "__main__":
    excel_file_path = r"E:/pythonProject1/测试多个模型/Deepseek-V3/审计问题分类1/output3.xlsx"
    task = Classification(excel_file_path)
    aggregated_results = task.evaluate()
    print(f"聚合结果: {aggregated_results}")