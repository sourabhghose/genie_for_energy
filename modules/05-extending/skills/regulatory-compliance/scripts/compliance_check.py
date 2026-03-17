#!/usr/bin/env python3
"""
AEMO/AER reliability standards compliance check for main.sourabh_energy_workshop.
Validates SAIDI/SAIFI thresholds, major event detection, and outage duration reporting.
"""

from pyspark.sql import SparkSession
from pyspark.sql import functions as F

SCHEMA = "main.sourabh_energy_workshop"
LOOKBACK_DAYS = 365
SAIDI_THRESHOLD = 90  # minutes per customer per year
SAIFI_THRESHOLD = 1.2  # events per customer per year
MAJOR_EVENT_DURATION_MIN = 240  # 4 hours
MAJOR_EVENT_CUSTOMERS = 5000  # ~10% of 50K
ROOT_CAUSE_REPORT_MIN = 480  # 8 hours


def get_spark():
    """Get or create Spark session."""
    return SparkSession.builder.getOrCreate()


def check_saidi_saifi(spark):
    """Check SAIDI and SAIFI against regulatory thresholds."""
    outages = spark.table(f"{SCHEMA}.raw_outages")
    customers = spark.table(f"{SCHEMA}.raw_customers")

    df = outages.join(customers, "customer_id", "inner").filter(
        F.col("outage_start") >= F.date_sub(F.current_date(), LOOKBACK_DAYS)
    ).filter(F.col("outage_type") == "unplanned")

    cust_counts = customers.groupBy("state").agg(
        F.countDistinct("customer_id").alias("total_customers")
    )

    agg = df.groupBy("state").agg(
        F.sum("customer_minutes_interrupted").alias("total_cm"),
        F.count("*").alias("interruptions"),
    ).join(cust_counts, "state")

    result = agg.withColumn(
        "saidi",
        F.col("total_cm") / F.nullif(F.col("total_customers"), 0),
    ).withColumn(
        "saifi",
        F.col("interruptions") / F.nullif(F.col("total_customers"), 0),
    ).withColumn(
        "saidi_compliant",
        F.when(F.col("saidi").isNull(), True).otherwise(F.col("saidi") <= SAIDI_THRESHOLD),
    ).withColumn(
        "saifi_compliant",
        F.when(F.col("saifi").isNull(), True).otherwise(F.col("saifi") <= SAIFI_THRESHOLD),
    ).select(
        "state", "saidi", "saifi", "saidi_compliant", "saifi_compliant"
    )

    return result


def check_major_events(spark):
    """Detect potential major events for exclusion review."""
    outages = spark.table(f"{SCHEMA}.raw_outages")

    df = outages.filter(
        F.col("outage_start") >= F.date_sub(F.current_date(), LOOKBACK_DAYS)
    ).filter(F.col("outage_type") == "unplanned")

    duration = df.withColumn(
        "duration_min",
        F.col("outage_end").cast("long") / 60 - F.col("outage_start").cast("long") / 60,
    )

    by_date_state = duration.groupBy(
        F.to_date("outage_start").alias("event_date"),
        "state",
    ).agg(
        F.sum("customer_minutes_interrupted").alias("total_cm"),
        F.countDistinct("customer_id").alias("affected_customers"),
        F.avg("duration_min").alias("avg_duration_min"),
    )

    major = by_date_state.filter(
        (F.col("avg_duration_min") > MAJOR_EVENT_DURATION_MIN)
        | (F.col("affected_customers") > MAJOR_EVENT_CUSTOMERS)
    ).withColumn("flag", F.lit("MAJOR_EVENT_CANDIDATE"))

    return major


def check_root_cause_reporting(spark):
    """Find outages requiring root cause report (> 8 hours)."""
    outages = spark.table(f"{SCHEMA}.raw_outages")

    df = outages.filter(F.col("outage_type") == "unplanned").withColumn(
        "duration_min",
        (F.col("outage_end").cast("long") - F.col("outage_start").cast("long")) / 60,
    )

    return df.filter(F.col("duration_min") > ROOT_CAUSE_REPORT_MIN).select(
        "outage_id", "customer_id", "outage_start", "outage_end", "duration_min"
    ).withColumn("requires_root_cause_report", F.lit(True))


def main():
    spark = get_spark()

    print("=== SAIDI/SAIFI Compliance ===")
    check_saidi_saifi(spark).show(truncate=False)

    print("=== Major Event Candidates ===")
    check_major_events(spark).show(truncate=False)

    print("=== Outages Requiring Root Cause Report ===")
    check_root_cause_reporting(spark).show(truncate=False)


if __name__ == "__main__":
    main()
