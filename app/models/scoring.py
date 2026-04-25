"""Scoring result model.

Represents the output of the lead scoring service.
"""

from pydantic import BaseModel


# TODO: Add score breakdown fields (fit_score, intent_score, composite_score, …)
# TODO: Add an explanation list[str] field for human-readable score reasons
class ScoringResult(BaseModel):
    lead_id: int
    score: float  # TODO: constrain to 0.0–100.0 with Field(ge=0, le=100)
    tier: str  # TODO: derive tier (hot/warm/cold) from score thresholds
