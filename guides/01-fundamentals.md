# Module 1: Genie Code Fundamentals — Complete Feature Tour

**Genie Code Energy Workshop — SmartGrid Analytics Platform**

This 60-minute hands-on guide walks you through every major Genie Code feature. You'll use slash commands, inline assistant, context references, error handling, and natural language filtering. By the end, you'll be comfortable using Genie Code for everyday data work.

**Prerequisites:** Complete [Module 0: Environment Setup](00-setup.md) first.

---

## Section 1A: Genie Code Pane & Navigation (10 min)

### Open the Genie Code Pane

> **Step 1:** Open the Genie Code pane.  
> **Action:** Click the **Genie Code icon** in the **upper-right corner** of the page (the AI assistant icon).  
> **What you'll see:** A pane opens—typically docked at the bottom or on the right side.  
> **Key concept:** Genie Code is available in notebooks, SQL editor, dashboards, and more. The pane is your main interface.

[Screenshot: Genie Code pane open]

### Explore Controls

> **Step 2:** Familiarize yourself with the pane controls.  
> **Action:** In the Genie Code header, look for:

| Control | Icon | Purpose |
|---------|------|---------|
| **New thread** | Plus or similar | Start a fresh conversation |

| **Settings** | Gear | Add custom instructions, workspace settings |

| **History** | Clock | View and reopen past chat threads |

| **Pane position** | Dock/Side | Choose where the pane appears (bottom, right side) |

| **Close** | X | Close the pane |

> **What you'll see:** Icons in the header. Click **History** to see past threads; click one to reopen it.  
> **Key concept:** You can switch between threads to keep different tasks separate.

### Chat Mode vs. Agent Mode

> **Step 3:** Locate the mode selector at the bottom of the Genie Code pane.  
> **Action:** Find the toggle or dropdown labeled **Chat** and **Agent**.  
> **What you'll see:** Two modes. For this module, use **Chat** mode unless you're doing multi-step tasks.

| Mode | Capabilities |
|------|--------------|
| **Chat** | Answers questions, generates code, explains concepts. Code runs in the chat. |
| **Agent** | Plans multi-step workflows, retrieves assets, runs code, fixes errors across cells. |

> **Key concept:** **Chat** is best for quick fixes and single-step tasks. **Agent** is best for "analyze this entire notebook" or "create a pipeline from these tables."

### Serverless Code Execution

> **Step 4:** Understand where Genie Code runs code.  
> **Action:** When Genie Code generates code in the chat, it can run it in a **side panel** using serverless compute. If your notebook already has a cluster attached, Genie Code may use that instead.  
> **What you'll see:** Code execution results appear in the Genie Code response or in your notebook.  
> **Key concept:** You don't need to run every snippet yourself—Genie Code can execute it for you. Review the output before trusting it.

---

## Section 1B: Slash Commands (15 min)

Slash commands are shortcuts for common prompts. Type `/` in the Genie Code prompt box to see all available commands. For each command below, **select the appropriate cell** (or create one) before typing the slash command.

### /explain

> **Step 5:** Use `/explain` to understand code.  
> **Action:** Open `01_energy_data_explorer` (or the energy data explorer notebook). **Select cell 1** (the one that loads `raw_customers`). In the Genie Code pane, type `/explain` and press Enter.  
> **What you'll see:** Genie Code explains what the code does—loading the customers table and displaying it.  
> **Key concept:** `/explain` is great for understanding unfamiliar code. You can add "be concise" or "explain line-by-line" for different detail levels.

[Screenshot: /explain response for a cell]

### /fix

> **Step 6:** Use `/fix` to repair errors.  
> **Action:** In `01_energy_data_explorer`, **run cell 2** (the "Bug 1" cell—average consumption). It will fail with an error about `kwh_used`. When the error appears, click **Diagnose Error** in the cell output, OR select the cell and type `/fix` in Genie Code.  
> **What you'll see:** Genie Code proposes a fix in a **diff view**—replace `kwh_used` with `kwh_consumed`. Click **Accept** to apply the change.  
> **Key concept:** `/fix` or **Diagnose Error** analyzes the error and suggests a correction. You can Accept or Reject. Accepting does not auto-run the cell—review first!

[Screenshot: /fix diff view with Accept/Reject]

### /doc

> **Step 7:** Use `/doc` to add documentation.  
> **Action:** Select the cell that has summary statistics (e.g., `customers_df.summary().display()`). Type `/doc` in Genie Code and press Enter.  
> **What you'll see:** Genie Code proposes a docstring or comments in a diff view. Accept to add them.  
> **Key concept:** `/doc` auto-generates documentation for your code. Useful for notebooks you'll share or reuse.

### /optimize

> **Step 8:** Use `/optimize` to improve SQL.  
> **Action:** Create a **new cell** and paste this unoptimized SQL:

```sql
SELECT * FROM main.sourabh_energy_workshop.raw_meter_readings WHERE kwh_consumed > 5
```

> Select the cell. Type `/optimize` in Genie Code and press Enter.  
> **What you'll see:** Genie Code suggests improvements—e.g., selecting only needed columns instead of `*`, adding partition hints if applicable, or filtering earlier.  
> **Key concept:** `/optimize` improves SQL and Python for performance, readability, and best practices.

[Screenshot: /optimize suggestions]

### /prettify

> **Step 9:** Use `/prettify` to format code.  
> **Action:** Create a new cell and paste this messy code:

```python
meter_readings_df=spark.table("main.sourabh_energy_workshop.raw_meter_readings")
avg=meter_readings_df.agg({"kwh_consumed":"avg"}).collect()[0][0]
print(avg)
```

> Select the cell. Type `/prettify` and press Enter.  
> **What you'll see:** Genie Code reformats the code with proper spacing, line breaks, and style.  
> **Key concept:** `/prettify` makes code readable without changing logic.

### /rename

> **Step 10:** Use `/rename` to suggest better names.  
> **Action:** Select any cell (e.g., a markdown cell or a code cell). Type `/rename` in Genie Code.  
> **What you'll see:** Genie Code suggests a more descriptive name for the cell or its content.  
> **Key concept:** `/rename` helps with notebook organization and clarity.

### /findTables

> **Step 11:** Use `/findTables` to discover tables.  
> **Action:** In Genie Code, type `/findTables consumption by region` and press Enter.  
> **What you'll see:** Genie Code searches Unity Catalog metadata and returns relevant tables (e.g., `raw_meter_readings`, `raw_customers`, `raw_billing`).  
> **Key concept:** `/findTables` finds tables by natural language. Mention "features" or "feature tables" to search for feature store assets.

### /findQueries

> **Step 12:** Use `/findQueries` to discover queries.  
> **Action:** In Genie Code, type `/findQueries billing reconciliation` and press Enter.  
> **What you'll see:** Genie Code searches for saved queries and metadata related to billing reconciliation.  
> **Key concept:** `/findQueries` helps you reuse existing queries across your organization.

### /settings

> **Step 13:** Use `/settings` to view notebook settings.  
> **Action:** In Genie Code, type `/settings` and press Enter.  
> **What you'll see:** Genie Code runs the settings assistant prompt and may show or adjust notebook settings (e.g., language, cluster).  
> **Key concept:** `/settings` lets you tweak notebook configuration from the chat.

### /repairEnvironment

> **Step 14:** Use `/repairEnvironment` for environment issues.  
> **Action:** In a cell, deliberately install a conflicting library, e.g. `%pip install pandas==1.0.0` (or another version that might conflict). Run the cell. When an error appears in the environment panel, look for a **Genie Code icon** in the bottom-right. Click it. Genie Code runs `/repairEnvironment` to diagnose and suggest fixes.  
> **What you'll see:** Genie Code analyzes the pip log and suggests a fix (e.g., upgrade/downgrade).  
> **Key concept:** `/repairEnvironment` helps with library installation failures and environment conflicts.

[Screenshot: Environment error with Genie Code repair icon]

---

## Section 1C: Inline Assistant & Autocomplete (10 min)

### Inline Assistant (Cmd+I / Ctrl+I)

> **Step 15:** Use the inline assistant in a cell.  
> **Action:** In an **empty cell**, press **Cmd+I** (Mac) or **Ctrl+I** (Windows). A text box appears inside the cell. Type:

```
Calculate the average daily kWh consumption per customer for the last quarter
```

> Press **Enter** (not Shift+Enter).  
> **What you'll see:** Genie Code generates Python or SQL code that answers your request. You can accept the code into the cell or run it.  
> **Key concept:** You can invoke Genie Code directly in a cell without opening the pane. Great for quick code generation.

[Screenshot: Inline assistant prompt in cell]

### Autocomplete

> **Step 16:** Try autocomplete.  
> **Action:** In a new cell, start typing:

```python
df = spark.read.table("main.sourabh_energy_workshop.
```

> **What you'll see:** As you type, Genie Code suggests table names (e.g., `raw_customers`, `raw_meter_readings`). Press **Tab** to accept a suggestion.  
> **Key concept:** Genie Code uses Unity Catalog metadata to autocomplete table and column names.

### Comment-to-Code

> **Step 17:** Generate code from a comment.  
> **Action:** In a new cell, type this comment:

```python
# join customers with billing and calculate total revenue per region
```

> Press **Enter**.  
> **What you'll see:** Genie Code may suggest code to implement the comment. Use **Option+Shift+Space** (Mac) or **Control+Shift+Space** (Windows) to manually trigger a suggestion if it doesn't appear.  
> **Key concept:** Writing comments in plain English can trigger code generation—Genie Code infers intent from your description.

---

## Section 1D: Context, References & Data Discovery (10 min)

### Reference Tables with @

> **Step 18:** Reference a table in your prompt.  
> **Action:** In the Genie Code pane, type `@` and start typing `raw_meter`. Select `raw_meter_readings` from the list. Then add: "What columns does this table have?"

> **What you'll see:** Genie Code includes the table schema in its context and answers with the column list.  
> **Key concept:** The `@` symbol lets you attach tables, notebooks, or other assets to your prompt. Genie Code uses this context for better answers.

[Screenshot: @ reference in prompt]

### Add Context

> **Step 19:** Attach multiple tables.  
> **Action:** In the Genie Code pane, click **Add context** (or similar). Select `raw_customers` and `raw_billing`. Ask: "How can I join these tables for revenue analysis?"

> **What you'll see:** Genie Code understands both schemas and suggests a join using `account_id` and `customer_id`.  
> **Key concept:** Adding context improves accuracy. Genie Code can see tables, columns, and lineage.

### Natural Language Filter in Catalog Explorer

> **Step 20:** Use natural language in Catalog Explorer.  
> **Action:** In the left sidebar, open **Catalog** (or **Data**). Navigate to **main** → **sourabh_energy_workshop** → **raw_customers**. Look for a natural language filter or search box. Type:

```
Show me commercial customers in the Northeast region with solar panels
```

> **What you'll see:** The Catalog Explorer filters or queries the table to show matching rows.  
> **Key concept:** You can explore data in Catalog Explorer using natural language, not just SQL.

[Screenshot: Catalog Explorer with natural language filter]

---

## Section 1E: Error Handling & Debugging (10 min)

The `01_energy_data_explorer` notebook has **3 intentional bugs**. Your job is to find and fix them using Genie Code.

### Bug 1: Wrong Column Name

> **Step 21:** Fix Bug 1.  
> **Action:** Open `01_energy_data_explorer`. **Run cell 2** (the "Bug 1" cell—average consumption). It will fail with an error like `AnalysisException: column kwh_used does not exist`. Click **Diagnose Error** in the cell output, or select the cell and type `/fix` in Genie Code.  
> **What you'll see:** Genie Code proposes changing `kwh_used` to `kwh_consumed`. Click **Accept**.  
> **Key concept:** **Diagnose Error** and **/fix** both analyze the traceback and suggest fixes. Use them for any runtime error.

### Bug 2: Missing Import

> **Step 22:** Fix Bug 2.  
> **Action:** **Run cell 3** (filter high-consumption readings). It will fail with `NameError: name 'F' is not defined`. Click **Diagnose Error** or type `/fix`.  
> **What you'll see:** Genie Code proposes adding `from pyspark.sql import functions as F` at the top of the cell (or in a preceding cell). Accept the fix.  
> **Key concept:** Genie Code understands Python imports and common patterns. It can add the right import.

### Bug 3: Wrong Join Column

> **Step 23:** Fix Bug 3.  
> **Action:** **Run cell 4** (join customers with billing). It may run but produce wrong results (empty or incorrect join), or fail. The bug is: the join uses `customer_name == customer_id` but should use `account_id == customer_id`. Select the cell and ask Genie Code: "Fix the join—customers have account_id and billing has customer_id." Or type `/fix` if the cell errors.  
> **What you'll see:** Genie Code corrects the join condition to `customers_df.account_id == billing_df.customer_id`.  
> **Key concept:** Even when code runs, semantic bugs (wrong join keys) can produce bad data. Genie Code can fix logical errors when you describe them.

### Success: Visualization

> **Step 24:** Run the visualization.  
> **Action:** After fixing all three bugs, **run cell 5** (consumption by customer segment).  
> **What you'll see:** A bar chart or table showing average amount charged by customer type.  
> **Key concept:** Once the data pipeline is correct, downstream visualizations work. Genie Code helps you get there faster.

[Screenshot: Working visualization]

---

## Section 1F: Natural Language Data Filtering (5 min)

> **Step 25:** Filter table output with natural language.  
> **Action:** Run a cell that displays a table (e.g., `customers_billing_df.display()` or a billing query). In the **output table**, look for a **Filter** icon. Click it. In the filter prompt, type:

```
Show me only delinquent commercial customers with balance over $500
```

> **What you'll see:** The table filters to show only rows matching that criteria.  
> **Key concept:** You can filter displayed data without writing SQL—Genie Code translates your natural language into the filter logic.

[Screenshot: Filter icon and natural language filter prompt]

---

## Hands-On Challenge

Complete these **4 tasks** independently using what you learned. Use Genie Code (Chat mode, slash commands, inline assistant, error handling) as needed.

### Task 1: Explain and Optimize

1. Open a notebook cell with a SQL query (or write one that selects from `raw_meter_readings`).
2. Use `/explain` to understand what it does.
3. Use `/optimize` to improve it. Accept the suggested changes.

### Task 2: Generate from Comment

1. In a new cell, type: `# Top 5 regions by total outage duration`
2. Press Enter and let Genie Code generate the code (or use Cmd+I).
3. Run the cell and verify the output.

### Task 3: Fix an Error

1. In a new cell, write:

```python
df = spark.table("main.sourabh_energy_workshop.raw_weather")
df = df.filter(F.col("temp_high") > 90)
df.display()
```

2. Run it (it will fail—missing import). Use **Diagnose Error** or `/fix` to repair it.
3. Run again and confirm it works.

### Task 4: Discover and Query

1. Use `/findTables` with a query like "demand response events".
2. Reference the found table with `@` in a new prompt.
3. Ask Genie Code: "What's the average actual_reduction_kwh for events where participated is true?"

---

## Summary

You've completed the Genie Code Fundamentals tour. You've used:

| Feature | Use case |
|---------|----------|
| **Slash commands** | `/explain`, `/fix`, `/doc`, `/optimize`, `/prettify`, `/rename`, `/findTables`, `/findQueries`, `/settings`, `/repairEnvironment` |
| **Inline assistant** | Cmd+I in a cell for quick code generation |
| **Autocomplete** | Tab to accept table/column suggestions |
| **Context** | `@` for tables, `Add context` for multiple assets |
| **Error handling** | Diagnose Error, Quick Fix, `/fix` |
| **Natural language filter** | Filter icon in table output |

**Next:** Proceed to Module 2 (Data Engineering) or Module 3 (Data Science) to use Genie Code in Agent mode for complex, multi-step workflows.
