# Architecture

## Layer overview

The project follows a simple layered structure. Each layer has one job and depends only on layers below it.

```
API (main.py)
  └── Services (services/)
        ├── Loaders (loaders/)
        └── Repositories (repositories/)
              └── Models (models/)

Utility (utility/) — used by all layers for logging
```

---

## models/

Domain entities and value objects. No business logic here.

| File | Purpose |
|------|---------|
| `lead.py` | `LeadORM` (SQLAlchemy table), `LeadCreate` (input schema), `LeadRead` (output schema) |
| `scoring.py` | `ScoringResult` — output of the scoring service |
| `decision.py` | `DecisionLogORM` — audit trail of every automated decision |

`LeadCreate` is the input contract: used for CSV ingestion and API creation requests.
`LeadRead` is the output contract: returned by API responses, constructed from ORM rows via `from_attributes`.

---

## services/

Application use cases. Each service orchestrates one coherent workflow.

| File | Purpose |
|------|---------|
| `lead_import.py` | Orchestrates CSV load → validation → DB persist. Returns `ImportResult`. |
| `scoring.py` | Applies deterministic scoring rules to a `LeadCreate`. Returns `ScoringResult`. |
| `enrichment.py` | Fills missing fields with mock or provider-backed data. Returns enriched `LeadCreate`. |
| `recommendation.py` | Maps a `ScoringResult` tier to a next action. Returns `Recommendation`. |

Services are async where they touch the DB. Pure logic functions (scoring, enrichment) are sync.

---

## repositories/

All database access goes through this layer. Services never write SQL directly.

| File | Purpose |
|------|---------|
| `lead_repository.py` | `create`, `get_by_id`, `list_all`, `upsert`, `delete` |

Functions take an `AsyncSession` as the first argument. The session is injected by the caller — repositories do not create sessions themselves.

---

## loaders/

Infrastructure I/O — reading external data sources into domain objects.

| File | Purpose |
|------|---------|
| `csv_loader.py` | Reads a CSV, normalises column names, validates each row against `LeadCreate`. Returns `LoadResult(valid, errors)`. |

The loader never writes to the DB. It only produces validated `LeadCreate` objects for the service layer to persist.

---

## utility/

Cross-cutting concerns shared across all layers.

| File | Purpose |
|------|---------|
| `codes.py` | `LogCode` enum — all log code constants in one place (`INF-001`, `ERR-003`, …) |
| `logger.py` | `AppLogger` — static methods that format every log line as `[CODE] message`. `configure_logging()` called once at startup. |

`LogCode` values are used exclusively as formatting prefixes in log calls. They do not type exceptions or affect control flow.

---

## Design decisions

**Why `LeadCreate` in `csv_loader`, not `LeadRead`?**
`LeadRead` requires `id` and `created_at`, which don't exist before DB insertion. The loader produces input data, so `LeadCreate` is the correct contract.

**Why `AsyncSession` injected into repositories?**
Keeps transaction boundaries in the caller (service or route), not inside the repository. A service that calls multiple repositories can wrap them in a single transaction.

**Why no `AppError` custom exception?**
Tried it, removed it. The added complexity of custom exception types wasn't worth it for this scale. Standard `ValueError` (wrapped by Pydantic into `ValidationError`) plus `Exception` for fatal I/O errors is sufficient. `LogCode` provides categorisation at the logging level without coupling it to the exception hierarchy.
