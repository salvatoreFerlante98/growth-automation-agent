"""Lead scoring service.

Applies a deterministic scoring algorithm to a lead and returns a ScoringResult.
"""

from app.models.lead import LeadSchema
from app.models.scoring import ScoringResult


# TODO: Define scoring weights as module-level constants (not magic numbers)
# TODO: Implement sub-scores: firmographic fit, role fit, intent signals
# TODO: Combine sub-scores into a composite 0–100 score
# TODO: Map composite score to tier: hot (>= 70), warm (40–69), cold (< 40)
def score_lead(lead: LeadSchema) -> ScoringResult:
    """Score a lead deterministically.  Not yet implemented."""
    # TODO: implement
    raise NotImplementedError
