from dataclasses import dataclass, field
from pathlib import Path

from sqlalchemy.ext.asyncio import AsyncSession

from app.loaders.csv_loader import load_leads_from_csv
from app.repositories import lead_repository
from app.utility.codes import LogCode
from app.utility.logger import AppLogger

DEFAULT_CSV = Path("data/sample_leads.csv")


@dataclass
class ImportResult:
    imported: int = 0
    skipped: int = 0
    errors: list[dict] = field(default_factory=list)


async def import_leads(session: AsyncSession, path: Path = DEFAULT_CSV) -> ImportResult:
    csv_result = load_leads_from_csv(path)
    result = ImportResult(skipped=len(csv_result.errors))

    for lead in csv_result.valid:
        try:
            await lead_repository.create(session, lead)
            result.imported += 1
        except Exception as exc:
            AppLogger.error(LogCode.ERR_DB_WRITE, f"Failed to persist lead {lead.email}: {exc}")
            result.errors.append({"lead": lead.email, "error": str(exc)})

    AppLogger.info(
        LogCode.INF_LEAD_CREATED,
        f"{path.name}: {result.imported} imported, {result.skipped} skipped",
    )
    return result
