from pydantic import BaseModel


class OjccCaseData(BaseModel):
    pdfLink: str
    ojccCaseNo: str
    telephone: str
    email: str
    medicalBenefitsCase: str
    lostTimeCase: str


class DataToBeReturned(BaseModel):
    userInputtedCaseNumber: str
    cases: list[OjccCaseData | None]
