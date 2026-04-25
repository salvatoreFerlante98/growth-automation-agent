import csv
from dataclasses import dataclass, field
from pathlib import Path

from pydantic import ValidationError

from app.models.lead import LeadCreate
from app.utility.codes import LogCode
from app.utility.logger import AppLogger


@dataclass
class LoadResult:
    valid: list[LeadCreate] = field(default_factory=list)
    errors: list[dict] = field(default_factory=list)

    @property
    def has_errors(self) -> bool:
        return bool(self.errors)


def load_leads_from_csv(path: Path) -> LoadResult:
    if not path.exists():
        AppLogger.raise_error(LogCode.ERR_FILE_NOT_FOUND, f"File not found: {path}")

    result = LoadResult()

    try:
        with path.open(newline="", encoding="utf-8") as f:
            for line_number, raw_row in enumerate(csv.DictReader(f), start=2):
                normalised = {k.strip().lower(): v.strip() for k, v in raw_row.items()}

                try:
                    result.valid.append(LeadCreate.model_validate(normalised))
                except ValidationError as exc:
                    messages = "; ".join(f"{e['loc'][0]}: {e['msg']}" for e in exc.errors())
                    AppLogger.warning(LogCode.WRN_CSV_ROW_SKIPPED, f"Line {line_number}: {messages}")
                    result.errors.append({"line": line_number, "errors": exc.errors()})

    except OSError as exc:
        AppLogger.raise_error(LogCode.ERR_CSV_PARSE, f"Cannot read {path}: {exc}")

    AppLogger.info(LogCode.INF_CSV_LOADED, f"{path.name}: {len(result.valid)} loaded, {len(result.errors)} skipped")
    return result
