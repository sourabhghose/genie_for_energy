# Databricks notebook source
# MAGIC %md
# MAGIC # Data Science Prompt Guide
# MAGIC ## Genie Code Agent in Databricks Notebooks - Module 3
# MAGIC
# MAGIC This notebook provides **exact prompts** for using the Genie Code Agent to build ML models for the SmartGrid energy use case. Tables: `main.sourabh_energy_workshop.*` (raw_customers, raw_meter_readings, raw_billing, raw_outages, raw_weather, raw_equipment, raw_demand_response).

# COMMAND ----------

# MAGIC %md
# MAGIC ---
# MAGIC # Part A: Customer Segmentation (25 min)
# MAGIC ---

# COMMAND ----------

# MAGIC %md
# MAGIC ## Context
# MAGIC
# MAGIC Segment customers based on consumption patterns, billing behavior, and demographics. Use clustering (e.g., K-Means) to identify distinct customer segments for targeted programs.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Exact Prompt

# COMMAND ----------

# MAGIC %md
# MAGIC ```
# MAGIC Using tables in main.sourabh_energy_workshop, build a customer segmentation model. Join raw_customers with raw_meter_readings and raw_billing to create features: average monthly consumption, total amount due, payment frequency, and customer_type. Use K-Means clustering with k=4 to segment customers. Save the model to MLflow and display the segment distribution with a bar chart.
# MAGIC ```
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ### Expected Behavior
# MAGIC - Genie Code generates feature engineering code (joins, aggregations)
# MAGIC - Fits a K-Means model (or similar) with 4 clusters
# MAGIC - Logs model to MLflow
# MAGIC - Produces a visualization of segment counts

# COMMAND ----------

# MAGIC %md
# MAGIC ### Follow-Up Prompts

# COMMAND ----------

# MAGIC %md
# MAGIC ```
# MAGIC Add silhouette score evaluation and suggest the optimal number of clusters (try k=3 to k=6).
# MAGIC ```
# MAGIC
# MAGIC ```
# MAGIC Create a profile for each segment: what are the typical consumption and billing characteristics of each cluster?
# MAGIC ```
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ---
# MAGIC # Part B: Demand Forecasting (20 min)
# MAGIC ---

# COMMAND ----------

# MAGIC %md
# MAGIC ## Context
# MAGIC
# MAGIC Forecast future energy demand using historical meter readings and weather data. Use a time-series approach (e.g., Prophet, ARIMA, or simple regression with lag features).

# COMMAND ----------

# MAGIC %md
# MAGIC ## Exact Prompt

# COMMAND ----------

# MAGIC %md
# MAGIC ```
# MAGIC Build a demand forecasting model using main.sourabh_energy_workshop.raw_meter_readings and main.sourabh_energy_workshop.raw_weather. Aggregate meter readings to daily totals by date. Join with weather (temperature, etc.). Train a forecasting model (Prophet or sklearn with lag features) to predict next 7 days of consumption. Log to MLflow and plot actual vs predicted.
# MAGIC ```
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ### Expected Behavior
# MAGIC - Daily aggregation of kwh_consumed
# MAGIC - Join with weather on date
# MAGIC - Model training and MLflow logging
# MAGIC - Forecast visualization

# COMMAND ----------

# MAGIC %md
# MAGIC ### Follow-Up Prompts

# COMMAND ----------

# MAGIC %md
# MAGIC ```
# MAGIC Add MAPE and RMSE evaluation metrics. How accurate is the model?
# MAGIC ```
# MAGIC
# MAGIC ```
# MAGIC Extend the forecast to 30 days and add a confidence interval.
# MAGIC ```
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ---
# MAGIC # Part C: Churn Prediction (15 min)
# MAGIC ---

# COMMAND ----------

# MAGIC %md
# MAGIC ## Context
# MAGIC
# MAGIC Predict which customers are at risk of churning (e.g., switching providers or disconnecting). Use billing, outage, and consumption data to build a binary classification model.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Exact Prompt

# COMMAND ----------

# MAGIC %md
# MAGIC ```
# MAGIC Build a churn prediction model. Define churn as: customers with 2+ late payments in the last 6 months OR 3+ outages in the last 3 months. Use raw_customers, raw_billing, raw_outages, and raw_meter_readings from main.sourabh_energy_workshop. Create features: payment history, outage count, consumption trend, customer tenure. Train a binary classifier (LogisticRegression or XGBoost). Log to MLflow, show feature importance, and display a confusion matrix.
# MAGIC ```
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ### Expected Behavior
# MAGIC - Churn label definition and feature engineering
# MAGIC - Binary classifier training
# MAGIC - MLflow logging, feature importance, confusion matrix

# COMMAND ----------

# MAGIC %md
# MAGIC ### Follow-Up Prompts

# COMMAND ----------

# MAGIC %md
# MAGIC ```
# MAGIC The dataset is imbalanced. Apply SMOTE or class weights to improve recall for the churn class.
# MAGIC ```
# MAGIC
# MAGIC ```
# MAGIC Deploy this model as a Databricks Model Serving endpoint for real-time churn scoring.
# MAGIC ```
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ---
# MAGIC # Hands-On Exercise
# MAGIC ---

# COMMAND ----------

# MAGIC %md
# MAGIC **Your task:** Combine two or more of the above use cases into a single notebook.
# MAGIC
# MAGIC **Exact prompt to type:**

# COMMAND ----------

# MAGIC %md
# MAGIC ```
# MAGIC In this notebook, add a section that uses the customer segments from Part A to improve the demand forecast in Part B. For each segment, train a separate demand forecasting model and compare accuracy. Which segment is easiest to forecast? Create a summary table and visualization.
# MAGIC ```
# MAGIC
