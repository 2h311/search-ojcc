from fastapi import APIRouter
from pydantic import BaseModel

api_router = APIRouter(prefix="/api", tags=["Receive Payload"])
case_list = list()


class CasePayload(BaseModel):
    caseStatus: str
    caseNumbers: list[str]


@api_router.post("/")
async def get_payload(payload: CasePayload):
    print(payload.caseNumbers)

    return {"data received"}


@api_router.get("/")
async def get_case_data_to_ui():
    print(len(case_list))
