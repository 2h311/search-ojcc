from fastapi import APIRouter

from .models import CasePayload
from .models import DataToBeReturned
from .ojcc import get_data_for_multiple_case_numbers

api_router = APIRouter(prefix="/api", tags=["Receive Payload"])


@api_router.post("/", response_model=list[DataToBeReturned])
async def get_payload(payload: CasePayload):
    case_list = list()
    for response in get_data_for_multiple_case_numbers(payload.caseNumbers):
        case_list.append(response)
    return case_list
