import logging
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.orm import Session
from contextlib import asynccontextmanager

from database import engine, get_db
import models
from routers import threat_intel as threat_intel_router

# Setup basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for safe database initialization on startup."""
    try:
        if engine:
            models.Base.metadata.create_all(bind=engine)
            logger.info("Database tables created/verified successfully on startup.")
        else:
            logger.warning("Database engine is not configured!")
    except Exception as e:
        logger.error(f"Failed to initialize database tables during startup: {e}")
    
    yield
    
app = FastAPI(title="Threat Intel API", version="1.0", lifespan=lifespan)

# CORS Middleware (Allow requests from Nginx frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(threat_intel_router.router)

# --- GLOBAL ROUTES ---

@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    """Health check endpoint to verify API and DB status."""
    try:
        db.execute(text("SELECT 1"))
        db_status = "connected"
    except Exception as e:
        db_status = f"disconnected ({str(e)})"

    return {
        "status": "online",
        "service": "Threat Intel Backend",
        "database": db_status
    }
