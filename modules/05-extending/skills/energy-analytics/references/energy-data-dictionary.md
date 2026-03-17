# Energy Data Dictionary

Column descriptions for tables in `main.sourabh_energy_workshop`. Schema supports a retail energy provider with ~50K customers across 6 Australian states (NSW, VIC, QLD, SA, WA, TAS). Coordinates (latitude/longitude) are available where applicable.

---

## raw_customers

| Column | Type | Description |
|--------|------|-------------|
| account_id | STRING | Unique customer identifier |
| customer_name | STRING | Customer name |
| street_address | STRING | Street address |
| city | STRING | City |
| state | STRING | One of: NSW, VIC, QLD, SA, WA, TAS |
| postcode | STRING | Australian postcode |
| customer_type | STRING | residential, commercial, industrial |
| rate_plan | STRING | flat, time_of_use, demand, solar_feed_in |
| signup_date | DATE | Customer signup/start date |
| contract_end_date | DATE | Contract end date |
| has_solar | BOOLEAN | Whether customer has solar |
| has_ev | BOOLEAN | Whether customer has EV |
| demand_response_enrolled | BOOLEAN | Enrolled in demand response |
| latitude | DOUBLE | Latitude coordinate |
| longitude | DOUBLE | Longitude coordinate |

---

## raw_meter_readings

| Column | Type | Description |
|--------|------|-------------|
| meter_id | STRING | Meter identifier |
| customer_id | STRING | References raw_customers.account_id |
| timestamp | TIMESTAMP | Reading timestamp |
| kwh_consumed | DOUBLE | Kilowatt-hours consumed |
| voltage | DOUBLE | Voltage (230V nominal) |
| power_factor | DOUBLE | Power factor (0–1) |
| is_peak_hour | BOOLEAN | Whether reading is during peak hours |

---

## raw_billing

| Column | Type | Description |
|--------|------|-------------|
| bill_id | STRING | Unique billing record identifier |
| customer_id | STRING | References raw_customers.account_id |
| billing_period | STRING | Billing period |
| total_kwh | DOUBLE | Total kWh consumed |
| peak_kwh | DOUBLE | Peak period kWh |
| off_peak_kwh | DOUBLE | Off-peak period kWh |
| amount_charged | DOUBLE | Amount charged (AUD) |
| amount_paid | DOUBLE | Amount paid (AUD) |
| payment_date | DATE | Payment date |
| balance | DOUBLE | Outstanding balance |
| is_delinquent | BOOLEAN | Whether account is delinquent |

---

## raw_outages

| Column | Type | Description |
|--------|------|-------------|
| outage_id | STRING | Unique outage identifier |
| state | STRING | Australian state (NSW, VIC, QLD, SA, WA, TAS) |
| start_time | TIMESTAMP | Outage start time |
| end_time | TIMESTAMP | Outage end time |
| duration_minutes | INT | Duration in minutes |
| cause | STRING | Root cause classification |
| affected_meters_count | INT | Number of affected meters |
| restoration_priority | STRING | Restoration priority |
| latitude | DOUBLE | Latitude coordinate |
| longitude | DOUBLE | Longitude coordinate |

---

## raw_weather

| Column | Type | Description |
|--------|------|-------------|
| date | DATE | Observation date |
| state | STRING | Australian state |
| temp_high_c | DOUBLE | Maximum temperature (Celsius) |
| temp_low_c | DOUBLE | Minimum temperature (Celsius) |
| humidity | DOUBLE | Relative humidity |
| wind_speed_kmh | DOUBLE | Wind speed (km/h) |
| precipitation_mm | DOUBLE | Precipitation (mm) |
| is_extreme_heat | BOOLEAN | >38°C |
| is_extreme_cold | BOOLEAN | <2°C |

---

## raw_equipment

| Column | Type | Description |
|--------|------|-------------|
| equipment_id | STRING | Unique equipment identifier |
| equipment_type | STRING | transformer, switchgear, meter, etc. |
| state | STRING | Australian state |
| install_date | DATE | Installation date |
| last_maintenance_date | DATE | Last maintenance date |
| maintenance_count | INT | Number of maintenance events |
| failure_count | INT | Number of failures |
| capacity_rating | INT | Rated capacity |
| current_load_pct | DOUBLE | Current load percentage |
| latitude | DOUBLE | Latitude coordinate |
| longitude | DOUBLE | Longitude coordinate |

---

## raw_demand_response

| Column | Type | Description |
|--------|------|-------------|
| event_id | STRING | Unique demand response event identifier |
| customer_id | STRING | References raw_customers.account_id |
| event_date | DATE | Event date |
| event_type | STRING | curtailment, shift, shed |
| target_reduction_kwh | DOUBLE | Target reduction (kWh) |
| actual_reduction_kwh | DOUBLE | Actual reduction (kWh) |
| incentive_paid | DOUBLE | Incentive paid (AUD) |
| participated | BOOLEAN | Whether customer participated |
