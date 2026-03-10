# LangSmith Evaluation Deep Dive — Notebook Explanation

## What This Notebook Does

This notebook is a **hands-on tutorial** teaching you how to use **LangSmith** — a platform for monitoring, testing, and improving LLM applications. Think of LangSmith as "unit testing + observability for AI apps."

---

## The 3 Big Ideas

### 1. Tracing — See exactly what your LLM app does under the hood
- Every LLM call, retrieval step, and function call gets logged
- You can inspect inputs, outputs, latency, and token usage
- Done via `@traceable` decorator or `wrap_openai()`

### 2. Evaluation — Systematically test if your LLM app gives good answers
- Create **datasets** (sets of input/expected-output pairs)
- Write **evaluators** (functions that score how good an answer is)
- Run `evaluate()` to test your app against the dataset and get scores

### 3. Comparison — Figure out which model/prompt/config is best
- Run the same dataset through different setups (different models, prompts, etc.)
- Compare results side-by-side
- Use **pairwise evaluation** to have an LLM pick the better answer

---

## Section-by-Section Breakdown

| Section | Cells | What It Teaches |
|---|---|---|
| **Setup** | 1-4 | API keys, SSL, LangSmith client |
| **Tracing** | 5-17 | Log LLM calls automatically with `wrap_openai` and `@traceable` |
| **Basic Evaluation** | 18-26 | Create a dataset, write a custom evaluator, run `evaluate()` |
| **LangSmith SDK** | 27-43 | Query runs, attach feedback, export data to CSV |
| **RAG Pipeline** | 44-55 | Build a retrieval-augmented generation app, evaluate its answers |
| **Regression Testing** | 56-60 | Compare 5 configs on the same dataset to catch quality drops |
| **Online Evaluators** | 61-66 | Auto-score new runs in real-time as they happen |
| **Backtesting** | 67-75 | Turn production traffic into test cases for new models |
| **Pairwise Eval** | 76-92 | Head-to-head model comparison (which answer is better?) |
| **Repetitions** | 93-99 | Run tests multiple times to measure variance |

---

## The Recurring Pattern

Every section follows the same 4-step workflow:

```
1. Define a target function    →  "Here's my LLM app"
2. Create/load a dataset       →  "Here are test cases"
3. Define an evaluator         →  "Here's how to score answers"
4. Run evaluate()              →  "Grade my app and show results"
```

---

## Detailed Section Explanations

### 1. Environment Setup (Cells 1-4)
Sets up SSL certificates, environment variables (`LANGCHAIN_API_KEY`, `LANGCHAIN_TRACING_V2`), and initializes the LangSmith client.

### 2. Tracing with `@traceable` and `wrap_openai` (Cells 5-17)
- Wraps an OpenAI-compatible client (Groq) with `wrap_openai()` so all API calls are automatically logged to LangSmith
- Demonstrates the `@traceable` decorator to trace custom functions
- Creates a simple Q&A function (`answer_dbrx_question_oai`) and shows how traces appear in LangSmith

### 3. Evaluation with Datasets (Cells 18-26)
- Creates a **"DBRX" dataset** in LangSmith with question/answer pairs
- Runs `evaluate()` against the dataset with a custom **chain-of-thought QA evaluator** (`cot_qa_evaluator`) that uses Groq to judge answer correctness
- Introduces **custom evaluators** and **summary evaluators** (aggregate metrics across all examples)

### 4. LangSmith SDK — Projects, Runs, Feedback (Cells 27-43)
- Lists projects and filters runs by time range
- Reads individual run inputs/outputs
- Attaches **feedback scores** (thumbs up/down, corrections) to runs programmatically
- Exports runs to **CSV/pandas DataFrames** for analysis

### 5. RAG Pipeline (Cells 44-55)
- Loads LCEL documentation from the web, splits it, and builds a **ChromaDB vector store** with Ollama embeddings
- Builds a `RagBot` class that retrieves relevant docs and generates answers using either Groq or Ollama
- Evaluates RAG quality using a custom evaluator on a **"RAG_QA_LCEL"** dataset

### 6. Regression Testing / Comparing Experiments (Cells 56-60)
- Creates an **"lcel-eval"** dataset with 5 LCEL Q&A pairs
- Runs **5 different model configurations** through the same dataset
- Compares experiment results side-by-side in LangSmith to detect regressions

### 7. Online Evaluators (Cells 61-66)
- Sets up **real-time evaluation rules** that automatically score new runs as they come in
- Uses Groq as an online evaluator to check hallucination and helpfulness

### 8. Backtesting (Cells 67-75)
- Takes **production runs** from a project and converts them into a test dataset using `convert_runs_to_test`
- Enables testing new models against real user queries

### 9. Pairwise Evaluation (Cells 76-92)
- Defines a **pairwise evaluator** that compares two model outputs and picks the better one
- Uses `evaluate_comparative()` to run head-to-head comparisons between experiments
- Runs a **paper summarization** use case: loads arxiv papers, creates tweet summaries with Groq and Ollama, then compares quality pairwise

### 10. Repetitions (Cells 93-99)
- Demonstrates `num_repetitions=3` to run each evaluation example **multiple times**
- Useful for measuring variance in non-deterministic LLM outputs and evaluator judgments

---

## Models Used

Since this was adapted to run without paid API keys:
- **Groq** (`llama-3.1-8b-instant`) — fast, free-tier cloud LLM for generation and evaluation
- **Ollama** (`llama3.2:1b`) — local LLM for embeddings and as an alternative generator

All results are logged to LangSmith where you can view traces, scores, and experiment comparisons in a web dashboard.
