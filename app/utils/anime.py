from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, not_
from models.models import Anime, Category
from fastapi import HTTPException, status
from schemas.anime import AnimeBase
from translate import Translator
import slugify
import random
from parsers.animego import get_animego_url


async def create_anime_slug(anime_title: str):
    """Функция-помощник для получение слага для аниме из русского названия аниме

    Args:
        anime_title (str): Название аниме

    Returns:
        _type_: _str_
    """
    translator = Translator(from_lang="russian", to_lang="english")
    trans = translator.translate(anime_title)

    slug = slugify.slugify(trans)
    return slug


async def get_all_anime(session: AsyncSession) -> list[Anime]:
    """Получение всех аниме из базы данных

    Args:
        session (AsyncSession): Получение из routes

    Returns:
        list[Anime]: Список всех аниме
    """
    animes = (await session.execute(select(Anime))).unique().scalars().all()

    if not animes:
        return []
    return animes


async def get_anime_slug(anime_slug: str, session: AsyncSession) -> Anime:
    """Получение аниме из базы данных

    Args:
        anime_slug (str): Получение из routes
        session (AsyncSession): Получение из routes

    Returns:
        Anime: Объект аниме
    """
    anime = (
        (await session.execute(select(Anime).where(Anime.slug == anime_slug)))
        .scalars()
        .first()
    )
    
    if not anime:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Anime with slug {anime_slug} not found",
        )

    if not anime.animego_url:
        anime.animego_url = await get_animego_url(anime.name)
        session.add(anime)
        await session.commit()



    return anime


async def create_anime(anime_info: AnimeBase, session: AsyncSession):
    """Создание нового аниме

    Args:
        anime_info (AnimeBase): Информация об аниме
        session (AsyncSession)

    Raises:
        HTTPException: Если данное аниме уже существует - 404

    Returns:
        _type_: Model.Anime
    """
    anime = (
        (await session.execute(select(Anime).where(Anime.slug == anime_info.slug)))
        .scalars()
        .first()
    )

    if anime:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Anime with slug {anime_info.slug} already exists",
        )

    # print(anime_info.model_dump(mode='python'))
    # return []
    new_anime = Anime(**anime_info.model_dump())

    session.add(new_anime)
    await session.commit()
    return new_anime


async def edit_anime(anime_slug: str, anime_info: AnimeBase, session: AsyncSession):
    """Изменение информации о аниме

    Args:
        anime_slug (str): Необходимо для получения аниме, которое будет редактироваться
        anime_info (AnimeBase): Новая информация о аниме
        session (AsyncSession)

    Raises:
        HTTPException: Если не нашли аниме с укзанным слагом - 404

    Returns:
        _type_: Model.Anime
    """
    anime = (
        (await session.execute(select(Anime).where(Anime.slug == anime_slug)))
        .scalars()
        .first()
    )

    if not anime:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Anime with slug {anime_slug} not found",
        )

    anime.name = anime_info.name
    anime.russ_name = anime_info.russ_name
    anime.description = anime_info.description
    anime.category = anime_info.category
    anime.seasons = anime_info.seasons
    anime.started = anime_info.started
    anime.ended = anime_info.ended
    anime.rating = anime_info.rating
    anime.slug = anime_info.slug
    anime.type = anime_info.type

    await session.commit()
    return anime


async def get_anime_by_category_slug(
    category_slug: str, only_slug: bool, session: AsyncSession
):
    """Получение рандомного аниме по категории

    Args:
        category_slug (str): Category.slug
        only (str): Ограничение на вывод только Anime.slug
        session (AsyncSession)

    Raises:
        HTTPException: Возврат 404 если не найдено аниме по указанному category_slug

    Returns:
        Model.Anime
    """
    if only_slug:
        anime_list = (
            (
                await session.execute(
                    select(Anime.slug)
                    .join(Category)
                    .where(and_(Category.slug == category_slug, Anime.type != "cm"))
                )
            )
            .unique()
            .scalars()
            .all()
        )
    else:
        anime_list = (
            (
                await session.execute(
                    select(Anime)
                    .join(Category)
                    .where(and_(Category.slug == category_slug, Anime.type != "cm"))
                )
            )
            .unique()
            .scalars()
            .all()
        )

    if not anime_list:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Anime with category slug {category_slug} not found",
        )

    anime: Anime = random.choice(anime_list)

    if only_slug:
        return anime

    if not anime.animego_url:
        anime.animego_url = await get_animego_url(anime.name)
        session.add(anime)
        await session.commit()
    return anime


async def get_random_anime_slug(session: AsyncSession):
    """Получение рандмного слага аниме

    Args:
        session (AsyncSession)

    Returns:
        _type_: slug:str
    """
    anime = (await session.execute(select(Anime.slug))).unique().scalars().all()

    if not anime:
        return []
    return random.choice(anime)
