from fastapi_limiter.depends import RateLimiter
from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from sqlalchemy.orm import Session
from imshare import schemas, crud


router = APIRouter()
templates = Jinja2Templates(directory="imshare/templates")


@router.get("/", response_class=HTMLResponse)
async def main_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})