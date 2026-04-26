"""API tests for /leads endpoints."""

# TODO: once TICKET-04 (app/database.py) is done, override get_session dependency
#       with an in-memory SQLite session so tests don't hit the real DB:
#
#   from app.database import get_session
#   from app.models.lead import Base
#   from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
#
#   @pytest.fixture
#   async def session():
#       engine = create_async_engine("sqlite+aiosqlite:///:memory:")
#       async with engine.begin() as conn:
#           await conn.run_sync(Base.metadata.create_all)
#       async with AsyncSession(engine) as s:
#           yield s
#   await engine.dispose()
#
#   @pytest.fixture
#   def client(session):
#       app.dependency_overrides[get_session] = lambda: session
#       yield TestClient(app)
#       app.dependency_overrides.clear()

# TODO: test_import_sample_returns_200
#   POST /leads/import-sample
#   assert response.status_code == 200
#   assert response.json()["imported"] == 5

# TODO: test_list_leads_returns_empty_initially
#   GET /leads
#   assert response.status_code == 200
#   assert response.json() == []

# TODO: test_list_leads_returns_imported_leads
#   POST /leads/import-sample first, then GET /leads
#   assert len(response.json()) == 5

# TODO: test_get_lead_returns_correct_lead
#   POST /leads/import-sample, then GET /leads/1
#   assert response.status_code == 200
#   assert response.json()["email"] is not None

# TODO: test_get_lead_returns_404_for_missing
#   GET /leads/9999
#   assert response.status_code == 404
#   assert response.json()["detail"] == "Lead not found"

# TODO: test_list_leads_pagination
#   POST /leads/import-sample, then GET /leads?limit=2&offset=0
#   assert len(response.json()) == 2
