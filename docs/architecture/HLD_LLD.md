# QANTAM AI - High Level Design + Low Level Design

This document is the master reference for QANTAM architecture.
See the full HLD+LLD document provided during project setup.

## Quick Reference

### 5 Tracks
1. **Infrastructure & DevOps** - Hetzner servers, K3s, CI/CD
2. **Data Layer** - PostgreSQL (operational), Neo4j (QKG intelligence)
3. **LLM & API Layer** - LiteLLM routing, FastAPI, confidence scoring
4. **CLARITY + PULSE** - Requirement intelligence + Test generation
5. **SIGNAL + FORGE + SENTINEL** - Release quality, code review, production monitoring

### 9 Sprints (18 months)
- Sprint 1-5: Phase 1 MVP (CLARITY + PULSE)
- Sprint 6-7: Phase 2 (SIGNAL + FORGE)
- Sprint 8-9: Phase 3 (SENTINEL + Ecosystem)

### Key Architecture Decisions
- **Multi-tenant isolation**: Every query includes tenant_id
- **Confidence scoring**: Every AI output has 0-100 confidence
- **Accuracy gates**: Prompts must pass threshold before shipping
- **QKG as brain**: Neo4j graph connects all quality intelligence

## Module Summary

| Module | Purpose | AI Model | Sprint |
|--------|---------|----------|--------|
| CLARITY | Requirement analysis | Claude Sonnet | 2-3 |
| PULSE | Test generation | Claude Haiku | 3-5 |
| SIGNAL | Release quality score | Rules + LLM | 6 |
| FORGE | PR quality risk | Rules + QKG | 7 |
| SENTINEL | Production monitoring | Llama 3.1 | 8-9 |
