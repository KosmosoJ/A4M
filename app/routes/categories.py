from fastapi.routing import APIRouter
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates
from models.database import get_session
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.models import Anime, Category


router = APIRouter()

@router.get("/")
async def get_categories(
    request: Request, session: AsyncSession = Depends(get_session)
):
    categories = await session.execute(select(Category))
    categories = categories.scalars().all()
    return ...


@router.get("/{id}")
async def get_category(
    id: int, request: Request, session: AsyncSession = Depends(get_session)
):
    animes = await session.execute(select(Anime).where(Anime.category == id))
    animes = animes.scalars().all()
    category = await session.execute(select(Category).where(Category.id == id))
    category = category.scalars().first()
    return ...
