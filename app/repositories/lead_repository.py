"""Lead repository.

All database access for leads goes through this module.
"""

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.lead import LeadORM, LeadSchema


# TODO: Add get_by_id(session, lead_id) -> LeadORM | None
# TODO: Add list_all(session, *, limit, offset) -> list[LeadORM]
# TODO: Add upsert(session, lead: LeadSchema) -> LeadORM
# TODO: Add delete(session, lead_id) -> bool
async def create(session: AsyncSession, lead: LeadSchema) -> LeadORM:
    """Persist a new lead row.  Not yet implemented."""
    # TODO: implement
    raise NotImplementedError
