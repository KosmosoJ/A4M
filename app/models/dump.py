import json
from .models import *
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

async def dump_models(session:AsyncSession):
    """Дамп данных из бд в JSON формат

    Args:
        session (AsyncSession)
    """
    anime = (await session.execute(select(Anime))).unique().scalars().all()
    categories = (await session.execute(select(Category))).unique().scalars().all()
    images = (await session.execute(select(Image))).unique().scalars().all()
    screenshots = (await session.execute(select(Screenshot))).unique().scalars().all()
    data = {'anime':anime,
            'categories':categories,
            'images':images,
            'screenshots':screenshots}
    
    for item in data:
        dump_data = [v.to_dict() for v in data[item]]
        # return {'data':dump_data}
        
        with open(f'dumped_data/dump_{item}.json', 'w') as f:
        #     # json.dump(data[item], f)
            json.dump(dump_data, f)
