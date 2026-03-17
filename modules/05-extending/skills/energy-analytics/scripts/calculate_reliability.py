#!/usr/bin/env python3
"""
Calculate grid reliability KPIs (SAIDI, SAIFI, CAIDI) from main.sourabh_energy_workshop.
Uses PySpark for Databricks compatibility.
"""

from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.window import Window

SCHEMA = "main.sourabh_energy_workshop"
LOOKBACK_DAYS = 365


def get_spark():
    """Get or create Spark session."""
    return SparkSession.builder.getOrCreate()


def calculate_saidi_saifi(spark, exclude_planned=True):
    """Calculate SAIDI and SAIFI by region."""
    outages = spark.table(f"{SCHEMA}.raw_outages")
    customers = spark.table(f"{SCHEMA}.raw_customers")

    df = outages.join(customers, "customer_id", "inner").filter(
        F.col("outage_start") >= F.date_sub(F.current_date(), LOOKBACK_DAYS)
    )

    if exclude_planned:
        df = df.filter(F.col("outage_type") == "unplanned")

    # Total customers per region (for denominator)
    cust_counts = customers.groupBy("region").agg(
        F.countDistinct("customer_id").alias("total_customers")
    )

    # Aggregations
    agg_df = df.groupBy("region").agg(
        F.sum("customer_minutes_interrupted").alias("total_customer_minutes"),
        F.count("*").alias("total_interruptions"),
        F.countDistinct("customer_id").alias("affected_customers"),
    )

    result = agg_df.join(cust_counts, "region").withColumn(
        "saidi_minutes",
        F.col("total_customer_minutes") / F.nullif(F.col("total_customers"), 0),
    ).withColumn(
        "saifi",
        F.col("total_interruptions") / F.nullif(F.col("total_customers"), 0),
    ).withColumn(
        "caidi_minutes",
        F.col("saidi_minutes") / F.nullif(F.col("saifi"), 0),
    ).select(
        "region",
        "saidi_minutes",
        "saifi",
        "caidi_minutes",
        "total_customer_minutes",
        "total_interruptions",
        "total_customers",
    )

    return result


def main():
    spark = get_spark()
    result = calculate_saidi_saifi(spark)
    result.show(truncate=False)
    return result


if __name__ == "__main__":
    main()
