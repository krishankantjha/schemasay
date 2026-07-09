import logging
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import settings
from app.api.routes import auth, connections, schema, assistant, query, insights
from app.database import Base, engine
from app.models.user import User
from app.models.connection import DatabaseConnection, QueryAuditLog, DatabaseSchemaCache

# Initialize structured logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("schemasay")

app = FastAPI(
    title="SchemaSay API",
    description="The backend engine for SchemaSay AI",
    version="1.0.0"
)

# Parse allowed origins from settings securely
origins = [origin.strip() for origin in settings.ALLOWED_ORIGINS.split(",") if origin.strip()]

# Configure CORS using strict origin list (wildcard origins with credentials allowed is restricted)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Startup configurations check
@app.on_event("startup")
def startup_checks():
    logger.info("Initializing SchemaSay API Engine startup checks...")
    
    # Create tables resiliently in target database on startup (for fresh Postgres/SQLite setups)
    # Skip during testing sessions to prevent database connection conflicts
    import sys
    if "pytest" not in sys.modules:
        logger.info("Verifying database schema tables...")
        Base.metadata.create_all(bind=engine)
    
    if not settings.OPENAI_API_KEY:
        logger.warning("OPENAI_API_KEY is not defined. Features utilizing OpenAI capabilities will be restricted.")
    if not settings.GEMINI_API_KEY:
        logger.warning("GEMINI_API_KEY is not defined. Features utilizing Gemini capabilities will be restricted.")
    logger.info("Startup checks completed.")

# Global Exception Handler to capture unhandled exceptions and prevent raw traceback leakage
@app.exception_handler(Exception)
def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled system exception on {request.method} {request.url.path}: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "An internal server error occurred."}
    )

app.include_router(auth.router, prefix="/api/v1")
app.include_router(connections.router, prefix="/api/v1")
app.include_router(schema.router, prefix="/api/v1")
app.include_router(assistant.router, prefix="/api/v1")
app.include_router(query.router, prefix="/api/v1")
app.include_router(insights.router, prefix="/api/v1")

@app.get("/")
def read_root():
    """
    Basic API root health verification.
    """
    return {"message": "Welcome to the SchemaSay API"}

@app.get("/health")
def health_check():
    """
    Basic service health check endpoint.
    """
    return {"status": "healthy"}
