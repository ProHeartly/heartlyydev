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

@app.get("/about")
def about(request: Request):
    return src.TemplateResponse("about.html", {"request": request})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)