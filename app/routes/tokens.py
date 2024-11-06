from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.routing import APIRouter
from parsers.tokens import request_new_tokens, get_tokens



router = APIRouter()


@router.get('/update')
async def update_tokens():
    return await request_new_tokens()

@router.get('/')
async def get_tokens_info():
    return await get_tokens()