"""Tests for lead_repository — run against an in-memory SQLite database."""

from datetime import UTC, datetime

import pytest
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from app.models.lead import Base, LeadRead
from app.repositories import lead_repository as repo

SAMPLE = {
    "name": "Alice Chen",
    "company": "Vertexio",
    "email": "alice.chen@vertexio.com",
    "phone": "3471234567",
    "role": "VP of Sales",
    "company_size": "medium",
    "industry": "SaaS",
    "employee_count": 320,
    "source": "csv",
}


def make_lead(**overrides) -> LeadRead:
    lead_id = overrides.pop("id", 1)
    return LeadRead(**{**SAMPLE, **overrides}, id=lead_id, created_at=datetime.now(UTC))


@pytest.fixture
async def session():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with AsyncSession(engine) as s:
        yield s
    await engine.dispose()


# --- create ---

async def test_create_returns_orm_row(session):
    lead = await repo.create(session, make_lead())
    assert lead.id is not None
    assert lead.name == "Alice Chen"


async def test_create_sets_timestamps(session):
    lead = await repo.create(session, make_lead())
    assert lead.created_at is not None
    assert lead.updated_at is not None


async def test_create_persists_to_db(session):
    created = await repo.create(session, make_lead())
    fetched = await repo.get_by_id(session, created.id)
    assert fetched is not None
    assert fetched.email == "alice.chen@vertexio.com"


# --- get_by_id ---

async def test_get_by_id_returns_none_when_missing(session):
    result = await repo.get_by_id(session, 999)
    assert result is None


# --- list_all ---

async def test_list_all_returns_created_leads(session):
    await repo.create(session, make_lead(email="a@test.com"))
    await repo.create(session, make_lead(email="b@test.com"))
    leads = await repo.list_all(session, limit=10, offset=0)
    assert len(leads) == 2


async def test_list_all_limit(session):
    for i in range(5):
        await repo.create(session, make_lead(email=f"lead{i}@test.com"))
    leads = await repo.list_all(session, limit=3, offset=0)
    assert len(leads) == 3


async def test_list_all_offset(session):
    for i in range(4):
        await repo.create(session, make_lead(email=f"lead{i}@test.com"))
    leads = await repo.list_all(session, limit=10, offset=3)
    assert len(leads) == 1


# --- upsert ---

async def test_upsert_creates_when_id_not_found(session):
    lead = await repo.upsert(session, make_lead(id=999))
    assert lead.id is not None
    assert lead.name == "Alice Chen"


async def test_upsert_updates_existing_lead(session):
    created = await repo.create(session, make_lead())
    updated_data = LeadRead(
        **{**SAMPLE, "name": "Alice Updated"},
        id=created.id,
        created_at=created.created_at,
    )
    updated = await repo.upsert(session, updated_data)
    assert updated.id == created.id
    assert updated.name == "Alice Updated"


async def test_upsert_preserves_created_at(session):
    created = await repo.create(session, make_lead())
    original_created_at = created.created_at
    updated_data = LeadRead(
        **{**SAMPLE, "name": "Alice Updated"},
        id=created.id,
        created_at=created.created_at,
    )
    updated = await repo.upsert(session, updated_data)
    assert updated.created_at == original_created_at


async def test_upsert_refreshes_updated_at(session):
    created = await repo.create(session, make_lead())
    original_updated_at = created.updated_at
    updated_data = LeadRead(
        **{**SAMPLE, "name": "Alice Updated"},
        id=created.id,
        created_at=created.created_at,
    )
    updated = await repo.upsert(session, updated_data)
    assert updated.updated_at >= original_updated_at


# --- delete ---

async def test_delete_returns_true_when_found(session):
    created = await repo.create(session, make_lead())
    result = await repo.delete(session, created.id)
    assert result is True


async def test_delete_removes_row_from_db(session):
    created = await repo.create(session, make_lead())
    await repo.delete(session, created.id)
    assert await repo.get_by_id(session, created.id) is None


async def test_delete_returns_false_when_not_found(session):
    result = await repo.delete(session, 999)
    assert result is False
