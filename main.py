from fastapi import FastAPI

from webapp.router import webapp_router


app = FastAPI(
    title="Adjuster Data Pull", description="This is a bot to access jcc.state.fl.us"
)
app.include_router(webapp_router)
