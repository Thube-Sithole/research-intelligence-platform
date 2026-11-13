# Research Intelligence Platform (RIP)

A hybrid, human-supervised research intelligence platform. The system plans investigations, discovers and extracts evidence, analyses and critiques findings, and produces traceable research outputs. Researchers remain in control of scope, interpretation and approval.

> **Current status:** foundational repository scaffold. The API and LangGraph workflow are intentionally an MVP skeleton. Literature-provider integrations, persistent graph checkpoints, authentication, tenant isolation, and production-grade evidence evaluation are not implemented yet.

## Product principles

1. **Evidence before eloquence:** every substantive claim in a report should resolve to source evidence.
2. **Honest provenance:** distinguish full-text access, abstract-only access, metadata-only access and user-supplied material.
3. **Human authority:** approval gates are explicit; agents cannot approve their own work.
4. **Scoped memory:** project knowledge and shared institutional knowledge are separate scopes with access checks.
5. **Reproducibility:** record research configuration, source versions, retrieval timestamps, model/provider versions and workflow events.
6. **Domain-aware evaluation:** clinical evidence appraisal, engineering experimental analysis and other disciplines use different evaluation criteria.
7. **Provider independence:** model and literature-provider adapters should be replaceable.

## Architecture

```text
React + TypeScript workspace
          |
       FastAPI
          |
  Application services
          |
 LangGraph orchestrator ---- Human approval checkpoints
    |       |       |
 Planner  Discovery  Evidence extraction
                 Analysis -> Critique -> Synthesis
          |
 Evidence/provenance services
          |
 PostgreSQL + pgvector | Object storage | Redis (later)
          |
 Literature adapters: OpenAlex, Crossref, PubMed, user uploads
```

### Memory scopes

- `project`: accessible only to authorised members of one research project.
- `shared`: institution/workspace knowledge, accessible only to users granted that workspace scope.
- No implicit promotion from project memory to shared memory. Promotion must be an explicit, audited action.
- Retrieval must apply access-control filters **before** returning candidate content. Vector similarity is not an authorisation mechanism.

## Repository layout

```text
backend/       FastAPI application and LangGraph workflow
frontend/      React + TypeScript research workspace starter
infra/         Local development infrastructure
 docs/         Architecture and product decisions
```

## Quick start

### Prerequisites

- Docker + Docker Compose
- Node.js 20+ (only if running the frontend outside Docker)
- Python 3.11+ (only if running the backend outside Docker)

### 1. Configure environment

```bash
cp .env.example .env
```

Set an LLM provider API key only when you add and enable a real model adapter. The initial graph uses deterministic placeholder nodes and does not call an LLM or external literature API.

### 2. Start services

```bash
docker compose up --build
```

- API: http://localhost:8000
- API docs: http://localhost:8000/docs
- Frontend: http://localhost:5173
- PostgreSQL: localhost:5432
- Redis: localhost:6379

### 3. Run backend tests locally

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -e '.[dev]'
pytest
```

## First API workflow

`POST /api/v1/research/runs` accepts a research question and returns an initial workflow result. The scaffold deliberately stops at `awaiting_human_review`; it does not pretend that literature discovery or evidence analysis has occurred.

Example:

```json
{
  "question": "How does reflux ratio affect energy use and separation in a distillation column?",
  "domain": "engineering",
  "project_id": "demo-project",
  "memory_scope": "project",
  "autonomy": "hybrid"
}
```

## Build sequence

1. Repository foundation and API contract (this scaffold).
2. Persistence: projects, memberships, research runs, sources, claims and workflow events.
3. Identity, authorisation and tenant/project isolation.
4. Literature adapters and source deduplication.
5. Document ingestion, parsing and page/section-level provenance.
6. Evidence extraction with schema validation.
7. Domain-specific appraisal and quantitative analysis.
8. Critical review, contradiction handling and evidence-gap loops.
9. Human approval/resume using a persistent LangGraph checkpointer.
10. Reports, evaluation datasets, observability and deployment hardening.

See [`docs/architecture.md`](docs/architecture.md) and [`docs/decisions.md`](docs/decisions.md).
