# Error handling flow

## Overview

Errors in this project are typed via `AppError`, which carries a `LogCode`.
This allows callers to branch on the specific error type without matching strings,
and ensures every error that crosses a module boundary is logged consistently.

---

## Components

| Module | Role |
|--------|------|
| `app/utility/codes.py` | Registry of all `LogCode` values (`ERR-001`, `WRN-001`, …) |
| `app/utility/errors.py` | `AppError(Exception)` — carries `code` and `detail` |
| `app/utility/logger.py` | `AppLogger` — static methods that format log lines as `[CODE] message` |
| `app/models/lead.py` | Raises `AppError` from Pydantic validators for business rule violations |
| `app/loaders/csv_loader.py` | Catches `AppError` and `ValidationError` separately per row |

---

## Why two exception types

Pydantic only catches `ValueError` and `AssertionError` inside `field_validator`.
Any other exception propagates directly out of `model_validate`.

This means:

- **`AppError`** (business rule violation) — escapes Pydantic, caught explicitly by the caller
- **`ValidationError`** (structural error) — raised by Pydantic for missing fields, wrong types, invalid email

The two cases are handled separately because they have different semantics and different information to surface.

---

## CSV ingestion flow

```
load_leads_from_csv(path)
│
├── path does not exist
│   └── AppLogger.raise_error(ERR-001)  →  AppError propagates to caller
│
├── OSError on file open/read
│   └── AppLogger.raise_error(ERR-002)  →  AppError propagates to caller
│
└── for each row:
    │
    ├── normalise keys and values (strip + lowercase)
    │
    └── LeadCreate.model_validate(normalised)
        │
        ├── phone not digits
        │   └── validator raises AppError(ERR-003)
        │       caught by: except AppError
        │       result: row added to LoadResult.errors with error_code + detail
        │
        ├── employee_count <= 0
        │   └── validator raises AppError(ERR-003)
        │       caught by: except AppError
        │       result: row added to LoadResult.errors with error_code + detail
        │
        ├── missing required field / wrong type / invalid email
        │   └── Pydantic raises ValidationError
        │       caught by: except ValidationError
        │       result: row added to LoadResult.errors with error_code + errors list
        │
        └── all fields valid
            └── lead appended to LoadResult.valid
```

---

## LoadResult

`load_leads_from_csv` never raises for individual row failures.
It always returns a `LoadResult` so the caller decides how to proceed.

```python
result = load_leads_from_csv(Path("data/sample_leads.csv"))

if result.has_errors:
    # inspect result.errors — list of dicts with "line", "error_code", "detail" or "errors"
    ...

for lead in result.valid:
    # LeadCreate instances, ready for enrichment or persistence
    ...
```

---

## Adding a new validator

1. Add a `LogCode` entry in `codes.py` if needed (reuse `ERR_LEAD_VALIDATION` for lead field rules).
2. Raise `AppError(LogCode.ERR_LEAD_VALIDATION, "descriptive detail")` in the validator.
3. No changes needed in `csv_loader.py` — `except AppError` already catches it.
4. Add a test in `tests/test_lead_schema.py` asserting `pytest.raises(AppError)` with the expected `exc.code`.
