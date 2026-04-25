# Error handling flow

## Overview

Errors use standard Python and Pydantic exceptions. `LogCode` values are
constants used exclusively for log formatting — they do not type exceptions
or affect control flow.

---

## Components

| Module | Role |
|--------|------|
| `app/utility/codes.py` | `LogCode` constants (`ERR-001`, `WRN-001`, …) used as log prefixes |
| `app/utility/logger.py` | `AppLogger` — formats every log line as `[CODE] message` |
| `app/models/lead.py` | Validators raise `ValueError`; Pydantic wraps them in `ValidationError` |
| `app/loaders/csv_loader.py` | Catches `ValidationError` per row; fatal I/O errors propagate as `Exception` |

---

## CSV ingestion flow

```
load_leads_from_csv(path)
│
├── path does not exist
│   └── AppLogger.raise_error(ERR-001)  →  Exception propagates to caller
│
├── OSError on file open/read
│   └── AppLogger.raise_error(ERR-002)  →  Exception propagates to caller
│
└── for each row:
    │
    ├── normalise keys and values (strip + lowercase)
    │
    └── LeadCreate.model_validate(normalised)
        │
        ├── any field invalid (phone, employee_count, email, missing field, …)
        │   └── Pydantic raises ValidationError
        │       caught by: except ValidationError
        │       logged as: [WRN-001] Line N: field: message
        │       result: row added to LoadResult.errors
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
    # result.errors — list of {"line": int, "errors": list[dict]}
    ...

for lead in result.valid:
    # LeadCreate instances, ready for enrichment or persistence
    ...
```

---

## Adding a new validator

1. Add the rule in `lead.py` as a `field_validator` that raises `ValueError`.
2. Add a test in `tests/test_lead_schema.py` with `pytest.raises(ValidationError)`.
3. No changes needed in `csv_loader.py`.
