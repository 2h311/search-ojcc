from fastapi import APIRouter
from fastapi import Request


webapp_router = APIRouter(include_in_schema=False)


@webapp_router.get("/")
def index(request: Request):
    return "index.html"
