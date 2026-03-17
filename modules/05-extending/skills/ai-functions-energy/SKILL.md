---
name: ai-functions-energy
description: "Teaches Genie Code to use Databricks built-in AI SQL functions for energy/utilities use cases: ai_forecast for demand prediction, ai_classify for complaint categorization, ai_extract for utility bill data, ai_query for natural language, ai_parse_document for regulatory filings. Use when building energy analytics, demand forecasting, or customer service automation."
---

# AI Functions for Energy & Utilities

Use Databricks built-in AI SQL functions for retail energy provider use cases. Data lives in `main.sourabh_energy_workshop` schema for a provider with ~50K customers across 6 Australian states (NSW, VIC, QLD, SA, WA, TAS).

## When to Use

- Demand forecasting and load prediction
- Categorizing customer complaints or support tickets
- Extracting structured data from utility bills or documents
- Natural language queries over energy data
- Parsing regulatory filings (PDFs, DOCX)

## Parameters

| Function | Use Case | Key Parameters |
|---------|----------|----------------|
| `ai_forecast()` | Demand prediction | `observed`, `horizon`, `time_col`, `value_col`, `group_col` |
| `ai_classify()` | Complaint categorization | `content`, `labels` (ARRAY) |
| `ai_extract()` | Bill/contract data | `content`, `labels` (entity types) |
| `ai_query()` | NL-to-SQL, summaries | `endpoint`, `request`, `responseFormat` |
| `ai_parse_document()` | Regulatory filings | `content` (binary), `options_map` |

## Quick Reference

### ai_forecast — Demand Prediction

```sql
SELECT * FROM ai_forecast(
  TABLE(
    SELECT reading_date, state, total_kwh
    FROM main.sourabh_energy_workshop.daily_consumption
    WHERE reading_date >= date_sub(current_date(), 365)
  ),
  horizon    => add_months(current_date(), 3),
  time_col   => 'reading_date',
  value_col  => 'total_kwh',
  group_col  => 'state',
  frequency  => 'day'
);
```

### ai_classify — Complaint Categories

```sql
SELECT
  complaint_id,
  description,
  ai_classify(
    description,
    ARRAY('billing', 'outage', 'meter_issue', 'rate_inquiry', 'enrollment', 'other')
  ) AS category
FROM main.sourabh_energy_workshop.customer_complaints
LIMIT 100;
```

### ai_extract — Utility Bill Data

```sql
SELECT
  bill_id,
  raw_text,
  ai_extract(raw_text, ARRAY('account_number', 'due_date', 'total_amount', 'usage_kwh')) AS extracted
FROM main.sourabh_energy_workshop.raw_bill_text;
```

### ai_query — Natural Language

```sql
SELECT ai_query(
  'databricks-claude-sonnet-4-5',
  'Summarize the top 3 drivers of high usage in NSW based on: ' || summary_text,
  responseFormat => 'STRUCT<drivers: ARRAY<STRING>, recommendation: STRING>'
) AS analysis
FROM main.sourabh_energy_workshop.state_summaries
WHERE state = 'NSW'
LIMIT 1;
```

### ai_parse_document — Regulatory Filings

```sql
WITH parsed AS (
  SELECT
    path,
    ai_parse_document(content, map('version', '2.0')) AS doc
  FROM read_files(
    '/Volumes/main/sourabh_energy_workshop/regulatory_filings/',
    format => 'binaryFile'
  )
)
SELECT
  path,
  ai_query(
    'databricks-claude-sonnet-4-5',
    CONCAT('Extract rate changes, effective date, and affected states from: ',
           doc:document:elements[0]:content::STRING),
    responseFormat => 'STRUCT<rate_changes: STRING, effective_date: STRING, states: ARRAY<STRING>>'
  ) AS filing_summary
FROM parsed;
```

## Examples

**Demand forecast by state:**
```sql
SELECT * FROM ai_forecast(
  TABLE(SELECT reading_date, state, total_kwh FROM main.sourabh_energy_workshop.daily_consumption),
  horizon => '2026-06-30',
  time_col => 'reading_date',
  value_col => 'total_kwh',
  group_col => 'state'
);
```

**Sentiment on complaints:**
```sql
SELECT
  complaint_id,
  ai_analyze_sentiment(description) AS sentiment,
  ai_classify(description, ARRAY('billing', 'outage', 'meter_issue', 'other')) AS category
FROM main.sourabh_energy_workshop.customer_complaints;
```

## Reference Files

- [references/ai-function-patterns.md](references/ai-function-patterns.md) — SQL patterns and best practices
- [references/energy-ai-examples.sql](references/energy-ai-examples.sql) — Full example queries

## Prerequisites

- Serverless SQL Warehouse (AI functions not available on Classic)
- Databricks Runtime 15.1+ (15.4 ML LTS recommended for batch)
- Use `LIMIT` during development to control token costs
