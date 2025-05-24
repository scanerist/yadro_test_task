import os
from fastapi import FastAPI, Request, Depends, BackgroundTasks
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from app.users.routers import router as users_router
from app.users.services import get_user, get_random_user, get_users, fetch_random_users, create_user, preload_users
from app.users.dependencies import get_db_session
from app.core.database import async_session_maker
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app):
    async with async_session_maker() as db:
        await preload_users(db)
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(users_router, prefix="/users", tags=["users"])

static_dir = os.path.join(os.path.dirname(__file__), "static")
app.mount("/static", StaticFiles(directory=static_dir), name="static")
templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), "templates"))

@app.get("/")
async def main_page(request: Request, page: int = 1, per_page: int = 20, db: AsyncSession = Depends(get_db_session)):
    skip = (page - 1) * per_page
    users = await get_users(db, skip=skip, limit=per_page)
    return templates.TemplateResponse("index.html", {"request": request, "users": users, "page": page, "per_page": per_page}) 