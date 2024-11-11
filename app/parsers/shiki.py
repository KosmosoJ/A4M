import aiohttp
import time
import asyncio
from .tokens import create_config
from sqlalchemy.ext.asyncio import AsyncSession
from models.models import Anime, Image, Screenshot
from utils.categories import get_or_create_category_id
from sqlalchemy import select
import httpx
from datetime import datetime



bearer_headers = {
    "User-Agent": "Anime4Mood",
    'Authorization': "Bearer HWWww81fiCbBqlwAjEhbt__6K9FFds9OnXLRMXVjpAM"}

class Limit(object):
    def __init__(self, calls=5, period=1):
        self.calls = calls
        self.period = period
        self.clock = time.monotonic
        self.last_reset = 0
        self.num_calls = 0

    def __call__(self, func):
        async def wrapper(*args, **kwargs):
            if self.num_calls >= self.calls:
                print('Прокнуло')
                await asyncio.sleep(self.__period_remaining())

            period_remaining = self.__period_remaining()

            if period_remaining <= 0:
                self.num_calls = 0
                self.last_reset = self.clock()

            self.num_calls += 1

            return await func(*args, **kwargs)

        return wrapper

    def __period_remaining(self):
        elapsed = self.clock() - self.last_reset
        return self.period - elapsed
    
async def request_shiki(url, params=None):
    # client = httpx.AsyncClient()
    # response = await client.get(url, params=params, headers=bearer_headers)
    # if response.status_code == 200:
    #     return response.json()
    async with httpx.AsyncClient(headers=bearer_headers, timeout=20) as client:
        response = await client.get(url, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            if response.status_code == 401:
                if response.json()['error'] == 'invalid_token':
                    return None
            await asyncio.sleep(62)
            response = await client.get(url, params=params)
            return response.json()
    # else:
    #     await asyncio.sleep(62)
    #     response = await client.get(url, params=params, headers=bearer_headers)
    #     return response.json()
        
        
    
async def fetch_anime_list(page:int) -> list:
    url = 'https://shikimori.one/api/animes'
    params = {
        'page':page,
        'limit':50,
        'order':'id'
        
    }
    anime_list = await request_shiki(url, params)
    if anime_list is None:
        return None
    if len(anime_list) == 0:
        return None
    return anime_list


async def request_shiki_anime_list(session:AsyncSession):    
    # config = await create_config()
    # bearer_headers['Authorization'] = f'Bearer {config.get('section_a', 'APP_ACCESS_TOKEN')}'
    page = 93
    while True:
        anime_list = await fetch_anime_list(page)
        
        if anime_list is None:
            break
        
        print(f'Поехала страница №{page}')
        for anime in anime_list:
            anime_item,extended_info = await create_anime_item(anime, session)
            if anime_item is None:
                continue
            
            await create_image_item(anime_info=anime, anime=anime_item,session=session)
            
            if len(extended_info['screenshots']) > 0:
                await create_screenshot_item(anime_info=extended_info, anime=anime_item, session=session)
            
        page += 1
    
    
async def get_mood(genres:dict):
    moods ={
        'Гурман':'Голодное',
        'Драма':'Грустное',
        'Комедия':'Веселое',
        'Повседневность':'Беззаботное',
        'Приключения':'Мечтательное',
        'Романтика':'Любовное',
        'Сверхъестественное':'Мистическое',
        'Спорт':'Воодушевленное',
        'Тайна':'Таинственное',
        'Триллер':'Напряженное',
        'Ужасы':'Тревожное',
        'Фантастика':'Мистическое',
        'Фэнтези':'Мистическое',
        'Экшен':'Воодушевленное',
    }
    genres_list = []
    for genre in genres:
        
        if genre in ['Сёнен', 'Сэйнэн', 'Сёдзё', 'Дзёсей', 'Детское']:
            continue
        
        genres_list.append(genre['russian'])
        
    if 'Хентай' in genres_list or 'Эротика' in genres_list:
        return 'Хорни'
    
    try:
        return moods[genres_list[0]]
    except KeyError:
        return None
    except IndexError:
        return None
    
    
async def create_anime_item(anime_info:dict, session:AsyncSession):
    # print(anime_info)
    anime_existence = (await session.execute(select(Anime).where(Anime.shiki_id == anime_info['id']))).scalars().first()
    if anime_existence:
        return (None,None)
    
    url = f'https://shikimori.one/api/animes/{anime_info['id']}'
    anime_extended_info = await request_shiki(url)
    mood = await get_mood(anime_extended_info['genres'])
    if mood is None:
        return (None,None)
    anime = Anime(name=anime_info['name'],
                  russ_name=anime_info['russian'],
                  type=anime_info['kind'],
                  started= datetime.strptime(anime_info['aired_on'],'%Y-%m-%d').date() if anime_info['aired_on'] else None,
                  ended = datetime.strptime(anime_info['released_on'],'%Y-%m-%d').date() if anime_info['released_on'] else None,
                  description=anime_extended_info['description'],
                  rating = 5,
                  seasons=1,
                  slug = f"{anime_info['id']}_{anime_extended_info['name'].strip()}",
                  category = await get_or_create_category_id(mood,session),
                  episodes = anime_extended_info['episodes'],
                  shiki_id = anime_info['id'],
                  shiki_url = f'https://shikimori.one{anime_info['url']}',
                  animego_url = None                  
                  )
    session.add(anime)
    await session.commit()
    return anime,anime_extended_info

async def create_screenshot_item(anime, anime_info, session:AsyncSession):
    for screen in anime_info['screenshots']:
        screenshot_item = Screenshot(preview=f'https://shikimori.one{screen['preview']}',
                        original=f'https://shikimori.one{screen['original']}',
                        anime=anime.id)
        session.add(screenshot_item)
    await session.commit()
    return screenshot_item
    
async def create_image_item(anime, anime_info, session:AsyncSession):
    image_item = Image(preview=f'https://shikimori.one{anime_info['image']['preview']}',
                       original=f'https://shikimori.one{anime_info['image']['original']}',
                       anime=anime.id)
    session.add(image_item)
    await session.commit()
    return image_item
    