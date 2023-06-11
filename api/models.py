from typing import Optional

from pydantic import BaseModel


class OjccCaseData(BaseModel):
    pdfLink: str
    caseNumber: str
    telephone: str
    email: str
    medicalBenefitsCase: str
    lostTimeCase: str


class DataToBeReturned(BaseModel):
    userInputtedCaseNumber: str
    cases: list[Optional[OjccCaseData]]


class CasePayload(BaseModel):
    caseStatus: str
    caseNumbers: list[str]
