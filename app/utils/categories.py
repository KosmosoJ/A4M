from sqlalchemy.ext.asyncio import AsyncSession
from models.database import get_session
from sqlalchemy import select
from fastapi import status, HTTPException
from models.models import Category
from schemas.category import BaseCategory
from translate import Translator
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
    translator = Translator(from_lang='russian', to_lang='english')
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
    categories = (await session.execute(select(Category))).unique().scalars().all()

    if not categories:
        return []
    return categories


async def get_category(category_slug: str, session: AsyncSession) -> Category|None:
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
                select(Category).where(Category.slug == category_slug)
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
