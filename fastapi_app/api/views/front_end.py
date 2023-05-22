from fastapi.templating import Jinja2Templates
from fastapi import APIRouter, Request

frontend_router = APIRouter(tags=["frontend"])
templates = Jinja2Templates(directory="./web_app")


@frontend_router.get("/login")
async def render_html(request: Request):
    return templates.TemplateResponse("1.html", {"request": request})

@frontend_router.get("/")
async def render_html(request: Request):
    return templates.TemplateResponse("3.html", {"request": request})
