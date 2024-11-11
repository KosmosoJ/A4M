from fastapi import APIRouter, Depends, BackgroundTasks
from parsers.shiki import request_shiki_anime_list
from models.database import get_session
from sqlalchemy.ext.asyncio import AsyncSession



router = APIRouter()


@router.get('/')
async def parse_shikimori(background:BackgroundTasks,session:AsyncSession = Depends(get_session)):
    background.add_task(request_shiki_anime_list,session=session)
    return {'message':'Парсинг начался'}