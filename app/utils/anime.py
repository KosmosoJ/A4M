from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.models import Anime
from fastapi import HTTPException, status
from schemas.anime import AnimeBase

async def get_all_anime(session:AsyncSession) -> list[Anime]:
    """Получение всех аниме из базы данных

    Args:
        session (AsyncSession): Получение из routes

    Returns:
        list[Anime]: Список всех аниме 
    """
    animes = (await session.execute(select(Anime))).scalars().all()
    
    if not animes:
        return []
    return animes

async def get_anime_slug(anime_slug:str, session:AsyncSession) -> Anime:
    """Получение аниме из базы данных

    Args:
        anime_slug (str): Получение из routes
        session (AsyncSession): Получение из routes

    Returns:
        Anime: Объект аниме
    """
    anime = (await session.execute(select(Anime).where(Anime.slug == anime_slug))).scalars().first()
    
    if not anime:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Anime with slug {anime_slug} not found')
    
    return anime


async def create_anime(anime_info:AnimeBase, session:AsyncSession):
    anime = (await session.execute(select(Anime).where(Anime.slug == anime_info.slug))).scalars().first()
    
    if anime:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'Anime with slug {anime_info.slug} already exists')

    # print(anime_info.model_dump(mode='python'))
    # return []
    new_anime = Anime(**anime_info.model_dump())
    
    session.add(new_anime)
    await session.commit()
    return new_anime