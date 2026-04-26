from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.lead import LeadRead
from app.services.lead_import import ImportResult

# TODO: import get_session from app.database once TICKET-04 is implemented
# TODO: import lead_repository for get_by_id and list_all
# TODO: import import_leads from app.services.lead_import

router = APIRouter(prefix="/leads", tags=["leads"])


# POST /leads/import-sample
# TODO: inject session via Depends(get_session)
# TODO: call import_leads(session) with the default sample CSV path
# TODO: return the ImportResult directly (imported, skipped, errors)
@router.post("/import-sample", response_model=ImportResult)
async def import_sample():
    raise NotImplementedError


# GET /leads
# TODO: inject session via Depends(get_session)
# TODO: call lead_repository.list_all(session, limit=limit, offset=offset)
# TODO: return list[LeadRead]
@router.get("/", response_model=list[LeadRead])
async def list_leads(limit: int = 20, offset: int = 0):
    raise NotImplementedError


# GET /leads/{lead_id}
# TODO: inject session via Depends(get_session)
# TODO: call lead_repository.get_by_id(session, lead_id)
# TODO: if None → raise HTTPException(status_code=404, detail="Lead not found")
# TODO: return the lead as LeadRead
@router.get("/{lead_id}", response_model=LeadRead)
async def get_lead(lead_id: int):
    raise NotImplementedError
