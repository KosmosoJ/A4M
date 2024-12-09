from sqlalchemy.ext.asyncio import AsyncSession
from models.database import get_session
from sqlalchemy import select
from fastapi import status, HTTPException
from models.models import Category, Anime
from schemas.category import BaseCategory
from sqlalchemy.orm import joinedload
from deep_translator import GoogleTranslator
import slugify


async def create_category(
    category_info: BaseCategory, session: AsyncSession
) -> Category | None:
    """Create a new category

    Args:
        category_info (BaseCategory): creating from pydantic model
        session (AsyncSession)

    Raises:
        HTTPException: if category already exists = http_400

    Returns:
        Category|None
    """
    category = (
        (
            await session.execute(
                select(Category).where(Category.name == category_info.name)
            )
        )
        .scalars()
        .first()
    )

    if category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Category with name {category_info.name} already exists",
        )
    translator = GoogleTranslator(source="ru", target="en")
    trans = translator.translate(category_info.name)

    if len(trans) < 0:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=translator)

    slug = slugify.slugify(trans)
    new_category = Category(name=category_info.name, slug=slug)
    session.add(new_category)
    await session.commit()
    return new_category


async def get_all_categories(session: AsyncSession) -> list[Category] | None:
    """Get all categories from db

    Args:
        session (AsyncSession): _description_

    Returns:
        list[Category]|None:
    """
    categories = (
        (await session.execute(select(Category).order_by(Category.name)))
        .unique()
        .scalars()
        .all()
    )

    if not categories:
        return []
    return categories


async def get_category(category_slug: str, session: AsyncSession) -> Category | None:
    """Get category from DB by slug

    Args:
        category_slug (str): category slug
        session (AsyncSession)

    Raises:
        HTTPException: if not found category with slug -> throw 404

    Returns:
        Category|None: return category
    """
    category = (
        (
            await session.execute(
                select(Category)
                .where(Category.slug == category_slug)
                .options(joinedload(Category.anime))
            )
        )
        .scalars()
        .first()
    )

    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Category with slug {category_slug} not found",
        )

    return category


async def get_or_create_category_id(category_name: str, session: AsyncSession):
    """Получение ID категории, в случае если категория не найдена - создается новая

    Args:
        category_name (str): Название категории
        session (AsyncSession)

    Raises:
        HTTPException: В случае если не получилось перевести название категории - выбрасывается 400

    Returns:
        _type_: int
    """
    category = (
        (await session.execute(select(Category).where(Category.name == category_name)))
        .scalars()
        .first()
    )

    if not category:
        translator = GoogleTranslator(source="ru", target="en")
        trans = translator.translate(category_name)

        if len(trans) < 0:
            await session.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=translator
            )

        slug = slugify.slugify(trans)
        category = Category(name=category_name, slug=slug)
        session.add(category)
        await session.commit()

    return category.id
