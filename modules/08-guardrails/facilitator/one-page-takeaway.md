# Genie Code Guardrails
## Customer Takeaway — One Page

---

### The one rule that matters

> **Instructions guide behavior. Permissions control what is possible.**

Genie Code runs with the user's own Databricks identity. It does not have elevated access. Every guardrail you apply to a human developer applies here too.

---

### What Genie Code provides for safety

| Control | How it works |
|---|---|
| **Human review gate** | All code runs require user approval before execution — the diff is always visible |
| **User instructions** | Per-user Markdown file; always-on context for coding style, conventions, prohibited actions |
| **Workspace instructions** | Set by workspace admin; applies to all users; cannot be disabled at user level |
| **AGENTS.md / CLAUDE.md** | Repo-local file; loaded automatically; travels with the code; works with any AI assistant |
| **Usage logging** | All interactions logged to `system.access.assistant_events` — who, when, where |

---

### What is not available today

| Gap | What to do instead |
|---|---|
| Account-level instructions (one policy, all workspaces) | Standardize workspace instructions via admin runbook |
| Workspace-level MCP allowlist | Document approved MCP servers in workspace instructions; train users |
| Automatic refusal of destructive actions | IAM least privilege + workspace instruction warnings + AGENTS.md rules |
| Genie-Code-native cost attribution | Standard Databricks budget policies + cluster policies |
| Full prompt/response content audit | Usage metadata available; content audit is a known gap |

---

### Defense in depth: the right model

```
1. Unity Catalog permissions      ← enforcement
2. Budget + cluster policies      ← spend control  
3. Workspace instructions         ← behavior guidance (all users)
4. AGENTS.md in every repo        ← repo-local context
5. Prompt design habits           ← user skill
```

All five layers. Not just instructions.

---

### Your minimum safe setup (do this before going to production)

- [ ] Workspace instructions configured by admin (see template)
- [ ] AGENTS.md committed to every active repository
- [ ] Least-privilege Unity Catalog permissions for all Genie Code users
- [ ] Budget alert set in Account Console
- [ ] Cluster policy in place (cap cluster sizes, set autotermination)
- [ ] Team trained on: scope statements, diff review, safe prompt patterns
- [ ] `system.access.assistant_events` dashboard or query ready for weekly review

---

### Key product facts

- Genie Code is **GA** and enabled by default (Agent Mode requires partner-powered AI)
- No additional cost — pay for the compute Genie Code triggers
- **HIPAA, PCI, and CSP None compliant** in Agent Mode
- Azure OpenAI abuse monitoring is disabled — prompts are not stored by the model provider
- Rate limits exist for abuse prevention; normal usage is unlikely to encounter them

---

### Questions?

| Topic | Who to ask |
|---|---|
| Workspace instruction setup | Your Databricks workspace admin |
| Unity Catalog permissions | Metastore admin |
| Usage dashboard | See Module 07 of the base lab |
| Account-level policy roadmap | Your Databricks account team |
| Security questionnaire | go/security-review (internal) or your account SE |

---

*Based on the Genie for Energy hands-on lab — Module 08: Guardrails & Governance*
*Product state as of May 2026. Check release notes for updates.*
