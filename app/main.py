from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
import os
from mangum import Mangum
from . import models
from .database import engine, get_db
from .routes import auth, links, billing

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="LinkForge API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(links.router)
app.include_router(billing.router)

# Static files (used locally; on Netlify, static is served directly)
static_dir = os.path.join(os.path.dirname(__file__), "..", "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir, html=True), name="static")

@app.get("/")
def serve_frontend():
    return FileResponse(os.path.join(static_dir, "index.html"))

@app.get("/{slug}")
def redirect_to_url(slug: str, db: Session = Depends(get_db)):
    if slug in ["favicon.ico", "robots.txt"]:
        return {"error": "Not found"}
    link = db.query(models.Link).filter(models.Link.slug == slug).first()
    if link:
        link.clicks += 1
        db.commit()
        return RedirectResponse(url=link.original_url)
    return {"error": "Link not found"}

# Netlify functions entry point
handler = Mangum(app, lifespan="off")
