import os
import time
import secrets
from pathlib import Path
from fastapi import FastAPI, Request, UploadFile, File, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
import json
from starlette.middleware.sessions import SessionMiddleware

import smtplib
from email.message import EmailMessage

from dotenv import load_dotenv
load_dotenv()

ADMIN_MAIL = os.environ.get("ADMIN_MAIL")
MAIL_PASS = os.environ.get("MAIL_PASS")

current_code = None
code_time = 0

# this sends the code to our mail
def send_code(code):
    msg = EmailMessage()
    msg["Subject"] = f"Your code: {code}"
    msg["From"] = "heartly@user.hackclub.app"
    msg["To"] = ADMIN_MAIL
    msg.set_content(f"Your login code is {code}")

    with smtplib.SMTP("mx.user.hackclub.app", 587, timeout=20) as s:
        s.starttls()
        s.login("heartly@user.hackclub.app", MAIL_PASS)
        s.send_message(msg)

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

@app.post("/gallery-upload/send-code")
def send_code_route():
    global current_code, code_time
    current_code = f"{secrets.randbelow(1000000):06d}"
    code_time = time.time()
    send_code(current_code)
    return RedirectResponse("/gallery-upload", status_code=303)

@app.post("/gallery-upload/login")
def login(request: Request, code: str = Form(...)):
    global current_code
    if current_code and code == current_code and time.time() - code_time < 600:
        request.session["admin"] = True
        current_code = None
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