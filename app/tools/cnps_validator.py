from app.schemas.models import ValidateCNPSInput, CNPSValidationOutput
from app.core.logging import get_logger

logger = get_logger(__name__)

REGION_PREFIXES: dict[str, str] = {
    "C": "Centre (Yaoundé)",
    "L": "Littoral (Douala)",
    "N": "Nord",
    "E": "Est",
    "S": "Sud",
    "O": "Ouest",
    "A": "Adamaoua",
    "W": "Nord-Ouest",
    "X": "Sud-Ouest",
    "F": "Extrême-Nord",
}


async def validate_cnps_number(params: ValidateCNPSInput) -> CNPSValidationOutput:
    logger.info(f"validate_cnps_number — matricule={params.matricule}")

    matricule = params.matricule.upper()
    prefix = matricule[0]

    if prefix not in REGION_PREFIXES:
        return CNPSValidationOutput(
            matricule=matricule,
            is_valid_format=False,
            status="format_invalide",
            message=f"Préfixe '{prefix}' non reconnu. Préfixes valides : {', '.join(REGION_PREFIXES.keys())}",
        )

    region = REGION_PREFIXES[prefix]
    logger.info(f"validate_cnps_number — format valide, région={region}")

    return CNPSValidationOutput(
        matricule=matricule,
        is_valid_format=True,
        status="format_valide",
        message=(
            f"Format valide. Matricule de la région {region}. "
            "Pour confirmer l'existence du compte, contactez la caisse CNPS locale."
        ),
    )
