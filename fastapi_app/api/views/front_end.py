from fastapi.templating import Jinja2Templates
from fastapi import APIRouter, Request

frontend_router = APIRouter(tags=["frontend"], prefix="/frontend")
templates = Jinja2Templates(directory="templates/web_app")


@frontend_router.get("/1.html")
async def render_html(request: Request):
    return templates.TemplateResponse("1.html", {"request": request})
