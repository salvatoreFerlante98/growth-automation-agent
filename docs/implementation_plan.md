# Implementation Plan

Each ticket below is a small, self-contained coding task.
Implement them in order — later tickets depend on earlier ones.

---

## Phase 2 — Domain model

### TICKET-01: Define `LeadORM` columns

**File:** `app/models/lead.py`

Add mapped columns to `LeadORM`:

- `first_name: Mapped[str]`
- `last_name: Mapped[str]`
- `email: Mapped[str]` (unique)
- `company: Mapped[str]`
- `title: Mapped[str | None]`
- `industry: Mapped[str | None]`
- `employee_count: Mapped[int | None]`
- `country: Mapped[str | None]`
- `linkedin_url: Mapped[str | None]`
- `created_at: Mapped[datetime]` with `default=datetime.utcnow`

---

### TICKET-02: Define `LeadCreate` and `LeadRead` Pydantic schemas

**File:** `app/models/lead.py`

- `LeadCreate` — all fields except `id` and `created_at`; add an `EmailStr` validator for `email`
- `LeadRead` — all fields including `id` and `created_at`; `model_config = {"from_attributes": True}`

---

### TICKET-03: Extend `ScoringResult`

**File:** `app/models/scoring.py`

Add:
- `fit_score: float` — 0–100, firmographic and role alignment
- `intent_score: float` — 0–100, placeholder (always 50 until intent data exists)
- `composite_score: float` — weighted average of sub-scores
- `tier: Literal["hot", "warm", "cold"]` — derived from composite_score
- `reasons: list[str]` — human-readable explanation lines

Constrain all floats with `Field(ge=0.0, le=100.0)`.

---

### TICKET-04: Wire up the async database engine

**File:** `app/database.py` *(create this file)*

- Create an `async_engine` using `create_async_engine` with a `DATABASE_URL` setting (default: `sqlite+aiosqlite:///./leads.db`)
- Create an `AsyncSessionLocal` session factory
- Add a `get_session()` async generator for FastAPI dependency injection
- Add a `create_tables()` coroutine that calls `Base.metadata.create_all`

Call `create_tables()` from `app/main.py` on startup using `@app.on_event("startup")`.

---

## Phase 3 — CSV ingestion

### TICKET-05: Implement `load_leads_from_csv`

**File:** `app/loaders/csv_loader.py`

- Open the file, use `csv.DictReader`
- Strip whitespace from all keys and values
- Validate each row against `LeadCreate`; catch `ValidationError`
- Return a simple result object (or named tuple) with `valid: list[LeadCreate]` and `errors: list[dict]`
  - Each error entry should include the row number and the validation message

---

## Phase 4 — Enrichment

### TICKET-06: Implement mock enrichment

**File:** `app/services/enrichment.py`

Rules (apply only when the field is `None` or blank):
- `industry`: infer from a small hardcoded keyword map on `company` name, default to `"Unknown"`
- `employee_count`: default to `50`
- `country`: default to `"US"`

Return a new `LeadCreate` (do not mutate the input).

---

## Phase 5 — Scoring

### TICKET-07: Implement `score_lead`

**File:** `app/services/scoring.py`

Scoring rules (deterministic):

**Fit score** (0–100):
- `+30` if `employee_count` is between 50 and 1000
- `+25` if `title` contains "VP", "Director", "Head", "CTO", "Founder", or "C-level"
- `+20` if `industry` is in a defined target-industry list (e.g. SaaS, Fintech, DevTools)
- `+10` if `country` is `"US"`, `"UK"`, or `"CA"`
- Up to `+15` spare — reserve for future signals

**Composite score:** `fit_score * 0.7 + intent_score * 0.3` (intent is always 50 for now)

**Tier:**
- `hot` if composite >= 70
- `warm` if composite >= 40
- `cold` otherwise

Collect a `reasons` list explaining which rules fired.

---

## Phase 6 — Recommendations

### TICKET-08: Implement `recommend_next_action`

**File:** `app/services/recommendation.py`

Define a `Recommendation` dataclass:
- `action: str` — e.g. `"schedule_call"`, `"send_email"`, `"add_to_nurture"`
- `channel: str` — `"phone"`, `"email"`, `"crm_sequence"`
- `reason: str` — one-line explanation

Mapping:
- `hot` → `schedule_call` via `phone`
- `warm` → `send_email` via `email`
- `cold` → `add_to_nurture` via `crm_sequence`

Override: if `employee_count > 500` and tier is `warm`, escalate to `schedule_call`.

---

## Phase 7 — Decision log

### TICKET-09: Persist decisions

**File:** `app/repositories/decision_repository.py` *(create this file)*

- Add a `create_decision(session, lead_id, action, actor="system")` function
- `actor` should be `"system"` for automated decisions and `"human"` for manual overrides

Call `create_decision` from the scoring and recommendation services after each run.

---

## Phase 8 — API routes

### TICKET-10: POST `/leads/ingest`

**File:** `app/main.py` (or a new `app/api/leads.py` router if the file grows large)

- Accept a multipart CSV upload
- Call `load_leads_from_csv`, then `enrich_lead`, then `create` (repository)
- Return `{"imported": N, "errors": [...]}`

### TICKET-11: GET `/leads/{id}/score`

- Load the lead from the DB
- Call `score_lead` and `recommend_next_action`
- Return the `ScoringResult` + `Recommendation` as JSON

### TICKET-12: GET `/leads`

- Paginated list of leads (`?limit=20&offset=0`)
- Return `list[LeadRead]`

---

## Phase 9 — LLM layer (optional, later)

### TICKET-13: Define a provider interface

**File:** `app/llm/base.py` *(create this file)*

- Define an abstract `LLMProvider` with a single `complete(prompt: str) -> str` method
- Implement a `NoOpProvider` that raises `NotImplementedError` with a clear message

### TICKET-14: Optional enrichment via LLM

**File:** `app/services/enrichment.py`

- Add an optional `provider: LLMProvider | None = None` parameter to `enrich_lead`
- If a provider is passed and a field is still missing after rule-based enrichment, call the provider
- Guard behind a config flag so CI never requires an API key
