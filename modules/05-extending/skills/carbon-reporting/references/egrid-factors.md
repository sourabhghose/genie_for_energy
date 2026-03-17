# EPA eGRID Emission Factors

EPA eGRID (Emissions & Generation Resource Integrated Database) provides emission factors for U.S. electricity by subregion. Values below are illustrative; use the latest eGRID release for reporting.

## Mapping: Workshop Regions → eGRID Subregions

| main.sourabh_energy_workshop.region | eGRID Subregion | kg CO2e/MWh (approx) |
|------------------------------------|-----------------|----------------------|
| Northeast | NEWE (New England), NYCW (NYC/Westchester) | 250–350 |
| Southeast | SRMV (SERC Mississippi Valley), SRTV, SRVC | 450–550 |
| Midwest | MROW (MRO West), MRCW, SRMW | 550–750 |
| Southwest | AZNM (Arizona/New Mexico), ERCT (Texas) | 350–450 |
| Northwest | NWPP (Northwest) | 200–350 |

## eGRID Subregion Reference (Simplified)

| Subregion | Name | kg CO2e/MWh |
|-----------|------|-------------|
| NEWE | New England | ~280 |
| NYCW | NYC/Westchester | ~320 |
| SRMV | SERC Mississippi Valley | ~520 |
| SRTV | SERC Tennessee Valley | ~480 |
| SRVC | SERC Virginia/Carolina | ~450 |
| MROW | MRO West | ~650 |
| MRCW | MRO Central | ~720 |
| SRMW | SERC Midwest | ~680 |
| AZNM | Arizona/New Mexico | ~400 |
| ERCT | Texas (ERCOT) | ~420 |
| NWPP | Northwest | ~280 |

## Usage in SQL

```sql
-- Example: Create region-to-eGRID mapping table
CREATE OR REPLACE TABLE main.sourabh_energy_workshop.egrid_factors (
  region STRING,
  egrid_subregion STRING,
  kg_co2e_per_mwh DOUBLE
);

INSERT INTO main.sourabh_energy_workshop.egrid_factors VALUES
  ('Northeast', 'NEWE', 280),
  ('Southeast', 'SRMV', 520),
  ('Midwest', 'MROW', 650),
  ('Southwest', 'AZNM', 400),
  ('Northwest', 'NWPP', 280);
```

## Data Source

- **EPA eGRID**: https://www.epa.gov/egrid
- Update factors when new eGRID release is published (typically every 2 years)
- Use `CO2` or `CO2e` (CO2 equivalent) per reporting requirement
