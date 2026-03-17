# Module 5: Extending Genie Code (75 min)

**Catalog/Schema:** `main.sourabh_energy_workshop`  
**Tables:** raw_customers, raw_meter_readings, raw_billing, raw_outages, raw_weather, raw_equipment, raw_demand_response  
**Skills location:** `/Users/{username}/.assistant/skills/`

![Agent Skills](../images/05-skills-folder.png)
*The 10 energy-specific Agent Skills organized in three tiers: Knowledge, AI Functions, and Creators.*

---

## 5A: Custom Instructions - User Level (15 min)

### Overview
User-level instructions let you customize Genie Code's behavior for your domain. These instructions apply to every response except **Quick Fix** and **Autocomplete**.

### Step-by-Step Instructions

**Step 1:** Open Genie Code settings
- Click the **Genie Code** icon in the left sidebar (or use the keyboard shortcut)
- Click the **gear/settings** icon to open Genie Code settings

**Step 2:** Add your instructions file
- Navigate to **User instructions** section
- Click **"Add instructions file"**
- This creates `.assistant_instructions.md` in your user workspace directory (typically `/Users/{username}/`)

**Step 3:** Add energy-specific instructions
- Open the newly created `.assistant_instructions.md` file
- Paste the following content:

```markdown
## Code Conventions
- Always use PySpark DataFrames for data processing, never pandas for large datasets
- Follow medallion naming: bronze_, silver_, gold_ prefixes
- Use kWh (not kwh or KWH) as the energy unit label
- When showing monetary values, use AUD with 2 decimal places
- Include data quality checks in all transformations
- Prefer Plotly for visualizations, with a dark theme

## Domain Context
- I work at a retail energy provider serving 50K customers across 6 Australian states
- Peak hours are 2pm-7pm weekdays. Off-peak is all other times.
- TOU = Time of Use rate plan. EV = Electric Vehicle rate plan.
- Our fiscal year starts April 1.
```

**Step 4:** Save the file and ensure Genie Code has picked it up
- Save the file (Cmd+S / Ctrl+S)
- Genie Code automatically loads user instructions on startup

**Step 5:** Test before/after behavior
- **Before:** Without instructions, prompt: `Show me the monthly consumption trend for commercial customers`
- **After:** With instructions, run the same prompt:

```
Show me the monthly consumption trend for commercial customers
```

**Expected results:**
- Code should use **PySpark** (not pandas) for data processing
- Tables should reference `main.sourabh_energy_workshop`
- Visualizations should use **Plotly with a dark theme**
- Monetary values formatted as AUD with 2 decimal places
- kWh used consistently as the unit label

### Key Concepts
| Concept | Description |
|---------|-------------|
| **User instructions** | Personal preferences that apply across all your Genie Code sessions |
| **Scope** | Applies to Agent mode, Chat, and inline suggestions—*not* Quick Fix or Autocomplete |
| **File location** | `.assistant_instructions.md` in your user workspace directory |

### Practical Tips
- Keep instructions concise; long instructions consume context window
- Use bullet points for clarity
- Test with a few prompts after adding instructions to verify behavior
- Update instructions as your conventions evolve

---

## 5B: Workspace Instructions (10 min)

### Overview
Workspace instructions are **admin-controlled** and apply to all users in a workspace. They enforce organizational standards.

### Step-by-Step Instructions

**Step 1:** Understand the difference
- **User instructions:** Personal, in your home directory, you control them
- **Workspace instructions:** Set by workspace admins, apply to everyone

**Step 2:** Example workspace instructions (for admins)
If you are an admin configuring workspace instructions, you might add:

```markdown
## Workspace Standards
- All tables must be in workshop_catalog
- Do not use SELECT * in production queries
- All notebooks must include a title cell
- Use Unity Catalog three-level naming: catalog.schema.table
```

**Step 3:** Discussion points
| Scenario | Use User Instructions | Use Workspace Instructions |
|----------|----------------------|----------------------------|
| Personal coding style | ✓ | |
| Company naming conventions | | ✓ |
| Security/compliance rules | | ✓ |
| Domain knowledge (energy) | ✓ | |
| Catalog/schema requirements | | ✓ |

### Key Concepts
- **Workspace instructions** override or complement user instructions
- Admins configure these in workspace settings
- Use workspace instructions for governance; user instructions for productivity

---

## 5C: Agent Skills - 10-Skill Energy Portfolio (45 min)

### 5C.1: Agent Skills Concept (5 min)

**What are Agent Skills?**
- Skills are reusable capability packages that extend Genie Code's knowledge
- Each skill lives in `/Users/{username}/.assistant/skills/`
- Structure: `SKILL.md` (required), optional references, scripts, assets
- **Auto-loaded** contextually in Agent mode
- Can be **@mentioned** explicitly (e.g., `@energy-analytics`)

**Three Tiers:**
| Tier | Type | Examples |
|------|------|----------|
| **Tier 1** | Knowledge | energy-analytics, regulatory-compliance, carbon-reporting |
| **Tier 2** | AI Functions | ai-functions-energy |
| **Tier 3** | Resource Creators | genie-space-creator, dashboard-deployer, job-deployer, pipeline-scaffolder, knowledge-assistant-creator, customer-communications |

---

### 5C.2: Build a Tier 1 Skill Together - energy-analytics (10 min)

**Step 1:** Navigate to the skill directory
```
/Users/{username}/.assistant/skills/energy-analytics/
```

**Step 2:** Open `SKILL.md` and review the structure
- Frontmatter (name, description, triggers)
- Instructions for the model
- Domain context (KPIs, metrics, energy terminology)

**Step 3:** Test the skill - Auto-load
In Genie Code Agent, type:

```
Calculate our Q1 reliability KPIs by state
```

**Expected:** Genie Code should use the energy-analytics skill context to understand reliability KPIs (SAIDI, SAIFI, CAIDI) and query the appropriate tables.

**Step 4:** Test the skill - Explicit @mention
In Genie Code Agent, type:

```
@energy-analytics What is our demand response effectiveness?
```

**Expected:** The skill is explicitly invoked. Response should reference demand response metrics, possibly from `raw_demand_response` and related tables.

**Step 5:** Explain
- `SKILL.md` auto-loads when the prompt matches skill triggers
- @mention forces the skill to load regardless of trigger matching
- Domain context in the skill guides SQL and analysis

---

### 5C.3: Walk Through All 10 Pre-Built Skills (15 min)

For each skill below, **open the SKILL.md** and **run the test prompt** in Genie Code Agent.

| # | Skill | Test Prompt |
|---|-------|-------------|
| 1 | **genie-space-creator** | `Create a Genie Space for our energy billing data` |
| 2 | **dashboard-deployer** | `Deploy our SmartGrid Operations Center dashboard` |
| 3 | **job-deployer** | `Deploy our energy pipeline as a nightly job at 2am` |
| 4 | **pipeline-scaffolder** | `Create a medallion pipeline for meter readings` |
| 5 | **knowledge-assistant-creator** | `Create a Knowledge Assistant for our rate schedule docs` |
| 6 | **ai-functions-energy** | `Forecast next week's energy demand` or `Classify these customer complaints` |
| 7 | **energy-analytics** | `Calculate our Q1 reliability KPIs` |
| 8 | **regulatory-compliance** | `Check if our metrics meet AEMO/AER standards` |
| 9 | **carbon-reporting** | `Calculate our Scope 2 emissions` |
| 10 | **customer-communications** | `Generate rate change notices for residential customers` |

**Expected results:** Each prompt should produce contextually relevant output—SQL, Python, configuration, or natural language—guided by the skill's instructions.

---

### 5C.4: Hands-On Exercises (15 min)

#### Exercise A (Tier 1): Extend energy-analytics with a new KPI

**Task:** Add a new KPI to the energy-analytics skill: **"Revenue per MWh by rate plan"**

**Steps:**
1. Open `/Users/{username}/.assistant/skills/energy-analytics/SKILL.md`
2. Find the KPIs or metrics section
3. Add a new bullet or section:
   ```markdown
   - **Revenue per MWh by rate plan:** Total billing revenue / Total MWh consumed, grouped by rate_plan. Use main.sourabh_energy_workshop.raw_billing and raw_meter_readings.
   ```
4. Save the file
5. Test: `@energy-analytics What is our revenue per MWh by rate plan?`

**Expected:** Genie Code generates a query joining billing and meter data, calculating revenue/MWh by rate plan.

---

#### Exercise B (Tier 2): Add a new ai_classify use case

**Task:** Add a new `ai_classify` use case for **equipment maintenance urgency**

**Steps:**
1. Open `/Users/{username}/.assistant/skills/ai-functions-energy/SKILL.md`
2. Find the ai_classify section
3. Add a new use case:
   ```markdown
   - **Equipment maintenance urgency:** Classify maintenance requests from raw_equipment or work orders into: Critical, High, Medium, Low. Use ai_classify with appropriate labels.
   ```
4. Save the file
5. Test: `@ai-functions-energy Classify these equipment maintenance requests by urgency`

**Expected:** Genie Code suggests an `ai_classify` SQL pattern with labels for maintenance urgency.

---

#### Exercise C (Tier 3): Modify genie-space-creator

**Task:** Add **3 custom sample questions** to the genie-space-creator skill

**Steps:**
1. Open `/Users/{username}/.assistant/skills/genie-space-creator/SKILL.md`
2. Find where sample questions or suggested prompts are defined
3. Add three energy-specific questions, e.g.:
   ```markdown
   - "What was our peak demand last month by state?"
   - "Which customers have the highest demand response participation?"
   - "Show me outage duration by cause code"
   ```
4. Save the file
5. Test: `@genie-space-creator Create a Genie Space for our energy data` — verify the output includes your sample questions

**Expected:** The generated Genie Space configuration or instructions include your custom sample questions.

---

## 5D: MCP Integration (20 min) [If Time Permits]

### Overview
**MCP (Model Context Protocol)** lets Genie Code connect to external tools and data sources as "servers" that expose capabilities.

### Step 1: Explain MCP
- MCP servers expose tools and resources to the AI
- Genie Code can call these tools during a conversation
- Common MCP servers: Genie Space, Unity Catalog Functions, GitHub, Slack

### Step 2: Demo - Connect Genie Space as MCP server
- In Genie Code settings, find **MCP servers** or **Integrations**
- Add a Genie Space as an MCP server (follow Databricks docs for connection details)
- Once connected, you can ask: "Query our Genie Space for billing insights"

### Step 3: Demo - Unity Catalog Functions as MCP tools
- Create a UC function, e.g. `calculate_degree_days(temperature, base_temp)`
- Expose it as an MCP tool
- Prompt: "Calculate degree days for our weather data" — Genie Code can invoke the function

### Step 4: Demo - GitHub MCP server
- Install/configure the GitHub MCP server (see GitHub MCP documentation)
- Enables: "Search our repo for energy pipeline code", "Create a PR for this change"

### Key Concepts
| MCP Component | Purpose |
|---------------|---------|
| **Server** | External service (Genie Space, GitHub, etc.) |
| **Tools** | Callable functions the AI can invoke |
| **Resources** | Read-only data the AI can access |

---

## 5E: Image Upload (5 min)

### Overview
Genie Code can process images—screenshots, diagrams, architecture drawings—and implement what it sees.

### Step-by-Step Instructions

**Step 1:** Prepare an image
- Use a screenshot of a data flow diagram, ERD, or architecture
- Or draw a simple flow: e.g., raw_meter_readings → bronze → silver → gold

**Step 2:** Upload to Genie Code
- In the Genie Code chat/agent input, click the **attachment** or **image** icon
- Select your image file (PNG, JPG supported)

**Step 3:** Prompt with context
```
Implement the data flow shown in this image. Use main.sourabh_energy_workshop tables.
```

**Expected:** Genie Code analyzes the image and generates notebooks, SQL, or pipeline code that matches the depicted flow.

### Practical Tips
- Use clear, high-contrast diagrams
- Add a short text prompt to clarify catalog/schema
- For complex diagrams, break into multiple prompts

---

## Summary Checklist

- [ ] Created and configured `.assistant_instructions.md` with energy conventions
- [ ] Tested user instructions with a consumption trend prompt
- [ ] Reviewed workspace vs user instruction use cases
- [ ] Explored all 10 pre-built energy skills
- [ ] Completed Exercise A: Revenue per MWh KPI
- [ ] Completed Exercise B: Equipment maintenance ai_classify
- [ ] Completed Exercise C: Custom sample questions in genie-space-creator
- [ ] (Optional) Explored MCP integration
- [ ] Tested image upload with a data flow diagram
