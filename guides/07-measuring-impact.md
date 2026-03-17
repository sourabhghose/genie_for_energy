# Module 7: Measuring Genie Code Impact (30 min)

**Context:** System tables for Genie Code usage, pre-built impact dashboard, and an impact metrics framework.

---

## 7A: System Table Queries (15 min)

### Overview
Databricks system tables capture Genie Code usage—interactions, users, workspaces. You can query these to measure adoption and engagement.

### Prerequisites
- Access to the `07_system_table_queries` notebook in the workshop
- Permissions to query system tables (typically workspace admin or analytics role)

### Step-by-Step Instructions

**Step 1:** Open the 07_system_table_queries notebook
- Navigate to your workspace
- Open the notebook: `07_system_table_queries` (or the path provided by your facilitator)

**Step 2:** Run Query 1 - Total interactions this week
Execute the following in a notebook cell:

```sql
SELECT COUNT(*) AS total_interactions
FROM system.genie_code.interactions
WHERE event_timestamp >= current_timestamp() - INTERVAL 7 DAY
```

**Expected results:**
- A single row with `total_interactions` (e.g., 1,247)
- Represents all Genie Code interactions in the last 7 days

---

**Step 3:** Run Query 2 - Top 10 users
Execute:

```sql
SELECT user_identity, COUNT(*) AS interaction_count
FROM system.genie_code.interactions
WHERE event_timestamp >= current_timestamp() - INTERVAL 30 DAY
GROUP BY user_identity
ORDER BY interaction_count DESC
LIMIT 10
```

**Expected results:**
- A table of the top 10 users by interaction count
- Use for identifying power users and adoption champions

---

**Step 4:** Run Query 3 - Daily active user trend
Execute:

```sql
SELECT DATE(event_timestamp) AS date, COUNT(DISTINCT user_identity) AS daily_active_users
FROM system.genie_code.interactions
WHERE event_timestamp >= current_timestamp() - INTERVAL 30 DAY
GROUP BY DATE(event_timestamp)
ORDER BY date
```

**Expected results:**
- A time series of daily active users
- Useful for tracking adoption trends over time

---

**Step 5:** Run Query 4 - Usage by workspace
Execute:

```sql
SELECT workspace_id, COUNT(*) AS interaction_count
FROM system.genie_code.interactions
WHERE event_timestamp >= current_timestamp() - INTERVAL 30 DAY
GROUP BY workspace_id
ORDER BY interaction_count DESC
```

**Expected results:**
- Interaction counts per workspace
- Helps identify which workspaces are adopting Genie Code most

---

**Step 6:** Create a simple dashboard from these queries
- In Databricks, go to **SQL** → **Dashboards**
- Click **Create dashboard** → **Create blank**
- Add 4 widgets:
  1. **Single value:** Query 1 (total interactions)
  2. **Bar chart:** Query 2 (top 10 users)
  3. **Line chart:** Query 3 (daily active users)
  4. **Bar chart:** Query 4 (usage by workspace)
- Name the dashboard: "Genie Code Impact - [Your Workshop]"

### Key Concepts
| System Table | Purpose |
|--------------|---------|
| `system.genie_code.interactions` | Records each Genie Code interaction (prompts, responses, etc.) |
| `event_timestamp` | When the interaction occurred |
| `user_identity` | User who triggered the interaction |
| `workspace_id` | Workspace where the interaction occurred |

### Practical Tips
- Adjust time windows (7 days, 30 days) based on your reporting needs
- Combine with other system tables (e.g., `system.billing.usage`) for cost correlation
- Schedule the notebook to run daily and append to a summary table for historical trends

---

## 7B: Import Impact Dashboard (10 min)

### Overview
A pre-built dashboard provides a comprehensive view of Genie Code impact metrics. You will import it from GitHub and explore it.

### Step-by-Step Instructions

**Step 1:** Download the pre-built dashboard JSON
- Navigate to the workshop GitHub repository (link provided by facilitator)
- Example: `https://github.com/databricks/genie-code-energy-workshop/blob/main/dashboards/genie_code_impact_dashboard.json`
- Download the JSON file (or use **Raw** → Save As)

**Step 2:** Import into your workspace
- In Databricks, go to **SQL** → **Dashboards**
- Click **New** → **Import dashboard**
- Select the downloaded `genie_code_impact_dashboard.json` file
- Choose the target folder/location
- Click **Import**

**Step 3:** Explore the dashboard
- Open the imported dashboard
- Review the widgets:
  - **Adoption:** Total users, new users, interaction counts
  - **Engagement:** Sessions per user, prompts per session
  - **Trends:** Weekly/monthly charts
  - **Top users/workspaces:** Leaderboards
- Note any filters (date range, workspace) and adjust as needed

**Step 4:** Verify data sources
- Click **Edit** on the dashboard
- Check that each widget's query points to the correct system tables
- If your workspace uses a different schema, update the table references

### Key Concepts
- Pre-built dashboards accelerate reporting
- JSON export/import allows sharing across workspaces
- System table schema may vary by Databricks version—verify column names

### Practical Tips
- Clone the dashboard before making changes
- Add a "Last refreshed" timestamp widget
- Share the dashboard link with stakeholders for self-service reporting

---

## 7C: Impact Metrics Framework (5 min)

### Overview
A structured framework for measuring Genie Code impact across adoption, engagement, and productivity.

### Adoption Metrics (from system tables)

| Metric | Source | Description |
|--------|--------|-------------|
| **Total interactions** | `system.genie_code.interactions` | Count of all Genie Code prompts/responses |
| **Unique users** | `COUNT(DISTINCT user_identity)` | Number of users who used Genie Code |
| **Daily/Weekly active users** | Group by date | Adoption trend over time |
| **Workspace penetration** | Users per workspace / Total users | % of workspaces with Genie Code usage |

### Engagement Metrics (from survey)

| Metric | How to collect | Description |
|--------|-----------------|-------------|
| **Sessions per week** | Survey | How often users open Genie Code |
| **Tasks completed** | Survey | "How many tasks did Genie Code help you complete?" |
| **Satisfaction (NPS/CSAT)** | Survey | User satisfaction with Genie Code |

### Productivity Metrics (from survey)

| Metric | How to collect | Description |
|--------|-----------------|-------------|
| **Time saved** | Survey | "How much time did Genie Code save you per week?" |
| **Tasks accelerated** | Survey | "Which tasks were faster with Genie Code?" |
| **Quality improvement** | Survey | "Did Genie Code improve your output quality?" |

### Survey Template

Provide this template to participants for post-workshop feedback:

```markdown
## Genie Code Impact Survey

1. How often did you use Genie Code in the past week?
   - [ ] Daily  [ ] 3-4 times  [ ] 1-2 times  [ ] Not at all

2. How many tasks did Genie Code help you complete?
   - [ ] 0  [ ] 1-3  [ ] 4-10  [ ] 10+

3. How much time did Genie Code save you per week? (estimate)
   - [ ] None  [ ] 1-2 hours  [ ] 3-5 hours  [ ] 5+ hours

4. Which tasks were most accelerated? (select all that apply)
   - [ ] Writing SQL  [ ] Building pipelines  [ ] Creating dashboards
   - [ ] Debugging  [ ] Documentation  [ ] Other: _______

5. How satisfied are you with Genie Code? (1-5)
   - 1 (Not satisfied) ... 5 (Very satisfied)

6. What would make Genie Code more valuable for you?
   - Free text: _______
```

### Key Concepts
- **System tables** = quantitative, automatic
- **Surveys** = qualitative, self-reported
- Combine both for a complete impact story

### Practical Tips
- Run the survey 2–4 weeks after the workshop for meaningful feedback
- Correlate survey responses with system table data (e.g., high users = high satisfaction?)
- Use impact metrics in business reviews and ROI discussions

---

## Summary Checklist

- [ ] Ran Query 1: Total interactions this week
- [ ] Ran Query 2: Top 10 users
- [ ] Ran Query 3: Daily active user trend
- [ ] Ran Query 4: Usage by workspace
- [ ] Created a simple dashboard with the 4 queries
- [ ] Downloaded and imported the pre-built impact dashboard
- [ ] Explored the dashboard widgets
- [ ] Reviewed the impact metrics framework (adoption, engagement, productivity)
- [ ] Saved or shared the survey template for post-workshop feedback
