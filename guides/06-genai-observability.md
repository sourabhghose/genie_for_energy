# Module 6: GenAI Observability (60 min)

**Context:** MLflow experiments, traces, evaluations, and instrumentation for GenAI agents and RAG applications.

---

## 6A: Capabilities Overview (10 min)

### Overview
When Genie Code is opened from an MLflow experiment context, it gains access to your GenAI observability data—traces, prompts, datasets, evaluations, and labeling sessions.

### Step-by-Step Instructions

**Step 1:** Open an MLflow experiment
- Navigate to your Databricks workspace
- Go to **MLflow** → **Experiments**
- Open an experiment that contains GenAI traces (e.g., from a RAG agent or chatbot)

**Step 2:** Open Genie Code from the MLflow context
- Click the **Genie Code** icon in the experiment view (or use the experiment's Genie Code entry point)
- Genie Code opens with access to the experiment's traces, datasets, and evaluations

**Step 3:** Discover what's accessible
Ask Genie Code:

```
What capabilities do you have in this MLflow context?
```

**Expected results:**
- Genie Code responds with a list of capabilities, such as:
  - **Traces:** Search, filter, analyze spans and token usage
  - **Prompts:** View and compare prompt versions
  - **Datasets:** List evaluation datasets
  - **Evaluations:** Run and review evaluation results
  - **Labeling sessions:** Reference human feedback

**Step 4:** Verify access
- Try: `List the traces in this experiment`
- Try: `Show me the evaluation datasets`

### Key Concepts
| Capability | Description |
|------------|-------------|
| **Traces** | Recorded execution flows of your GenAI application (spans, inputs, outputs) |
| **Prompts** | Stored prompt templates and versions |
| **Datasets** | Evaluation datasets (Q&A pairs, test cases) |
| **Evaluations** | Scorer results (Correctness, Safety, RetrievalGroundedness, etc.) |
| **Labeling sessions** | Human feedback used for fine-tuning or evaluation |

### Practical Tips
- Always open Genie Code from the MLflow experiment to get observability context
- If Genie Code doesn't show MLflow capabilities, ensure you're in the experiment view

---

## 6B: Trace Analysis (20 min)

### Overview
Traces capture the full execution of a GenAI application. Genie Code can search, filter, and analyze them to find failures, bottlenecks, and quality issues.

### Step-by-Step Instructions

**Step 1:** Find failing traces
In Genie Code (within MLflow experiment context), prompt:

```
Show me failing traces in the last 24 hours
```

**Expected results:**
- A list or table of traces with status "FAILED" or "ERROR"
- Optionally: trace IDs, timestamps, error messages
- You can drill into specific traces for root cause analysis

---

**Step 2:** Find traces with empty retrieval
Prompt:

```
Find traces where the retriever returned no results
```

**Expected results:**
- Traces where a retrieval/vector search span returned zero documents
- Useful for debugging RAG applications where "no context" leads to poor answers

---

**Step 3:** Identify token-heavy spans
Prompt:

```
Which spans consume the most tokens?
```

**Expected results:**
- A breakdown of token usage by span (e.g., LLM calls, embedding calls)
- Helps identify cost drivers and optimization opportunities

---

**Step 4:** Deep-dive a specific trace
When you have a trace ID or a problematic trace, prompt:

```
This trace has an incorrect response. What went wrong?
```

Or, with a trace ID:

```
Trace ID abc123 has an incorrect response. Analyze it and tell me what went wrong.
```

**Expected results:**
- Genie Code walks through the trace spans
- Identifies: wrong retrieval results, prompt issues, model behavior, missing context
- Suggests fixes (e.g., improve retrieval, adjust prompt, add fallbacks)

### Key Concepts
| Concept | Description |
|---------|-------------|
| **Trace** | Full execution record of one GenAI request |
| **Span** | A single step (e.g., retrieval, LLM call, tool use) |
| **Token usage** | Input/output tokens per span; drives cost and latency |

### Practical Tips
- Use time filters ("last 24 hours", "this week") to narrow results
- Combine filters: "Failing traces where retriever returned no results"
- Export trace IDs for batch analysis or evaluation

---

## 6C: Evaluation Setup (20 min)

### Overview
MLflow GenAI evaluation lets you score your agent's outputs with built-in and custom scorers. Genie Code can help set up evaluations, create datasets, and analyze results.

### Step-by-Step Instructions

**Step 1:** Set up evaluation for a RAG agent
Prompt:

```
Help me set up evaluation for my RAG agent with Correctness and RetrievalGroundedness scorers
```

**Expected results:**
- Genie Code generates Python code using `mlflow.genai.evaluate()`
- Includes `Correctness` and `RetrievalGroundedness` scorers
- May include dataset loading, model/agent reference, and evaluation run logic

---

**Step 2:** Create an evaluation dataset
Prompt:

```
Create an evaluation dataset with 20 billing Q&A pairs
```

**Expected results:**
- A dataset structure (e.g., pandas DataFrame or JSON) with columns like `question`, `expected_answer` or `ground_truth`
- 20 example pairs relevant to energy billing (e.g., "What is my current balance?", "When is my next payment due?")
- Code to save/register the dataset in MLflow

---

**Step 3:** Query latency metrics
Prompt:

```
What are the P50/P95 latencies?
```

**Expected results:**
- Percentile latency statistics (P50, P95, etc.) for traces or evaluation runs
- May show end-to-end latency or per-span latency

---

**Step 4:** Compare time periods
Prompt:

```
Compare this week vs last week
```

**Expected results:**
- Side-by-side or trend comparison of metrics (latency, token usage, pass rates, etc.)
- Helps track regressions or improvements after changes

### Key Concepts
| Concept | Description |
|---------|-------------|
| **Scorer** | Function that scores model output (Correctness, Safety, RetrievalGroundedness, custom) |
| **Evaluation dataset** | Input-output pairs used to run evaluations |
| **P50/P95** | 50th and 95th percentile latencies; P95 indicates tail latency |

### Practical Tips
- Start with small datasets (10–20 pairs) for quick iteration
- Use RetrievalGroundedness for RAG to ensure answers are grounded in retrieved docs
- Run evaluations after each prompt or model change to catch regressions

---

## 6D: Instrumentation (10 min)

### Overview
To get traces and evaluations, your GenAI application must be instrumented. Genie Code can generate instrumentation code for your energy chatbot or agent.

### Step-by-Step Instructions

**Step 1:** Request instrumentation help
Prompt:

```
Help me add tracing to my energy chatbot code
```

**Expected results:**
- Genie Code generates Python code that includes:
  - **`mlflow.genai.autolog()`** — automatic tracing for supported frameworks (LangChain, OpenAI, etc.)
  - **`@mlflow.trace`** — decorator for custom functions
  - **Manual spans** — `with mlflow.start_span(...)` for granular tracing
- Code tailored to a chatbot (e.g., conversation turns, retrieval, LLM calls)

**Step 2:** Review the generated code
- Identify where traces are created (entry point, each turn)
- Identify spans for: retrieval, LLM call, tool use, response formatting

**Step 3:** Integrate into your project
- Copy the instrumentation patterns into your energy chatbot
- Ensure `MLFLOW_TRACKING_URI` or Databricks workspace is configured
- Run a test request and verify traces appear in MLflow

### Key Concepts
| Method | Use Case |
|--------|----------|
| **autolog()** | Automatic tracing for LangChain, OpenAI, etc. |
| **@mlflow.trace** | Decorate functions to create trace spans |
| **start_span()** | Manual span for custom logic |

### Practical Tips
- Use `autolog()` first for quick setup; add manual spans for custom logic
- Ensure trace context is passed through async or multi-turn flows
- Add span attributes (e.g., `customer_id`, `region`) for filtering

---

## Summary Checklist

- [ ] Opened Genie Code from an MLflow experiment
- [ ] Asked "What capabilities do you have in this MLflow context?"
- [ ] Ran trace analysis: failing traces, empty retrieval, token-heavy spans
- [ ] Deep-dove a trace with an incorrect response
- [ ] Set up evaluation with Correctness and RetrievalGroundedness
- [ ] Created a 20-pair billing Q&A evaluation dataset
- [ ] Queried P50/P95 latencies and compared this week vs last week
- [ ] Generated instrumentation code for an energy chatbot
