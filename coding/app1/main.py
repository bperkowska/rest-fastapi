"""FastAPI application entry point."""

from fastapi import FastAPI, APIRouter
from database import Base, engine
from routers.v1 import tasks


# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="Task API",
    description="Simple Task CRUD API",
    version="1.0.0"
)

# API v1 router
v1_router = APIRouter(prefix="/v1")
v1_router.include_router(tasks.router)
app.include_router(v1_router)


@app.get("/", tags=["Root"])
def root():
    """Root endpoint."""
    return {
        "message": "Task API",
        "version": "1.0.0",
        "endpoints": {
            "tasks": "/v1/tasks",
            "docs": "/docs"
        }
    }


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}
