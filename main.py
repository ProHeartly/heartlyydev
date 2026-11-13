import os
import time
import secrets
from datetime import date
from pathlib import Path
from fastapi import FastAPI, Request, UploadFile, File, Form, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse, FileResponse, JSONResponse
import json
import urllib.request
import urllib.parse
from starlette.middleware.sessions import SessionMiddleware
import re
import threading
import hashlib


from markdown_it import MarkdownIt
md = MarkdownIt("commonmark").enable(["table", "strikethrough"])


import smtplib
from email.message import EmailMessage

from dotenv import load_dotenv
load_dotenv()

ADMIN_MAIL = os.environ.get("ADMIN_MAIL")
MAIL_PASS = os.environ.get("MAIL_PASS")

current_code = None
code_time = 0

# this sends the code to given mail
def send_code(to, code):
    msg = EmailMessage()
    msg["Subject"] = f"Code for heartlyy.dev"
    msg["From"] = "heartly@user.hackclub.app"
    msg["To"] = to
    msg.set_content(f"Your code is {code}, please don't share with others :D")

    with smtplib.SMTP("mx.user.hackclub.app", 587, timeout=20) as s:
        s.starttls()
        s.login("heartly@user.hackclub.app", MAIL_PASS)
        s.send_message(msg)

sent = {}

def send_mail(subject, body, reply_to=""):
    mail = EmailMessage()
    mail["Subject"] = subject
    mail["From"] = "heartly@user.hackclub.app"
    mail["To"] = ADMIN_MAIL
    if "@" in reply_to:
        mail["Reply-To"] = reply_to

    mail.set_content(body)

    with smtplib.SMTP("mx.user.hackclub.app", 587, timeout=20) as s:
            s.starttls()
            s.login("heartly@user.hackclub.app", MAIL_PASS)
            s.send_message(mail)

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key=os.environ.get("SESSION_SECRET"), max_age=None)

app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/photos", StaticFiles(directory="content/gallery"), name="photos")
app.mount("/images", StaticFiles(directory="images"), name="images")

src = Jinja2Templates(directory="src")

gallery_path = Path("content/gallery")
caption_path = Path("content/caption.json")
projects_path = Path("content/projects.json")
notes_path = Path("content/notes.json")

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
        "html": md.render(text)
    }

# "devlog-11" -> ["devlog-", "11", ""], so like 11 is conpared as number not text
def natural_sorting(text):
    return [int(part) if part.isdigit() else part for part in re.split(r"(\d+)", text)]

def get_posts(folder):
    posts = [read_post(f) for f in folder.glob("*.md")]
    posts.sort(key=lambda p: (p["date"], natural_sorting(p["slug"])), reverse=True)
    return posts


previews = {} # songs we alr looked up, so we only ask once per song

def get_json(url):
    with urllib.request.urlopen(url, timeout=8) as res:
        return json.loads(res.read())


GITHUB = "ProHeartly"

def fill(project, repo):
    if not project.get("name"):
        project["name"] = repo["name"].replace("-", " ")
    if not project.get("description"):
        project["description"] = repo["description"] or ""
    if not project.get("picture"):
        project["picture"] = readme_pic(repo["name"], repo["default_branch"])
    if not project.get("demo"):
        project["demo"] = repo["homepage"] or ""
    if not project.get("github"):
        project["github"] = repo["html_url"]
    return project

# grabs the first pic from a repo's README (if it has)
def readme_pic(repo, branch):
    readme = ""
    for file in ["README.md", "readme.md", "Readme.md"]:
        try:
            readme = urllib.request.urlopen(f"https://raw.githubusercontent.com/{GITHUB}/{repo}/{branch}/{file}", timeout=8).read().decode()
            break
        except Exception:
            pass

    found = re.search(r'!\[.*?\]\((\S+?)\)|<img[^>]+src="(.+?)"', readme) # works for ![alt](pic.png) and <img src="pic.png">
    if not found:
        return "" # no pic

    pic = found.group(1) or found.group(2)

    # pic is inside the repo, so make it a full link
    if not pic.startswith("http"):
        pic = f"https://raw.githubusercontent.com/{GITHUB}/{repo}/{branch}/{pic.removeprefix('./')}"

    return pic

# finds my repos with the `heartlyy` tag and puts them in projects.json
# stuff i wrote myself in json stays, only empty things get filledd
def sync_projects():
    repos = get_json(f"https://api.github.com/users/{GITHUB}/repos?per_page=100")
    projects = json.loads(projects_path.read_text(encoding="utf-8"))

    saved = [p.get("github", "").rstrip("/").split("/")[-1] for p in projects]

    for repo in repos:
        if "heartlyy" not in repo["topics"]:
            continue

        if repo["name"] in saved:
            fill(projects[saved.index(repo["name"])], repo)
        else:
            projects.append(fill({}, repo))

    temp = projects_path.with_suffix(".tmp")
    temp.write_text(json.dumps(projects, indent=2, ensure_ascii=False), encoding="utf-8")
    temp.replace(projects_path)

notes_codes = {} # mail -> code, time, tries
code_asks = {} # ip -> times they asked for a code

# hasing
def scramble(email):
    return hashlib.sha256(email.encode()).hexdigest()

def already_posted(email):
    notes = json.loads(notes_path.read_text(encoding="utf-8"))
    return any(n["email"] == scramble(email) for n in notes)

def oops(error):
    return {"ok": False, "error": error}

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
    send_code(ADMIN_MAIL, current_code)
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

@app.get("/dino")
def dino(request: Request):
    return src.TemplateResponse(request=request, name="dino.html")

@app.get("/sw.js")
def service_worker():
    return FileResponse("static/sw.js", media_type="application/javascript")

@app.get("/api/preview")
def preview(song: str, artist: str = ""):
    key = f"{song} {artist}".lower()
    if key in previews and time.time() - previews[key]["time"] < 600:
        return previews[key]

    result = {"preview": None, "links": {}, "time": time.time()}

    found = get_json("https://api.deezer.com/search?limit=1&q=" + urllib.parse.quote(key))["data"]
    if found:
        result["preview"] = found[0]["preview"]

        q = urllib.parse.quote(f"{song} {artist}")
        result["links"] = {
            "spotify": f"https://open.spotify.com/search/{q}",
            "youtube": f"https://www.youtube.com/results?search_query={q}",
            "appleMusic": f"https://music.apple.com/search?term={q}",
        }

    previews[key] = result
    return result

@app.get("/projects")
def projects(request: Request):
    return src.TemplateResponse(
        request=request,
        name="projects.html",
        context= {"projects": json.loads(projects_path.read_text(encoding="utf-8"))}
    )

@app.get("/contact")
def contact(request: Request):
    return src.TemplateResponse(request=request, name="contact.html")

@app.post("/contact")
def contact_send(request: Request, msg: str = Form(""), reply: str = Form(""), website: str = Form(""), seconds: float = Form(0)):
    if website or seconds < 3:
        return {"ok": True} # pretend that it worked :D

    if not msg.strip():
        return JSONResponse({"ok": False}, status_code=400)

    # max 3 msg an hour per one person
    ip = request.headers.get("x-forwarded-for", request.client.host).split(",")[0]
    now = time.time()
    sent[ip] = [t for t in sent.get(ip, []) if now - t < 3600]
    if len(sent[ip]) >= 3:
        return JSONResponse({"ok": False}, status_code=429)
    sent[ip].append(now)

    send_mail("new msg from heartlyy.dev", f"{msg[:2000]}\n\nreply to: {reply or 'not given'}", reply)
    return {"ok": True}

@app.get("/notes")
def notes(request: Request):
    notes = json.loads(notes_path.read_text(encoding="utf-8"))
    shown = [{"text": n["text"], "name": n["name"], "x": n["x"], "y": n["y"]} for n in notes if n["show"]]
    return src.TemplateResponse(request=request, name="notes.html", context={"notes": shown})

@app.post("/notes/send-code")
def notes_send_code(request: Request, email: str = Form("")):
    email = email.strip().lower()
    if already_posted(email):
        return oops("this email already added a note :)")

    # max 5 codes an hour
    ip = request.headers.get("x-forwarded-for", request.client.host).split(",")[0]
    now = time.time()
    code_asks[ip] = [t for t in code_asks.get(ip, []) if now - t < 3600]
    if len(code_asks[ip]) >= 5:
        return oops("too many codes, try later")

    code_asks[ip].append(now)

    code = f"{secrets.randbelow(1000000):06d}"
    notes_codes[email] = {"code": code, "time": now, "tries": 0}
    send_code(email, code)
    return {"ok": True}

@app.post("/notes/add")
def notes_add(email: str = Form(""), code: str = Form(""), text: str = Form(""), name: str = Form(""), x: int = Form(0), y: int = Form(0)):
    email = email.strip().lower()
    saved = notes_codes.get(email)

    if not saved or time.time() - saved["time"] > 600:
        return oops("code expired, get a new one")

    if code.strip() != saved["code"]:
        saved["tries"] += 1
        if saved["tries"] >= 5:
            del notes_codes[email] # too many guesses
        return oops("wrong code")

    if already_posted(email):
        return oops("this email already added a note :)")

    key = secrets.token_urlsafe(16) # random secret, only goes in my mail
    name = name.strip()[:30] or "anonymous"
    notes = json.loads(notes_path.read_text(encoding="utf-8"))
    notes.append({
        "text": text.strip()[:200],
        "name": name,
        "x": x,
        "y": y,
        "email": scramble(email),
        "date": str(date.today()),
        "show": False, # I make it true after review
        "key": key
    })

    temp = notes_path.with_suffix(".tmp")
    temp.write_text(json.dumps(notes, indent=2, ensure_ascii=False), encoding="utf-8")
    temp.replace(notes_path)

    del notes_codes[email]
    send_mail("new note on heartlyy.dev", f"{text}\n\n- {name}\n\n accept: https://heartlyy.dev/notes/accept/{key}")

    return {"ok": True}

@app.get("/notes/accept/{key}")
def notes_accept(key: str):
    notes = json.loads(notes_path.read_text(encoding="utf-8"))
    for n in notes:
        if n.get("key") == key:
            n["show"] = True

    temp = notes_path.with_suffix(".tmp")
    temp.write_text(json.dumps(notes, indent=2, ensure_ascii=False), encoding="utf-8")
    temp.replace(notes_path)
    return RedirectResponse("/notes", status_code=303)

@app.exception_handler(404)
def not_found(request: Request, exc):
    return src.TemplateResponse(request=request, name="404.html", status_code=404)

def sync_loop():
    while True:
        try:
            sync_projects()
        except Exception:
            pass
        time.sleep(3600)

threading.Thread(target=sync_loop, daemon=True).start()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)