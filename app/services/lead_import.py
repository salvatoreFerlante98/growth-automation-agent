from dataclasses import dataclass, field
from pathlib import Path

from sqlalchemy.ext.asyncio import AsyncSession

from app.loaders.csv_loader import load_leads_from_csv
from app.utility.codes import LogCode
from app.utility.logger import AppLogger

DEFAULT_CSV = Path("data/sample_leads.csv")


@dataclass
class ImportResult:
    imported: int = 0
    skipped: int = 0
    errors: list[dict] = field(default_factory=list)


# TODO: call load_leads_from_csv(path) to get a LoadResult
# TODO: for each lead in LoadResult.valid, call lead_repository.create(session, lead)
#       wrap each create in try/except and append failures to ImportResult.errors
# TODO: set ImportResult.imported = number of successfully persisted leads
# TODO: set ImportResult.skipped = len(LoadResult.errors)
# TODO: log a summary with AppLogger.info(LogCode.INF_LEAD_CREATED, ...)
async def import_leads(session: AsyncSession, path: Path = DEFAULT_CSV) -> ImportResult:
    raise NotImplementedError
