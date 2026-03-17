# Australian NGA Emission Factors

Australian Clean Energy Regulator National Greenhouse Accounts (NGA) emission factors for electricity by state. Values below are illustrative; use the latest NGA release for reporting.

## Mapping: Workshop States → NGA Emission Factors

| main.sourabh_energy_workshop.state | Grid | kg CO2e/kWh (approx) | Notes |
|------------------------------------|------|----------------------|-------|
| NSW | NEM | 0.79 | Black coal dominant |
| VIC | NEM | 0.98 | Brown coal (Latrobe Valley) |
| QLD | NEM | 0.81 | Mix of coal and gas |
| SA | NEM | 0.35 | High wind and solar penetration |
| WA | SWIS | 0.69 | Gas and coal (not in NEM) |
| TAS | NEM | 0.15 | Predominantly hydro |

## Australian Electricity Grids

| Grid | Name | Coverage |
|------|------|----------|
| NEM | National Electricity Market | NSW, VIC, QLD, SA, TAS |
| SWIS | South West Interconnected System | WA (Perth region) |
| NWIS | North West Interconnected System | WA (Pilbara) |

## Usage in SQL

```sql
-- Create state-to-emission-factor mapping table
CREATE OR REPLACE TABLE main.sourabh_energy_workshop.emission_factors (
  state STRING,
  grid STRING,
  kg_co2e_per_kwh DOUBLE
);

INSERT INTO main.sourabh_energy_workshop.emission_factors VALUES
  ('NSW', 'NEM', 0.79),
  ('VIC', 'NEM', 0.98),
  ('QLD', 'NEM', 0.81),
  ('SA',  'NEM', 0.35),
  ('WA',  'SWIS', 0.69),
  ('TAS', 'NEM', 0.15);
```

## Data Source

- **Australian Clean Energy Regulator NGA**: https://www.cleanenergyregulator.gov.au/
- **Department of Climate Change, Energy, the Environment and Water**: National Greenhouse Accounts Factors
- Update factors when new NGA release is published (typically annually)
- Use Scope 2 (indirect emissions from purchased electricity) for consumption-based reporting
