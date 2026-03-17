# Databricks notebook source
# MAGIC %md
# MAGIC # Energy Data Explorer
# MAGIC ## SmartGrid Analytics Platform - Module 1
# MAGIC
# MAGIC This notebook explores energy data from the SmartGrid Analytics Platform. You will work with customer data, meter readings, and billing information to understand consumption patterns.
# MAGIC
# MAGIC **Exercise Context:** Use Genie Code to find and fix the **3 intentional bugs** in this notebook. Each bug will cause an error when you run the cell—your job is to identify the issue and correct it with Genie Code assistance.

# COMMAND ----------

# MAGIC %md
# MAGIC ## 1. Load and Explore Customer Data
# MAGIC
# MAGIC Read the raw customers table and display summary statistics.

# COMMAND ----------

customers_df = spark.table("main.sourabh_energy_workshop.raw_customers")
customers_df.display()

# COMMAND ----------

customers_df.summary().display()

# COMMAND ----------

# MAGIC %md
# MAGIC ## 2. Analyze Meter Readings - Average Consumption
# MAGIC
# MAGIC Calculate the average energy consumption from meter readings.
# MAGIC
# MAGIC **Bug 1:** This cell uses a column name that does not exist in the schema. Can you find and fix it?

# COMMAND ----------

meter_readings_df = spark.table("main.sourabh_energy_workshop.raw_meter_readings")
avg_consumption = meter_readings_df.agg({"kwh_used": "avg"}).collect()[0][0]
print(f"Average consumption: {avg_consumption:.2f} kWh")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 3. Filter High-Consumption Readings
# MAGIC
# MAGIC Filter meter readings where consumption exceeds the average.
# MAGIC
# MAGIC **Bug 2:** This cell references `F.col` but the required import is missing. Add the import statement!

# COMMAND ----------

high_consumption_df = meter_readings_df.filter(F.col("kwh_consumed") > avg_consumption)
high_consumption_df.display()

# COMMAND ----------

# MAGIC %md
# MAGIC ## 4. Join Customers with Billing Data
# MAGIC
# MAGIC Enrich billing records with customer information for analysis.
# MAGIC
# MAGIC **Bug 3:** The join condition uses the wrong columns. Customers have `account_id` and billing has `customer_id` -- they should match on those identifiers, not on `customer_name`!

# COMMAND ----------

billing_df = spark.table("main.sourabh_energy_workshop.raw_billing")
customers_billing_df = customers_df.join(billing_df, customers_df.customer_name == billing_df.customer_id, "inner")
customers_billing_df.display()

# COMMAND ----------

# MAGIC %md
# MAGIC ## 5. Visualization - Consumption by Customer Segment
# MAGIC
# MAGIC Create a simple bar chart showing average consumption by customer segment.

# COMMAND ----------

from pyspark.sql import functions as F

summary_by_type = (
    customers_billing_df
    .groupBy("customer_type")
    .agg(F.avg("amount_charged").alias("avg_amount_charged"))
)
summary_by_type.display()
