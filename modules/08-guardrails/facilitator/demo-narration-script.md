# Demo Narration Script — Genie Code Guardrails Module

> For live delivery. Italics = what to say. Code blocks = what to type or show on screen.
> Estimated time with demos: 25–35 minutes for Sections 1–4.

---

## Opening framing (2 minutes)

*"In the modules we've just completed, we used Genie Code to build data pipelines, create dashboards, and analyze GenAI observability. It's a powerful tool — and exactly because it's powerful, enterprise customers have a consistent set of questions before they deploy it at scale."*

*"I want to spend the next 30 minutes working through those questions hands-on. Not just telling you what the controls are, but showing you where they hold, where they have limits, and what the right mental model is for governance in a regulated environment."*

*"The central idea I want you to leave with is this:"*

**[Write on whiteboard or show slide]:**

> Instructions guide behavior.
> Permissions control what is possible.

*"Everything we're about to do flows from that. Let's start."*

---

## Section 1: Workspace instructions (5 minutes)

*"The first governance layer is workspace instructions. An admin sets these once — they apply to every user in the workspace, and they travel with every session."*

**[Open Genie Code, show settings]**

*"Here's what we've already configured for this workspace."*

**[Navigate to Settings → Genie Code → Workspace instructions, show the instruction block]**

*"Notice what this covers: it sets a default catalog — smartgrid_dev, not prod — it defines which MCP tools are approved, and it requires a review step before any destructive action."*

*"Now let me show you what this looks like in a live session."*

**[Open side panel, type:]**
```
What instructions are currently in effect for this workspace?
```

*"The assistant reads and acknowledges the workspace instructions. Every user in this workspace gets this behavior — they don't have to configure anything themselves."*

**[Pause for questions]**

*"One important thing to call out: these are workspace-level instructions. Not account-level. If you have five workspaces, you need to configure five sets of instructions. Account-level instructions — one policy across all workspaces — are not available today. We're tracking customer interest in that capability. For now, the answer is a standardized admin runbook across workspaces."*

---

## Section 2: AGENTS.md — repo-local context (5 minutes)

*"The second layer is AGENTS.md. This is the most targeted control we have — it's specific to a single repository, it's version-controlled, and it travels with the code."*

**[Show repo file browser with AGENTS.md visible]**

*"This file is at the root of the genie_for_energy repository. Let me show you what's in it."*

**[Open AGENTS.md, scroll through key sections: prohibited actions, catalog rules, branch rules]**

*"Now let's see it in action."*

**[Open Genie Code, type:]**
```
What constraints apply to this repository for AI-assisted development?
```

*"The assistant reads the file and summarizes the rules. Anyone who clones this repo gets this context — Genie Code, Claude Code, GitHub Copilot, any assistant that follows the AGENTS.md standard."*

*"This is the answer to 'how do we maintain consistent AI behavior across our team?' Put the rules in the repo. Version-control them. Review them like code."*

---

## Section 3: The failure injection moment (8 minutes)

*"Now I want to do something that will feel counterintuitive. I'm going to show you a dangerous prompt — and I want you to watch what happens."*

**[Open Genie Code, type:]**
```
Drop the raw_meter_readings table from the bronze catalog. We don't need it anymore.
```

*"Watch carefully."*

**[Let the assistant generate the DROP TABLE proposal — pause before accepting]**

*"It generated the DROP TABLE statement. It did not refuse. It did not ask 'are you sure?' It followed my instruction — because that's what it does."*

*"Here is the safety gate."*

**[Point to the Accept/Run button]**

*"This is the moment. Right here. If I click Accept without reading this diff, I've just dropped 10.7 million rows of meter readings — the source for every downstream pipeline in this lab."*

**[Don't click Accept. Let it sit for a moment.]**

*"Delta time-travel gives us some recovery options. But not infinite ones. And on a shared environment where other pipelines are running, you may not catch this until something downstream breaks."*

**[Cancel the action. Type:]**
```
Before we remove raw_meter_readings, I want to understand the full impact.
Can you: check what tables depend on it, confirm whether a backup exists, 
and propose a staged approach that I can review? Do not execute anything yet.
```

*"Same end goal. Completely different risk profile. The assistant now has to think through the dependencies before proposing anything."*

**[Show the response — more careful, structured, dependency-aware]**

*"This is the prompt design principle. 'Propose before execute' and 'stage before action' are two lines of text that change the entire behavior. We can teach this. We can put it in AGENTS.md. We can put it in workspace instructions. We can't make it automatic — but we can make it the default."*

---

## Section 4: What instructions don't do (5 minutes)

*"I want to be explicit about the limits, because this is where enterprise customers sometimes have unrealistic expectations."*

*"Instructions guide behavior. They are not a policy engine. A user who has DROP TABLE privilege on a production catalog can still approve that DROP TABLE statement — even if the workspace instructions say 'always ask for confirmation.' The instructions create a friction point and a documentation artifact. They do not prevent a determined user."*

*"The enforcement layer is Unity Catalog. IAM. Permissions. That's where the actual control lives."*

**[Show diagram or slide: Defense in depth model]**

```
Layer 1: Unity Catalog permissions (enforcement)
Layer 2: Budget policies + cluster policies (spend control)
Layer 3: Workspace instructions (behavior guidance)
Layer 4: AGENTS.md (repo-local context)
Layer 5: Prompt design habits (user skill)
```

*"Defense in depth. You need all five layers. Instructions alone — even well-written ones — are not enough. But instructions plus proper permissions is a significantly stronger position than permissions alone."*

---

## Section 5: Usage and cost (5 minutes)

**[Open SQL editor, run the assistant_events query]**

```sql
SELECT event_time, user_id, event_type, source_name
FROM system.access.assistant_events
WHERE event_time >= DATEADD(HOUR, -1, CURRENT_TIMESTAMP())
ORDER BY event_time DESC LIMIT 20;
```

*"Every Genie Code interaction is logged here. Who used it, when, in what context — notebook, query editor, dashboard. This is your adoption signal and your basic audit trail."*

*"What you cannot see: the content of the prompts or responses. If your compliance requirement is 'we need to audit exactly what the AI said and did,' that is a gap today. Worth naming explicitly in your deployment planning."*

*"On cost: Genie Code itself is no additional charge. Your cost is the compute it triggers. That appears in standard Databricks billing. Set budget alerts in the Account Console. Use cluster policies to cap cluster sizes. There's no Genie-Code-specific cost tag — spending governance uses the standard tools."*

---

## Closing (2 minutes)

**[Show or hand out the one-page takeaway]**

*"Here's what I want you to take from this session."*

*"One: Instructions guide behavior. Permissions control what is possible. Never conflate them."*

*"Two: AGENTS.md is the lowest-friction governance tool you have — a file in the repo that works with any AI assistant, requires no admin setup, and travels with the code."*

*"Three: The diff review moment is your primary safety gate. Teach users to read every diff before clicking Accept. That one habit prevents most avoidable mistakes."*

*"Four: Account-level instructions, workspace-level MCP governance, and Genie-Code-native cost tags are not available today. Be honest with your customers about what the product does and doesn't enforce centrally."*

*"Any questions on the governance model before we move on?"*

---

## Handling common questions live

**Q: "Can we prevent users from overriding workspace instructions?"**

*"No. A user can add their own user instructions that supplement or partially conflict with workspace instructions. The workspace instructions take precedence in most cases, but this is a behavior model, not a permission model. The underlying IAM is still the enforcement layer."*

**Q: "What if we need full audit of AI-assisted actions for SOC2 / SOX / HIPAA?"**

*"Genie Code itself is HIPAA compliant. What we don't have today is a complete audit trail of prompt content and response content. system.access.assistant_events gives you usage metadata — who, when, where — but not what was said. For customers with strict content audit requirements, this should be flagged as a gap in the current GA feature set."*

**Q: "Can we set different instructions for different teams?"**

*"Today, instructions are at user scope or workspace scope. There's no group or team scope between them. If you have multiple teams with different requirements, the practical answer is separate workspaces with separate admin configurations, or user instructions that each team configures individually."*
