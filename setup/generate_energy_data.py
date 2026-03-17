# Databricks notebook source
# MAGIC %md
# MAGIC # SmartGrid Analytics Platform -- Data Generation
# MAGIC Generates 7 synthetic energy tables for the Genie Code Workshop.
# MAGIC Run this notebook once during workshop setup.
# MAGIC
# MAGIC **Locale:** Australia — 6 states/territories, Australian postcodes, AUD pricing, Celsius weather, 230V grid.

# COMMAND ----------

# MAGIC %pip install faker
# MAGIC %restart_python

# COMMAND ----------

import random, math
from datetime import datetime, timedelta
from faker import Faker
from pyspark.sql import functions as F
from pyspark.sql.types import *

fake = Faker("en_AU")
Faker.seed(42)
random.seed(42)

CATALOG = "main"
SCHEMA = "sourabh_energy_workshop"

spark.sql(f"CREATE SCHEMA IF NOT EXISTS {CATALOG}.{SCHEMA}")
spark.sql(f"USE CATALOG {CATALOG}")
spark.sql(f"USE SCHEMA {SCHEMA}")

STATES = ["NSW", "VIC", "QLD", "SA", "WA", "TAS"]
CUSTOMER_TYPES = ["residential", "commercial", "industrial"]
RATE_PLANS = ["flat", "time_of_use", "demand", "solar_feed_in"]

# Australian city coordinates by state
CITY_DATA = {
    "NSW": [
        ("Sydney", "2000", -33.8688, 151.2093),
        ("Newcastle", "2300", -32.9283, 151.7817),
        ("Wollongong", "2500", -34.4278, 150.8931),
        ("Central Coast", "2250", -33.4200, 151.3420),
        ("Coffs Harbour", "2450", -30.2963, 153.1157),
        ("Wagga Wagga", "2650", -35.1082, 147.3598),
        ("Tamworth", "2340", -31.0927, 150.9320),
        ("Orange", "2800", -33.2839, 149.1013),
        ("Dubbo", "2830", -32.2569, 148.6011),
        ("Albury", "2640", -36.0737, 146.9135),
    ],
    "VIC": [
        ("Melbourne", "3000", -37.8136, 144.9631),
        ("Geelong", "3220", -38.1499, 144.3617),
        ("Ballarat", "3350", -37.5622, 143.8503),
        ("Bendigo", "3550", -36.7570, 144.2794),
        ("Shepparton", "3630", -36.3833, 145.3988),
        ("Warrnambool", "3280", -38.3830, 142.4878),
        ("Mildura", "3500", -34.1855, 142.1625),
        ("Traralgon", "3844", -38.1953, 146.5413),
    ],
    "QLD": [
        ("Brisbane", "4000", -27.4698, 153.0251),
        ("Gold Coast", "4217", -28.0167, 153.4000),
        ("Sunshine Coast", "4558", -26.6500, 153.0667),
        ("Townsville", "4810", -19.2590, 146.8169),
        ("Cairns", "4870", -16.9186, 145.7781),
        ("Toowoomba", "4350", -27.5598, 151.9507),
        ("Mackay", "4740", -21.1411, 149.1861),
        ("Rockhampton", "4700", -23.3791, 150.5100),
        ("Bundaberg", "4670", -24.8661, 152.3489),
    ],
    "SA": [
        ("Adelaide", "5000", -34.9285, 138.6007),
        ("Mount Gambier", "5290", -37.8314, 140.7832),
        ("Whyalla", "5600", -33.0250, 137.5246),
        ("Murray Bridge", "5253", -35.1197, 139.2730),
        ("Port Augusta", "5700", -32.4909, 137.7830),
        ("Mount Barker", "5251", -35.0688, 138.8590),
    ],
    "WA": [
        ("Perth", "6000", -31.9505, 115.8605),
        ("Bunbury", "6230", -33.3271, 115.6414),
        ("Geraldton", "6530", -28.7744, 114.6150),
        ("Mandurah", "6210", -32.5269, 115.7217),
        ("Kalgoorlie", "6430", -30.7489, 121.4660),
        ("Albany", "6330", -35.0269, 117.8840),
        ("Broome", "6725", -17.9614, 122.2359),
    ],
    "TAS": [
        ("Hobart", "7000", -42.8821, 147.3272),
        ("Launceston", "7250", -41.4332, 147.1441),
        ("Devonport", "7310", -41.1796, 146.3514),
        ("Burnie", "7320", -41.0525, 145.9066),
    ],
}

print(f"Target: {CATALOG}.{SCHEMA}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Table 1: raw_customers (~50K)
# MAGIC Includes latitude/longitude coordinates based on city.

# COMMAND ----------

NUM_CUSTOMERS = 50000

def gen_customers():
    rows = []
    ct_weights = [0.75, 0.20, 0.05]
    rp_weights = [0.35, 0.25, 0.25, 0.15]
    for i in range(NUM_CUSTOMERS):
        ctype = random.choices(CUSTOMER_TYPES, ct_weights)[0]
        state = random.choices(STATES, [0.32, 0.26, 0.20, 0.08, 0.10, 0.04])[0]
        city_info = random.choice(CITY_DATA[state])
        city, postcode, base_lat, base_lon = city_info
        lat = round(base_lat + random.gauss(0, 0.05), 6)
        lon = round(base_lon + random.gauss(0, 0.05), 6)
        signup = fake.date_between(start_date="-10y", end_date="-6m")
        contract_end = signup + timedelta(days=random.choice([365, 730, 1095]))
        has_solar = random.random() < (0.35 if state in ["QLD", "SA", "WA"] else 0.20 if state == "NSW" else 0.12)
        has_ev = random.random() < (0.10 if ctype == "residential" else 0.03)
        rows.append((
            f"ACCT-{i+1:06d}", fake.name(), fake.street_address(), city,
            state, postcode, ctype,
            random.choices(RATE_PLANS, rp_weights)[0],
            str(signup), str(contract_end), has_solar, has_ev, random.random() < 0.25,
            lat, lon,
        ))
    return rows

schema_cust = StructType([
    StructField("account_id", StringType()), StructField("customer_name", StringType()),
    StructField("street_address", StringType()), StructField("city", StringType()),
    StructField("state", StringType()), StructField("postcode", StringType()),
    StructField("customer_type", StringType()),
    StructField("rate_plan", StringType()), StructField("signup_date", StringType()),
    StructField("contract_end_date", StringType()), StructField("has_solar", BooleanType()),
    StructField("has_ev", BooleanType()), StructField("demand_response_enrolled", BooleanType()),
    StructField("latitude", DoubleType()), StructField("longitude", DoubleType()),
])

print("Generating 50K customers...")
df_cust = spark.createDataFrame(gen_customers(), schema=schema_cust)
df_cust = df_cust.withColumn("signup_date", F.col("signup_date").cast("date")).withColumn("contract_end_date", F.col("contract_end_date").cast("date"))
df_cust.write.mode("overwrite").saveAsTable("raw_customers")
print(f"  raw_customers: {spark.table('raw_customers').count():,} rows")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Table 2: raw_meter_readings (~10M)
# MAGIC Uses Spark-native generation for performance. Australian 230V grid.

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

# Australia: summer = Dec/Jan/Feb, winter = Jun/Jul/Aug
seasonal = F.when(F.col("month").isin(12, 1, 2), 1.4).when(F.col("month").isin(6, 7, 8), 1.2).otherwise(1.0)

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

null_mask = F.rand(seed=11) < 0.02
neg_mask = (~null_mask) & (F.rand(seed=13) < 0.001)
df_meters = df_meters.withColumn(
    "kwh_consumed",
    F.when(null_mask, F.lit(None).cast("double"))
    .when(neg_mask, -F.abs(F.col("kwh_consumed")))
    .otherwise(F.col("kwh_consumed"))
)

# Australian grid: 230V nominal
df_meters = df_meters.withColumn("voltage", F.round(F.lit(230) + F.randn(seed=55) * 5, 1))
df_meters = df_meters.withColumn("power_factor", F.round(F.lit(0.85) + F.rand(seed=77) * 0.15, 3))
is_peak = (F.col("hour").between(14, 20)) & (F.col("day_of_week").between(2, 6))
df_meters = df_meters.withColumn("is_peak_hour", is_peak)

df_meters = df_meters.select("meter_id", "customer_id", "timestamp", "kwh_consumed", "voltage", "power_factor", "is_peak_hour")
df_meters.write.mode("overwrite").saveAsTable("raw_meter_readings")
cnt = spark.table("raw_meter_readings").count()
print(f"  raw_meter_readings: {cnt:,} rows")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Table 3: raw_billing (~600K)
# MAGIC Australian pricing in AUD cents/kWh.

# COMMAND ----------

print("Generating billing records...")
billing_rows = []
bill_id = 1

for i in range(NUM_CUSTOMERS):
    acct = f"ACCT-{i+1:06d}"
    ctype = random.choices(CUSTOMER_TYPES, [0.75, 0.20, 0.05])[0]
    base_monthly = {"residential": 180, "commercial": 950, "industrial": 6000}[ctype]
    for m in range(12):
        ms = datetime(2024, 4, 1) + timedelta(days=30 * m)
        # Australia: summer peak Dec-Feb, winter heating Jun-Aug
        sf = {12: 1.4, 1: 1.5, 2: 1.3, 6: 1.2, 7: 1.3, 8: 1.2}.get(ms.month, 1.0)
        total_kwh = base_monthly * (0.7 + 0.6 * random.random()) * sf
        peak_pct = random.uniform(0.3, 0.6)
        # AUD rates (cents/kWh converted to $/kWh)
        rate = {"residential": 0.30, "commercial": 0.24, "industrial": 0.18}[ctype]
        amt = round(total_kwh * rate + random.uniform(15, 40), 2)
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
# MAGIC Includes latitude/longitude for map visualisations.

# COMMAND ----------

OUTAGE_CAUSES = ["weather", "equipment_failure", "planned_maintenance", "unknown", "vegetation", "animal"]

STATE_COORDS = {
    "NSW": (-33.5, 150.5), "VIC": (-37.5, 145.0), "QLD": (-25.0, 152.0),
    "SA": (-34.5, 138.5), "WA": (-31.5, 116.0), "TAS": (-42.0, 147.0),
}

print("Generating outage records...")
outage_rows = []
for i in range(5000):
    state = random.choice(STATES)
    start = fake.date_time_between(start_date="-12m", end_date="now")
    dur = int(random.expovariate(1 / 120) + 5)
    end = start + timedelta(minutes=dur)
    cause = random.choices(OUTAGE_CAUSES, [0.35, 0.25, 0.15, 0.10, 0.10, 0.05])[0]
    affected = random.randint(10, 5000) if cause != "planned_maintenance" else random.randint(50, 500)
    base_lat, base_lon = STATE_COORDS[state]
    lat = round(base_lat + random.gauss(0, 1.0), 6)
    lon = round(base_lon + random.gauss(0, 1.0), 6)
    if random.random() < 0.01:
        start = datetime.now() + timedelta(days=random.randint(1, 30))
        end = start + timedelta(minutes=dur)
    outage_rows.append((
        f"OUT-{i+1:06d}", state, str(start), str(end), dur, cause, affected,
        random.choice(["critical", "high", "medium", "low"]),
        lat, lon,
    ))

schema_out = StructType([
    StructField("outage_id", StringType()), StructField("state", StringType()),
    StructField("start_time", StringType()), StructField("end_time", StringType()),
    StructField("duration_minutes", IntegerType()), StructField("cause", StringType()),
    StructField("affected_meters_count", IntegerType()), StructField("restoration_priority", StringType()),
    StructField("latitude", DoubleType()), StructField("longitude", DoubleType()),
])
df_out = spark.createDataFrame(outage_rows, schema=schema_out)
df_out = df_out.withColumn("start_time", F.col("start_time").cast("timestamp")).withColumn("end_time", F.col("end_time").cast("timestamp"))
df_out.write.mode("overwrite").saveAsTable("raw_outages")
print(f"  raw_outages: {spark.table('raw_outages').count():,} rows")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Table 5: raw_weather (~2.2K)
# MAGIC Australian climate in Celsius. 6 states x 365 days.

# COMMAND ----------

# Celsius climate profiles per state
STATE_CLIMATE = {
    "NSW":  {"summer_high": 32, "winter_low": 6,  "humidity": 60},
    "VIC":  {"summer_high": 28, "winter_low": 4,  "humidity": 55},
    "QLD":  {"summer_high": 33, "winter_low": 12, "humidity": 70},
    "SA":   {"summer_high": 36, "winter_low": 7,  "humidity": 35},
    "WA":   {"summer_high": 35, "winter_low": 9,  "humidity": 40},
    "TAS":  {"summer_high": 22, "winter_low": 2,  "humidity": 65},
}

print("Generating weather records...")
weather_rows = []
for day in range(365):
    d = datetime(2024, 4, 1) + timedelta(days=day)
    # Southern hemisphere: peak summer around Jan (month ~10 from April start)
    sf = math.cos((d.month - 1) * math.pi / 6)
    for state, c in STATE_CLIMATE.items():
        range_temp = c["summer_high"] - c["winter_low"]
        th = c["winter_low"] + range_temp * (0.5 + 0.5 * sf) + random.gauss(0, 2.5)
        tl = th - random.uniform(5, 12)
        weather_rows.append((
            str(d.date()), state, round(th, 1), round(tl, 1),
            round(max(0, min(100, c["humidity"] + random.gauss(0, 10))), 1),
            round(max(0, random.gauss(15, 6)), 1),
            round(max(0, random.expovariate(1/0.3)) if random.random() < 0.3 else 0, 2),
            th > 38, tl < 2,
        ))

schema_w = StructType([
    StructField("date", StringType()), StructField("state", StringType()),
    StructField("temp_high_c", DoubleType()), StructField("temp_low_c", DoubleType()),
    StructField("humidity", DoubleType()), StructField("wind_speed_kmh", DoubleType()),
    StructField("precipitation_mm", DoubleType()), StructField("is_extreme_heat", BooleanType()),
    StructField("is_extreme_cold", BooleanType()),
])
df_w = spark.createDataFrame(weather_rows, schema=schema_w).withColumn("date", F.col("date").cast("date"))
df_w.write.mode("overwrite").saveAsTable("raw_weather")
print(f"  raw_weather: {spark.table('raw_weather').count():,} rows")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Table 6: raw_equipment (~2K)
# MAGIC Includes latitude/longitude for geospatial analysis.

# COMMAND ----------

ETYPES = ["transformer", "substation", "feeder", "capacitor_bank", "recloser"]
print("Generating equipment records...")
eq_rows = []
for i in range(2000):
    etype = random.choices(ETYPES, [0.40, 0.10, 0.30, 0.10, 0.10])[0]
    state = random.choice(STATES)
    install = fake.date_between(start_date="-30y", end_date="-1y")
    age = (datetime.now().date() - install).days / 365
    failures = max(0, int(random.gauss(0.02 * (age/10)**1.5 * 10, 2)))
    maint = failures + random.randint(1, int(age/2 + 1))
    cap = {"transformer": 500, "substation": 5000, "feeder": 1000, "capacitor_bank": 200, "recloser": 300}[etype]
    load = min(100, max(5, random.gauss(60, 20) + age * 0.5))
    base_lat, base_lon = STATE_COORDS[state]
    lat = round(base_lat + random.gauss(0, 0.8), 6)
    lon = round(base_lon + random.gauss(0, 0.8), 6)
    eq_rows.append((
        f"EQ-{i+1:05d}", etype, state, str(install),
        str(fake.date_between(start_date="-2y", end_date="today")),
        maint, failures, cap, round(load, 1),
        lat, lon,
    ))

schema_eq = StructType([
    StructField("equipment_id", StringType()), StructField("equipment_type", StringType()),
    StructField("state", StringType()), StructField("install_date", StringType()),
    StructField("last_maintenance_date", StringType()), StructField("maintenance_count", IntegerType()),
    StructField("failure_count", IntegerType()), StructField("capacity_rating", IntegerType()),
    StructField("current_load_pct", DoubleType()),
    StructField("latitude", DoubleType()), StructField("longitude", DoubleType()),
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

print("\n=== SmartGrid Analytics Platform -- Data Summary (Australia) ===\n")
for t in ["raw_customers", "raw_meter_readings", "raw_billing", "raw_outages", "raw_weather", "raw_equipment", "raw_demand_response"]:
    cnt = spark.table(t).count()
    cols = len(spark.table(t).columns)
    print(f"  {t:30s} | {cnt:>10,} rows | {cols:>3} columns")
print(f"\nAll 7 tables created in {CATALOG}.{SCHEMA}")
