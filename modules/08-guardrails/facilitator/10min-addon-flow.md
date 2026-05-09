# 10-Minute Guardrails Add-On Workshop Flow

> For facilitators who need to deliver the guardrails message in a tight time window.
> This is a highlight reel — not a replacement for the full 60-90 min module.

---

## Setup (before the session starts)

- Workspace instructions loaded and visible in Settings → Genie Code
- AGENTS.md committed to a feature branch in the energy repo
- `system.access.assistant_events` query ready in a notebook cell
- Demo narration script open in a separate window

---

## Flow (10 minutes total)

### Minute 0–1: Frame the conversation

> "We just saw how powerful Genie Code is for data engineering and analytics. Now let's talk about the question every enterprise customer asks: *what could go wrong, and how do we prevent it?*"

Key statement to deliver:

> "Genie Code runs with your own identity and permissions. It doesn't have elevated access. That means the same guardrails you apply to any developer — least privilege, non-prod by default, peer review — apply here too. The AI doesn't change the equation; it adds a new surface that needs the same governance."

---

### Minute 1–3: Show workspace instructions in action (live demo)

1. Open Genie Code side panel
2. Ask: *"What instructions are in effect for this workspace?"*
3. Show the assistant reading and acknowledging the workspace instructions
4. Point to the key rules: non-prod default, approved MCP list, review requirement

> "These instructions were set by an admin. Every user in this workspace gets them. This is how you encode org-wide conventions — not just coding style, but safety rules."

**Key talking point:** Workspace instructions apply to all users. User instructions are per-user. Account-level instructions — one policy across all workspaces — **are not available today.**

---

### Minute 3–5: Show AGENTS.md in the repo

1. Open the repo file browser — show AGENTS.md at the repo root
2. Open Genie Code and ask: *"What constraints apply to this repository?"*
3. Show the assistant citing the AGENTS.md content

> "This file travels with the code. Anyone who clones this repo and uses an AI assistant gets the same context. No admin setup required — just a file in the right place."

**Key talking point:** AGENTS.md is the most targeted form of instruction. It's repo-specific, version-controlled, and works with any AI assistant that follows the standard.

---

### Minute 5–7: The failure injection moment (most impactful 2 minutes)

1. Type this prompt live:

```
Drop the raw_meter_readings table from the bronze catalog. We don't need it anymore.
```

2. Let the assistant propose the `DROP TABLE` statement
3. **Do not click Accept** — pause here

> "Here's the thing: it proposed the action. It didn't refuse. That's by design — the assistant follows your instructions. The safety gate is right here." (point to the Accept button)

> "Now look at what would happen if I clicked this without reading the diff. That table has 10 million rows. It's the source for every downstream pipeline. There's no undo that's faster than a Delta time-travel restore — which itself requires preparation."

4. Cancel the action. Then type:

```
Before we remove raw_meter_readings, check what depends on it, 
confirm there's a restore path, and propose a staged approach.
```

5. Show the contrast in responses

> "Same outcome, completely different risk profile. The prompt design matters — and that's something we can teach."

---

### Minute 7–9: Usage visibility (30 seconds) + cost framing (90 seconds)

**Usage (30 seconds):**

```sql
SELECT event_time, user_id, event_type, source_name
FROM system.access.assistant_events
WHERE event_time >= DATEADD(HOUR, -1, CURRENT_TIMESTAMP())
ORDER BY event_time DESC LIMIT 10;
```

> "Every interaction is logged. You can see who's using Genie Code, when, and in what context. You cannot see the prompts or responses today — that's a known gap for customers with full audit requirements."

**Cost (60 seconds):**

> "Genie Code itself costs nothing extra. Your cost comes from the compute it triggers — clusters, warehouses, pipelines. That shows up in standard Databricks billing. Use budget policies and cluster policies to govern spend. There's no Genie-Code-specific cost tag today."

---

### Minute 9–10: Leave-behind and the one rule

Hand out (or share link to) the one-page takeaway. Then deliver:

> "Here's the one rule that covers 90% of enterprise concerns about AI-assisted development:"

Write or display:

> **"Instructions guide behavior. Permissions control what is possible."**

> "Get the permissions right first. Use instructions to reduce accidental mistakes. Monitor usage. Set budget alerts. That's the complete picture."

---

## If you have 5 extra minutes

Add the customer objection simulation: pick one talking point from Section E and role-play it with the room.

Suggested: the "account-level policy enforcement" concern — it consistently surfaces in enterprise accounts and the nuanced answer (workspace instructions today, account-level not yet available) is worth practicing.
