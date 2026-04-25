"""Next-action recommendation service.

Produces a recommended action (and optional message template) for a scored lead.
"""

from app.models.scoring import ScoringResult


# TODO: Define a Recommendation dataclass: action, channel, template_id, reason
# TODO: Map tier → default action (hot → "call", warm → "email", cold → "nurture")
# TODO: Add rule overrides (e.g. enterprise leads always get a call regardless of tier)
def recommend_next_action(result: ScoringResult) -> str:
    """Return a next-action string for a scored lead.  Not yet implemented."""
    # TODO: implement
    raise NotImplementedError
