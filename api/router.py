from fastapi import APIRouter


api_router = APIRouter(prefix="/api", tags=["Receive Payload"])


@api_router.post("/")
async def get_payload():
    print("Hello world")
