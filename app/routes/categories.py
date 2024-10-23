from fastapi.routing import APIRouter
from fastapi.requests import Request
from models.database import get_session
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
import utils.categories as cat_utils
import schemas.category as cat_schemas


router = APIRouter()

@router.get("/")
async def get_categories(
    request: Request, session: AsyncSession = Depends(get_session)
):
    
    return await cat_utils.get_all_categories(session)


@router.get("/{slug}")
async def get_category(
    slug: str, request: Request, session: AsyncSession = Depends(get_session)
):
    category = await cat_utils.get_category(slug,session)
    return category

@router.post('/')
async def create_category(category_info:cat_schemas.BaseCategory, session:AsyncSession = Depends(get_session)):
    category = await cat_utils.create_category(category_info, session)
    return category
