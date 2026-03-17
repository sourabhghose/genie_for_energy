-- Energy AI Examples for main.sourabh_energy_workshop
-- Retail energy provider: ~50K customers, 6 Australian states (NSW, VIC, QLD, SA, WA, TAS)

-- =============================================================================
-- 1. ai_forecast: Demand prediction by state
-- =============================================================================

SELECT * FROM ai_forecast(
  TABLE(
    SELECT reading_date, state, total_kwh
    FROM main.sourabh_energy_workshop.daily_consumption
    WHERE reading_date >= date_sub(current_date(), 365)
  ),
  horizon                   => add_months(current_date(), 3),
  time_col                  => 'reading_date',
  value_col                 => 'total_kwh',
  group_col                 => 'state',
  prediction_interval_width => 0.95,
  frequency                 => 'day'
);

-- =============================================================================
-- 2. ai_classify: Categorize customer complaints
-- =============================================================================

SELECT
  complaint_id,
  customer_id,
  description,
  ai_classify(
    description,
    ARRAY('billing', 'outage', 'meter_issue', 'rate_inquiry', 'enrollment', 'other')
  ) AS category,
  ai_analyze_sentiment(description) AS sentiment
FROM main.sourabh_energy_workshop.customer_complaints
LIMIT 100;

-- =============================================================================
-- 3. ai_extract: Extract utility bill data from raw text
-- =============================================================================

SELECT
  bill_id,
  customer_id,
  ai_extract(
    raw_text,
    ARRAY('account_number', 'due_date', 'total_amount', 'usage_kwh', 'rate_tier')
  ) AS extracted
FROM main.sourabh_energy_workshop.raw_bill_text
LIMIT 50;

-- =============================================================================
-- 4. ai_query: Natural language summary of state performance
-- =============================================================================

SELECT
  state,
  ai_query(
    'databricks-claude-sonnet-4-5',
    CONCAT(
      'Summarize in one sentence the key insight from this energy data: ',
      'State: ', state, ', Avg usage: ', CAST(avg_kwh AS STRING), ' kWh, Trend: ', trend
    ),
    responseFormat => 'STRUCT<summary: STRING>'
  ) AS insight
FROM main.sourabh_energy_workshop.state_summaries
WHERE state = 'NSW'
LIMIT 1;

-- =============================================================================
-- 5. ai_parse_document: Parse regulatory filings (PDF) and extract structured data
-- =============================================================================

WITH raw_docs AS (
  SELECT path, content
  FROM read_files(
    '/Volumes/main/sourabh_energy_workshop/regulatory_filings/',
    format => 'binaryFile',
    pathGlobFilter => '*.pdf'
  )
),
parsed AS (
  SELECT path, ai_parse_document(content, map('version', '2.0')) AS doc
  FROM raw_docs
)
SELECT
  path,
  ai_query(
    'databricks-claude-sonnet-4-5',
    CONCAT(
      'Extract from this regulatory filing: rate_change_pct (number), effective_date (YYYY-MM-DD), affected_states (comma-separated). Text: ',
      doc:document:elements[0]:content::STRING
    ),
    responseFormat => 'STRUCT<rate_change_pct: DOUBLE, effective_date: STRING, affected_states: STRING>'
  ) AS filing_summary
FROM parsed
LIMIT 10;

-- =============================================================================
-- 6. Combined: Forecast + classify + sentiment (pipeline pattern)
-- =============================================================================

-- Step 1: Forecast next 30 days by state
CREATE OR REPLACE TEMPORARY VIEW forecast_by_state AS
SELECT * FROM ai_forecast(
  TABLE(
    SELECT reading_date, state, total_kwh
    FROM main.sourabh_energy_workshop.daily_consumption
    WHERE reading_date >= date_sub(current_date(), 365)
  ),
  horizon   => date_add(current_date(), 30),
  time_col  => 'reading_date',
  value_col => 'total_kwh',
  group_col => 'state'
);

-- Step 2: Categorize recent complaints
CREATE OR REPLACE TEMPORARY VIEW complaints_categorized AS
SELECT
  complaint_id,
  description,
  ai_classify(description, ARRAY('billing', 'outage', 'meter_issue', 'rate_inquiry', 'other')) AS category,
  ai_analyze_sentiment(description) AS sentiment
FROM main.sourabh_energy_workshop.customer_complaints
WHERE created_at >= date_sub(current_date(), 7);

-- Step 3: Join or use in downstream queries
SELECT * FROM forecast_by_state;
SELECT * FROM complaints_categorized;
