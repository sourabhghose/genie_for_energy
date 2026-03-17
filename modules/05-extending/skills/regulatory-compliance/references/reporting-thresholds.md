# Regulatory Reporting Thresholds

Thresholds for energy utility regulatory reporting. Values are illustrative; verify against applicable state and federal requirements.

## Reliability Metrics

| Metric | Threshold | Action |
|--------|-----------|--------|
| SAIDI | > 90 min/customer/year | Report to state PUC; may trigger corrective action plan |
| SAIFI | > 1.2 events/customer/year | Report to state PUC |
| CAIDI | > 90 min/event | Review restoration practices |

## Major Event Exclusion

Events that may be excluded from SAIDI/SAIFI (jurisdiction-dependent):

| Criterion | Threshold |
|-----------|-----------|
| Duration | > 4 hours average |
| Customer impact | > 10% of customers in affected area |
| Cause | Typically weather or external event |

**Note:** Exclusions must be documented and reported. Some states do not allow major event exclusions.

## Outage Reporting

| Condition | Threshold | Action |
|-----------|------------|--------|
| Single outage duration | > 8 hours | Mandatory root cause analysis and report |
| Widespread outage | > 5,000 customers | Expedited notification to regulator |
| Fatality or serious injury | Any | Immediate report |

## Data Quality

| Requirement | Description |
|-------------|-------------|
| Outage start/end | Must be recorded for all unplanned outages |
| Customer count | Must match served customers in affected area |
| Cause code | Required for all outages |

## Schema Alignment

For `main.sourabh_energy_workshop`:

- `raw_outages.outage_type` — Filter `unplanned` for SAIDI/SAIFI
- `raw_outages.customer_minutes_interrupted` — Used in SAIDI numerator
- `raw_outages.outage_start`, `raw_outages.outage_end` — For duration and major event checks
