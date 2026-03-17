---
name: customer-communications
description: Generates customer-facing communications for energy utilities including rate change notices, outage notifications, demand response enrollment, and bill explanations. Use when drafting customer letters, emails, or regulatory notices.
---

# Customer Communications

Generates customer-facing communications for retail energy providers. Uses templates with placeholders; fill from `main.sourabh_energy_workshop` or user input.

## When to Use

- User asks for rate change notice, outage notification, or bill explanation
- User needs demand response (DR) enrollment letter or email
- User wants to draft customer-facing communications
- User mentions regulatory notice, customer letter, or outreach template

## Available Templates

| Template | Use Case | Path |
|----------|----------|------|
| Rate Change Notice | Tariff/rate updates, effective date | [rate-change-notice.md](assets/templates/rate-change-notice.md) |
| Outage Notification | Planned/unplanned outage alerts | [outage-notification.md](assets/templates/outage-notification.md) |
| DR Enrollment | Demand response program sign-up | [dr-enrollment.md](assets/templates/dr-enrollment.md) |
| Bill Explanation | Bill breakdown, usage summary | [bill-explanation.md](assets/templates/bill-explanation.md) |

## Data Sources

- `raw_customers` — Customer name, address, state, rate_class
- `raw_billing` — Billing period, amounts, usage
- `raw_outages` — Outage times, affected areas
- `raw_demand_response` — DR program details

## Template Variables

| Variable | Source | Example |
|----------|--------|---------|
| `{{customer_name}}` | raw_customers | Jane Smith |
| `{{service_address}}` | raw_customers | 42 Collins St, Melbourne VIC 3000 |
| `{{state}}` | raw_customers | VIC |
| `{{rate_class}}` | raw_customers | R1 |
| `{{effective_date}}` | User/rate filing | 2025-04-01 |
| `{{outage_start}}` | raw_outages | 2:00 PM |
| `{{billing_period}}` | raw_billing | March 2025 |

## Workflow

1. Identify template from use case
2. Load template from `assets/templates/`
3. Resolve placeholders from schema or user input
4. Customize tone/length per channel (email vs letter)

## Edge Cases

- **Regulatory requirements**: Rate change notices may need specific language; check state energy ombudsman rules
- **Outage severity**: Use different templates for planned vs emergency outages
- **Multi-language**: Templates are English; add translations if required

## Template Locations

- [assets/templates/rate-change-notice.md](assets/templates/rate-change-notice.md)
- [assets/templates/outage-notification.md](assets/templates/outage-notification.md)
- [assets/templates/dr-enrollment.md](assets/templates/dr-enrollment.md)
- [assets/templates/bill-explanation.md](assets/templates/bill-explanation.md)
