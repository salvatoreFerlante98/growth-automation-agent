"""Lead enrichment service.

Augments a lead with additional data from a mock (or real) enrichment source.
"""

from app.models.lead import LeadSchema


# TODO: Define an EnrichmentResult dataclass/Pydantic model for the extra fields
# TODO: Implement mock enrichment that fills missing fields with plausible test data
# TODO: Add a real-provider integration path guarded by a feature flag / config key
async def enrich_lead(lead: LeadSchema) -> LeadSchema:
    """Enrich a lead with additional data.  Not yet implemented."""
    # TODO: implement
    raise NotImplementedError
