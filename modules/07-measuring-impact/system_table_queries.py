# Databricks notebook source
# MAGIC %md
# MAGIC # Measuring Genie Code Impact
# MAGIC ## Module 7: System Table Queries & Impact Dashboard
# MAGIC
# MAGIC This notebook contains **pre-built SQL queries** against `system.access.assistant_events` to measure Genie Code adoption and usage. Use these queries in SQL Editor or run them here to build your own impact dashboard.
# MAGIC
# MAGIC **Table:** `system.access.assistant_events` — each row is a message sent by a user in the Genie Code window or in-cell Assistant.
# MAGIC
# MAGIC **Schema columns:** `event_id`, `account_id`, `workspace_id`, `event_time`, `event_date`, `user_agent`, `initiated_by`

# COMMAND ----------

# MAGIC %md
# MAGIC ## Query 1: How Many Genie Code Interactions This Week?
# MAGIC
# MAGIC Total message count for the last 7 days.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT COUNT(*) AS interaction_count
# MAGIC FROM system.access.assistant_events
# MAGIC WHERE event_time >= current_timestamp() - INTERVAL 7 DAYS;

# COMMAND ----------

# MAGIC %md
# MAGIC ## Query 2: Top 10 Users by Interaction Count
# MAGIC
# MAGIC Most active Genie Code users in the last 30 days.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC   initiated_by AS user_email,
# MAGIC   COUNT(*) AS interaction_count
# MAGIC FROM system.access.assistant_events
# MAGIC WHERE event_time >= current_timestamp() - INTERVAL 30 DAYS
# MAGIC GROUP BY initiated_by
# MAGIC ORDER BY interaction_count DESC
# MAGIC LIMIT 10;

# COMMAND ----------

# MAGIC %md
# MAGIC ## Query 3: Daily Active User Trend
# MAGIC
# MAGIC Number of unique users per day over the last 30 days.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC   event_date,
# MAGIC   COUNT(DISTINCT initiated_by) AS daily_active_users,
# MAGIC   COUNT(*) AS total_interactions
# MAGIC FROM system.access.assistant_events
# MAGIC WHERE event_time >= current_timestamp() - INTERVAL 30 DAYS
# MAGIC GROUP BY event_date
# MAGIC ORDER BY event_date;

# COMMAND ----------

# MAGIC %md
# MAGIC ## Query 4: Usage by Product Surface
# MAGIC
# MAGIC Genie Code events can originate from the Genie Code window or in-cell Assistant. The `user_agent` column indicates request origination. This query groups by workspace to show usage distribution; adjust if your schema includes a product surface column.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC   workspace_id,
# MAGIC   COUNT(*) AS interaction_count,
# MAGIC   COUNT(DISTINCT initiated_by) AS unique_users
# MAGIC FROM system.access.assistant_events
# MAGIC WHERE event_time >= current_timestamp() - INTERVAL 30 DAYS
# MAGIC GROUP BY workspace_id
# MAGIC ORDER BY interaction_count DESC;

# COMMAND ----------

# MAGIC %md
# MAGIC ### Alternative: Usage by Workspace (for multi-workspace accounts)
# MAGIC
# MAGIC If you have multiple workspaces, use the query above. For a single workspace, use Query 1–3. If `system.access.assistant_events` adds a `product_surface` or `context` column in the future, update this query to group by that column.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Query 5: Hourly Interaction Pattern (Python + SQL)
# MAGIC
# MAGIC Use Python to run the query and visualize hourly patterns.

# COMMAND ----------

df = spark.sql("""
  SELECT
    date_trunc('hour', event_time) AS hour,
    COUNT(*) AS interactions
  FROM system.access.assistant_events
  WHERE event_time >= current_timestamp() - INTERVAL 7 DAYS
  GROUP BY date_trunc('hour', event_time)
  ORDER BY hour
""")
display(df)

# COMMAND ----------

# MAGIC %md
# MAGIC ---
# MAGIC # Import Pre-Built Impact Dashboard
# MAGIC ---

# COMMAND ----------

# MAGIC %md
# MAGIC ## Instructions for Importing the Genie Code Impact Dashboard
# MAGIC
# MAGIC Databricks provides a pre-built **Assistant usage dashboard** that visualizes Genie Code adoption using `system.access.assistant_events`. The dashboard includes:
# MAGIC
# MAGIC - **Submission data:** Per workspace and total
# MAGIC - **Top users overall**
# MAGIC - **Active users per workspace**
# MAGIC - **Active users by day and month**
# MAGIC
# MAGIC ### Steps to Import
# MAGIC
# MAGIC 1. **Download the dashboard file** from GitHub:
# MAGIC    - Navigate to: [Databricks TMM - Assistant Events Dashboard](https://github.com/databricks/tmm/tree/main/System-Tables-Demo/Assistant-Events)
# MAGIC    - Download the JSON dashboard file
# MAGIC
# MAGIC 2. **Import into your workspace:**
# MAGIC    - Go to **Dashboards** in the Databricks workspace
# MAGIC    - Click **Create** → **Import dashboard**
# MAGIC    - Select the downloaded JSON file
# MAGIC    - Configure the SQL warehouse/data source if prompted
# MAGIC    - Save the dashboard
# MAGIC
# MAGIC 3. **Verify data source:** Ensure the dashboard's datasets point to `system.access.assistant_events` and that your workspace has access to this system table (Unity Catalog enabled, admin permissions).
# MAGIC
# MAGIC 4. **Customize:** Add the queries from this notebook as new widgets or pages to extend the dashboard with "Interactions this week," "Top 10 users," and "Daily active user trend."

# COMMAND ----------

# MAGIC %md
# MAGIC ---
# MAGIC # Survey Template Section
# MAGIC ---

# COMMAND ----------

# MAGIC %md
# MAGIC ## Genie Code Adoption Survey Template
# MAGIC
# MAGIC Use this template to collect qualitative feedback alongside system table metrics. Distribute to users who have used Genie Code.
# MAGIC
# MAGIC ### Survey Questions
# MAGIC
# MAGIC 1. **Frequency:** How often do you use Genie Code? (Daily / Weekly / Monthly / Rarely)
# MAGIC
# MAGIC 2. **Primary use case:** Where do you use Genie Code most? (Notebooks / SQL Editor / Lakeflow Pipelines / Dashboards / Other)
# MAGIC
# MAGIC 3. **Productivity impact:** On a scale of 1–5, how much has Genie Code improved your productivity? (1 = Not at all, 5 = Significantly)
# MAGIC
# MAGIC 4. **Time saved:** Roughly how much time do you save per week using Genie Code? (None / 1–2 hours / 3–5 hours / 5+ hours)
# MAGIC
# MAGIC 5. **Quality:** How would you rate the quality of Genie Code's suggestions? (Poor / Fair / Good / Excellent)
# MAGIC
# MAGIC 6. **Blockers:** What prevents you from using Genie Code more often? (Open text)
# MAGIC
# MAGIC 7. **Feature requests:** What would make Genie Code more useful for you? (Open text)
# MAGIC
# MAGIC ### How to Use
# MAGIC
# MAGIC - Create a Google Form or similar survey with these questions
# MAGIC - Send to your team after a pilot period (e.g., 4–6 weeks)
# MAGIC - Correlate survey responses with `initiated_by` and interaction counts from `system.access.assistant_events` to identify power users vs. occasional users
# MAGIC - Use feedback to prioritize training, documentation, and feature adoption
