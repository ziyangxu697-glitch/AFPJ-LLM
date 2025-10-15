## AuditJudgLLM: A Domain-Specific Large Language Model and Benchmark for Evaluating Audit Judgment

### 🧾 Project Overview

**Project Type:** Audit-specific data distillation, Large Language Model (LLM) fine-tuning, and systematic evaluation and testing via code.
**This repository contains:**

  * Scripts for generating the core dataset.
  * Scripts for extracting answers embedded within `<think>` tags (often used in Chain-of-Thought responses).
  * Evaluation scripts tailored for generative, classification, and extraction tasks within the dataset.
  * A complete framework implementation for model distillation and comprehensive evaluation.

*(Optional: Placeholder for conceptual framework diagrams, e.g., Model Distillation Flowchart, Data Generation & Evaluation Architecture Diagram)*

-----

### ⚡ Quick Start

#### 2.1 Obtaining Rationales for Knowledge Distillation

The following template serves as the input prompt to facilitate the **teacher model** (a powerful LLM) in generating high-quality *rationales* (Chain-of-Thought or reasoning steps) for knowledge distillation. This process is crucial for training the student (smaller) model.

```python
f"Generate a complete and clear reasoning process for the question: '{question}', ensuring the final answer is STRICTLY consistent with the expected answer: '{my_answer}'. The reasoning process must include the following sections:\n"
f"---\n"
f"**1. Problem Analysis:**\n"
f"- Briefly analyze the core content of the question, clearly identifying the key points that need to be addressed, including all parts of the task requirements.\n"
f"\n"
f"**2. Reasoning Steps:**\n"
f"- **Step 1**: Identify the background and task requirements of the problem, clarifying the manifestation of the audit issue.\n"
f"- **Step 2**: Based on the issue's manifestation, analyze potentially applicable laws and regulations, focusing on qualitative basis/evidence.\n"
f"- **Step 3**: Based on the qualitative findings, determine the basis for handling or punishment (if applicable).\n"
f"- **Step 4**: Verify the consistency of the reasoning result with the expected answer '{my_answer}', and adjust the format or content.\n"
f"\n"
f"**3. Final Answer (Strict Requirement):**\n"
f"- MUST be strictly equal to the expected answer: '{my_answer}', including punctuation and wording.\n"
f"- Output the answer directly, with no extra explanation.\n"
f"---\n"
f"⚠️ Note:\n"
f"- You MUST fully write out the Problem Analysis and at least 4 Reasoning Steps; do not skip any.\n"
f"- Strictly adhere to the above format, ensuring the logic is detailed and coherent.\n"
```
