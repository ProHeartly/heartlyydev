import os
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

src = Jinja2Templates(directory="src")

@app.get("/")
def index(request: Request):
    return src.TemplateResponse("index.html", {"request": request})