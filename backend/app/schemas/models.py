from pydantic import BaseModel, Field, field_validator
from typing import Optional
import re


class SearchCompaniesInput(BaseModel):
    query: str = Field(..., min_length=2, max_length=100)
    region: Optional[str] = None
    limit: int = Field(10, ge=1, le=50)


class Company(BaseModel):
    name: str
    region: str
    sector: str
    registration_id: Optional[str] = None


class SearchCompaniesOutput(BaseModel):
    results: list[Company]
    total: int
    source: str = "Open Data Cameroun"


class TaxCalendarInput(BaseModel):
    year: int = Field(..., ge=2020, le=2030)
    month: Optional[int] = Field(None, ge=1, le=12)


class TaxDeadline(BaseModel):
    date: str
    obligation: str
    description: str
    penalite: str


class TaxCalendarOutput(BaseModel):
    deadlines: list[TaxDeadline]
    period: str


class ValidateCNPSInput(BaseModel):
    matricule: str = Field(..., description="Ex: C1234567A")

    @field_validator("matricule")
    @classmethod
    def validate_format(cls, v: str) -> str:
        pattern = r"^[A-Z]\d{7}[A-Z]$"
        if not re.match(pattern, v.upper()):
            raise ValueError("Format invalide. Attendu : C1234567A")
        return v.upper()


class CNPSValidationOutput(BaseModel):
    matricule: str
    is_valid_format: bool
    status: str
    message: str


class Employee(BaseModel):
    name: str
    gross_salary: float = Field(..., gt=0)


class SocialContributionsInput(BaseModel):
    employees: list[Employee] = Field(..., min_length=1, max_length=100)
    month: str = Field(..., pattern=r"^\d{4}-\d{2}$")


class EmployeeContribution(BaseModel):
    name: str
    gross_salary: float
    cnps_employee: float
    cnps_employer: float
    irpp_estimate: float
    net_salary: float


class SocialContributionsOutput(BaseModel):
    month: str
    contributions: list[EmployeeContribution]
    total_cnps_employee: float
    total_cnps_employer: float
    total_net_payroll: float
    note: str = "Taux CNPS officiels Cameroun. IRPP estimatif."


class PublicDatasetsInput(BaseModel):
    category: Optional[str] = None
    limit: int = Field(5, ge=1, le=20)


class Dataset(BaseModel):
    title: str
    description: str
    organization: str
    url: str
    format: Optional[str] = None


class PublicDatasetsOutput(BaseModel):
    datasets: list[Dataset]
    total: int
    source: str = "data.gouv.cm"


class MCPResponse(BaseModel):
    tool: str
    result: dict
    error: Optional[str] = None
    request_id: str
