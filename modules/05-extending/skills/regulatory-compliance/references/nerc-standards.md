# NERC Reliability Standards

Summary of key North American Electric Reliability Corporation (NERC) standards relevant to retail energy providers and distribution utilities.

## CIP — Critical Infrastructure Protection

| Standard | Description |
|----------|-------------|
| CIP-002 | Identify and classify Critical Cyber Assets |
| CIP-003 | Security management controls |
| CIP-005 | Electronic security perimeters |
| CIP-006 | Physical security of Critical Cyber Assets |
| CIP-007 | Systems security management |
| CIP-008 | Incident reporting and response planning |

**Relevance:** Protects grid cyber and physical assets. Applies to entities with Bulk Electric System (BES) assets.

---

## TPL — Transmission Planning

| Standard | Description |
|----------|-------------|
| TPL-001 | Transmission system planning performance |
| TPL-002 | Transmission system planning performance – extreme events |

**Relevance:** Ensures transmission planning meets reliability criteria. Distribution utilities may have obligations under interconnection agreements.

---

## PRC — Protection and Control

| Standard | Description |
|----------|-------------|
| PRC-002 | Disturbance monitoring and reporting |
| PRC-004 | Protection system misoperations |
| PRC-005 | Protection system maintenance |

**Relevance:** Protection system performance and reporting. Affects outage cause classification and root cause analysis.

---

## EOP — Emergency Operations

| Standard | Description |
|----------|-------------|
| EOP-002 | Capacity and energy emergency |
| EOP-004 | Event reporting |
| EOP-006 | Reliability coordination – system restoration |

**Relevance:** Emergency procedures and event reporting. Aligns with outage notification and restoration protocols.

---

## Distribution-Level Considerations

Retail energy providers and distribution utilities typically:

- Report reliability metrics (SAIDI, SAIFI) to state PUCs
- Follow state-specific outage reporting rules
- May have NERC obligations if they own/operate BES assets
- Use NERC cause codes for outage classification where applicable

---

## Cause Code Alignment

Common cause codes for `raw_outages.cause_code`:

| Code | Description |
|------|-------------|
| WEATHER | Weather-related (storm, wind, ice) |
| EQUIPMENT | Equipment failure |
| ANIMAL | Animal contact |
| VEGETATION | Tree contact, vegetation |
| HUMAN | Human error, excavation damage |
| PLANNED | Planned maintenance (excluded from SAIDI/SAIFI) |
