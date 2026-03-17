# Databricks notebook source
# MAGIC %md
# MAGIC # SmartGrid Analytics Platform -- Data Generation
# MAGIC Generates 7 synthetic energy tables for the Genie Code Workshop.
# MAGIC Run this notebook once during workshop setup.

# COMMAND ----------

# MAGIC %pip install faker
# MAGIC %restart_python

# COMMAND ----------

import random, math
from datetime import datetime, timedelta
from faker import Faker
from pyspark.sql import functions as F
from pyspark.sql.types import *

fake = Faker()
Faker.seed(42)
random.seed(42)

CATALOG = "main"
SCHEMA = "sourabh_energy_workshop"

spark.sql(f"CREATE SCHEMA IF NOT EXISTS {CATALOG}.{SCHEMA}")
spark.sql(f"USE CATALOG {CATALOG}")
spark.sql(f"USE SCHEMA {SCHEMA}")

REGIONS = ["Northeast", "Southeast", "Midwest", "Southwest", "Northwest"]
CUSTOMER_TYPES = ["residential", "commercial", "industrial"]
RATE_PLANS = ["fixed", "variable", "TOU", "EV"]

print(f"Target: {CATALOG}.{SCHEMA}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Table 1: raw_customers (~50K)

# COMMAND ----------

NUM_CUSTOMERS = 50000

def gen_customers():
    rows = []
    ct_weights = [0.75, 0.20, 0.05]
    rp_weights = [0.35, 0.25, 0.30, 0.10]
    for i in range(NUM_CUSTOMERS):
        ctype = random.choices(CUSTOMER_TYPES, ct_weights)[0]
        region = random.choice(REGIONS)
        signup = fake.date_between(start_date="-10y", end_date="-6m")
        contract_end = signup + timedelta(days=random.choice([365, 730, 1095]))
        has_solar = random.random() < (0.15 if region in ["Southwest", "Southeast"] else 0.05)
        has_ev = random.random() < (0.12 if ctype == "residential" else 0.03)
        rows.append((
            f"ACCT-{i+1:06d}", fake.name(), fake.street_address(), fake.city(),
            fake.state_abbr(), fake.zipcode(), region, ctype,
            random.choices(RATE_PLANS, rp_weights)[0],
            str(signup), str(contract_end), has_solar, has_ev, random.random() < 0.25,
        ))
    return rows

schema_cust = StructType([
    StructField("account_id", StringType()), StructField("customer_name", StringType()),
    StructField("street_address", StringType()), StructField("city", StringType()),
    StructField("state", StringType()), StructField("zipcode", StringType()),
    StructField("region", StringType()), StructField("customer_type", StringType()),
    StructField("rate_plan", StringType()), StructField("signup_date", StringType()),
    StructField("contract_end_date", StringType()), StructField("has_solar", BooleanType()),
    StructField("has_ev", BooleanType()), StructField("demand_response_enrolled", BooleanType()),
])

print("Generating 50K customers...")
df_cust = spark.createDataFrame(gen_customers(), schema=schema_cust)
df_cust = df_cust.withColumn("signup_date", F.col("signup_date").cast("date")).withColumn("contract_end_date", F.col("contract_end_date").cast("date"))
df_cust.write.mode("overwrite").saveAsTable("raw_customers")
print(f"  raw_customers: {spark.table('raw_customers').count():,} rows")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Table 2: raw_meter_readings (~2M)
# MAGIC Uses Spark-native generation for performance.

# COMMAND ----------

NUM_METERS = 5000
START_DATE = "2025-01-01"
END_DATE = "2025-03-31"

meter_base = spark.range(NUM_METERS).withColumn("meter_id", F.format_string("MTR-%06d", F.col("id") + 1))
meter_base = meter_base.withColumn("customer_id", F.format_string("ACCT-%06d", (F.rand(seed=42) * NUM_CUSTOMERS).cast("int") + 1))
ctype_expr = F.when(F.rand(seed=7) < 0.75, F.lit("residential")).when(F.rand(seed=7) < 0.9375, F.lit("commercial")).otherwise(F.lit("industrial"))
meter_base = meter_base.withColumn("customer_type", ctype_expr)

timestamps = spark.sql(f"""
  SELECT explode(sequence(
    timestamp('{START_DATE}'),
    timestamp('{END_DATE}'),
    interval 1 hour
  )) as timestamp
""")

print(f"Generating meter readings ({NUM_METERS} meters x {timestamps.count()} hours)...")

df_meters = meter_base.crossJoin(timestamps)
df_meters = df_meters.withColumn("hour", F.hour("timestamp"))
df_meters = df_meters.withColumn("month", F.month("timestamp"))
df_meters = df_meters.withColumn("day_of_week", F.dayofweek("timestamp"))

seasonal = F.when(F.col("month").isin(6,7,8), 1.4).when(F.col("month").isin(12,1,2), 1.2).otherwise(1.0)

res_diurnal = (
    F.when((F.col("hour") >= 0) & (F.col("hour") <= 5), 0.15)
    .when((F.col("hour") >= 6) & (F.col("hour") <= 9), 0.6)
    .when((F.col("hour") >= 17) & (F.col("hour") <= 22), 1.0)
    .otherwise(0.35)
)
com_diurnal = F.when((F.col("hour") >= 8) & (F.col("hour") <= 18), 1.2).otherwise(0.3)
ind_diurnal = F.when((F.col("hour") >= 6) & (F.col("hour") <= 22), 0.9).otherwise(0.4)

diurnal = (
    F.when(F.col("customer_type") == "residential", res_diurnal)
    .when(F.col("customer_type") == "commercial", com_diurnal)
    .otherwise(ind_diurnal)
)

base_kwh = (
    F.when(F.col("customer_type") == "residential", 1.2)
    .when(F.col("customer_type") == "commercial", 5.0)
    .otherwise(20.0)
)

df_meters = df_meters.withColumn(
    "kwh_consumed",
    F.round(base_kwh * diurnal * seasonal * (0.8 + 0.4 * F.rand(seed=99)), 4)
)

# Inject ~2% nulls and ~0.1% negatives
null_mask = F.rand(seed=11) < 0.02
neg_mask = (~null_mask) & (F.rand(seed=13) < 0.001)
df_meters = df_meters.withColumn(
    "kwh_consumed",
    F.when(null_mask, F.lit(None).cast("double"))
    .when(neg_mask, -F.abs(F.col("kwh_consumed")))
    .otherwise(F.col("kwh_consumed"))
)

df_meters = df_meters.withColumn("voltage", F.round(F.lit(240) + F.randn(seed=55) * 5, 1))
df_meters = df_meters.withColumn("power_factor", F.round(F.lit(0.85) + F.rand(seed=77) * 0.15, 3))
is_peak = (F.col("hour").between(14, 19)) & (F.col("day_of_week").between(2, 6))
df_meters = df_meters.withColumn("is_peak_hour", is_peak)

df_meters = df_meters.select("meter_id", "customer_id", "timestamp", "kwh_consumed", "voltage", "power_factor", "is_peak_hour")
df_meters.write.mode("overwrite").saveAsTable("raw_meter_readings")
cnt = spark.table("raw_meter_readings").count()
print(f"  raw_meter_readings: {cnt:,} rows")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Table 3: raw_billing (~600K)

# COMMAND ----------

print("Generating billing records...")
billing_rows = []
bill_id = 1

for i in range(NUM_CUSTOMERS):
    acct = f"ACCT-{i+1:06d}"
    ctype = random.choices(CUSTOMER_TYPES, [0.75, 0.20, 0.05])[0]
    base_monthly = {"residential": 150, "commercial": 800, "industrial": 5000}[ctype]
    for m in range(12):
        ms = datetime(2024, 4, 1) + timedelta(days=30 * m)
        sf = {6:1.3,7:1.5,8:1.4,12:1.2,1:1.3,2:1.2}.get(ms.month, 1.0)
        total_kwh = base_monthly * (0.7 + 0.6 * random.random()) * sf
        peak_pct = random.uniform(0.3, 0.6)
        rate = {"residential": 0.12, "commercial": 0.10, "industrial": 0.08}[ctype]
        amt = round(total_kwh * rate + random.uniform(10, 30), 2)
        dq = random.random() < 0.08
        paid = 0 if dq else amt
        pdate = None if dq else str((ms + timedelta(days=random.randint(15, 28))).date())
        billing_rows.append((
            f"BILL-{bill_id:08d}", acct, ms.strftime("%Y-%m"),
            round(total_kwh, 2), round(total_kwh * peak_pct, 2),
            round(total_kwh * (1 - peak_pct), 2), amt, round(paid, 2),
            pdate, round(amt - paid, 2), dq,
        ))
        bill_id += 1
        if random.random() < 0.005:
            billing_rows.append(billing_rows[-1])

schema_bill = StructType([
    StructField("bill_id", StringType()), StructField("customer_id", StringType()),
    StructField("billing_period", StringType()), StructField("total_kwh", DoubleType()),
    StructField("peak_kwh", DoubleType()), StructField("off_peak_kwh", DoubleType()),
    StructField("amount_charged", DoubleType()), StructField("amount_paid", DoubleType()),
    StructField("payment_date", StringType()), StructField("balance", DoubleType()),
    StructField("is_delinquent", BooleanType()),
])

df_bill = spark.createDataFrame(billing_rows, schema=schema_bill)
df_bill = df_bill.withColumn("payment_date", F.col("payment_date").cast("date"))
df_bill.write.mode("overwrite").saveAsTable("raw_billing")
print(f"  raw_billing: {spark.table('raw_billing').count():,} rows")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Table 4: raw_outages (~5K)

# COMMAND ----------

OUTAGE_CAUSES = ["weather", "equipment_failure", "planned_maintenance", "unknown", "vegetation", "animal"]
print("Generating outage records...")
outage_rows = []
for i in range(5000):
    region = random.choice(REGIONS)
    start = fake.date_time_between(start_date="-12m", end_date="now")
    dur = int(random.expovariate(1 / 120) + 5)
    end = start + timedelta(minutes=dur)
    cause = random.choices(OUTAGE_CAUSES, [0.35, 0.25, 0.15, 0.10, 0.10, 0.05])[0]
    affected = random.randint(10, 5000) if cause != "planned_maintenance" else random.randint(50, 500)
    if random.random() < 0.01:
        start = datetime.now() + timedelta(days=random.randint(1, 30))
        end = start + timedelta(minutes=dur)
    outage_rows.append((
        f"OUT-{i+1:06d}", region, str(start), str(end), dur, cause, affected,
        random.choice(["critical", "high", "medium", "low"]),
    ))

schema_out = StructType([
    StructField("outage_id", StringType()), StructField("region", StringType()),
    StructField("start_time", StringType()), StructField("end_time", StringType()),
    StructField("duration_minutes", IntegerType()), StructField("cause", StringType()),
    StructField("affected_meters_count", IntegerType()), StructField("restoration_priority", StringType()),
])
df_out = spark.createDataFrame(outage_rows, schema=schema_out)
df_out = df_out.withColumn("start_time", F.col("start_time").cast("timestamp")).withColumn("end_time", F.col("end_time").cast("timestamp"))
df_out.write.mode("overwrite").saveAsTable("raw_outages")
print(f"  raw_outages: {spark.table('raw_outages').count():,} rows")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Table 5: raw_weather (~1.8K)

# COMMAND ----------

REGION_CLIMATE = {
    "Northeast": {"sh": 85, "wl": 15, "hum": 65}, "Southeast": {"sh": 95, "wl": 35, "hum": 75},
    "Midwest": {"sh": 88, "wl": 5, "hum": 60}, "Southwest": {"sh": 110, "wl": 40, "hum": 20},
    "Northwest": {"sh": 80, "wl": 30, "hum": 70},
}
print("Generating weather records...")
weather_rows = []
for day in range(365):
    d = datetime(2024, 4, 1) + timedelta(days=day)
    sf = math.sin((d.month - 1) * math.pi / 11)
    for region, c in REGION_CLIMATE.items():
        th = c["wl"] + (c["sh"] - c["wl"]) * (0.5 + 0.5 * sf) + random.gauss(0, 5)
        tl = th - random.uniform(10, 25)
        weather_rows.append((
            str(d.date()), region, round(th, 1), round(tl, 1),
            round(max(0, min(100, c["hum"] + random.gauss(0, 10))), 1),
            round(max(0, random.gauss(8, 4)), 1),
            round(max(0, random.expovariate(1/0.2)) if random.random() < 0.3 else 0, 2),
            th > 95, tl < 20,
        ))

schema_w = StructType([
    StructField("date", StringType()), StructField("region", StringType()),
    StructField("temp_high", DoubleType()), StructField("temp_low", DoubleType()),
    StructField("humidity", DoubleType()), StructField("wind_speed", DoubleType()),
    StructField("precipitation", DoubleType()), StructField("is_extreme_heat", BooleanType()),
    StructField("is_extreme_cold", BooleanType()),
])
df_w = spark.createDataFrame(weather_rows, schema=schema_w).withColumn("date", F.col("date").cast("date"))
df_w.write.mode("overwrite").saveAsTable("raw_weather")
print(f"  raw_weather: {spark.table('raw_weather').count():,} rows")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Table 6: raw_equipment (~2K)

# COMMAND ----------

ETYPES = ["transformer", "substation", "feeder", "capacitor_bank", "recloser"]
print("Generating equipment records...")
eq_rows = []
for i in range(2000):
    etype = random.choices(ETYPES, [0.40, 0.10, 0.30, 0.10, 0.10])[0]
    region = random.choice(REGIONS)
    install = fake.date_between(start_date="-30y", end_date="-1y")
    age = (datetime.now().date() - install).days / 365
    failures = max(0, int(random.gauss(0.02 * (age/10)**1.5 * 10, 2)))
    maint = failures + random.randint(1, int(age/2 + 1))
    cap = {"transformer": 500, "substation": 5000, "feeder": 1000, "capacitor_bank": 200, "recloser": 300}[etype]
    load = min(100, max(5, random.gauss(60, 20) + age * 0.5))
    eq_rows.append((
        f"EQ-{i+1:05d}", etype, region, str(install),
        str(fake.date_between(start_date="-2y", end_date="today")),
        maint, failures, cap, round(load, 1),
    ))

schema_eq = StructType([
    StructField("equipment_id", StringType()), StructField("equipment_type", StringType()),
    StructField("region", StringType()), StructField("install_date", StringType()),
    StructField("last_maintenance_date", StringType()), StructField("maintenance_count", IntegerType()),
    StructField("failure_count", IntegerType()), StructField("capacity_rating", IntegerType()),
    StructField("current_load_pct", DoubleType()),
])
df_eq = spark.createDataFrame(eq_rows, schema=schema_eq)
df_eq = df_eq.withColumn("install_date", F.col("install_date").cast("date")).withColumn("last_maintenance_date", F.col("last_maintenance_date").cast("date"))
df_eq.write.mode("overwrite").saveAsTable("raw_equipment")
print(f"  raw_equipment: {spark.table('raw_equipment').count():,} rows")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Table 7: raw_demand_response (~20K)

# COMMAND ----------

print("Generating demand response records...")
dr_rows = []
for i in range(20000):
    target = round(random.uniform(0.5, 15.0), 2)
    participated = random.random() < 0.7
    actual = round(target * random.uniform(0.3, 1.2), 2) if participated else 0
    dr_rows.append((
        f"DR-{i+1:06d}", f"ACCT-{random.randint(1, NUM_CUSTOMERS):06d}",
        str(fake.date_between(start_date="-12m", end_date="today")),
        random.choice(["curtailment", "shift", "shed"]),
        target, actual, round(actual * random.uniform(0.05, 0.15), 2) if participated else 0, participated,
    ))

schema_dr = StructType([
    StructField("event_id", StringType()), StructField("customer_id", StringType()),
    StructField("event_date", StringType()), StructField("event_type", StringType()),
    StructField("target_reduction_kwh", DoubleType()), StructField("actual_reduction_kwh", DoubleType()),
    StructField("incentive_paid", DoubleType()), StructField("participated", BooleanType()),
])
df_dr = spark.createDataFrame(dr_rows, schema=schema_dr).withColumn("event_date", F.col("event_date").cast("date"))
df_dr.write.mode("overwrite").saveAsTable("raw_demand_response")
print(f"  raw_demand_response: {spark.table('raw_demand_response').count():,} rows")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Verify All Tables

# COMMAND ----------

print("\n=== SmartGrid Analytics Platform -- Data Summary ===\n")
for t in ["raw_customers", "raw_meter_readings", "raw_billing", "raw_outages", "raw_weather", "raw_equipment", "raw_demand_response"]:
    cnt = spark.table(t).count()
    cols = len(spark.table(t).columns)
    print(f"  {t:30s} | {cnt:>10,} rows | {cols:>3} columns")
print(f"\nAll 7 tables created in {CATALOG}.{SCHEMA}")
