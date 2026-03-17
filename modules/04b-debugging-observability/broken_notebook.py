# Databricks notebook source
# MAGIC %md
# MAGIC # Broken Notebook - Debugging Exercise
# MAGIC ## Module 4B: 4 Complex Bugs for Genie Code Debugging
# MAGIC
# MAGIC This notebook contains **4 intentional bugs**. Use Genie Code to find and fix each one.
# MAGIC
# MAGIC **Catalog/Schema:** `main.sourabh_energy_workshop`. Tables: `raw_customers`, `raw_meter_readings`, `raw_billing`, `raw_outages`, `raw_weather`, `raw_equipment`, `raw_demand_response`.
# MAGIC
# MAGIC | Bug | Location | Description |
# MAGIC |-----|----------|-------------|
# MAGIC | 1 | Cell 3 → Cell 5 | Schema change: column renamed mid-pipeline |
# MAGIC | 2 | Cell 6 | Slow aggregation: full table scan without partition pruning |
# MAGIC | 3 | Cell 8 | Library conflict: prophet import/version mismatch |
# MAGIC | 4 | Cell 10 | Wrong churn scoring: incorrect column for threshold |

# COMMAND ----------

# MAGIC %md
# MAGIC ## Cell 1: Load Customers
# MAGIC
# MAGIC Load raw customers. No bug here.

# COMMAND ----------

customers_df = spark.table("main.sourabh_energy_workshop.raw_customers")
customers_df.display()

# COMMAND ----------

# MAGIC %md
# MAGIC ## Cell 2: Load Meter Readings
# MAGIC
# MAGIC Load raw meter readings. No bug here.

# COMMAND ----------

meter_readings_df = spark.table("main.sourabh_energy_workshop.raw_meter_readings")
meter_readings_df.display()

# COMMAND ----------

# MAGIC %md
# MAGIC ## Cell 3: Join and Rename Column (BUG 1 - Schema Change)
# MAGIC
# MAGIC **Bug 1:** This cell renames `account_id` to `cust_id` in the joined dataframe. Cell 5 still expects `account_id` and will fail with "cannot resolve 'account_id'".

# COMMAND ----------

from pyspark.sql import functions as F

# BUG 1: Renaming account_id to cust_id - downstream cell 5 expects account_id
customers_meters_df = (
    customers_df
    .join(meter_readings_df, customers_df.account_id == meter_readings_df.customer_id, "inner")
    .select(
        customers_df.account_id.alias("cust_id"),  # Renamed! Cell 5 uses account_id
        "customer_name",
        "customer_type",
        "kwh_consumed",
        "timestamp"
    )
)
customers_meters_df.display()

# COMMAND ----------

# MAGIC %md
# MAGIC ## Cell 4: Aggregate by Segment
# MAGIC
# MAGIC Uses cust_id (works with Cell 3 output). No bug here.

# COMMAND ----------

type_summary = (
    customers_meters_df
    .groupBy("customer_type")
    .agg(
        F.count("cust_id").alias("customer_count"),
        F.sum("kwh_consumed").alias("total_kwh")
    )
)
type_summary.display()

# COMMAND ----------

# MAGIC %md
# MAGIC ## Cell 5: Filter High-Value Customers (FAILS - BUG 1)
# MAGIC
# MAGIC **Bug 1 manifests here:** References `account_id` which was renamed to `cust_id` in Cell 3. This will raise: `AnalysisException: cannot resolve 'account_id'`.

# COMMAND ----------

# BUG 1: account_id was renamed to cust_id in cell 3 - this will fail
high_value = customers_meters_df.filter(F.col("account_id").isNotNull())  # Wrong column: should be cust_id
high_value.display()

# COMMAND ----------

# MAGIC %md
# MAGIC ## Cell 6: Daily Aggregation (BUG 2 - Slow, No Partition Pruning)
# MAGIC
# MAGIC **Bug 2:** Full table scan on `raw_meter_readings` without filtering on `reading_date`. If the table is partitioned by `reading_date`, this query ignores partition pruning and scans the entire table.

# COMMAND ----------

# BUG 2: No partition filter - full table scan on raw_meter_readings (10M+ rows)
# Should add: .filter(F.col("timestamp") >= "2025-03-01") or similar to limit scan
daily_totals = (
    spark.table("main.sourabh_energy_workshop.raw_meter_readings")
    .withColumn("reading_date", F.to_date("timestamp"))
    .groupBy("reading_date")
    .agg(F.sum("kwh_consumed").alias("daily_kwh"))
    .orderBy("reading_date")
)
daily_totals.display()

# COMMAND ----------

# MAGIC %md
# MAGIC ## Cell 7: Prepare for Forecasting
# MAGIC
# MAGIC Prepare time series data. No bug here (unless prophet fails in Cell 8).

# COMMAND ----------

ts_pdf = daily_totals.select(F.col("reading_date").alias("ds"), F.col("daily_kwh").alias("y")).toPandas()
print(ts_pdf.head(10))

# COMMAND ----------

# MAGIC %md
# MAGIC ## Cell 8: Prophet Import (BUG 3 - Library Conflict)
# MAGIC
# MAGIC **Bug 3:** Tries to import `Prophet` from `prophet`. In prophet 1.x the class is `Prophet`, but in prophet 2.x it may be `prophet.Prophet` or the API changed. This can cause `ImportError` or `AttributeError` depending on installed version.

# COMMAND ----------

# BUG 3: Prophet import - may fail with version conflict
# prophet 1.0: from prophet import Prophet
# prophet 2.x: different import path or API
from prophet import Prophet  # May fail: ImportError or wrong API

model = Prophet()
model.fit(ts_pdf)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Cell 9: Churn Scoring Setup
# MAGIC
# MAGIC Create a dataframe with churn_probability and risk_score. No bug here.

# COMMAND ----------

# Simulated churn scores - churn_probability is 0-1, risk_score is 1-10
churn_df = (
    customers_df
    .withColumn("churn_probability", F.rand())
    .withColumn("risk_score", F.floor(F.rand() * 10 + 1).cast("int"))
)
churn_df.display()

# COMMAND ----------

# MAGIC %md
# MAGIC ## Cell 10: Flag At-Risk Customers (BUG 4 - Wrong Column)
# MAGIC
# MAGIC **Bug 4:** Churn threshold should use `churn_probability` (0-1 scale). This cell incorrectly uses `risk_score` (1-10 scale) with threshold 0.5, so almost no customers are flagged.

# COMMAND ----------

# BUG 4: Should use churn_probability for threshold, not risk_score
# risk_score is 1-10; churn_probability is 0-1. Threshold 0.5 makes sense for churn_probability only.
CHURN_THRESHOLD = 0.5
at_risk = churn_df.filter(F.col("risk_score") > CHURN_THRESHOLD)  # Wrong! Should be churn_probability
at_risk.display()
