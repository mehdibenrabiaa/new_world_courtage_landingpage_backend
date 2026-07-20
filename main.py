from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.config import settings
from core.database import Base, engine
from models import lead  # noqa: F401 — registers models on Base before create_all
from routers.leads import router as leads_router
from routers.admin import router as admin_router

is_dev = settings.ENVIRONMENT == "development"

app = FastAPI(
    title="New World Courtage — Landing Page API",
    version="0.1.0",
    docs_url="/docs" if is_dev else None,
    redoc_url="/redoc" if is_dev else None,
    openapi_url="/openapi.json" if is_dev else None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(leads_router)
app.include_router(admin_router)


@app.get("/health")
def health():
    return {"status": "ok"}
