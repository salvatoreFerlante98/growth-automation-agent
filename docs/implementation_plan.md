# Implementation Plan

Each ticket is a small, self-contained coding task.
Implement them in order — later tickets depend on earlier ones.

---

## Phase 2 — Domain model ✅

### TICKET-01 ✅ Define `LeadORM` columns
`app/models/lead.py` — done. Columns: `name`, `company`, `email`, `phone`, `role`, `company_size`, `industry`, `employee_count`, `source`, `created_at`, `updated_at`.

### TICKET-02 ✅ Define `LeadCreate` and `LeadRead` schemas
`app/models/lead.py` — done. `LeadCreate` for input (with validators), `LeadRead(LeadCreate)` for output.

### TICKET-03: Extend `ScoringResult`

**File:** `app/models/scoring.py`

Add:
- `fit_score: float` — 0–100, firmographic and role alignment
- `intent_score: float` — 0–100, placeholder (always 50)
- `composite_score: float` — weighted average
- `tier: Literal["hot", "warm", "cold"]` — derived from composite_score
- `reasons: list[str]` — human-readable explanation lines

Constrain all floats with `Field(ge=0.0, le=100.0)`.

### TICKET-04: Wire up the async database engine

**File:** `app/database.py` *(create this file)*

- `async_engine` via `create_async_engine` — default URL: `sqlite+aiosqlite:///./leads.db`
- `AsyncSessionLocal` session factory
- `get_session()` async generator for FastAPI dependency injection
- `create_tables()` coroutine that calls `Base.metadata.create_all`

Call `create_tables()` from `app/main.py` inside the existing `lifespan` context manager.

---

## Phase 3 — CSV ingestion + import ✅

### TICKET-05 ✅ Implement `load_leads_from_csv`
`app/loaders/csv_loader.py` — done. Normalises columns, validates against `LeadCreate`, returns `LoadResult(valid, errors)`.

### TICKET-06 ✅ Implement `lead_repository` CRUD
`app/repositories/lead_repository.py` — done. `create`, `get_by_id`, `list_all`, `upsert`, `delete`.

### TICKET-07 ✅ Implement `import_leads` use case
`app/services/lead_import.py` — done. Orchestrates loader → repository, returns `ImportResult(imported, skipped, errors)`.

---

## Phase 4 — Enrichment

### TICKET-08: Implement mock enrichment

**File:** `app/services/enrichment.py`

Rules (apply only when the field is blank):
- `industry`: infer from a hardcoded keyword map on `company` name, default `"Unknown"`
- `employee_count`: default `50`
- `source`: default `"enriched"`

Return a new `LeadCreate` — do not mutate the input.
Add tests in `tests/test_enrichment.py`.

---

## Phase 5 — Scoring

### TICKET-09: Extend `ScoringResult` (see TICKET-03 above)

### TICKET-10: Implement `score_lead`

**File:** `app/services/scoring.py`

Scoring rules (deterministic, no randomness):

**Fit score** (0–100):
- `+30` if `employee_count` is between 50 and 1000
- `+25` if `role` contains "VP", "Director", "Head", "CTO", "Founder"
- `+20` if `industry` is in a target list (SaaS, Fintech, DevTools, …)
- `+15` if `company_size` is `"medium"` or `"large"`

**Composite score:** `fit_score * 0.7 + intent_score * 0.3` (intent defaults to 50)

**Tier:** hot ≥ 70 / warm ≥ 40 / cold < 40

Add tests in `tests/test_scoring.py`.

---

## Phase 6 — Recommendations

### TICKET-11: Implement `recommend_next_action`

**File:** `app/services/recommendation.py`

Define a `Recommendation` dataclass: `action`, `channel`, `reason`.

Mapping:
- `hot` → `schedule_call` / `phone`
- `warm` → `send_email` / `email`
- `cold` → `add_to_nurture` / `crm_sequence`

Override: `employee_count > 500` and tier `warm` → escalate to `schedule_call`.
Add tests in `tests/test_recommendation.py`.

---

## Phase 7 — Decision log

### TICKET-12: Implement `DecisionLogORM` columns

**File:** `app/models/decision.py`

- Add FK to `leads.id`
- Columns: `action: str`, `actor: str` (`"system"` | `"human"`), `reason: str | None`, `created_at: datetime`

### TICKET-13: Add `decision_repository`

**File:** `app/repositories/decision_repository.py` *(create)*

- `create_decision(session, lead_id, action, actor="system", reason=None) -> DecisionLogORM`

Call from scoring and recommendation services after each run.

---

## Phase 8 — API routes

### TICKET-14: `POST /leads/ingest`

Accept a multipart CSV upload, call `import_leads`, return `ImportResult` as JSON.

### TICKET-15: `GET /leads`

Paginated list — `?limit=20&offset=0`. Returns `list[LeadRead]`.

### TICKET-16: `GET /leads/{id}/score`

Load lead → enrich → score → recommend. Returns `ScoringResult` + `Recommendation` as JSON.

---

## Phase 9 — LLM layer (optional)

### TICKET-17: Define a provider interface

**File:** `app/llm/base.py` *(create)*

Abstract `LLMProvider` with `complete(prompt: str) -> str`.
Implement `NoOpProvider` that raises `NotImplementedError`.

### TICKET-18: Optional LLM enrichment

**File:** `app/services/enrichment.py`

Add `provider: LLMProvider | None = None` to `enrich_lead`.
Guard behind a config flag — CI must never require an API key.
