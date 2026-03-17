-- Gold: Aggregated daily consumption by region
-- Catalog: {{catalog}}, Schema: {{schema}}

CREATE OR REFRESH MATERIALIZED VIEW {{catalog}}.{{schema}}.gold_daily_consumption
CLUSTER BY (reading_date, region)
AS
SELECT
  reading_date,
  region,
  COUNT(DISTINCT customer_id) AS customer_count,
  SUM(kwh) AS total_kwh,
  AVG(kwh) AS avg_kwh
FROM {{catalog}}.{{schema}}.silver_readings
GROUP BY reading_date, region;
