from fastapi import APIRouter
from fastapi import Request
from fastapi.templating import Jinja2Templates

webapp_router = APIRouter(include_in_schema=False)
templating = Jinja2Templates(directory="webapp/templates")


@webapp_router.get("/")
def index(request: Request):
    return templating.TemplateResponse("index.html", context={"request": request})
