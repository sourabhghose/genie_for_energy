# Australian Energy Regulatory Standards

Summary of key Australian Energy Market Operator (AEMO) and Australian Energy Regulator (AER) standards relevant to retail energy providers and distribution network service providers (DNSPs).

## NER — National Electricity Rules

| Chapter | Description |
|---------|-------------|
| Chapter 4 | Power system security — generator and network operator obligations |
| Chapter 5 | Network connections and access — connection standards, network planning |
| Chapter 6 | Distribution network pricing and economic regulation |
| Chapter 6A | Transmission network pricing and economic regulation |
| Chapter 7 | Metering — smart meter standards, data management |

**Relevance:** The NER governs the NEM (National Electricity Market) covering NSW, VIC, QLD, SA, and TAS. WA operates under the Wholesale Electricity Market (WEM) rules.

---

## AER — Distribution Reliability Standards

| Standard | Description |
|----------|-------------|
| SAIDI limits | State-specific annual SAIDI targets set by AER |
| SAIFI limits | State-specific annual SAIFI targets set by AER |
| GSL payments | Guaranteed Service Level payments for prolonged outages |
| Annual reporting | DNSPs report reliability performance to AER annually |

**Relevance:** Each DNSP has regulatory targets for SAIDI and SAIFI. Exceeding targets may trigger AER review or penalty.

---

## AEMO — Market and System Operations

| Function | Description |
|----------|-------------|
| System security | Real-time management of power system stability |
| Demand forecasting | ESOO (Electricity Statement of Opportunities) |
| Event classification | Major event day (MED) methodology |
| Market operations | Dispatch, pricing, settlement for NEM participants |

**Relevance:** AEMO classifies major event days (MEDs) which may be excluded from SAIDI/SAIFI reporting. AEMO also publishes demand forecasts used for capacity planning.

---

## AEMC — Rule Making

| Function | Description |
|----------|-------------|
| Rule changes | National Electricity Rule change process |
| Reliability standard | Unserved energy standard (currently 0.002%) |
| Review process | Regular review of market rules and frameworks |

**Relevance:** The Australian Energy Market Commission (AEMC) sets the reliability standard and reviews market rules.

---

## Distribution-Level Considerations

Retail energy providers and DNSPs in Australia typically:

- Report reliability metrics (SAIDI, SAIFI) to the AER annually
- Follow state-specific outage reporting rules and GSL obligations
- Comply with NER Chapter 7 metering standards
- Use AEMO MED methodology for major event exclusions
- Classify outages per AER cause code categories

---

## Cause Code Alignment

Common cause codes for `raw_outages.cause`:

| Code | Description |
|------|-------------|
| weather | Weather-related (storm, wind, lightning, heat) |
| equipment_failure | Equipment failure (transformer, cable, switch) |
| animal | Animal contact (possum, bird, snake) |
| vegetation | Tree contact, vegetation encroachment |
| planned_maintenance | Planned maintenance (excluded from SAIDI/SAIFI) |
| unknown | Unknown or under investigation |
