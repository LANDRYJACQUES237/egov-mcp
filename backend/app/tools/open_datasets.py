import httpx
from app.schemas.models import PublicDatasetsInput, PublicDatasetsOutput, Dataset
from app.config import get_settings
from app.core.logging import get_logger

logger = get_logger(__name__)

CATEGORY_MAP: dict[str, str] = {
    "finance": "finances-publiques",
    "education": "education",
    "santé": "sante",
    "agriculture": "agriculture",
    "emploi": "emploi",
    "économie": "economie",
}


async def get_public_datasets(params: PublicDatasetsInput) -> PublicDatasetsOutput:
    settings = get_settings()
    url = f"{settings.open_data_base_url}/action/package_search"

    query_params: dict = {"rows": params.limit, "sort": "metadata_modified desc"}

    if params.category:
        ckan_group = CATEGORY_MAP.get(params.category.lower(), params.category)
        query_params["fq"] = f"groups:{ckan_group}"
        logger.info(f"get_public_datasets — catégorie={params.category}")
    else:
        logger.info("get_public_datasets — tous les datasets")

    async with httpx.AsyncClient(timeout=10.0) as client:
        resp = await client.get(url, params=query_params)
        resp.raise_for_status()
        data = resp.json()

    results_raw = data.get("result", {}).get("results", [])
    total = data.get("result", {}).get("count", 0)

    datasets = []
    for item in results_raw:
        resources = item.get("resources", [])
        fmt = resources[0].get("format", "N/A") if resources else "N/A"
        org = item.get("organization") or {}
        datasets.append(Dataset(
            title=item.get("title", "Sans titre"),
            description=(item.get("notes") or "Pas de description")[:200],
            organization=org.get("title", "N/A"),
            url=f"https://www.data.gouv.cm/dataset/{item.get('name', '')}",
            format=fmt,
        ))

    logger.info(f"get_public_datasets — {len(datasets)}/{total} datasets retournés")
    return PublicDatasetsOutput(datasets=datasets, total=total)
