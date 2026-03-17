# Energy Data Dictionary

Column descriptions for tables in `main.sourabh_energy_workshop`. Schema supports a retail energy provider with ~50K customers across 5 regions (Northeast, Southeast, Midwest, Southwest, Northwest).

---

## raw_customers

| Column | Type | Description |
|--------|------|-------------|
| customer_id | STRING | Unique customer identifier |
| region | STRING | One of: Northeast, Southeast, Midwest, Southwest, Northwest |
| customer_type | STRING | residential, commercial, industrial |
| service_address | STRING | Physical service location |
| meter_id | STRING | Associated meter identifier |
| rate_class | STRING | Rate tariff class (e.g., R1, C1, I1) |
| enrollment_date | DATE | Customer enrollment/start date |
| churn_rate | DOUBLE | Annual churn probability (0–1) |
| created_at | TIMESTAMP | Record creation timestamp |
| updated_at | TIMESTAMP | Last update timestamp |

---

## raw_meter_readings

| Column | Type | Description |
|--------|------|-------------|
| reading_id | STRING | Unique reading identifier |
| customer_id | STRING | References raw_customers.customer_id |
| meter_id | STRING | Meter identifier |
| reading_date | DATE | Date of reading |
| reading_time | STRING | Time of reading (HH:mm) |
| kwh | DOUBLE | Kilowatt-hours consumed |
| demand_kw | DOUBLE | Peak demand in kW (if applicable) |
| power_factor | DOUBLE | Power factor (0–1) |
| source | STRING | manual, ami, estimated |
| created_at | TIMESTAMP | Record creation timestamp |

---

## raw_billing

| Column | Type | Description |
|--------|------|-------------|
| billing_id | STRING | Unique billing record identifier |
| customer_id | STRING | References raw_customers.customer_id |
| billing_period_start | DATE | Billing period start date |
| billing_period_end | DATE | Billing period end date |
| delivered_kwh | DOUBLE | Total kWh delivered to customer |
| billed_kwh | DOUBLE | Total kWh billed (may differ due to losses, adjustments) |
| total_amount | DOUBLE | Total bill amount in currency |
| demand_charge | DOUBLE | Demand charge component |
| energy_charge | DOUBLE | Energy charge component |
| taxes_fees | DOUBLE | Taxes and fees |
| status | STRING | pending, paid, overdue, disputed |
| created_at | TIMESTAMP | Record creation timestamp |

---

## raw_outages

| Column | Type | Description |
|--------|------|-------------|
| outage_id | STRING | Unique outage identifier |
| customer_id | STRING | References raw_customers.customer_id |
| outage_start | TIMESTAMP | Outage start time |
| outage_end | TIMESTAMP | Outage end time |
| customer_minutes_interrupted | INT | Customer-minutes of interruption |
| outage_type | STRING | unplanned, planned, maintenance |
| cause_code | STRING | Root cause classification |
| equipment_id | STRING | Related equipment (if applicable) |
| region | STRING | Region (denormalized for analytics) |
| created_at | TIMESTAMP | Record creation timestamp |

---

## raw_weather

| Column | Type | Description |
|--------|------|-------------|
| weather_id | STRING | Unique weather record identifier |
| region | STRING | Geographic region |
| observation_date | DATE | Date of observation |
| avg_temp_f | DOUBLE | Average temperature (Fahrenheit) |
| max_temp_f | DOUBLE | Maximum temperature (Fahrenheit) |
| min_temp_f | DOUBLE | Minimum temperature (Fahrenheit) |
| precipitation_in | DOUBLE | Precipitation in inches |
| humidity_pct | DOUBLE | Relative humidity (0–100) |
| cooling_degree_days | INT | Cooling degree days |
| heating_degree_days | INT | Heating degree days |
| created_at | TIMESTAMP | Record creation timestamp |

---

## raw_equipment

| Column | Type | Description |
|--------|------|-------------|
| equipment_id | STRING | Unique equipment identifier |
| equipment_type | STRING | transformer, switchgear, meter, etc. |
| region | STRING | Geographic region |
| installation_date | DATE | Installation date |
| last_inspection_date | DATE | Last inspection date |
| condition_score | STRING | good, fair, poor, critical |
| capacity_kva | DOUBLE | Rated capacity in kVA |
| age_years | INT | Age in years |
| created_at | TIMESTAMP | Record creation timestamp |
| updated_at | TIMESTAMP | Last update timestamp |

---

## raw_demand_response

| Column | Type | Description |
|--------|------|-------------|
| dr_event_id | STRING | Unique demand response event identifier |
| event_id | STRING | Event grouping identifier |
| customer_id | STRING | References raw_customers.customer_id |
| event_start | TIMESTAMP | Event start time |
| event_end | TIMESTAMP | Event end time |
| baseline_kwh | DOUBLE | Baseline consumption (kWh) |
| actual_kwh | DOUBLE | Actual consumption during event (kWh) |
| event_status | STRING | scheduled, completed, cancelled, no_show |
| incentive_amount | DOUBLE | Incentive paid (if applicable) |
| created_at | TIMESTAMP | Record creation timestamp |
