"""Lead domain model.

SQLAlchemy ORM table and Pydantic schema for a sales lead.
"""

from pydantic import BaseModel, ValidationError, field_validator
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass

# TODO: Add relationship to DecisionLog once that model exists
class LeadORM(Base):
    __tablename__ = "leads"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    company: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False)
    phone: Mapped[str] = mapped_column(nullable=False)
    role: Mapped[str] = mapped_column(nullable=False)
    company_size: Mapped[str] = mapped_column(nullable=False)
    industry: Mapped[str] = mapped_column(nullable=False)
    employee_count: Mapped[int] = mapped_column(nullable=False)
    source: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[str] = mapped_column(nullable=False)
    updated_at: Mapped[str] = mapped_column(nullable=False)


# TODO: Add field validators (email normalisation, phone stripping, …)
# TODO: Add a LeadCreate schema (no id) and a LeadRead schema (with id)
class LeadSchema(BaseModel):
    id: int | None = None
    name: str | None = None
    company: str | None = None
    email: str | None = None
    phone: str | None = None
    role: str | None = None
    company_size: str | None = None
    industry: str | None = None
    employee_count: int | None = None
    source: str | None = None
    created_at: str | None = None

    model_config = {"from_attributes": True}
