---
name: carbon-reporting
description: Calculates Scope 1/2/3 emissions, applies EPA eGRID factors, and supports ESG reporting frameworks. Use when computing carbon footprint, emissions from electricity consumption, or preparing sustainability/ESG reports.
---

# Carbon Reporting

Calculates greenhouse gas (GHG) emissions for energy utilities using Scope 1/2/3 definitions, EPA eGRID emission factors, and ESG frameworks. Data schema: `main.sourabh_energy_workshop`.

## When to Use

- User asks about Scope 1, 2, or 3 emissions
- User needs carbon footprint or GHG calculations
- User mentions EPA eGRID, emission factors, or regional emissions
- User is preparing ESG, sustainability, or carbon reports

## Scope Definitions

| Scope | Description | Typical Sources |
|-------|-------------|-----------------|
| Scope 1 | Direct emissions from owned/controlled sources | Fleet, generation, fugitive |
| Scope 2 | Indirect emissions from purchased energy | Electricity, steam, heat |
| Scope 3 | Other indirect emissions in value chain | Supply chain, customer use |

See [emissions-definitions.md](references/emissions-definitions.md) for full definitions.

## Scope 2 (Electricity) Formula

```
Scope 2 Emissions (kg CO2e) = Consumption (kWh) × eGRID Factor (kg CO2e/MWh) / 1000
```

## eGRID Factors by Region

| Region | Subregion | kg CO2e/MWh (approx) |
|--------|-----------|----------------------|
| Northeast | NEWE, NYCW | 250–350 |
| Southeast | SRMV, SRTV, SRVC | 450–550 |
| Midwest | MROW, MRCW, SRMW | 550–750 |
| Southwest | AZNM, ERCT | 350–450 |
| Northwest | NWPP | 200–350 |

See [egrid-factors.md](references/egrid-factors.md) for full EPA eGRID factors.

## SQL: Scope 2 from Consumption

```sql
-- Map regions to eGRID subregions and calculate Scope 2
WITH consumption AS (
  SELECT
    c.region,
    SUM(m.kwh) AS total_kwh
  FROM main.sourabh_energy_workshop.raw_meter_readings m
  JOIN main.sourabh_energy_workshop.raw_customers c ON m.customer_id = c.customer_id
  WHERE m.reading_date >= DATE_SUB(CURRENT_DATE(), 365)
  GROUP BY c.region
),
egrid AS (
  SELECT region, egrid_subregion, kg_co2e_per_mwh
  FROM (VALUES
    ('Northeast', 'NEWE', 280),
    ('Southeast', 'SRMV', 520),
    ('Midwest', 'MROW', 650),
    ('Southwest', 'AZNM', 400),
    ('Northwest', 'NWPP', 280)
  ) AS t(region, egrid_subregion, kg_co2e_per_mwh)
)
SELECT
  cons.region,
  cons.total_kwh,
  e.kg_co2e_per_mwh,
  cons.total_kwh * e.kg_co2e_per_mwh / 1000 AS scope2_kg_co2e
FROM consumption cons
JOIN egrid e ON cons.region = e.region;
```

## ESG Frameworks

- **GHG Protocol**: Corporate Standard for Scope 1/2/3
- **CDP**: Carbon Disclosure Project questionnaires
- **GRI**: Global Reporting Initiative 305 (Emissions)
- **SASB**: Sustainability Accounting Standards Board utilities standard

## Edge Cases

- **Market-based vs location-based**: Location-based uses grid average (eGRID); market-based uses contractual instruments (RECs, PPAs)
- **Time granularity**: Hourly factors improve accuracy; annual averages are common for reporting
- **Region mapping**: Map `main.sourabh_energy_workshop.raw_customers.region` to eGRID subregions

## Additional Resources

- [references/emissions-definitions.md](references/emissions-definitions.md) — Scope 1/2/3 definitions
- [references/egrid-factors.md](references/egrid-factors.md) — EPA eGRID emission factors by region
