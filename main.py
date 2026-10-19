import os
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import json

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/gallery", StaticFiles(directory="content/gallery"), name="gallery")

src = Jinja2Templates(directory="src")

gallery_path = Path("content/gallery")
caption_path = Path("content/caption.json")

@app.get("/")
def index(request: Request):
    return src.TemplateResponse(request=request, name="index.html")

@app.get("/about")
def about(request: Request):
    return src.TemplateResponse(request=request, name="about.html")

@app.get("/gallery")
def gallery(request: Request):
    images = []
    captions = {}
    captions = json.loads(caption_path.read_text(encoding="utf-8"))
    for f in sorted(gallery_path.iterdir()):
        images.append({
            "file": f.name,
            "caption": captions.get(f.name, f.stem),
        })

    return src.TemplateResponse(
        request=request,
        name="gallery.html",
        context={"request": request, "images": images},
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)