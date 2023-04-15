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


@api_router.get("/", response_model=list[CasePayload | None])
async def get_case_data_to_ui():
    return case_list.pop() if case_list else case_list
