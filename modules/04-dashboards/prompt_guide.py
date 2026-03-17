# Databricks notebook source
# MAGIC %md
# MAGIC # Dashboard Prompt Guide
# MAGIC ## Genie Code Agent in Lakeview - Module 4
# MAGIC
# MAGIC This notebook provides **exact prompts** to use when building the SmartGrid Operations Center dashboard with the Genie Code Agent in Lakeview. Copy and paste these prompts to create dashboards, add visualizations, and enable interactivity.
# MAGIC
# MAGIC **Catalog/Schema:** All table references use `main.sourabh_energy_workshop`. Tables: `raw_customers`, `raw_meter_readings`, `raw_billing`, `raw_outages`, `raw_weather`, `raw_equipment`, `raw_demand_response`.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Prompt 1: Create the SmartGrid Operations Center Dashboard
# MAGIC
# MAGIC **When to use:** When starting a new dashboard from scratch.
# MAGIC
# MAGIC **Exact prompt to type:**

# COMMAND ----------

# MAGIC %md
# MAGIC ```
# MAGIC Create a new Lakeview dashboard called "SmartGrid Operations Center" for the energy workshop. Use tables from main.sourabh_energy_workshop. Add an overview page with:
# MAGIC - Total customer count
# MAGIC - Total meter readings this month
# MAGIC - Average consumption (kWh)
# MAGIC - Count of active outages
# MAGIC Use cards or KPI widgets for these metrics.
# MAGIC ```
# MAGIC
# MAGIC **Expected behavior:** Genie Code creates a new dashboard with a single page containing 4 KPI/card widgets pulling from the specified tables.
# MAGIC
# MAGIC **Key concepts:** Dashboard creation, dataset binding, KPI widgets, table references with catalog.schema.table.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Prompt 2: Add Custom Calculation - Consumption Growth
# MAGIC
# MAGIC **When to use:** When you need a derived metric not in the source table.
# MAGIC
# MAGIC **Exact prompt to type:**

# COMMAND ----------

# MAGIC %md
# MAGIC ```
# MAGIC Add a custom calculation to the dashboard: "Month-over-month consumption growth %". Use raw_meter_readings from main.sourabh_energy_workshop. Compare current month total kwh_consumed to previous month. Formula: ((current - previous) / previous) * 100.
# MAGIC ```
# MAGIC
# MAGIC **Expected behavior:** Genie Code adds a calculated field or SQL expression for MoM growth and displays it as a KPI or in a table.
# MAGIC
# MAGIC **Key concepts:** Custom calculations, date filtering, aggregation, SQL expressions in Lakeview.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Prompt 3: Add Custom Calculation - Outage Duration
# MAGIC
# MAGIC **When to use:** When you need to compute duration or time-based metrics.
# MAGIC
# MAGIC **Exact prompt to type:**

# COMMAND ----------

# MAGIC %md
# MAGIC ```
# MAGIC Add a calculated field for average outage duration in hours. Use raw_outages from main.sourabh_energy_workshop. Compute duration as (end_time - start_time) in hours. Show the average across all outages.
# MAGIC ```
# MAGIC
# MAGIC **Expected behavior:** Genie Code creates a duration calculation and displays average outage hours.
# MAGIC
# MAGIC **Key concepts:** Date/time arithmetic, DATEDIFF or timestamp subtraction, aggregation.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Prompt 4: Add Time Series Visualization
# MAGIC
# MAGIC **When to use:** When you need to show trends over time.
# MAGIC
# MAGIC **Exact prompt to type:**

# COMMAND ----------

# MAGIC %md
# MAGIC ```
# MAGIC Add a line chart showing daily total consumption (kwh_consumed) over the last 90 days. Use raw_meter_readings from main.sourabh_energy_workshop. X-axis: date, Y-axis: sum of kwh_consumed. Title: "Daily Consumption Trend".
# MAGIC ```
# MAGIC
# MAGIC **Expected behavior:** Genie Code adds a line chart with date on X-axis and aggregated consumption on Y-axis.
# MAGIC
# MAGIC **Key concepts:** Time series charts, date aggregation, line charts.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Prompt 5: Add Bar Chart by Segment
# MAGIC
# MAGIC **When to use:** When you need to compare categories.
# MAGIC
# MAGIC **Exact prompt to type:**

# COMMAND ----------

# MAGIC %md
# MAGIC ```
# MAGIC Add a horizontal bar chart showing average consumption by customer_type. Use raw_customers joined with raw_meter_readings from main.sourabh_energy_workshop. Group by customer_type, aggregate avg(kwh_consumed). Title: "Consumption by Customer Type".
# MAGIC ```
# MAGIC
# MAGIC **Expected behavior:** Genie Code creates a bar chart with segments on one axis and average consumption on the other.
# MAGIC
# MAGIC **Key concepts:** Joins in datasets, group-by aggregation, bar charts.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Prompt 6: Add Cross-Filtering
# MAGIC
# MAGIC **When to use:** When you want widgets to filter each other.
# MAGIC
# MAGIC **Exact prompt to type:**

# COMMAND ----------

# MAGIC %md
# MAGIC ```
# MAGIC Enable cross-filtering on the SmartGrid Operations Center dashboard. When I click a state on the outage map or a segment on the bar chart, all other widgets should filter to that selection.
# MAGIC ```
# MAGIC
# MAGIC **Expected behavior:** Genie Code configures dashboard-level or page-level cross-filtering so selections propagate.
# MAGIC
# MAGIC **Key concepts:** Cross-filtering, dashboard parameters, linked filters.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Prompt 7: Add Parameter Dropdown
# MAGIC
# MAGIC **When to use:** When you need user-selectable filters.
# MAGIC
# MAGIC **Exact prompt to type:**

# COMMAND ----------

# MAGIC %md
# MAGIC ```
# MAGIC Add a dropdown parameter to filter the dashboard by state. Use the state column from raw_outages or raw_customers in main.sourabh_energy_workshop. Default to "All States". Apply this filter to all widgets on the page.
# MAGIC ```
# MAGIC
# MAGIC **Expected behavior:** Genie Code adds a parameter control and wires it to filter all visualizations.
# MAGIC
# MAGIC **Key concepts:** Parameters, dropdown filters, filter propagation.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Prompt 8: What-If Analysis - Rate Scenario
# MAGIC
# MAGIC **When to use:** When you need scenario-based revenue projections.
# MAGIC
# MAGIC **Exact prompt to type:**

# COMMAND ----------

# MAGIC %md
# MAGIC ```
# MAGIC Add a what-if widget: let me enter a hypothetical rate (AUD/kWh). Show projected revenue = sum(kwh_consumed) * rate from raw_meter_readings in main.sourabh_energy_workshop. Display the result as a KPI that updates when I change the rate.
# MAGIC ```
# MAGIC
# MAGIC **Expected behavior:** Genie Code adds an input parameter for rate and a calculated KPI for projected revenue.
# MAGIC
# MAGIC **Key concepts:** What-if parameters, calculated fields with parameters, dynamic KPI.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Prompt 9: What-If Analysis - Demand Response Impact
# MAGIC
# MAGIC **When to use:** When modeling demand response program impact.
# MAGIC
# MAGIC **Exact prompt to type:**

# COMMAND ----------

# MAGIC %md
# MAGIC ```
# MAGIC Add a what-if: if X% of customers participate in demand response and reduce consumption by Y%, what is the total kWh savings? Use raw_demand_response and raw_meter_readings from main.sourabh_energy_workshop. Add sliders for participation % and reduction %.
# MAGIC ```
# MAGIC
# MAGIC **Expected behavior:** Genie Code adds slider parameters and a calculated savings metric.
# MAGIC
# MAGIC **Key concepts:** Multi-parameter what-if, sliders, conditional calculations.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Prompt 10: What-If Analysis - Outage Threshold
# MAGIC
# MAGIC **When to use:** When modeling SLA or outage threshold scenarios.
# MAGIC
# MAGIC **Exact prompt to type:**

# COMMAND ----------

# MAGIC %md
# MAGIC ```
# MAGIC Add a what-if: show count of outages that exceed a user-specified duration threshold (in hours). Use raw_outages from main.sourabh_energy_workshop. Add a slider for threshold (1-24 hours). Display the count and % of total outages.
# MAGIC ```
# MAGIC
# MAGIC **Expected behavior:** Genie Code adds a duration slider and displays filtered outage count and percentage.
# MAGIC
# MAGIC **Key concepts:** Threshold filtering, parameterized filters, percentage calculations.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Prompt 11: Publish and Share Dashboard
# MAGIC
# MAGIC **When to use:** When ready to share the dashboard with stakeholders.
# MAGIC
# MAGIC **Exact prompt to type:**

# COMMAND ----------

# MAGIC %md
# MAGIC ```
# MAGIC How do I publish this dashboard and share it with my team? I want to give view-only access to specific users and optionally schedule a PDF export.
# MAGIC ```
# MAGIC
# MAGIC **Expected behavior:** Genie Code explains publishing steps, permissions, and scheduled export options.
# MAGIC
# MAGIC **Key concepts:** Dashboard permissions, sharing, scheduled reports, PDF export.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Prompt 12: Debug Dashboard - Fix Broken Widget
# MAGIC
# MAGIC **When to use:** When a widget shows an error or unexpected data.
# MAGIC
# MAGIC **Exact prompt to type:**

# COMMAND ----------

# MAGIC %md
# MAGIC ```
# MAGIC This widget shows "No data" or an error. The dataset uses raw_equipment from main.sourabh_energy_workshop. Help me debug: check if the table exists, the query is valid, and the filters aren't too restrictive.
# MAGIC ```
# MAGIC
# MAGIC **Expected behavior:** Genie Code walks through validation steps: table existence, query syntax, filter logic, and suggests fixes.
# MAGIC
# MAGIC **Key concepts:** Dashboard debugging, dataset validation, query troubleshooting.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Prompt 13: Map Visualization - Outage Locations
# MAGIC
# MAGIC **When to use:** When you need a geographic view of outages, customers, or equipment across Australia.
# MAGIC
# MAGIC **Exact prompt to type:**

# COMMAND ----------

# MAGIC %md
# MAGIC ```
# MAGIC Add a map visualization showing outage locations across Australia. Use raw_outages from main.sourabh_energy_workshop — it has latitude and longitude columns. Color-code markers by cause (weather, equipment_failure, vegetation, etc.). Size markers by affected_meters_count. Title: "Outage Map — Australia".
# MAGIC ```
# MAGIC
# MAGIC **Expected behavior:** Genie Code creates a map (scatter-on-map or marker map) using the lat/lon columns from raw_outages. Markers are colored by cause type and sized by impact.
# MAGIC
# MAGIC **Key concepts:** Map visualizations, latitude/longitude columns, color encoding, size encoding.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Prompt 14: Map Visualization - Customer Density
# MAGIC
# MAGIC **When to use:** When you want to see where customers are concentrated geographically.
# MAGIC
# MAGIC **Exact prompt to type:**

# COMMAND ----------

# MAGIC %md
# MAGIC ```
# MAGIC Add a customer density map showing where our 50K customers are located across Australia. Use raw_customers from main.sourabh_energy_workshop — it has latitude and longitude columns. Use a heatmap or cluster layer to show density. Add a filter for customer_type (residential, commercial, industrial).
# MAGIC ```
# MAGIC
# MAGIC **Expected behavior:** Genie Code creates a heatmap or clustered marker map of customer locations using lat/lon.
# MAGIC
# MAGIC **Key concepts:** Heatmap layers, geographic density, coordinate-based mapping.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Prompt 15: Map Visualization - Equipment & Outage Overlay
# MAGIC
# MAGIC **When to use:** When you want to correlate equipment locations with outage hotspots.
# MAGIC
# MAGIC **Exact prompt to type:**

# COMMAND ----------

# MAGIC %md
# MAGIC ```
# MAGIC Create a "Grid Infrastructure" map page. Plot equipment locations from raw_equipment (has latitude, longitude) colored by equipment_type, and overlay outage locations from raw_outages (also has latitude, longitude) colored by restoration_priority. Use main.sourabh_energy_workshop. Add filters for state and equipment_type.
# MAGIC ```
# MAGIC
# MAGIC **Expected behavior:** Genie Code creates a map page with two layers — equipment and outages — enabling spatial correlation analysis.
# MAGIC
# MAGIC **Key concepts:** Multi-layer maps, spatial overlay, infrastructure visualization.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Hands-On Exercise: Build Equipment Reliability Page
# MAGIC
# MAGIC **Your task:** Use Genie Code to add a new page to the SmartGrid Operations Center dashboard called "Equipment Reliability".
# MAGIC
# MAGIC **Exact prompt to type:**

# COMMAND ----------

# MAGIC %md
# MAGIC ```
# MAGIC Add a new page "Equipment Reliability" to the SmartGrid Operations Center dashboard. Use raw_equipment and raw_outages from main.sourabh_energy_workshop.
# MAGIC
# MAGIC Include:
# MAGIC 1. KPI: Total equipment count
# MAGIC 2. KPI: Equipment with outages in last 30 days
# MAGIC 3. Table: Equipment ID, type, installation_date, last_maintenance_date, outage_count (join with outages)
# MAGIC 4. Bar chart: Outage count by equipment type
# MAGIC 5. Line chart: Outages over time (last 90 days)
# MAGIC
# MAGIC Enable cross-filtering so clicking equipment type filters the table and charts.
# MAGIC ```
# MAGIC
# MAGIC **Expected behavior:** Genie Code creates the new page with all 5 widgets and configures cross-filtering.
# MAGIC
# MAGIC **Key concepts:** Multi-widget pages, joins across tables, cross-filtering, equipment analytics.
