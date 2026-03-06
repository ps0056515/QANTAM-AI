# QANTAM AI

**Quality Engineering AI Platform** — Intelligent requirement analysis, test generation, and release quality scoring.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    EXTERNAL SYSTEMS                             │
│  [Jira/ADO]  [GitHub/GitLab]  [Confluence]  [Slack/Teams]      │
└──────┬───────────────┬──────────────┬──────────────┬───────────┘
       │               │              │              │
       ▼               ▼              ▼              ▼
┌─────────────────────────────────────────────────────────────────┐
│                  QANTAM PLATFORM                                │
│                                                                 │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────────────┐  │
│  │ CLARITY  │ │  PULSE   │ │  SIGNAL  │ │ FORGE / SENTINEL │  │
│  │Req Intel │ │Test Suite│ │ Release  │ │ Code / Prod Mon  │  │
│  └────┬─────┘ └────┬─────┘ └────┬─────┘ └────────┬─────────┘  │
│       └─────────────┴─────────────┴────────────────┘           │
│                           │                                     │
│              ┌────────────▼────────────┐                       │
│              │  Quality Knowledge Graph │                       │
│              │  (QKG — Neo4j)           │                       │
│              └────────────┬────────────┘                       │
│                           │                                     │
│  ┌────────────────────────▼──────────────────────────────────┐ │
│  │  LLM Orchestration Layer (LiteLLM + LangChain)            │ │
│  │  Claude Sonnet ◄► Claude Haiku ◄► Llama 3.1 8B (local)   │ │
│  └───────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

## Modules

| Module | Purpose | Status |
|--------|---------|--------|
| **CLARITY** | Requirement Intelligence — ambiguity detection, completeness, conflicts | Sprint 2-3 |
| **PULSE** | Test Suite Factory — generate positive, negative, edge, compliance tests | Sprint 3-5 |
| **SIGNAL** | Release Quality Score — Go/No-Go decisions with evidence | Sprint 6 |
| **FORGE** | Code Review Quality — PR quality risk scoring | Sprint 7 |
| **SENTINEL** | Production Monitoring — escaped defect tracing | Sprint 8-9 |

## Quick Start

### Prerequisites
- Docker & Docker Compose
- Node.js 20+
- Python 3.11+
- Make

### Local Development

```bash
# Start all services (PostgreSQL, Neo4j, Redis, MinIO, Meilisearch, Ollama)
make dev

# Run backend (FastAPI)
make api

# Run frontend (Next.js)
make web

# Run tests
make test

# Evaluate prompts against golden dataset
make eval
```

## Project Structure

```
qantam-ai/
├── apps/
│   ├── api/                 # FastAPI backend
│   │   ├── routers/         # API endpoints (clarity, pulse, signal, forge)
│   │   ├── services/        # Business logic
│   │   ├── models/          # PostgreSQL ORM + Pydantic schemas
│   │   ├── middleware/      # Auth, RBAC, tenant isolation
│   │   ├── graph/           # Neo4j QKG queries
│   │   └── ai/              # LLM routing, prompts, confidence scoring
│   └── web/                 # Next.js frontend
│       ├── src/app/         # App router pages
│       ├── src/components/  # React components
│       └── src/lib/         # Utilities, API client
├── infra/
│   ├── ansible/             # Server provisioning
│   ├── k3s/                 # Kubernetes manifests
│   └── docker-compose.yml   # Local development stack
├── db/
│   ├── postgres/            # Alembic migrations
│   └── neo4j/               # Cypher constraints
├── eval/                    # Prompt evaluation harness
│   ├── golden_datasets/     # Annotated test data
│   └── results/             # Evaluation reports
└── docs/                    # Architecture & API documentation
```

## Tech Stack

| Layer | Technology |
|-------|------------|
| **Backend** | FastAPI, Python 3.11, Pydantic, SQLAlchemy |
| **Frontend** | Next.js 14, React, TypeScript, Tailwind CSS |
| **Database** | PostgreSQL 16 (operational), Neo4j 5 (QKG) |
| **Cache/Queue** | Redis 7 (sessions, task queue) |
| **Search** | Meilisearch |
| **Storage** | MinIO (S3-compatible) |
| **LLM** | LiteLLM → Claude Sonnet/Haiku, Llama 3.1 8B (Ollama) |
| **Orchestration** | K3s (lightweight Kubernetes) |
| **CI/CD** | GitHub Actions |
| **Monitoring** | Grafana, Prometheus, Loki |

## Environment Variables

```bash
# .env.example
DATABASE_URL=postgresql://qantam:qantam@localhost:5432/qantam
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=qantam123
REDIS_URL=redis://localhost:6379
MINIO_ENDPOINT=localhost:9000
MINIO_ACCESS_KEY=qantam
MINIO_SECRET_KEY=qantam123
ANTHROPIC_API_KEY=sk-ant-...
OLLAMA_HOST=http://localhost:11434
```

## Sprint Timeline

| Sprint | Dates | Focus |
|--------|-------|-------|
| Sprint 1 | Mar 4-18 | Infrastructure + Data Layer + LLM Routing |
| Sprint 2 | Mar 18 - Apr 1 | CLARITY Ingestion + Ambiguity Detection |
| Sprint 3 | Apr 1-15 | CLARITY Complete + PULSE Positive Tests |
| Sprint 4 | Apr 15-29 | PULSE Negative/Edge + Review Workflow |
| Sprint 5 | Apr 29 - May 13 | Jira Integration + ROI Dashboard |
| Sprint 6 | May 13-27 | SIGNAL RQS Engine |
| Sprint 7 | May 27 - Jun 10 | FORGE PR Quality |
| Sprint 8 | Jun 10-24 | SENTINEL Production Monitoring |
| Sprint 9 | Jun 24 - Jul 8 | Ecosystem APIs + Marketplace |

## License

CONFIDENTIAL — Test Yantra Internal
