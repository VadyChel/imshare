from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .routers import images, html
from imshare.database import engine, Base


Base.metadata.create_all(bind=engine)
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(images.router)
app.include_router(html.router)
files = StaticFiles(directory='imshare/files')
app.mount('/r', files)
app.mount('/raw', files)
app.mount('/static', StaticFiles(directory='imshare/static'), name='static')