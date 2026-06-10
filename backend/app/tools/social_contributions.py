from app.schemas.models import (
    SocialContributionsInput,
    SocialContributionsOutput,
    EmployeeContribution,
)
from app.core.logging import get_logger

logger = get_logger(__name__)

CNPS_EMPLOYEE_RATE = 0.028
CNPS_EMPLOYER_RATE = 0.112
SMIG = 41_875

IRPP_TRANCHES = [
    (0,         2_000_000,  0.10),
    (2_000_001, 3_000_000,  0.15),
    (3_000_001, 5_000_000,  0.25),
    (5_000_001, float("inf"), 0.35),
]


def _compute_irpp(annual_net: float) -> float:
    tax = 0.0
    for low, high, rate in IRPP_TRANCHES:
        if annual_net <= low:
            break
        taxable = min(annual_net, high) - low
        tax += taxable * rate
    return round(tax / 12, 0)


async def calculate_social_contributions(
    params: SocialContributionsInput,
) -> SocialContributionsOutput:
    logger.info(f"calculate_social_contributions — {len(params.employees)} employé(s) mois={params.month}")

    contributions = []
    total_cnps_employee = 0.0
    total_cnps_employer = 0.0
    total_net = 0.0

    for emp in params.employees:
        gross = max(emp.gross_salary, SMIG)

        cnps_emp  = round(gross * CNPS_EMPLOYEE_RATE, 0)
        cnps_empl = round(gross * CNPS_EMPLOYER_RATE, 0)

        base_irpp_annual = (gross - cnps_emp) * 12 * 0.70
        irpp_monthly = _compute_irpp(base_irpp_annual)

        net = round(gross - cnps_emp - irpp_monthly, 0)

        contributions.append(EmployeeContribution(
            name=emp.name,
            gross_salary=gross,
            cnps_employee=cnps_emp,
            cnps_employer=cnps_empl,
            irpp_estimate=irpp_monthly,
            net_salary=net,
        ))

        total_cnps_employee += cnps_emp
        total_cnps_employer += cnps_empl
        total_net += net

    logger.info(f"calculate_social_contributions — masse salariale nette={total_net}")

    return SocialContributionsOutput(
        month=params.month,
        contributions=contributions,
        total_cnps_employee=round(total_cnps_employee, 0),
        total_cnps_employer=round(total_cnps_employer, 0),
        total_net_payroll=round(total_net, 0),
    )
