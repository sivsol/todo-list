from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import Base, engine
from app import routers

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Todo List API",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routers.router, prefix="/api")


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok"}