"""Lead domain model.

SQLAlchemy ORM table and Pydantic schema for a sales lead.
"""

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from pydantic import BaseModel


class Base(DeclarativeBase):
    pass


# TODO: Add all lead fields (company, title, industry, employee_count, …)
# TODO: Add created_at / updated_at timestamp columns
# TODO: Add relationship to DecisionLog once that model exists
class LeadORM(Base):
    __tablename__ = "leads"

    id: Mapped[int] = mapped_column(primary_key=True)
    # TODO: define remaining columns


# TODO: Add field validators (email normalisation, phone stripping, …)
# TODO: Add a LeadCreate schema (no id) and a LeadRead schema (with id)
class LeadSchema(BaseModel):
    id: int | None = None
    # TODO: mirror LeadORM fields here

    model_config = {"from_attributes": True}
