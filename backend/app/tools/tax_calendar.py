from app.schemas.models import TaxCalendarInput, TaxCalendarOutput, TaxDeadline
from app.core.logging import get_logger

logger = get_logger(__name__)

TAX_DEADLINES: dict[int, list[dict]] = {
    1:  [
        {"date": "{year}-01-15", "obligation": "Acompte IS / IRCM", "description": "Versement acompte impôt sur les sociétés 4ème trimestre N-1", "penalite": "10% + 1.5%/mois"},
        {"date": "{year}-01-31", "obligation": "DSF", "description": "Dépôt de la Déclaration Statistique et Fiscale (exercice N-1)", "penalite": "25% des droits"},
    ],
    2:  [
        {"date": "{year}-02-15", "obligation": "Acompte IS / IRCM", "description": "Acompte 1er trimestre", "penalite": "10% + 1.5%/mois"},
        {"date": "{year}-02-28", "obligation": "TVA Janvier", "description": "Déclaration et paiement TVA du mois de janvier", "penalite": "25% + intérêts"},
    ],
    3:  [
        {"date": "{year}-03-15", "obligation": "Acompte IS", "description": "Acompte mensuel IS", "penalite": "10% + 1.5%/mois"},
        {"date": "{year}-03-31", "obligation": "TVA Février", "description": "Déclaration et paiement TVA du mois de février", "penalite": "25% + intérêts"},
    ],
    4:  [
        {"date": "{year}-04-15", "obligation": "Acompte IS", "description": "Acompte mensuel IS", "penalite": "10% + 1.5%/mois"},
        {"date": "{year}-04-30", "obligation": "TVA Mars + Liasse fiscale", "description": "TVA mars + dépôt liasse fiscale", "penalite": "25% + intérêts"},
    ],
    5:  [{"date": "{year}-05-15", "obligation": "Acompte IS", "description": "Acompte mensuel IS 2ème trimestre", "penalite": "10%"}],
    6:  [{"date": "{year}-06-30", "obligation": "TVA Mai + Patente", "description": "TVA mai + paiement patente", "penalite": "25%"}],
    7:  [{"date": "{year}-07-15", "obligation": "Acompte IS", "description": "Acompte mensuel IS 3ème trimestre", "penalite": "10%"}],
    8:  [{"date": "{year}-08-31", "obligation": "TVA Juillet", "description": "Déclaration TVA juillet", "penalite": "25%"}],
    9:  [{"date": "{year}-09-15", "obligation": "Acompte IS", "description": "Acompte mensuel IS", "penalite": "10%"}],
    10: [{"date": "{year}-10-31", "obligation": "TVA Septembre", "description": "Déclaration TVA septembre", "penalite": "25%"}],
    11: [{"date": "{year}-11-15", "obligation": "Acompte IS 4ème trim.", "description": "Dernier acompte IS de l'année", "penalite": "10%"}],
    12: [{"date": "{year}-12-31", "obligation": "TVA Novembre + Clôture", "description": "TVA novembre + préparation clôture exercice", "penalite": "25%"}],
}


async def get_tax_calendar(params: TaxCalendarInput) -> TaxCalendarOutput:
    logger.info(f"get_tax_calendar — year={params.year} month={params.month}")

    if params.month:
        months = [params.month]
        period = f"{params.year}-{params.month:02d}"
    else:
        months = list(range(1, 13))
        period = str(params.year)

    deadlines = []
    for m in months:
        for d in TAX_DEADLINES.get(m, []):
            deadlines.append(TaxDeadline(
                date=d["date"].replace("{year}", str(params.year)),
                obligation=d["obligation"],
                description=d["description"],
                penalite=d["penalite"],
            ))

    logger.info(f"get_tax_calendar — {len(deadlines)} échéances retournées")
    return TaxCalendarOutput(deadlines=deadlines, period=period)
