from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .ojccrouter.router import api_router
from .webapp.router import webapp_router


app = FastAPI(
    title="Adjuster Data Pull", description="This is a bot to access jcc.state.fl.us"
)
app.include_router(webapp_router)
app.include_router(api_router)
app.mount(
    "/static", StaticFiles(directory=Path("api", "webapp", "static")), name="static"
)
