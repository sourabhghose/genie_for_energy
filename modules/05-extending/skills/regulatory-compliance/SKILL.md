---
name: regulatory-compliance
description: Validates AEMO/AER reliability standards compliance and regulatory reporting thresholds for energy utilities. Use when checking compliance, preparing regulatory reports, or validating outage/reliability data against AEMO/AER requirements.
---

# Regulatory Compliance

Validates energy utility data against AEMO (Australian Energy Market Operator) and AER (Australian Energy Regulator) reliability standards and regulatory reporting thresholds. Data schema: `main.sourabh_energy_workshop`.

## When to Use

- User asks about AEMO/AER compliance, reliability standards, or regulatory thresholds
- User needs to validate outage or reliability data for reporting
- User mentions regulatory reporting, compliance checks, or audit requirements
- User wants to identify violations or exceptions

## Key Standards

| Standard | Focus | Reference |
|----------|-------|-----------|
| AEMO NER | National Electricity Rules | [nerc-standards.md](references/nerc-standards.md) |
| AER reliability standards | Transmission and reliability planning | [nerc-standards.md](references/nerc-standards.md) |
| AEMO NER | Protection and Control | [nerc-standards.md](references/nerc-standards.md) |
| AEMO NER | Emergency Operations | [nerc-standards.md](references/nerc-standards.md) |

## Reporting Thresholds (AER)

| Metric | Threshold | Action |
|--------|-----------|--------|
| SAIDI | > 90 min/year | Report to AER |
| SAIFI | > 1.2 events/year | Report to AER |
| Major Event | > 4 hours, > 10% customers | Exclude from SAIDI/SAIFI |
| Outage Duration | > 8 hours | Mandatory root cause report |

See [reporting-thresholds.md](references/reporting-thresholds.md) for full list.

## Compliance Check Patterns

### SAIDI/SAIFI Threshold Check

```sql
-- Flag states exceeding SAIDI threshold (90 min/year)
WITH reliability AS (
  SELECT
    state,
    SUM(customer_minutes_interrupted) / NULLIF(COUNT(DISTINCT c.customer_id), 0) AS saidi,
    COUNT(*) * 1.0 / NULLIF(COUNT(DISTINCT c.customer_id), 0) AS saifi
  FROM main.sourabh_energy_workshop.raw_outages o
  JOIN main.sourabh_energy_workshop.raw_customers c ON o.customer_id = c.customer_id
  WHERE o.outage_start >= DATE_SUB(CURRENT_DATE(), 365)
    AND o.outage_type = 'unplanned'
  GROUP BY state
)
SELECT state, saidi, saifi,
  CASE WHEN saidi > 90 THEN 'EXCEEDS_SAIDI_THRESHOLD' ELSE 'OK' END AS saidi_status,
  CASE WHEN saifi > 1.2 THEN 'EXCEEDS_SAIFI_THRESHOLD' ELSE 'OK' END AS saifi_status
FROM reliability;
```

### Major Event Detection

```sql
-- Detect events that may qualify for major event exclusion
SELECT
  DATE(outage_start) AS event_date,
  state,
  SUM(customer_minutes_interrupted) AS total_customer_minutes,
  COUNT(DISTINCT customer_id) AS affected_customers,
  AVG(TIMESTAMPDIFF(MINUTE, outage_start, outage_end)) AS avg_duration_minutes
FROM main.sourabh_energy_workshop.raw_outages
WHERE outage_type = 'unplanned'
  AND outage_start >= DATE_SUB(CURRENT_DATE(), 365)
GROUP BY DATE(outage_start), state
HAVING AVG(TIMESTAMPDIFF(MINUTE, outage_start, outage_end)) > 240  -- 4 hours
   OR COUNT(DISTINCT customer_id) > 5000;  -- >10% of ~50K
```

### Outage Duration Compliance

```sql
-- Outages requiring root cause report (> 8 hours)
SELECT outage_id, customer_id, outage_start, outage_end,
  TIMESTAMPDIFF(MINUTE, outage_start, outage_end) AS duration_minutes
FROM main.sourabh_energy_workshop.raw_outages
WHERE outage_type = 'unplanned'
  AND TIMESTAMPDIFF(MINUTE, outage_start, outage_end) > 480;
```

## Scripts

Run full compliance check:
```bash
python scripts/compliance_check.py
```

## Edge Cases

- **Major event exclusion**: Some jurisdictions allow excluding storms/events >4 hours; document exclusions
- **Planned vs unplanned**: Only unplanned outages count toward SAIDI/SAIFI for most reports
- **Momentary interruptions**: Some standards exclude interruptions <5 minutes; check local rules

## Additional Resources

- [references/nerc-standards.md](references/nerc-standards.md) — AEMO/AER reliability standards
- [references/reporting-thresholds.md](references/reporting-thresholds.md) — AER regulatory thresholds
