-- Silver: Cleaned and validated energy readings
-- Catalog: {{catalog}}, Schema: {{schema}}

CREATE OR REFRESH STREAMING TABLE {{catalog}}.{{schema}}.silver_readings
CLUSTER BY (reading_date, region)
AS
SELECT
  meter_id,
  customer_id,
  reading_date,
  kwh,
  region,
  _ingested_at,
  _source_file
FROM stream({{catalog}}.{{schema}}.bronze_readings)
WHERE kwh IS NOT NULL
  AND kwh >= 0
  AND customer_id IS NOT NULL
  AND reading_date IS NOT NULL;
