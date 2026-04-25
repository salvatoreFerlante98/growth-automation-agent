"""Tests for LeadCreate and LeadRead field validators and structure."""

from datetime import UTC, datetime

import pytest
from pydantic import ValidationError

from app.models.lead import LeadCreate, LeadRead

VALID_DATA = {
    "name": "Alice Chen",
    "company": "Vertexio",
    "email": "alice.chen@vertexio.com",
    "phone": "3471234567",
    "role": "VP of Sales",
    "company_size": "medium",
    "industry": "SaaS",
    "employee_count": 320,
    "source": "csv",
}


# --- structure ---

def test_valid_lead_instantiates():
    lead = LeadCreate(**VALID_DATA)
    assert lead.name == "Alice Chen"
    assert lead.company == "Vertexio"


def test_missing_required_field_raises():
    data = {k: v for k, v in VALID_DATA.items() if k != "name"}
    with pytest.raises(ValidationError) as exc_info:
        LeadCreate(**data)
    assert any(e["loc"] == ("name",) for e in exc_info.value.errors())


# --- email ---

def test_valid_email_accepted():
    lead = LeadCreate(**{**VALID_DATA, "email": "user@example.com"})
    assert lead.email == "user@example.com"


def test_invalid_email_raises():
    with pytest.raises(ValidationError) as exc_info:
        LeadCreate(**{**VALID_DATA, "email": "not-an-email"})
    assert any(e["loc"] == ("email",) for e in exc_info.value.errors())


# --- phone ---

def test_valid_phone_accepted():
    lead = LeadCreate(**{**VALID_DATA, "phone": "3471234567"})
    assert lead.phone == "3471234567"


def test_phone_with_spaces_raises():
    with pytest.raises(ValidationError) as exc_info:
        LeadCreate(**{**VALID_DATA, "phone": "347 123 4567"})
    assert any(e["loc"] == ("phone",) for e in exc_info.value.errors())


def test_phone_with_dashes_raises():
    with pytest.raises(ValidationError):
        LeadCreate(**{**VALID_DATA, "phone": "347-123-4567"})


def test_phone_with_plus_prefix_raises():
    with pytest.raises(ValidationError):
        LeadCreate(**{**VALID_DATA, "phone": "+39347123456"})


# --- employee_count ---

def test_positive_employee_count_accepted():
    lead = LeadCreate(**{**VALID_DATA, "employee_count": 1})
    assert lead.employee_count == 1


def test_zero_employee_count_raises():
    with pytest.raises(ValidationError) as exc_info:
        LeadCreate(**{**VALID_DATA, "employee_count": 0})
    assert any(e["loc"] == ("employee_count",) for e in exc_info.value.errors())


def test_negative_employee_count_raises():
    with pytest.raises(ValidationError):
        LeadCreate(**{**VALID_DATA, "employee_count": -5})


# --- LeadRead ---

def test_lead_read_requires_id_and_created_at():
    lead = LeadRead(**VALID_DATA, id=1, created_at=datetime(2024, 1, 15, tzinfo=UTC))
    assert lead.id == 1
    assert lead.updated_at is None


def test_lead_read_inherits_validators():
    with pytest.raises(ValidationError):
        LeadRead(**{**VALID_DATA, "phone": "not-digits"}, id=1, created_at=datetime(2024, 1, 15, tzinfo=UTC))


def test_lead_read_from_attributes_enabled():
    assert LeadRead.model_config.get("from_attributes") is True
