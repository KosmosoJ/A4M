from fastapi.routing import APIRouter
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from models.database import get_session
from schemas.anime import AnimeBase
import utils.anime as anime_utils
from fastapi.responses import FileResponse, Response, StreamingResponse
import os 


router = APIRouter()

@router.post('/')
async def create_anime(anime_info:AnimeBase ,session:AsyncSession = Depends(get_session)):
    return await anime_utils.create_anime(anime_info, session)
    
@router.get('/')
async def get_all_animes(session:AsyncSession = Depends(get_session)):
    return await anime_utils.get_all_anime(session)

@router.get('/by/{category_slug}')
async def get_anime_random_by_category_slug(category_slug:str, session:AsyncSession = Depends(get_session)):
    return await anime_utils.get_anime_by_category_slug(category_slug, session)

@router.get('/{anime_slug}')
async def get_anime_by_slug(anime_slug:str, session:AsyncSession = Depends(get_session)):
    return await anime_utils.get_anime_slug(anime_slug, session)
    
@router.put('/{anime_slug}')
async def edit_anime_by_slug(anime_slug:str, anime_info:AnimeBase, session:AsyncSession = Depends(get_session)):
    anime = await anime_utils.edit_anime(anime_slug, anime_info, session)
    return anime



@router.get('/files/screensmall')
async def get_anime_screenshot():
    path = 'media/anime/Screenshot_5.png'
    return FileResponse(path)

@router.get('/files/screenbig')
async def get_anime_screenshot_():
    path = 'media/anime/big.jpg'
    return FileResponse(path)

@router.get('/files/screenverybig')
async def get_anime_screenshot__():
    path = 'media/anime/very_big.jpg'
    return FileResponse(path)

    