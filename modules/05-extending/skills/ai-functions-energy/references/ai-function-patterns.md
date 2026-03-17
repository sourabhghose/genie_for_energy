# AI Function Patterns for Energy & Utilities

## ai_forecast Patterns

### Single-Series Demand Forecast

```sql
SELECT * FROM ai_forecast(
  TABLE(
    SELECT reading_date, SUM(total_kwh) AS total_kwh
    FROM main.sourabh_energy_workshop.daily_consumption
    GROUP BY reading_date
    HAVING reading_date >= date_sub(current_date(), 365)
  ),
  horizon   => add_months(current_date(), 3),
  time_col  => 'reading_date',
  value_col => 'total_kwh',
  frequency => 'day'
);
```

### Multi-State Forecast (group_col)

```sql
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
  prediction_interval_width => 0.90,
  frequency                 => 'day'
);
```

### Multi-Metric Forecast

```sql
SELECT * FROM ai_forecast(
  TABLE(
    SELECT reading_date, state, total_kwh, customer_count
    FROM main.sourabh_energy_workshop.daily_consumption
  ),
  horizon   => '2026-06-30',
  time_col  => 'reading_date',
  value_col => ARRAY('total_kwh', 'customer_count'),
  group_col => 'state'
);
```

---

## ai_classify Patterns

### Complaint Routing

```sql
SELECT
  complaint_id,
  description,
  ai_classify(
    description,
    ARRAY('billing', 'outage', 'meter_issue', 'rate_inquiry', 'enrollment', 'other')
  ) AS category
FROM main.sourabh_energy_workshop.customer_complaints;
```

### Priority Classification

```sql
SELECT
  ticket_id,
  ai_classify(
    CONCAT(subject, ' ', body),
    ARRAY('urgent', 'high', 'medium', 'low')
  ) AS priority
FROM main.sourabh_energy_workshop.support_tickets;
```

---

## ai_extract Patterns

### Bill Data Extraction

```sql
SELECT
  bill_id,
  ai_extract(
    raw_text,
    ARRAY('account_number', 'due_date', 'total_amount', 'usage_kwh', 'rate_tier')
  ) AS extracted
FROM main.sourabh_energy_workshop.raw_bill_text;
```

### Contract Clause Extraction

```sql
SELECT
  contract_id,
  ai_extract(content, ARRAY('effective_date', 'termination_date', 'rate', 'penalty_clause')) AS terms
FROM main.sourabh_energy_workshop.contracts;
```

---

## ai_query Patterns

### Structured Output

```sql
SELECT ai_query(
  'databricks-claude-sonnet-4-5',
  CONCAT('From this energy summary, extract key metrics: ', summary_text),
  responseFormat => 'STRUCT<peak_usage: DOUBLE, avg_rate: DOUBLE, recommendation: STRING>'
) AS analysis
FROM main.sourabh_energy_workshop.state_summaries;
```

### Batch with failOnError

```sql
SELECT
  id,
  COALESCE(result.result, 'error') AS answer,
  result.errorMessage AS error
FROM (
  SELECT
    id,
    ai_query(
      'databricks-claude-sonnet-4-5',
      question,
      failOnError => false
    ) AS result
  FROM main.sourabh_energy_workshop.questions
);
```

---

## ai_parse_document Patterns

### Parse PDF Regulatory Filings

```sql
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
  doc:document:elements[0]:content::STRING AS first_page_text
FROM parsed;
```

### Chain with ai_query for Structured Extraction

```sql
WITH parsed AS (
  SELECT path, ai_parse_document(content) AS doc
  FROM read_files('/Volumes/main/sourabh_energy_workshop/filings/', format => 'binaryFile')
)
SELECT
  path,
  ai_query(
    'databricks-claude-sonnet-4-5',
    CONCAT('Extract: rate_change_pct, effective_date, affected_states. Text: ',
           doc:document:elements[0]:content::STRING),
    responseFormat => 'STRUCT<rate_change_pct: DOUBLE, effective_date: STRING, affected_states: ARRAY<STRING>>'
  ) AS filing_data
FROM parsed;
```

---

## Best Practices

1. **Use LIMIT** during development to control token costs.
2. **Pre-filter** observed data for ai_forecast (e.g., last 365 days).
3. **Keep labels short** for ai_classify (2–20 elements).
4. **Use failOnError => false** for batch ai_query when some rows may fail.
5. **Serverless SQL Warehouse** required; AI functions not available on Classic.
