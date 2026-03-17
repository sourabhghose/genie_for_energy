-- Bronze: Raw ingestion for energy data
-- Catalog: {{catalog}}, Schema: {{schema}}, Source: {{source_path}}

CREATE OR REFRESH STREAMING TABLE {{catalog}}.{{schema}}.bronze_readings
CLUSTER BY (reading_date)
AS
SELECT
  *,
  current_timestamp() AS _ingested_at,
  _metadata.file_path AS _source_file
FROM read_files(
  '{{source_path}}',
  format => 'json',
  schemaHints => 'meter_id STRING, customer_id STRING, reading_date DATE, kwh DOUBLE, region STRING'
);
