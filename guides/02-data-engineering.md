# Module 2: Data Engineering with Lakeflow

**Duration:** 60 minutes  
**Catalog/Schema:** `main.sourabh_energy_workshop`

---

## Storyline

Our energy company ingests raw meter data, billing records, and weather data. We need a production pipeline that cleans, enriches, and aggregates this into analytics-ready tables.

---

## Data Context

| Table | Rows | Key Columns |
|-------|------|-------------|
| `raw_customers` | 50K | account_id, customer_name, region, customer_type, rate_plan, has_solar, has_ev |
| `raw_meter_readings` | 10.7M | meter_id, customer_id, timestamp, kwh_consumed, is_peak_hour |
| `raw_billing` | 600K | bill_id, customer_id, billing_period, total_kwh, amount_charged, is_delinquent |
| `raw_weather` | 1.8K | date, region, temp_high, temp_low, humidity, precipitation |
| `raw_equipment` | 2K | equipment_id, equipment_type, region, failure_count, current_load_pct |
| `raw_outages` | 5K | outage records by region |

**Regions:** Northeast, Southeast, Midwest, Southwest, Northwest

**Known data quality issues:**
- ~2% null meter readings
- ~0.1% negative values in consumption
- ~0.5% duplicate bills

---

## Step 1: Open Lakeflow Pipelines Editor (5 min)

1. In your Databricks workspace, go to **New** → **Pipeline** → **Lakeflow Declarative Pipeline**.
2. Name the pipeline: **SmartGrid Energy Pipeline**.
3. In the side panel, locate the **Genie Code** section and toggle **Agent mode ON**.
4. **Key concept:** Agent mode lets Genie Code create, edit, and run multiple pipeline files autonomously—you describe what you want, and it builds the pipeline.

---

## Step 2: Build the Medallion Pipeline (20 min)

### 2.1 Initial Prompt

Type this exact prompt into the Genie Code agent:

```
Build a medallion architecture pipeline for our energy data. Ingest raw_meter_readings, raw_customers, raw_billing, and raw_weather from main.sourabh_energy_workshop. Clean the data, handle nulls and duplicates, and create gold-layer aggregations for customer consumption profiles and regional grid load.
```

### 2.2 What to Watch For

Genie Code will create:

| Layer | Expected Tables | Purpose |
|-------|-----------------|---------|
| **Bronze** | `bronze_meter_readings`, `bronze_customers`, `bronze_billing`, `bronze_weather` | Schema enforcement, raw ingestion |
| **Silver** | `silver_meter_readings`, `silver_customers`, `silver_billing`, `silver_weather` | Cleaning, dedup, validation |
| **Gold** | `gold_customer_consumption`, `gold_regional_load`, `gold_billing_summary` | Aggregations for analytics |

**Silver layer specifics:**
- `silver_meter_readings`: nulls and negatives removed, deduplicated
- `silver_customers`: standardized region/customer_type
- `silver_billing`: deduplicated by bill_id, reconciled
- `silver_weather`: validated date/region ranges

**Gold layer specifics:**
- `gold_customer_consumption`: monthly profiles per customer
- `gold_regional_load`: hourly consumption by region
- `gold_billing_summary`: revenue metrics, payment stats

### 2.3 Review Generated Files

1. Open each generated transformation file (`.sql` or `.py`).
2. Ask Genie Code: **"Explain each transformation in this pipeline"**.
3. Verify joins and column mappings match the source schema.

### 2.4 Add Data Quality Expectations

Type:

```
Add data quality expectations: kwh_consumed >= 0, meter_id IS NOT NULL, no duplicate bill_ids
```

Genie Code should add `EXPECT` clauses or validation logic to enforce these rules.

### 2.5 Run the Pipeline

1. **Dry-run first:** Use the pipeline UI to run in validation/dry-run mode if available.
2. **Full refresh:** Run the pipeline with a full refresh.
3. Confirm all tables materialize successfully.

---

## Step 3: Debug a Pipeline Failure (10 min)

### 3.1 Introduce a Deliberate Error

Ask Genie Code:

```
Change the silver_billing table to reference a column called 'billing_amount' instead of 'amount_charged'
```

This will break the pipeline because `billing_amount` does not exist in the source.

### 3.2 Run and Observe Failure

1. Run the pipeline again.
2. Note the error message (e.g., column not found, schema mismatch).

### 3.3 Ask Genie Code to Fix

Type:

```
Fix the failure in this pipeline
```

**What to watch:** Genie Code should diagnose the error, identify the wrong column reference, and revert or correct it to use `amount_charged`.

---

## Step 4: Explain the Pipeline (5 min)

Ask:

```
Explain every step of this pipeline from bronze to gold
```

Review the explanation. Genie Code should walk through:
- Bronze: how each source is ingested
- Silver: cleaning rules, deduplication logic
- Gold: aggregation logic and business meaning

---

## Hands-on Exercise (20 min)

### Task

Add a new gold table `gold_equipment_health` that joins `raw_equipment` with `raw_outages` to create an equipment risk score.

### Prompt to Use

```
Add a gold table called gold_equipment_health that joins equipment data with outage data to calculate a risk score based on equipment age, failure count, current load percentage, and nearby outage frequency
```

**Source tables:** `main.sourabh_energy_workshop.raw_equipment`, `main.sourabh_energy_workshop.raw_outages`

### Expected Output Columns

| Column | Description |
|--------|-------------|
| `equipment_id` | From raw_equipment |
| `equipment_type` | From raw_equipment |
| `region` | From raw_equipment |
| `age_years` | Derived from install_date |
| `failure_count` | From raw_equipment |
| `current_load_pct` | From raw_equipment |
| `nearby_outage_count` | Count of outages in same region |
| `risk_score` | Composite score (e.g., weighted combination) |

### Tips

- If Genie Code's output differs slightly from expected, that's normal—it's non-deterministic. The important thing is the general approach: bronze/silver/gold, joins, and aggregation.
- You may need to clarify the join key between equipment and outages (e.g., region, or a spatial/temporal relationship).

---

## Summary

| Step | Time | Key Takeaway |
|------|------|--------------|
| 1 | 5 min | Genie Code Agent mode enables autonomous pipeline creation |
| 2 | 20 min | Medallion architecture: bronze → silver → gold with cleaning and aggregation |
| 3 | 10 min | Genie Code can diagnose and fix pipeline failures |
| 4 | 5 min | Natural language explanations for pipeline logic |
| Exercise | 20 min | Extend pipeline with new gold tables and joins |
