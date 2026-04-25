"""CSV lead loader.

Reads a CSV file and yields raw lead dicts for further validation.
"""

from pathlib import Path


# TODO: Validate each row against LeadSchema; collect and surface row-level errors
# TODO: Normalise column names (strip whitespace, lowercase) before parsing
# TODO: Return a LoadResult(valid: list[LeadSchema], invalid: list[dict]) dataclass
def load_leads_from_csv(path: Path) -> list[dict]:
    """Read CSV rows as plain dicts.  Validation is not yet implemented."""
    # TODO: implement
    raise NotImplementedError
