from pathlib import Path
from fastapi import APIRouter
from fastapi import Request
from fastapi.templating import Jinja2Templates

webapp_router = APIRouter(include_in_schema=False)
templates = Jinja2Templates(
    directory=str(Path(__file__).resolve().parent / "templates")
)

# print(Path(__file__).resolve().parent / "templates")


@webapp_router.get("/")
def index(request: Request):
    return templates.TemplateResponse(request=request, name="index.html", context={})
