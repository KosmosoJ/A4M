from fastapi.routing import APIRouter
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from models.database import get_session
from schemas.anime import AnimeBase
import utils.anime as anime_utils


router = APIRouter()

@router.post('/')
async def create_anime(anime_info:AnimeBase ,session:AsyncSession = Depends(get_session)):
    return await anime_utils.create_anime(anime_info, session)
    
@router.get('/')
async def get_all_animes(session:AsyncSession = Depends(get_session)):
    return await anime_utils.get_all_anime(session)

@router.get('/{anime_slug}')
async def get_anime_by_slug(anime_slug:str, session:AsyncSession = Depends(get_session)):
    return await anime_utils.get_anime_slug(anime_slug, session)
    
