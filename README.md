# Growth Automation Agent

A portfolio MVP for a Sales/GTM workflow automation backend.

The project simulates a realistic lead processing pipeline: ingest leads from CSV, validate and normalise them, apply mock enrichment, score them deterministically, and produce next-action recommendations with a full decision log.

It is designed as a portfolio and experimental backend project built around production-oriented principles — not a production system.

---

## Architecture overview

```
app/
  main.py              — FastAPI application entry point
  models/
    lead.py            — Lead ORM (SQLAlchemy) + Pydantic schema
    scoring.py         — ScoringResult value object
    decision.py        — DecisionLog ORM row
  services/
    scoring.py         — deterministic lead scoring logic
    enrichment.py      — mock enrichment (fills missing fields)
    recommendation.py  — maps score tier to next action
  repositories/
    lead_repository.py — all DB access for leads
  loaders/
    csv_loader.py      — reads and validates a CSV file of leads
data/
  sample_leads.csv     — five realistic fake leads for local testing
tests/
  test_app.py          — smoke tests (import, /health)
docs/
  implementation_plan.md — ordered coding tickets
```

Layers (loosely):

| Folder | Responsibility |
|--------|---------------|
| `models/` | Domain entities, value objects, ORM mappings |
| `services/` | Application logic (scoring, enrichment, recommendations) |
| `repositories/` | Persistence (SQLAlchemy async sessions) |
| `loaders/` | Infrastructure I/O (CSV ingestion) |
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

## Planned implementation phases

| Phase | Description |
|-------|-------------|
| 1 — Foundation | Project scaffold, `/health` endpoint, CI *(current)* |
| 2 — Domain model | Fill out `LeadORM` columns, Pydantic schemas, DB migration |
| 3 — CSV ingestion | Implement `csv_loader.py`, row validation, error reporting |
| 4 — Enrichment | Mock enrichment rules in `enrichment.py` |
| 5 — Scoring | Deterministic scoring algorithm in `scoring.py` |
| 6 — Recommendations | Tier-to-action mapping in `recommendation.py` |
| 7 — Decision log | Persist every action to `decision_logs` |
| 8 — API routes | Expose ingestion, scoring, and recommendation via REST |
| 9 — LLM layer (optional) | Provider-abstracted LLM enrichment behind a feature flag |

---

## Manual coding roadmap

See [`docs/implementation_plan.md`](docs/implementation_plan.md) for individual coding tickets.

Each ticket is small and self-contained so the project owner can implement them incrementally.
