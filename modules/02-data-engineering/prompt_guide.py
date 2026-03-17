# Databricks notebook source
# MAGIC %md
# MAGIC # Data Engineering Prompt Guide
# MAGIC ## Genie Code Agent in Lakeflow Pipelines Editor - Module 2
# MAGIC
# MAGIC This notebook provides **exact prompts** to use when working with the Genie Code Agent in the Lakeflow Pipelines Editor. Copy and paste these prompts to build a medallion architecture for energy data.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Introduction: Medallion Architecture Goal
# MAGIC
# MAGIC Our goal is to build a **medallion architecture** (bronze → silver → gold) for the SmartGrid energy data:
# MAGIC - **Bronze:** Raw data ingestion with schema enforcement
# MAGIC - **Silver:** Cleaned, deduplicated, and conformed data
# MAGIC - **Gold:** Business-level aggregations and analytics tables
# MAGIC
# MAGIC All tables live in `main.sourabh_energy_workshop`. Source tables: `raw_customers`, `raw_meter_readings`, `raw_billing`, `raw_outages`, `raw_weather`, `raw_equipment`, `raw_demand_response`.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Prompt 1: Build Medallion Pipeline
# MAGIC
# MAGIC **When to use:** When starting a new Lakeflow pipeline or adding medallion layers.
# MAGIC
# MAGIC **Exact prompt to type:**

# COMMAND ----------

# MAGIC %md
# MAGIC ```
# MAGIC Build a medallion pipeline for energy data in main.sourabh_energy_workshop. Create:
# MAGIC
# MAGIC Bronze tables: Ingest raw_customers, raw_meter_readings, raw_billing, raw_outages, raw_weather, raw_equipment, raw_demand_response with schema enforcement.
# MAGIC
# MAGIC Silver tables: Clean and deduplicate each bronze table. Handle nulls, standardize date formats, and remove duplicates.
# MAGIC
# MAGIC Gold tables: Create gold_customer_summary (aggregate consumption by customer), gold_daily_consumption (daily totals), and gold_outage_summary (outage stats by region).
# MAGIC ```
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ### Expected Outcome
# MAGIC - **Bronze tables:** `bronze_customers`, `bronze_meter_readings`, `bronze_billing`, etc. with schema enforcement
# MAGIC - **Silver tables:** `silver_customers`, `silver_meter_readings`, etc. with cleaning and deduplication logic
# MAGIC - **Gold tables:** `gold_customer_summary`, `gold_daily_consumption`, `gold_outage_summary` with aggregations

# COMMAND ----------

# MAGIC %md
# MAGIC ## Prompt 2: Fix Pipeline Errors
# MAGIC
# MAGIC **When to use:** When the pipeline fails due to data quality issues (e.g., schema mismatch, null values, type errors).
# MAGIC
# MAGIC **Exact prompt to type:**

# COMMAND ----------

# MAGIC %md
# MAGIC ```
# MAGIC The pipeline is failing with a data quality error. The raw_meter_readings table has some rows where kwh_consumed is null or negative. Fix the silver_meter_readings transformation to:
# MAGIC 1. Filter out rows where kwh_consumed is null or <= 0
# MAGIC 2. Add a data quality check that raises a clear error if more than 5% of rows are invalid
# MAGIC ```
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ## Prompt 3: Explain the Pipeline End-to-End
# MAGIC
# MAGIC **When to use:** To understand the full data flow and validate the design.
# MAGIC
# MAGIC **Exact prompt to type:**

# COMMAND ----------

# MAGIC %md
# MAGIC ```
# MAGIC Explain this pipeline end-to-end. Walk me through the bronze, silver, and gold layers. What transformations are applied at each stage? How do the tables connect (keys, joins)? Are there any potential issues or optimizations?
# MAGIC ```
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ## Hands-On Exercise: Add gold_equipment_health Table
# MAGIC
# MAGIC **Your task:** Use Genie Code to add a new gold table for equipment health analytics.
# MAGIC
# MAGIC **Exact prompt to type:**

# COMMAND ----------

# MAGIC %md
# MAGIC ```
# MAGIC Add a gold_equipment_health table to the pipeline. It should aggregate equipment data from silver_equipment to show:
# MAGIC - Equipment ID
# MAGIC - Installation date
# MAGIC - Last maintenance date
# MAGIC - Count of associated outages
# MAGIC - Health score (you can derive a simple score based on age and outage count)
# MAGIC
# MAGIC Join with silver_outages where applicable. Output to main.sourabh_energy_workshop.gold_equipment_health.
# MAGIC ```
# MAGIC
