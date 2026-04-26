# Growth Automation Agent

A portfolio MVP for a Sales/GTM workflow automation backend.

The project simulates a realistic lead processing pipeline: ingest leads from CSV, validate and normalise them, apply mock enrichment, score them deterministically, and produce next-action recommendations with a full decision log.

It is designed as a portfolio and experimental backend project built around production-oriented principles — not a production system.

---

## Architecture overview

```
app/
  main.py                    — FastAPI app, lifespan, /health endpoint
  models/
    lead.py                  — LeadORM (SQLAlchemy), LeadCreate, LeadRead (Pydantic)
    scoring.py               — ScoringResult value object
    decision.py              — DecisionLogORM
  services/
    lead_import.py           — import use case: CSV → validate → persist
    scoring.py               — deterministic lead scoring (stub)
    enrichment.py            — mock enrichment (stub)
    recommendation.py        — next-action recommendation (stub)
  repositories/
    lead_repository.py       — CRUD: create, get_by_id, list_all, upsert, delete
  loaders/
    csv_loader.py            — reads CSV, normalises rows, validates against LeadCreate
  utility/
    codes.py                 — LogCode registry (INF / WRN / ERR / DBG)
    logger.py                — AppLogger static methods + configure_logging()
data/
  sample_leads.csv           — five realistic fake leads for local testing
tests/
  test_app.py                — smoke tests (import, /health)
  test_lead_schema.py        — LeadCreate / LeadRead validator tests
  test_lead_repository.py    — repository CRUD against in-memory SQLite
  test_lead_import.py        — end-to-end import use case tests
docs/
  architecture.md            — layer responsibilities and design decisions
  error_handling_flow.md     — error and logging conventions
  implementation_plan.md     — ordered coding tickets
```

Layers:

| Folder | Responsibility |
|--------|----------------|
| `models/` | Domain entities, value objects, ORM mappings |
| `services/` | Application use cases and business logic |
| `repositories/` | All database access (SQLAlchemy async) |
| `loaders/` | Infrastructure I/O (CSV ingestion) |
| `utility/` | Cross-cutting: structured logging, error codes |
| `main.py` | API layer (FastAPI routes) |

---

## Local setup

```bash
# 1. Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate

# 2. Install runtime + dev dependencies
pip install -e ".[dev]"

# 3. Run the API server
uvicorn app.main:app --reload

# 4. Verify
curl http://localhost:8000/health
# {"status": "ok"}

# 5. Run tests
pytest
```

---

## Implementation phases

| Phase | Description | Status |
|-------|-------------|--------|
| 1 — Foundation | Project scaffold, `/health` endpoint, CI | ✅ Done |
| 2 — Domain model | `LeadORM`, `LeadCreate`, `LeadRead`, timestamps | ✅ Done |
| 3 — CSV ingestion + import | `csv_loader`, `lead_repository` CRUD, `lead_import` use case | ✅ Done |
| 4 — Enrichment | Mock enrichment rules in `enrichment.py` | 🔲 Next |
| 5 — Scoring | Deterministic scoring algorithm in `scoring.py` | 🔲 Pending |
| 6 — Recommendations | Tier-to-action mapping in `recommendation.py` | 🔲 Pending |
| 7 — Decision log | Persist every action to `decision_logs` | 🔲 Pending |
| 8 — API routes | Expose ingestion, scoring, recommendation via REST | 🔲 Pending |
| 9 — LLM layer (optional) | Provider-abstracted LLM enrichment behind a feature flag | 🔲 Pending |

---

## Coding roadmap

See [`docs/implementation_plan.md`](docs/implementation_plan.md) for individual coding tickets.
