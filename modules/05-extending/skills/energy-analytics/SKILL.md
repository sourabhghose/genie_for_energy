---
name: energy-analytics
description: Calculates energy and utility KPIs including SAIDI, SAIFI, CAIDI, Load Factor, T&D Loss, CLV, and DR Effectiveness. Use when analyzing grid reliability, customer value, demand response, or energy efficiency for retail energy providers.
---

# Energy Analytics

Calculates industry-standard energy and utility KPIs for retail energy providers. Data schema: `main.sourabh_energy_workshop` (~50K customers, 5 regions: Northeast, Southeast, Midwest, Southwest, Northwest).

## When to Use

- User asks for reliability metrics (SAIDI, SAIFI, CAIDI)
- User needs load factor, T&D loss, or capacity utilization
- User wants customer lifetime value (CLV) or demand response effectiveness
- User mentions energy KPIs, grid reliability, or utility analytics

## Key KPIs

| KPI | Formula | Reference |
|-----|---------|-----------|
| SAIDI | Sum(Customer-Minutes Interrupted) / Total Customers | [kpi-definitions.md](references/kpi-definitions.md) |
| SAIFI | Sum(Interruption Events) / Total Customers | [kpi-definitions.md](references/kpi-definitions.md) |
| CAIDI | SAIDI / SAIFI | [kpi-definitions.md](references/kpi-definitions.md) |
| Load Factor | Avg Demand / Peak Demand | [kpi-definitions.md](references/kpi-definitions.md) |
| T&D Loss | (Delivered - Billed) / Delivered × 100 | [kpi-definitions.md](references/kpi-definitions.md) |
| CLV | (Revenue - Cost) × Retention / Churn | [kpi-definitions.md](references/kpi-definitions.md) |
| DR Effectiveness | (Baseline - Event Load) / Baseline × 100 | [kpi-definitions.md](references/kpi-definitions.md) |

## Data Sources

All tables in `main.sourabh_energy_workshop`:
- `raw_customers`, `raw_meter_readings`, `raw_billing`, `raw_outages`, `raw_weather`, `raw_equipment`, `raw_demand_response`

See [energy-data-dictionary.md](references/energy-data-dictionary.md) for column descriptions.

## Reliability KPIs (SAIDI, SAIFI, CAIDI)

```sql
-- SAIDI: System Average Interruption Duration Index (minutes)
SELECT
  region,
  SUM(customer_minutes_interrupted) / NULLIF(COUNT(DISTINCT customer_id), 0) AS saidi_minutes
FROM main.sourabh_energy_workshop.raw_outages o
JOIN main.sourabh_energy_workshop.raw_customers c ON o.customer_id = c.customer_id
WHERE outage_start >= DATE_SUB(CURRENT_DATE(), 365)
GROUP BY region;

-- SAIFI: System Average Interruption Frequency Index (events per customer)
SELECT
  region,
  COUNT(*) * 1.0 / NULLIF(COUNT(DISTINCT customer_id), 0) AS saifi
FROM main.sourabh_energy_workshop.raw_outages o
JOIN main.sourabh_energy_workshop.raw_customers c ON o.customer_id = c.customer_id
WHERE outage_start >= DATE_SUB(CURRENT_DATE(), 365)
GROUP BY region;

-- CAIDI = SAIDI / SAIFI (average duration per interruption)
```

## Load Factor

```sql
SELECT
  customer_id,
  AVG(kwh) / NULLIF(MAX(kwh), 0) AS load_factor
FROM main.sourabh_energy_workshop.raw_meter_readings
WHERE reading_date >= DATE_SUB(CURRENT_DATE(), 365)
GROUP BY customer_id;
```

## T&D Loss

```sql
SELECT
  region,
  (SUM(delivered_kwh) - SUM(billed_kwh)) / NULLIF(SUM(delivered_kwh), 0) * 100 AS td_loss_pct
FROM main.sourabh_energy_workshop.raw_billing b
JOIN main.sourabh_energy_workshop.raw_customers c ON b.customer_id = c.customer_id
WHERE billing_period_end >= DATE_SUB(CURRENT_DATE(), 365)
GROUP BY region;
```

## DR Effectiveness

```sql
SELECT
  event_id,
  AVG(baseline_kwh - actual_kwh) / NULLIF(AVG(baseline_kwh), 0) * 100 AS dr_effectiveness_pct
FROM main.sourabh_energy_workshop.raw_demand_response
WHERE event_status = 'completed'
GROUP BY event_id;
```

## Edge Cases

- **Exclude planned outages** for SAIDI/SAIFI unless explicitly requested
- **Null handling**: Use `NULLIF(denominator, 0)` to avoid division by zero
- **Time windows**: Default to rolling 12 months; confirm with user for different periods
- **Major event exclusion**: Some regulators exclude events >X hours; document if applied

## Scripts

Run reliability KPI calculation:
```bash
python scripts/calculate_reliability.py
```

## Additional Resources

- [references/kpi-definitions.md](references/kpi-definitions.md) — Formulas, SQL snippets, industry benchmarks
- [references/energy-data-dictionary.md](references/energy-data-dictionary.md) — Column descriptions for all 7 tables
