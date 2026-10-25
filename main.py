import os
import time
import secrets
import markdown
from datetime import date
from pathlib import Path
from fastapi import FastAPI, Request, UploadFile, File, Form, HTTPException
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
app.mount("/images", StaticFiles(directory="images"), name="images")

src = Jinja2Templates(directory="src")

gallery_path = Path("content/gallery")
caption_path = Path("content/caption.json")

blogs_dir = Path("content/blogs")

def read_post(file):
    text = file.read_text(encoding="utf-8")
    info = {}

    # optional info block at the top:
    # ---
    # title: ...
    # date: 2026-10-24
    # summary: ...
    # ---
    if text.startswith("---"):
        _, top, text = text.split("---", 2)
        for line in top.strip().splitlines():
            key, value = line.split(":", 1)
            info[key.strip()] = value.strip()

    first_line = ""
    for line in text.splitlines():
        if line.strip() and not line.startswith(("#", "```", ">", "|", "-")):
            first_line = line.strip()
            break

    return {
        "slug": file.stem,
        "title": info.get("title", file.stem),
        "date": info.get("date", ""),
        "summary": info.get("summary", first_line),
        "has_summary": "summary" in info,
        "html": markdown.markdown(text, extensions=["fenced_code", "tables"])
    }

def get_posts(folder):
    posts = [read_post(f) for f in folder.glob("*.md")]
    posts.sort(key=lambda p: (p["date"], p["slug"]), reverse=True)
    return posts

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

@app.get("/blogs")
def blogs(request: Request):
    boards = []
    for folder in sorted(blogs_dir.iterdir()):
        posts = get_posts(folder)
        boards.append({
            "name": folder.name,
            "count": len(posts),
            "latest": posts[0] if posts else None
        })
    return src.TemplateResponse(
        request=request,
        name="blogs.html",
        context={"boards": boards, "today": date.today().strftime("%B %d, %Y")},
    )

@app.get("/blogs/{board}")
def blog_board(request: Request, board: str):
    folder = blogs_dir / board
    if ".." in board or not folder.is_dir():
        raise HTTPException(status_code=404)

    return src.TemplateResponse(
        request=request,
        name="blog_board.html",
        context={
            "board": board,
            "posts": get_posts(folder),
            "today": date.today().strftime("%B %d, %Y")
        }
    )

@app.get("/blogs/{board}/{post}")
def blog_post(request: Request, board: str, post: str):
    file = blogs_dir / board / f"{post}.md"
    if ".." in board or ".." in post or not file.is_file():
        raise HTTPException(status_code=404)

    return src.TemplateResponse(
        request=request,
        name="blog_post.html",
        context={
            "board": board,
            "post": read_post(file),
            "today": date.today().strftime("%B %d, %Y")
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)