from fastapi import APIRouter, Depends, Query, HTTPException, Form, Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.users.schemas import UserRead, UserCreate
from app.users.services import create_user, get_user, get_users, get_random_user, fetch_random_users
from app.users.dependencies import get_db_session
from typing import List
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.exc import IntegrityError

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/", response_model=List[UserRead])
async def list_users(skip: int = 0, limit: int = 1000, db: AsyncSession = Depends(get_db_session)):
    return await get_users(db, skip=skip, limit=limit)

@router.get("/random", response_model=UserRead)
async def get_random(db: AsyncSession = Depends(get_db_session)):
    user = await get_random_user(db)
    if not user:
        raise HTTPException(status_code=404, detail="No users in database")
    return user


@router.get("/{user_id}", response_model=UserRead)
async def get_user_by_id(user_id: int, db: AsyncSession = Depends(get_db_session)):
    user = await get_user(db, user_id)
    print("USER:", user)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user



@router.post("/fetch", include_in_schema=False)
async def fetch_and_store_users_form(count: int = Form(...), db: AsyncSession = Depends(get_db_session)):
    users_data = await fetch_random_users(count)
    for user_data in users_data:
        user = UserCreate(
            gender=user_data["gender"],
            first_name=user_data["name"]["first"],
            last_name=user_data["name"]["last"],
            phone=user_data["phone"],
            email=user_data["email"],
            location=", ".join([user_data["location"]["country"], user_data["location"]["city"]]),
            picture=user_data["picture"]["thumbnail"]
        )
        try:
            await create_user(db, user)
        except IntegrityError:
            await db.rollback()
    return RedirectResponse("/", status_code=303)

@router.get("/user/{user_id}")
async def user_page(request: Request, user_id: int, db: AsyncSession = Depends(get_db_session)):
    user = await get_user(db, user_id)
    if not user:
        return RedirectResponse("/", status_code=302)
    return templates.TemplateResponse("user.html", {"request": request, "user": user})

@router.get("/random-page")
async def random_user_page(request: Request, db: AsyncSession = Depends(get_db_session)):
    user = await get_random_user(db)
    if not user:
        return RedirectResponse("/", status_code=302)
    return templates.TemplateResponse("user.html", {"request": request, "user": user}) 