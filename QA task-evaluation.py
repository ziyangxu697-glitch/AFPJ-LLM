import os
import sys
import jieba
import pandas as pd  # 添加 pandas 用于读写 Excel
from bert_score import score
from rouge_chinese import Rouge

# 环境配置
os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'
os.environ['HF_HUB_OFFLINE'] = '1'

class QAwithString():
    def rougeChinese(self, items):
        jieba.load_userdict(r"E:/pythonProject1/qwen 7b基座模型测试/审计分词表.txt")
        hyps, refs = map(list, zip(*[[' '.join(jieba.cut(d[0])), ' '.join(jieba.cut(d[1]))] for d in items]))

        filter_hyps = []
        filter_refs = []
        for i in range(len(hyps)):
            hyp = hyps[i]
            ref = refs[i]
            if hyp.strip() and ref.strip():
                filter_hyps.append(hyp)
                filter_refs.append(ref)

        rouge = Rouge()
        scores = rouge.get_scores(filter_hyps, filter_refs, avg=True, ignore_empty=True)
        return scores

    def bert_score(self, items):
        golds, preds = zip(*items)
        P, R, F1 = score(golds, preds, lang="zh", model_type="bert-base-chinese", verbose=True)
        output_dict = {
            "precision": P.tolist(),
            "recall": R.tolist(),
            "f1": F1.tolist(),
        }
        return sum(output_dict["f1"]) / len(output_dict["f1"])

def compute_method(excel_file_path, output_excel_path):
    qa_task = QAwithString()

    # 加载 Excel 数据
    df = pd.read_excel(excel_file_path, engine='openpyxl')

    items = []
    for _, row in df.iterrows():
        answer = str(row["answer"]).strip()
        response = str(row["response"]).strip()
        if answer and response:
            items.append((answer, response))

    bert_score_result = qa_task.bert_score(items)
    rouge_result = qa_task.rougeChinese(items)

    # 将结果保存为 Excel 文件
    metrics_data = {
        "Metric": ["ROUGE-1", "ROUGE-2", "ROUGE-L", "BERT Score (F1)"],
        "Value": [
            rouge_result["rouge-1"]['f'],
            rouge_result["rouge-2"]['f'],
            rouge_result["rouge-l"]['f'],
            bert_score_result
        ]
    }
    metrics_df = pd.DataFrame(metrics_data)
    metrics_df.to_excel(output_excel_path, index=False, engine='openpyxl')

    return bert_score_result, rouge_result

if __name__ == '__main__':
    # excel_file_path = r"D:\研究生\论文材料\result\result_更新数据集\deepseek-r1\自动问答\Audit_Target.xlsx"
    excel_file_path = r"E:/pythonProject1/测试多个模型/Deepseek-V3/问题短语-表现形式1/output2.xlsx"
    output_excel_path = r"E:/pythonProject1/测试多个模型/Deepseek-V3/问题短语-表现形式1/output_Target.xlsx"

    bert_score, rouge_chinese = compute_method(excel_file_path, output_excel_path)

    print(excel_file_path)
    print("ROUGE-1: {:.4f}".format(rouge_chinese["rouge-1"]['f']))
    print("ROUGE-2: {:.4f}".format(rouge_chinese["rouge-2"]['f']))
    print("ROUGE-L: {:.4f}".format(rouge_chinese["rouge-l"]['f']))
    print("BERT Score (F1): {:.4f}".format(bert_score))
    print("********************************************************")