import httpx
from app.schemas.models import SearchCompaniesInput, SearchCompaniesOutput, Company
from app.config import get_settings
from app.core.logging import get_logger

logger = get_logger(__name__)


async def search_companies(params: SearchCompaniesInput) -> SearchCompaniesOutput:
    settings = get_settings()
    url = f"{settings.open_data_base_url}/action/package_search"

    query = params.query
    if params.region:
        query += f" {params.region}"

    request_params = {
        "q": query,
        "rows": params.limit,
    }

    logger.info(f"search_companies — query={params.query} region={params.region}")

    async with httpx.AsyncClient(timeout=10.0) as client:
        resp = await client.get(url, params=request_params)
        resp.raise_for_status()
        data = resp.json()

    results_raw = data.get("result", {}).get("results", [])
    total = data.get("result", {}).get("count", 0)

    companies = []
    for item in results_raw:
        groups = item.get("groups", [])
        sector = groups[0].get("display_name", "Non spécifié") if groups else "Non spécifié"
        companies.append(Company(
            name=item.get("title", "N/A"),
            region=params.region or "Non spécifié",
            sector=sector,
            registration_id=item.get("name"),
        ))

    logger.info(f"search_companies — {len(companies)} résultats")
    return SearchCompaniesOutput(results=companies, total=total)
