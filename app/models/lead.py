"""Lead domain model.

SQLAlchemy ORM table and Pydantic schema for a sales lead.
"""
from datetime import datetime

from pydantic import BaseModel, EmailStr, field_validator
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
    created_at: Mapped[datetime] = mapped_column(nullable=False)
    updated_at: Mapped[datetime] = mapped_column(nullable=False)


class LeadCreate(BaseModel):
    """Input schema — used for CSV ingestion and API creation requests."""

    name: str
    company: str
    email: EmailStr
    phone: str
    role: str
    company_size: str
    industry: str
    employee_count: int
    source: str

    @field_validator("phone")
    @classmethod
    def phone_must_be_valid(cls, v: str) -> str:
        if not v.isdigit():
            raise ValueError("Phone number must contain digits only")
        return v

    @field_validator("employee_count")
    @classmethod
    def employee_count_must_be_positive(cls, v: int) -> int:
        if v <= 0:
            raise ValueError("Employee count must be positive")
        return v


class LeadRead(LeadCreate):
    """Output schema — returned by API responses, constructed from ORM rows."""

    id: int
    created_at: datetime
    updated_at: datetime | None = None

    model_config = {"from_attributes": True}
