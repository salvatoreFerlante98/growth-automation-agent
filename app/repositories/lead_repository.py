"""Lead repository.

All database access for leads goes through this module.
"""

from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.lead import LeadORM, LeadRead


async def create(session: AsyncSession, lead: LeadRead) -> LeadORM:
    now = datetime.now()
    db_lead = LeadORM(
        name=lead.name,
        company=lead.company,
        email=lead.email,
        phone=lead.phone,
        role=lead.role,
        company_size=lead.company_size,
        industry=lead.industry,
        employee_count=lead.employee_count,
        source=lead.source,
        created_at=now,
        updated_at=now,
    )
    session.add(db_lead)
    await session.commit()
    await session.refresh(db_lead)
    return db_lead


async def get_by_id(session: AsyncSession, lead_id: int) -> LeadORM | None:
    stmt = select(LeadORM).where(
        LeadORM.id == lead_id,
    )
    result = await session.execute(stmt)
    return result.scalars().first()


async def list_all(session: AsyncSession, *, limit: int, offset: int) -> list[LeadORM]:
    stmt = select(LeadORM).limit(limit).offset(offset)
    result = await session.execute(stmt)
    return list(result.scalars().all())


async def upsert(session: AsyncSession, lead: LeadRead) -> LeadORM:
    db_lead = await get_by_id(session, lead.id)
    now = datetime.now()

    if db_lead is None:
        db_lead = LeadORM(
            name=lead.name,
            company=lead.company,
            email=lead.email,
            phone=lead.phone,
            role=lead.role,
            company_size=lead.company_size,
            industry=lead.industry,
            employee_count=lead.employee_count,
            source=lead.source,
            created_at=now,
            updated_at=now,
        )
        session.add(db_lead)
    else:
        db_lead.name = lead.name
        db_lead.company = lead.company
        db_lead.email = lead.email
        db_lead.phone = lead.phone
        db_lead.role = lead.role
        db_lead.company_size = lead.company_size
        db_lead.industry = lead.industry
        db_lead.employee_count = lead.employee_count
        db_lead.source = lead.source
        db_lead.updated_at = now

    await session.commit()
    await session.refresh(db_lead)
    return db_lead


async def delete(session: AsyncSession, lead_id: int) -> bool:
    db_lead = await get_by_id(session, lead_id)
    if db_lead is None:
        return False
    await session.delete(db_lead)
    await session.commit()
    return True
