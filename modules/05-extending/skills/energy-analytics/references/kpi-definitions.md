# Energy KPI Definitions

Formulas, SQL snippets, and industry benchmarks for energy and utility analytics.

## Reliability KPIs

### SAIDI (System Average Interruption Duration Index)

**Formula:** `SAIDI = Σ(Customer-Minutes Interrupted) / Total Customers Served`

**Unit:** Minutes per customer per year

**SQL:**
```sql
SELECT
  region,
  SUM(customer_minutes_interrupted) / NULLIF(COUNT(DISTINCT customer_id), 0) AS saidi_minutes
FROM main.sourabh_energy_workshop.raw_outages o
JOIN main.sourabh_energy_workshop.raw_customers c ON o.customer_id = c.customer_id
WHERE outage_start >= DATE_SUB(CURRENT_DATE(), 365)
  AND outage_type = 'unplanned'  -- exclude planned maintenance
GROUP BY region;
```

**Benchmarks:**
| Tier | SAIDI (min/year) |
|------|-------------------|
| Excellent | < 60 |
| Good | 60–90 |
| Average | 90–150 |
| Poor | > 150 |

---

### SAIFI (System Average Interruption Frequency Index)

**Formula:** `SAIFI = Σ(Number of Interruptions) / Total Customers Served`

**Unit:** Interruptions per customer per year

**SQL:**
```sql
SELECT
  region,
  COUNT(*) * 1.0 / NULLIF(COUNT(DISTINCT customer_id), 0) AS saifi
FROM main.sourabh_energy_workshop.raw_outages o
JOIN main.sourabh_energy_workshop.raw_customers c ON o.customer_id = c.customer_id
WHERE outage_start >= DATE_SUB(CURRENT_DATE(), 365)
  AND outage_type = 'unplanned'
GROUP BY region;
```

**Benchmarks:**
| Tier | SAIFI (events/year) |
|------|---------------------|
| Excellent | < 0.5 |
| Good | 0.5–1.0 |
| Average | 1.0–2.0 |
| Poor | > 2.0 |

---

### CAIDI (Customer Average Interruption Duration Index)

**Formula:** `CAIDI = SAIDI / SAIFI`

**Unit:** Minutes per interruption (average duration when a customer experiences an outage)

**SQL:**
```sql
-- Compute as SAIDI / SAIFI from subquery
SELECT
  region,
  saidi_minutes / NULLIF(saifi, 0) AS caidi_minutes
FROM (
  SELECT
    region,
    SUM(customer_minutes_interrupted) / NULLIF(COUNT(DISTINCT customer_id), 0) AS saidi_minutes,
    COUNT(*) * 1.0 / NULLIF(COUNT(DISTINCT customer_id), 0) AS saifi
  FROM main.sourabh_energy_workshop.raw_outages o
  JOIN main.sourabh_energy_workshop.raw_customers c ON o.customer_id = c.customer_id
  WHERE outage_start >= DATE_SUB(CURRENT_DATE(), 365) AND outage_type = 'unplanned'
  GROUP BY region
) t;
```

---

## Load Factor

**Formula:** `Load Factor = Average Demand / Peak Demand`

**Unit:** Dimensionless (0–1 or 0–100%)

**SQL:**
```sql
SELECT
  customer_id,
  AVG(kwh) / NULLIF(MAX(kwh), 0) AS load_factor
FROM main.sourabh_energy_workshop.raw_meter_readings
WHERE reading_date >= DATE_SUB(CURRENT_DATE(), 365)
GROUP BY customer_id;
```

**Benchmarks:**
| Customer Type | Typical Load Factor |
|---------------|---------------------|
| Residential | 0.25–0.40 |
| Commercial | 0.50–0.70 |
| Industrial | 0.60–0.85 |

---

## T&D Loss (Transmission & Distribution Loss)

**Formula:** `T&D Loss % = (Delivered - Billed) / Delivered × 100`

**Unit:** Percent

**SQL:**
```sql
SELECT
  region,
  (SUM(delivered_kwh) - SUM(billed_kwh)) / NULLIF(SUM(delivered_kwh), 0) * 100 AS td_loss_pct
FROM main.sourabh_energy_workshop.raw_billing b
JOIN main.sourabh_energy_workshop.raw_customers c ON b.customer_id = c.customer_id
WHERE billing_period_end >= DATE_SUB(CURRENT_DATE(), 365)
GROUP BY region;
```

**Benchmarks:**
| Tier | T&D Loss % |
|------|------------|
| Excellent | < 5 |
| Good | 5–8 |
| Average | 8–12 |
| Poor | > 12 |

---

## CLV (Customer Lifetime Value)

**Formula:** `CLV = (Avg Revenue - Avg Cost) × (1 / Churn Rate)` or `(Revenue - Cost) × Retention / Churn`

**SQL (simplified):**
```sql
SELECT
  customer_id,
  AVG(total_amount) * (1 / NULLIF(churn_rate, 0)) AS clv
FROM main.sourabh_energy_workshop.raw_billing b
JOIN main.sourabh_energy_workshop.raw_customers c ON b.customer_id = c.customer_id
WHERE billing_period_end >= DATE_SUB(CURRENT_DATE(), 365)
GROUP BY customer_id, churn_rate;
```

---

## DR Effectiveness (Demand Response)

**Formula:** `DR Effectiveness % = (Baseline - Event Load) / Baseline × 100`

**Unit:** Percent reduction during event

**SQL:**
```sql
SELECT
  event_id,
  AVG(baseline_kwh - actual_kwh) / NULLIF(AVG(baseline_kwh), 0) * 100 AS dr_effectiveness_pct
FROM main.sourabh_energy_workshop.raw_demand_response
WHERE event_status = 'completed'
GROUP BY event_id;
```

**Benchmarks:**
| Tier | DR Effectiveness % |
|------|---------------------|
| Excellent | > 15 |
| Good | 10–15 |
| Average | 5–10 |
| Poor | < 5 |
