import os
from pathlib import Path
from fastapi import FastAPI, Request, UploadFile, File, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
import json
from starlette.middleware.sessions import SessionMiddleware

from dotenv import load_dotenv
load_dotenv()

ADMIN_CODE = os.environ.get("ADMIN_CODE")

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key=os.environ.get("SESSION_SECRET"), max_age=None)

app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/photos", StaticFiles(directory="content/gallery"), name="photos")

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

@app.get("/gallery-upload")
def upload_page(request: Request):
    return src.TemplateResponse(
        request=request,
        name="upload.html",
        context={"logged_in": request.session.get("admin", False)}
    )

@app.post("/gallery-upload/login")
def login(request: Request, code: str = Form(...)):
    if code == ADMIN_CODE:
        request.session["admin"]= True
    return RedirectResponse("/gallery-upload", status_code=303)

@app.post("/gallery-upload")
async def upload(request: Request, photo: UploadFile = File(...), caption: str = Form("")):
    if not request.session.get("admin"):
        return RedirectResponse("/gallery-upload", status_code=303)

    name = Path(photo.filename).name
    (gallery_path / name).write_bytes(await photo.read())

    captions = json.loads(caption_path.read_text(encoding="utf-8"))
    captions[name] = caption
    caption_path.write_text(json.dumps(captions, indent=2), encoding="utf-8")

    return RedirectResponse("/gallery-upload", status_code=303)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)