# Databricks notebook source
# MAGIC %md
# MAGIC # GenAI Observability Prompt Guide
# MAGIC ## Genie Code in MLflow Experiment UI - Module 6
# MAGIC
# MAGIC This notebook provides **exact prompts** to use when working with Genie Code in the MLflow Experiment UI for GenAI observability. Use these prompts to analyze traces, set up evaluations, and instrument your GenAI applications.

# COMMAND ----------

# MAGIC %md
# MAGIC ---
# MAGIC # Section A: Capabilities Overview
# MAGIC ---

# COMMAND ----------

# MAGIC %md
# MAGIC ## A1: What Can I Do with GenAI Observability?
# MAGIC
# MAGIC **When to use:** When first exploring the MLflow Experiment UI for GenAI.
# MAGIC
# MAGIC **Exact prompt to type:**

# COMMAND ----------

# MAGIC %md
# MAGIC ```
# MAGIC What can I do with GenAI observability in the MLflow Experiment UI? Explain: traces, prompts, datasets, and evaluations. How do they work together?
# MAGIC ```
# MAGIC
# MAGIC **Expected behavior:** Genie Code explains the four pillars—traces (request/response flow), prompts (versioned inputs), datasets (test sets), evaluations (quality metrics)—and how they connect.
# MAGIC
# MAGIC **Key concepts:** Trace lifecycle, prompt management, evaluation datasets, evaluation runs.

# COMMAND ----------

# MAGIC %md
# MAGIC ## A2: Traces Overview
# MAGIC
# MAGIC **Exact prompt to type:**

# COMMAND ----------

# MAGIC %md
# MAGIC ```
# MAGIC How do traces work in MLflow? What information is captured in a trace (spans, inputs, outputs, tokens, latency)? How can I filter and search traces?
# MAGIC ```
# MAGIC
# MAGIC **Expected behavior:** Genie Code describes trace structure, span hierarchy, metadata (tokens, latency), and filtering options in the UI.
# MAGIC
# MAGIC **Key concepts:** Traces, spans, token usage, latency, trace filtering.

# COMMAND ----------

# MAGIC %md
# MAGIC ## A3: Prompts and Datasets
# MAGIC
# MAGIC **Exact prompt to type:**

# COMMAND ----------

# MAGIC %md
# MAGIC ```
# MAGIC What are MLflow prompts and datasets? How do I create a dataset from traces? How do I use a dataset to run evaluations?
# MAGIC ```
# MAGIC
# MAGIC **Expected behavior:** Genie Code explains prompt versioning, dataset creation from traces, and linking datasets to evaluation runs.
# MAGIC
# MAGIC **Key concepts:** Prompt registry, dataset from traces, evaluation workflow.

# COMMAND ----------

# MAGIC %md
# MAGIC ## A4: Evaluations Overview
# MAGIC
# MAGIC **Exact prompt to type:**

# COMMAND ----------

# MAGIC %md
# MAGIC ```
# MAGIC How do GenAI evaluations work in MLflow? What built-in scorers are available (correctness, safety, groundedness)? How do I define custom scorers?
# MAGIC ```
# MAGIC
# MAGIC **Expected behavior:** Genie Code lists built-in scorers and explains how to add custom @scorer functions.
# MAGIC
# MAGIC **Key concepts:** Built-in scorers, custom scorers, evaluation runs, scoring outputs.

# COMMAND ----------

# MAGIC %md
# MAGIC ---
# MAGIC # Section B: Trace Analysis Prompts
# MAGIC ---

# COMMAND ----------

# MAGIC %md
# MAGIC ## B1: Find Failing Traces
# MAGIC
# MAGIC **When to use:** When you need to identify traces that failed or returned errors.
# MAGIC
# MAGIC **Exact prompt to type:**

# COMMAND ----------

# MAGIC %md
# MAGIC ```
# MAGIC How do I find traces that failed or had errors in the MLflow Experiment UI? What filters or queries should I use?
# MAGIC ```
# MAGIC
# MAGIC **Expected behavior:** Genie Code explains how to filter by status (error/failed), search by error message, or use the trace list filters.
# MAGIC
# MAGIC **Key concepts:** Trace status, error filtering, trace search.

# COMMAND ----------

# MAGIC %md
# MAGIC ## B2: Investigate Root Cause of Failed Trace
# MAGIC
# MAGIC **When to use:** When you have a specific failed trace and need to debug it.
# MAGIC
# MAGIC **Exact prompt to type:**

# COMMAND ----------

# MAGIC %md
# MAGIC ```
# MAGIC I have a trace ID that failed. How do I investigate the root cause? Walk me through: 1) Opening the trace, 2) Identifying which span failed, 3) Reading the error message and inputs/outputs, 4) Tracing back to the source of the failure.
# MAGIC ```
# MAGIC
# MAGIC **Expected behavior:** Genie Code provides a step-by-step guide to trace inspection and root cause analysis.
# MAGIC
# MAGIC **Key concepts:** Trace detail view, span hierarchy, error propagation, input/output inspection.

# COMMAND ----------

# MAGIC %md
# MAGIC ## B3: Compare Traces Side-by-Side
# MAGIC
# MAGIC **Exact prompt to type:**

# COMMAND ----------

# MAGIC %md
# MAGIC ```
# MAGIC How can I compare two traces side-by-side in MLflow? I want to see differences in prompts, model outputs, token usage, and latency between a working trace and a failing one.
# MAGIC ```
# MAGIC
# MAGIC **Expected behavior:** Genie Code explains comparison features (if available) or how to open multiple traces and manually compare.
# MAGIC
# MAGIC **Key concepts:** Trace comparison, A/B analysis, prompt/output diff.

# COMMAND ----------

# MAGIC %md
# MAGIC ---
# MAGIC # Section C: Evaluation Setup Prompts
# MAGIC ---

# COMMAND ----------

# MAGIC %md
# MAGIC ## C1: Create Dataset from Traces
# MAGIC
# MAGIC **When to use:** When you want to build an evaluation dataset from existing traces.
# MAGIC
# MAGIC **Exact prompt to type:**

# COMMAND ----------

# MAGIC %md
# MAGIC ```
# MAGIC How do I create an evaluation dataset from traces in MLflow? I want to select traces from the last 7 days, extract inputs and expected outputs, and save as a dataset for evaluation.
# MAGIC ```
# MAGIC
# MAGIC **Expected behavior:** Genie Code explains the workflow: filter traces, export to dataset, define input/output columns.
# MAGIC
# MAGIC **Key concepts:** Dataset from traces, trace export, evaluation dataset schema.

# COMMAND ----------

# MAGIC %md
# MAGIC ## C2: Run Evaluation with Built-in Scorers
# MAGIC
# MAGIC **When to use:** When you want to run an evaluation using MLflow's built-in scorers.
# MAGIC
# MAGIC **Exact prompt to type:**

# COMMAND ----------

# MAGIC %md
# MAGIC ```
# MAGIC How do I run an evaluation in MLflow using built-in scorers like Correctness and Safety? I have a dataset with inputs and expected outputs. Walk me through the evaluation run setup.
# MAGIC ```
# MAGIC
# MAGIC **Expected behavior:** Genie Code explains how to configure an evaluation run, select scorers, and run it against a dataset.
# MAGIC
# MAGIC **Key concepts:** Evaluation run, built-in scorers, dataset binding.

# COMMAND ----------

# MAGIC %md
# MAGIC ## C3: Compare Evaluation Results
# MAGIC
# MAGIC **When to use:** When you have multiple evaluation runs and want to compare performance.
# MAGIC
# MAGIC **Exact prompt to type:**

# COMMAND ----------

# MAGIC %md
# MAGIC ```
# MAGIC I ran evaluations for two different prompts. How do I compare their results in MLflow? I want to see which prompt has better correctness, lower latency, and fewer token usage.
# MAGIC ```
# MAGIC
# MAGIC **Expected behavior:** Genie Code explains how to view evaluation runs, compare metrics, and interpret the comparison view.
# MAGIC
# MAGIC **Key concepts:** Evaluation comparison, metric aggregation, run selection.

# COMMAND ----------

# MAGIC %md
# MAGIC ---
# MAGIC # Section D: Instrumentation Guidance Prompts
# MAGIC ---

# COMMAND ----------

# MAGIC %md
# MAGIC ## D1: Add Tracing to My App
# MAGIC
# MAGIC **When to use:** When you want to instrument a GenAI application for observability.
# MAGIC
# MAGIC **Exact prompt to type:**

# COMMAND ----------

# MAGIC %md
# MAGIC ```
# MAGIC How do I add MLflow tracing to my GenAI application? I'm using Python with OpenAI/LangChain. Show me the minimal code to start tracing requests.
# MAGIC ```
# MAGIC
# MAGIC **Expected behavior:** Genie Code provides code snippets for enabling tracing (e.g., mlflow.open_tracing, or framework-specific setup).
# MAGIC
# MAGIC **Key concepts:** Tracing setup, OpenAI/LangChain integration, trace client.

# COMMAND ----------

# MAGIC %md
# MAGIC ## D2: Trace Custom Spans
# MAGIC
# MAGIC **Exact prompt to type:**

# COMMAND ----------

# MAGIC %md
# MAGIC ```
# MAGIC How do I create custom spans in my traced application? I want to log retrieval steps, tool calls, and post-processing as separate spans.
# MAGIC ```
# MAGIC
# MAGIC **Expected behavior:** Genie Code shows how to use mlflow.start_span or equivalent to create nested spans.
# MAGIC
# MAGIC **Key concepts:** Custom spans, span nesting, span attributes.

# COMMAND ----------

# MAGIC %md
# MAGIC ## D3: Send Traces to MLflow
# MAGIC
# MAGIC **Exact prompt to type:**

# COMMAND ----------

# MAGIC %md
# MAGIC ```
# MAGIC How do I configure my application to send traces to the MLflow tracking server? What environment variables or config do I need for Databricks?
# MAGIC ```
# MAGIC
# MAGIC **Expected behavior:** Genie Code explains MLflow tracking URI, Databricks workspace config, and authentication for trace ingestion.
# MAGIC
# MAGIC **Key concepts:** Tracking URI, Databricks config, trace ingestion.
