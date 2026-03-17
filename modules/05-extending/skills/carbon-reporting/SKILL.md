---
name: carbon-reporting
description: Calculates Scope 1/2/3 emissions, applies Australian Clean Energy Regulator NGA factors, and supports ESG reporting frameworks. Use when computing carbon footprint, emissions from electricity consumption, or preparing sustainability/ESG reports.
---

# Carbon Reporting

Calculates greenhouse gas (GHG) emissions for energy utilities using Scope 1/2/3 definitions, Australian Clean Energy Regulator NGA (National Greenhouse Accounts) emission factors, and ESG frameworks. Data schema: `main.sourabh_energy_workshop`.

## When to Use

- User asks about Scope 1, 2, or 3 emissions
- User needs carbon footprint or GHG calculations
- User mentions NGA factors, emission factors, or state emissions
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
Scope 2 Emissions (kg CO2e) = Consumption (kWh) × NGA Factor (kg CO2e/kWh)
```

## NGA Emission Factors by State (NEM)

| State | kg CO2e/kWh |
|-------|-------------|
| NSW | 0.79 |
| VIC | 0.98 |
| QLD | 0.81 |
| SA | 0.35 |
| WA | 0.69 |
| TAS | 0.15 |

**Note:** NSW, VIC, QLD, SA, and TAS are in the NEM (National Electricity Market). WA operates the separate SWIS (South West Interconnected System); use WA factors for Western Australian customers.

See [egrid-factors.md](references/egrid-factors.md) for full Australian Clean Energy Regulator NGA factors.

## SQL: Scope 2 from Consumption

```sql
-- Map states to NGA emission factors and calculate Scope 2
WITH consumption AS (
  SELECT
    c.state,
    SUM(m.kwh) AS total_kwh
  FROM main.sourabh_energy_workshop.raw_meter_readings m
  JOIN main.sourabh_energy_workshop.raw_customers c ON m.customer_id = c.customer_id
  WHERE m.reading_date >= DATE_SUB(CURRENT_DATE(), 365)
  GROUP BY c.state
),
nga AS (
  SELECT state, kg_co2e_per_kwh
  FROM (VALUES
    ('NSW', 0.79),
    ('VIC', 0.98),
    ('QLD', 0.81),
    ('SA', 0.35),
    ('WA', 0.69),
    ('TAS', 0.15)
  ) AS t(state, kg_co2e_per_kwh)
)
SELECT
  cons.state,
  cons.total_kwh,
  n.kg_co2e_per_kwh,
  cons.total_kwh * n.kg_co2e_per_kwh AS scope2_kg_co2e
FROM consumption cons
JOIN nga n ON cons.state = n.state;
```

## ESG Frameworks

- **GHG Protocol**: Corporate Standard for Scope 1/2/3
- **CDP**: Carbon Disclosure Project questionnaires
- **GRI**: Global Reporting Initiative 305 (Emissions)
- **SASB**: Sustainability Accounting Standards Board utilities standard

## Edge Cases

- **Market-based vs location-based**: Location-based uses grid average (NGA factors); market-based uses contractual instruments (RECs, PPAs)
- **Time granularity**: Hourly factors improve accuracy; annual averages are common for reporting
- **State mapping**: Map `main.sourabh_energy_workshop.raw_customers.state` to NGA emission factors
- **NEM vs SWIS**: WA is not in the NEM; use WA-specific factors for Western Australian customers

## Additional Resources

- [references/emissions-definitions.md](references/emissions-definitions.md) — Scope 1/2/3 definitions
- [references/egrid-factors.md](references/egrid-factors.md) — Australian Clean Energy Regulator NGA emission factors by state
