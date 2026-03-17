# Bill Explanation

**Template:** Bill Explanation  
**Use:** Explain bill components, usage summary, or answer "why is my bill high?"  
**Channel:** Letter, Email, In-app

---

## Your Bill Explained – {{billing_period}}

Dear {{customer_name}},

Here’s a breakdown of your electricity bill for **{{billing_period}}** ({{billing_period_start}} – {{billing_period_end}}).

### Usage Summary

| Metric | This Period | Last Period | Change |
|--------|-------------|-------------|--------|
| **kWh Used** | {{kwh_used}} | {{kwh_prior}} | {{kwh_change}} |
| **Peak Demand (kW)** | {{peak_demand}} | {{peak_demand_prior}} | {{demand_change}} |
| **Days in Period** | {{days_in_period}} | {{days_prior}} | — |

### Bill Breakdown

| Component | Amount | Description |
|-----------|--------|-------------|
| **Energy Charge** | {{energy_charge}} | {{kwh_used}} kWh × {{energy_rate}}/kWh |
| **Demand Charge** | {{demand_charge}} | {{peak_demand}} kW × {{demand_rate}}/kW |
| **Taxes & Fees** | {{taxes_fees}} | State/local taxes, regulatory fees |
| **Total** | **{{total_amount}}** | |

### Why Did My Bill Change?

{{explanation}}

- **Usage:** {{usage_explanation}} (e.g., higher cooling due to warmer weather)
- **Rates:** {{rate_explanation}} (e.g., no rate change this period)
- **Days:** {{days_explanation}} (e.g., 31 days vs 30 last month)

### Compare to Similar Customers

Your usage compared to similar {{rate_class}} customers in {{region}}:

| Comparison | Your Usage | Typical |
|------------|------------|---------|
| kWh/month | {{kwh_used}} | {{typical_kwh}} |
| Percentile | {{percentile}} | — |

### Tips to Save

- **Peak hours:** Shift usage to off-peak when possible
- **Programs:** Enroll in demand response or time-of-use rates
- **Efficiency:** Check rebates for efficient appliances at {{rebates_url}}

### Questions?

- **Portal:** {{portal_url}}  
- **Phone:** {{contact_phone}}  
- **Email:** {{contact_email}}

Thank you for being a customer.

{{utility_name}}
