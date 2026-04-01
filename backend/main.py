from fastapi import FastAPI

from backend.core.config import settings
from backend.core.database import Base, engine
from backend.models.user import User
from backend.routers import auth, cities, health


Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.app_name)

app.include_router(health.router)
app.include_router(auth.router)
app.include_router(cities.router)


@app.get("/")
def root() -> dict[str, str]:
    return {"message": f"{settings.app_name} API"}