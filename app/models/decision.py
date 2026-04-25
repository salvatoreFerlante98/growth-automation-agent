"""Decision log model.

Records every automated or human decision made for a lead.
"""

from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column

from app.models.lead import Base


# TODO: Add a ForeignKey to leads.id and a relationship to LeadORM
# TODO: Add a `reason` text column for the rationale behind the decision
# TODO: Add an `actor` column (system | human) to distinguish automated vs manual
class DecisionLogORM(Base):
    __tablename__ = "decision_logs"

    id: Mapped[int] = mapped_column(primary_key=True)
    lead_id: Mapped[int]  # TODO: make this a FK
    action: Mapped[str]  # e.g. "enrich", "score", "recommend"
    created_at: Mapped[datetime]
