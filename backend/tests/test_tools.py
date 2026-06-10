import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from app.tools.tax_calendar import get_tax_calendar
from app.tools.cnps_validator import validate_cnps_number
from app.tools.social_contributions import calculate_social_contributions
from app.schemas.models import (
    TaxCalendarInput, ValidateCNPSInput,
    SocialContributionsInput, Employee,
    SearchCompaniesInput, PublicDatasetsInput,
)


# ── Tax Calendar ──────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_tax_calendar_full_year():
    result = await get_tax_calendar(TaxCalendarInput(year=2025))
    assert len(result.deadlines) > 0
    assert result.period == "2025"
    for d in result.deadlines:
        assert d.date.startswith("2025-")


@pytest.mark.asyncio
async def test_tax_calendar_single_month():
    result = await get_tax_calendar(TaxCalendarInput(year=2025, month=3))
    assert result.period == "2025-03"
    assert len(result.deadlines) > 0
    for d in result.deadlines:
        assert "2025-03" in d.date


@pytest.mark.asyncio
async def test_tax_calendar_has_required_fields():
    result = await get_tax_calendar(TaxCalendarInput(year=2025, month=1))
    for d in result.deadlines:
        assert d.obligation
        assert d.description
        assert d.penalite


# ── CNPS Validator ────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_cnps_valid_centre():
    result = await validate_cnps_number(ValidateCNPSInput(matricule="C1234567A"))
    assert result.is_valid_format is True
    assert result.status == "format_valide"
    assert "Centre" in result.message


@pytest.mark.asyncio
async def test_cnps_valid_littoral():
    result = await validate_cnps_number(ValidateCNPSInput(matricule="L9876543B"))
    assert result.is_valid_format is True
    assert "Littoral" in result.message


@pytest.mark.asyncio
async def test_cnps_invalid_prefix():
    result = await validate_cnps_number(ValidateCNPSInput(matricule="Z1234567A"))
    assert result.is_valid_format is False
    assert result.status == "format_invalide"


def test_cnps_invalid_format_raises():
    with pytest.raises(ValueError):
        ValidateCNPSInput(matricule="123")


def test_cnps_invalid_format_too_short():
    with pytest.raises(ValueError):
        ValidateCNPSInput(matricule="C123A")


# ── Social Contributions ──────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_social_contributions_single_employee():
    params = SocialContributionsInput(
        employees=[Employee(name="Jean Dupont", gross_salary=300_000)],
        month="2025-03",
    )
    result = await calculate_social_contributions(params)
    assert len(result.contributions) == 1
    emp = result.contributions[0]
    assert emp.cnps_employee == round(300_000 * 0.028, 0)
    assert emp.cnps_employer == round(300_000 * 0.112, 0)
    assert emp.net_salary < emp.gross_salary


@pytest.mark.asyncio
async def test_social_contributions_smig_floor():
    params = SocialContributionsInput(
        employees=[Employee(name="Test", gross_salary=10_000)],
        month="2025-01",
    )
    result = await calculate_social_contributions(params)
    assert result.contributions[0].gross_salary == 41_875


@pytest.mark.asyncio
async def test_social_contributions_multiple_employees():
    params = SocialContributionsInput(
        employees=[
            Employee(name="Alice", gross_salary=500_000),
            Employee(name="Bob", gross_salary=250_000),
        ],
        month="2025-03",
    )
    result = await calculate_social_contributions(params)
    assert len(result.contributions) == 2
    assert result.total_net_payroll < sum(
        e.gross_salary for e in result.contributions
    )


@pytest.mark.asyncio
async def test_social_contributions_totals():
    params = SocialContributionsInput(
        employees=[Employee(name="Alice", gross_salary=300_000)],
        month="2025-03",
    )
    result = await calculate_social_contributions(params)
    assert result.total_cnps_employee == result.contributions[0].cnps_employee
    assert result.total_cnps_employer == result.contributions[0].cnps_employer


# ── Search Companies (mock HTTP) ──────────────────────────────────────────────

@pytest.mark.asyncio
async def test_search_companies_mock():
    mock_response = {
        "result": {
            "count": 1,
            "results": [{
                "title": "ACME Cameroun SA",
                "tags": [],
                "groups": [{"display_name": "Commerce"}],
                "name": "acme-cameroun",
            }],
        }
    }
    from app.tools.search_companies import search_companies

    # Mock correct : resp.json() est synchrone dans httpx
    mock_resp = MagicMock()
    mock_resp.json.return_value = mock_response
    mock_resp.raise_for_status.return_value = None

    mock_client = AsyncMock()
    mock_client.get.return_value = mock_resp
    mock_client.__aenter__.return_value = mock_client
    mock_client.__aexit__.return_value = None

    with patch("httpx.AsyncClient", return_value=mock_client):
        result = await search_companies(SearchCompaniesInput(query="ACME"))
        assert result.total == 1
        assert result.results[0].name == "ACME Cameroun SA"


# ── Public Datasets (mock HTTP) ───────────────────────────────────────────────

@pytest.mark.asyncio
async def test_get_public_datasets_mock():
    mock_response = {
        "result": {
            "count": 2,
            "results": [
                {
                    "title": "Budget de l'État 2024",
                    "notes": "Données budgétaires",
                    "organization": {"title": "Ministère des Finances"},
                    "name": "budget-2024",
                    "resources": [{"format": "CSV"}],
                },
                {
                    "title": "Statistiques éducation",
                    "notes": "Données scolaires",
                    "organization": {"title": "Ministère de l'Éducation"},
                    "name": "stats-education",
                    "resources": [{"format": "XLSX"}],
                },
            ],
        }
    }
    from app.tools.open_datasets import get_public_datasets

    mock_resp = MagicMock()
    mock_resp.json.return_value = mock_response
    mock_resp.raise_for_status.return_value = None

    mock_client = AsyncMock()
    mock_client.get.return_value = mock_resp
    mock_client.__aenter__.return_value = mock_client
    mock_client.__aexit__.return_value = None

    with patch("httpx.AsyncClient", return_value=mock_client):
        result = await get_public_datasets(PublicDatasetsInput(limit=5))
        assert result.total == 2
        assert result.datasets[0].title == "Budget de l'État 2024"
        assert result.datasets[0].format == "CSV"
