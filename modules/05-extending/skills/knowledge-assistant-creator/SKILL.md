---
name: knowledge-assistant-creator
description: "Creates RAG Knowledge Assistants programmatically via Databricks SDK. Indexes documents from Unity Catalog volumes for energy policies, regulatory docs, and support FAQs. Use when automating KA deployment for energy/utilities document Q&A."
---

# Knowledge Assistant Creator

Create Databricks Knowledge Assistants (RAG chatbots) programmatically via the Databricks SDK. Index documents from Unity Catalog volumes for energy policies, regulatory filings, and support FAQs.

## When to Use

- Automating Knowledge Assistant creation from document volumes
- Deploying energy policy or regulatory document Q&A
- Building support FAQ chatbots for utilities
- Workshop demos requiring pre-configured KAs

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `name` | Yes | KA display name |
| `volume_path` | Yes | Unity Catalog volume path (e.g., `/Volumes/main/sourabh_energy_workshop/docs/`) |
| `description` | No | What the KA does |
| `instructions` | No | How the KA should answer |

## Workflow

1. **Prepare documents** — PDF, TXT, MD, DOCX in a Volume
2. **Create KA** — POST Knowledge Assistants API
3. **Add knowledge source** — Link volume path
4. **Sync** — Index documents (may take minutes)

## Script Usage

```bash
python scripts/create_ka.py \
  --name "Energy Policy Assistant" \
  --volume-path /Volumes/main/sourabh_energy_workshop/policies/
```

## Reference Files

- [references/ka-config-guide.md](references/ka-config-guide.md) — API payload structure and config options

## Prerequisites

- Databricks SDK
- Unity Catalog enabled
- Documents in Volume (PDF, TXT, MD, DOCX, PPT/PPTX)
- Serverless compute, Production MLflow monitoring
- Foundation model access via system.ai
