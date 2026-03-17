# Databricks notebook source
# MAGIC %md
# MAGIC # Debugging & Observability Prompt Guide
# MAGIC ## Cross-Surface Debugging with Genie Code - Module 4B
# MAGIC
# MAGIC This notebook provides prompts and pre-built queries for debugging across **Notebooks**, **SQL Editor**, and **Lakeflow Pipelines**. Use Genie Code to diagnose runtime errors, performance issues, and pipeline failures.
# MAGIC
# MAGIC **Catalog/Schema:** All table references use `main.sourabh_energy_workshop`. Tables: `raw_customers`, `raw_meter_readings`, `raw_billing`, `raw_outages`, `raw_weather`, `raw_equipment`, `raw_demand_response`.
# MAGIC
# MAGIC **Broken artifacts:** See `broken_notebook.py` for a notebook with 4 complex bugs. Broken SQL queries are included in Section B.

# COMMAND ----------

# MAGIC %md
# MAGIC ---
# MAGIC # Section A: Notebook Debugging Scenarios
# MAGIC ---

# COMMAND ----------

# MAGIC %md
# MAGIC ## A1: Runtime Error Chain
# MAGIC
# MAGIC **When to use:** When a cell fails and the error references another cell or upstream data.
# MAGIC
# MAGIC **Exact prompt to type:**

# COMMAND ----------

# MAGIC %md
# MAGIC ```
# MAGIC Cell 5 is failing with "AnalysisException: cannot resolve 'customer_id' given input columns". The error says the column doesn't exist. Trace back: which cell creates or modifies the dataframe used in cell 5? Did a schema change in cell 3 rename or drop customer_id? Help me fix the error chain.
# MAGIC ```
# MAGIC
# MAGIC **Expected behavior:** Genie Code traces the data flow, identifies the schema change in cell 3, and suggests aligning column names or updating cell 5 to use the correct column.
# MAGIC
# MAGIC **Key concepts:** Error propagation, schema evolution, cell dependencies.

# COMMAND ----------

# MAGIC %md
# MAGIC ## A2: Performance Debugging
# MAGIC
# MAGIC **When to use:** When a cell or query runs very slowly.
# MAGIC
# MAGIC **Exact prompt to type:**

# COMMAND ----------

# MAGIC %md
# MAGIC ```
# MAGIC This aggregation on raw_meter_readings is taking 10+ minutes. The table is partitioned by reading_date. Help me: 1) Check if the query uses partition pruning, 2) Suggest adding a filter on reading_date to limit the scan, 3) Recommend indexes or Z-ordering if applicable.
# MAGIC ```
# MAGIC
# MAGIC **Expected behavior:** Genie Code analyzes the query, identifies full table scan, and suggests partition filters or optimizations.
# MAGIC
# MAGIC **Key concepts:** Partition pruning, predicate pushdown, query optimization.

# COMMAND ----------

# MAGIC %md
# MAGIC ## A3: Environment / Library Debugging
# MAGIC
# MAGIC **When to use:** When imports fail or library versions conflict.
# MAGIC
# MAGIC **Exact prompt to type:**

# COMMAND ----------

# MAGIC %md
# MAGIC ```
# MAGIC I'm getting "ImportError: cannot import name 'Prophet' from 'prophet'" or a version conflict. The cluster has prophet 1.0 but my code expects a different API. Help me: 1) Check installed prophet version, 2) Fix the import or use the correct API for this version, 3) Or suggest using a different library if prophet is incompatible.
# MAGIC ```
# MAGIC
# MAGIC **Expected behavior:** Genie Code checks the environment, identifies the version mismatch, and suggests code changes or alternative approaches.
# MAGIC
# MAGIC **Key concepts:** Library versions, import errors, environment isolation.

# COMMAND ----------

# MAGIC %md
# MAGIC ## A4: Step-Through Debugging
# MAGIC
# MAGIC **When to use:** When logic is wrong but no exception is raised.
# MAGIC
# MAGIC **Exact prompt to type:**

# COMMAND ----------

# MAGIC %md
# MAGIC ```
# MAGIC The churn scoring logic in this cell is wrong—it's flagging the wrong customers. The threshold comparison uses the wrong column (it should use churn_probability, not risk_score). Help me step through the logic, identify the bug, and fix the comparison.
# MAGIC ```
# MAGIC
# MAGIC **Expected behavior:** Genie Code traces the logic, finds the incorrect column reference, and corrects the threshold comparison.
# MAGIC
# MAGIC **Key concepts:** Logic debugging, column semantics, business rule validation.

# COMMAND ----------

# MAGIC %md
# MAGIC ---
# MAGIC # Section B: SQL Editor Debugging
# MAGIC ---

# COMMAND ----------

# MAGIC %md
# MAGIC ## B1: Broken Query - Syntax / Schema
# MAGIC
# MAGIC **Broken SQL (intentional errors):**

# COMMAND ----------

# MAGIC %md
# MAGIC ```sql
# MAGIC -- BROKEN: Column kwh_used does not exist (correct: kwh_consumed)
# MAGIC SELECT customer_id, SUM(kwh_used) AS total_kwh
# MAGIC FROM main.sourabh_energy_workshop.raw_meter_readings
# MAGIC GROUP BY customer_id;
# MAGIC ```
# MAGIC
# MAGIC **Exact prompt to type:**

# COMMAND ----------

# MAGIC %md
# MAGIC ```
# MAGIC This SQL fails with "cannot resolve 'kwh_used'". The table is main.sourabh_energy_workshop.raw_meter_readings. Help me find the correct column name and fix the query.
# MAGIC ```
# MAGIC
# MAGIC **Expected behavior:** Genie Code suggests using `kwh_consumed` instead of `kwh_used`.

# COMMAND ----------

# MAGIC %md
# MAGIC ## B2: Broken Query - Join Key
# MAGIC
# MAGIC **Broken SQL (intentional error):**

# COMMAND ----------

# MAGIC %md
# MAGIC ```sql
# MAGIC -- BROKEN: Joining on customer_name instead of customer_id
# MAGIC SELECT c.customer_id, c.customer_name, SUM(b.amount_due) AS total_due
# MAGIC FROM main.sourabh_energy_workshop.raw_customers c
# MAGIC JOIN main.sourabh_energy_workshop.raw_billing b ON c.customer_name = b.customer_name
# MAGIC GROUP BY c.customer_id, c.customer_name;
# MAGIC ```
# MAGIC
# MAGIC **Exact prompt to type:**

# COMMAND ----------

# MAGIC %md
# MAGIC ```
# MAGIC This join might produce wrong results—customers and billing should be joined on account/customer ID, not name. Fix the join condition for main.sourabh_energy_workshop.raw_customers and raw_billing.
# MAGIC ```
# MAGIC
# MAGIC **Expected behavior:** Genie Code changes the join to use `customer_id` or equivalent key.

# COMMAND ----------

# MAGIC %md
# MAGIC ## B3: Performance Profiling
# MAGIC
# MAGIC **Exact prompt to type:**

# COMMAND ----------

# MAGIC %md
# MAGIC ```
# MAGIC This query on main.sourabh_energy_workshop.raw_meter_readings is slow. Help me profile it: enable query profiling, check for full table scans, and suggest adding a date filter or partition predicate.
# MAGIC ```
# MAGIC
# MAGIC **Expected behavior:** Genie Code explains how to use the Query Profile, identifies bottlenecks, and suggests optimizations.

# COMMAND ----------

# MAGIC %md
# MAGIC ---
# MAGIC # Section C: Lakeflow Pipeline Debugging
# MAGIC ---

# COMMAND ----------

# MAGIC %md
# MAGIC ## C1: Failure Diagnosis
# MAGIC
# MAGIC **Exact prompt to type:**

# COMMAND ----------

# MAGIC %md
# MAGIC ```
# MAGIC My Lakeflow pipeline failed. How do I diagnose the failure? Walk me through: 1) Where to find the error in the UI, 2) How to read the event logs, 3) Which system tables to query for run history and error details.
# MAGIC ```
# MAGIC
# MAGIC **Expected behavior:** Genie Code explains the pipeline run UI, event log structure, and system table queries.

# COMMAND ----------

# MAGIC %md
# MAGIC ## C2: Event Logs and System Tables
# MAGIC
# MAGIC **Exact prompt to type:**

# COMMAND ----------

# MAGIC %md
# MAGIC ```
# MAGIC Query system tables to show recent Lakeflow pipeline runs, their status, duration, and any failure messages. Use system.lakeflow tables.
# MAGIC ```
# MAGIC
# MAGIC **Expected behavior:** Genie Code provides or refines SQL against `system.lakeflow.*` tables.

# COMMAND ----------

# MAGIC %md
# MAGIC ## C3: Matrix / Gantt Views
# MAGIC
# MAGIC **Exact prompt to type:**

# COMMAND ----------

# MAGIC %md
# MAGIC ```
# MAGIC How do I use the matrix or Gantt view in Lakeflow to understand task dependencies and identify which task is the bottleneck?
# MAGIC ```
# MAGIC
# MAGIC **Expected behavior:** Genie Code explains matrix/Gantt views and how to interpret task timelines.

# COMMAND ----------

# MAGIC %md
# MAGIC ---
# MAGIC # Pre-Built SQL Queries for System Tables
# MAGIC ---
# MAGIC
# MAGIC Use these queries to inspect Lakeflow pipeline runs. Run them in SQL Editor or a notebook.

# COMMAND ----------

# MAGIC %md
# MAGIC ### Query 1: Job Run Timeline
# MAGIC
# MAGIC Lists recent Lakeflow job runs with status and timing.

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Job run timeline (replace pipeline_id if needed)
# MAGIC SELECT
# MAGIC   job_id,
# MAGIC   run_id,
# MAGIC   state,
# MAGIC   start_time,
# MAGIC   end_time,
# MAGIC   DATEDIFF('second', start_time, end_time) AS duration_seconds,
# MAGIC   failure_message
# MAGIC FROM system.lakeflow.job_run_timeline
# MAGIC ORDER BY start_time DESC
# MAGIC LIMIT 50;

# COMMAND ----------

# MAGIC %md
# MAGIC ### Query 2: Failed Runs with Error Details
# MAGIC
# MAGIC Filters for failed runs and shows failure info.

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Failed runs with error details
# MAGIC SELECT
# MAGIC   job_id,
# MAGIC   run_id,
# MAGIC   state,
# MAGIC   start_time,
# MAGIC   failure_message,
# MAGIC   error_details
# MAGIC FROM system.lakeflow.job_run_timeline
# MAGIC WHERE state = 'FAILED'
# MAGIC ORDER BY start_time DESC
# MAGIC LIMIT 20;

# COMMAND ----------

# MAGIC %md
# MAGIC ### Query 3: Task-Level Run History
# MAGIC
# MAGIC Task-level view for pipeline runs (schema may vary by workspace).

# COMMAND ----------

# MAGIC %md
# MAGIC ```sql
# MAGIC -- Task-level run history (adjust table name if your workspace uses different system tables)
# MAGIC SELECT
# MAGIC   job_id,
# MAGIC   run_id,
# MAGIC   task_key,
# MAGIC   state,
# MAGIC   start_time,
# MAGIC   end_time,
# MAGIC   duration_ms
# MAGIC FROM system.lakeflow.task_run_timeline
# MAGIC WHERE run_id = '<your_run_id>'
# MAGIC ORDER BY start_time;
# MAGIC ```
# MAGIC
# MAGIC **Note:** Table names like `system.lakeflow.job_run_timeline` and `system.lakeflow.task_run_timeline` may vary. Check your workspace's system table documentation.

# COMMAND ----------

# MAGIC %md
# MAGIC ### Query 4: Pipeline Event Logs
# MAGIC
# MAGIC Event-level logs for debugging pipeline behavior.

# COMMAND ----------

# MAGIC %md
# MAGIC ```sql
# MAGIC -- Pipeline event logs
# MAGIC SELECT
# MAGIC   event_time,
# MAGIC   pipeline_id,
# MAGIC   run_id,
# MAGIC   event_type,
# MAGIC   message,
# MAGIC   details
# MAGIC FROM system.lakeflow.pipeline_events
# MAGIC WHERE run_id = '<your_run_id>'
# MAGIC ORDER BY event_time;
# MAGIC ```
# MAGIC
# MAGIC **Reference:** Use `broken_notebook.py` in this folder for hands-on debugging exercises with 4 complex bugs.
