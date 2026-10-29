# Neurovians AI Gateway

**A governed execution layer for enterprise AI.**

Neurovians AI Gateway is an API-first platform for registering, evaluating, governing, and operating LLMs across an organization—without coupling product teams to individual model providers.

It is being built around one practical question:

> Given a request, which model should answer it, under which policy, at what cost, with what evidence, and how do we prove the result was acceptable?

---

## Why this exists

Most organizations adopt LLMs one application at a time. The result is fragmented model usage, unclear spend, inconsistent safety controls, and no durable evidence of quality.

Neurovians provides a shared control plane for AI:

- Register and govern approved LLMs.
- Compare models against the same prompt and evaluation dataset.
- Measure quality, latency, token use, and cost.
- Apply request and response guardrails.
- Preserve prompts, responses, evaluations, and audit trails.
- Route future requests to the most suitable approved model.

The goal is not merely to call an LLM. The goal is to make AI use **observable, comparable, controllable, and accountable**.

---

## Current capability

The current MVP includes:

- FastAPI-based gateway.
- Persistent LLM registry backed by Neon PostgreSQL.
- Browser UI for viewing and registering approved models.
- Organization-scoped model records.
- API CRUD endpoints for registered models.
- Request-level trace IDs and structured request timing logs.
- Foundation for comparative evaluation, FinOps, guardrails, and agentic orchestration.

---

## Architecture direction

```text
UI / CI-CD / Enterprise Application
                |
                v
       FastAPI Gateway Controllers
                |
                +--> Validate request
                +--> Persist request and audit metadata
                +--> Publish event
                         |
                         v
                 Agentic Event Harness
                         |
       +-----------------+------------------+
       |                 |                  |
       v                 v                  v
 Prompt creation     Model execution    Cost + audit
       |                 |                  |
       +-----------------+------------------+
                         |
                         v
                 Response + evaluation
                         |
                         v
                   UI / API callback