from fastapi import APIRouter
from parsers.shiki import request_shiki_anime_list

router = APIRouter()


@router.get('/')
async def parse_shikimori():
    return await request_shiki_anime_list()