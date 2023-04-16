from fastapi import APIRouter

from .models import CasePayload
from .models import DataToBeReturned

# from .ojcc import get_data_for_multiple_case_numbers

api_router = APIRouter(prefix="/api", tags=["Receive Payload"])
case_list = list()


@api_router.post("/")
async def get_payload(payload: CasePayload):
    print(payload.caseNumbers)
    return {"data received"}


@api_router.get("/", response_model=list[DataToBeReturned | None])
async def get_case_data_to_ui():
    return case_list.pop() if case_list else case_list
