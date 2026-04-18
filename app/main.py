from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
import models
from database import engine, get_db
from routes import auth, links, billing

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="LinkForge API", version="1.0.0")

# CORS: allow all origins for simplicity (you can restrict later)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files (frontend)
app.mount("/static", StaticFiles(directory="static", html=True), name="static")

# Include API routers
app.include_router(auth.router)
app.include_router(links.router)
app.include_router(billing.router)

@app.get("/")
def serve_frontend():
    from fastapi.responses import FileResponse
    return FileResponse("static/index.html")

@app.get("/{slug}")
def redirect_to_url(slug: str, db: Session = Depends(get_db)):
    link = db.query(models.Link).filter(models.Link.slug == slug).first()
    if link:
        link.clicks += 1
        db.commit()
        return RedirectResponse(url=link.original_url)
    return {"error": "Link not found"}
