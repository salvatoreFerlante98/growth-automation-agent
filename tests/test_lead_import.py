"""End-to-end tests for the lead import use case."""

from pathlib import Path

import pytest
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from app.models.lead import Base
from app.repositories import lead_repository as repo
from app.services.lead_import import ImportResult, import_leads

SAMPLE_CSV = Path("data/sample_leads.csv")


@pytest.fixture
async def session():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with AsyncSession(engine) as s:
        yield s
    await engine.dispose()


async def test_import_sample_csv_succeeds(session):
    result = await import_leads(session, SAMPLE_CSV)
    assert isinstance(result, ImportResult)
    assert result.imported == 5
    assert result.skipped == 0
    assert result.errors == []


async def test_import_persists_all_leads_to_db(session):
    await import_leads(session, SAMPLE_CSV)
    leads = await repo.list_all(session, limit=10, offset=0)
    assert len(leads) == 5


async def test_import_lead_data_is_correct(session):
    await import_leads(session, SAMPLE_CSV)
    leads = await repo.list_all(session, limit=10, offset=0)
    emails = {lead.email for lead in leads}
    assert "alice.chen@vertexio.com" in emails
    assert "sara.l@nordicflow.se" in emails


async def test_import_invalid_csv_path_raises(session):
    with pytest.raises(Exception):
        await import_leads(session, Path("data/nonexistent.csv"))


async def test_import_partial_failure(session, tmp_path):
    csv = tmp_path / "leads.csv"
    csv.write_text(
        "name,company,email,phone,role,company_size,industry,employee_count,source\n"
        "Alice Chen,Vertexio,alice.chen@vertexio.com,3471234567,VP of Sales,medium,SaaS,320,csv\n"
        "Bad Lead,Acme,not-an-email,3471234567,Dev,small,Tech,10,csv\n"
        "Sara lasd,NordicFlow,sara.l@nordicflow.se,4701234567,Director,large,Logistics,670,csv\n"
    )
    result = await import_leads(session, csv)
    assert result.imported == 2
    assert result.skipped == 1
