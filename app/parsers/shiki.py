import aiohttp
import time
import asyncio
from .tokens import create_config


bearer_headers = {
    "User-Agent": "Anime4Mood",
    'Authorization': ''}

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
    
@Limit(calls=90, period=60)
async def fetch_anime_list(page:int) -> list:
    url = 'https://shikimori.one/api/animes'
    params = {'page':page, 'order':'id','limit':50}
    async with aiohttp.ClientSession(headers=bearer_headers) as session:
        async with session.get(url, params=params) as response:
            anime_list = await response.json()
    if len(anime_list) == 0:
        return None
    return anime_list


async def request_shiki_anime_list():    
    config = await create_config()
    bearer_headers['Authorization'] = config.get('section_a', 'APP_ACCESS_TOKEN')
    page = 1
    while True:
        anime_list = await fetch_anime_list(page)
        
        if anime_list is None:
            break
        # anime_list['anime'] Доставать инфу отсюдова
        return {'anime':anime_list}
        for anime in anime_list:
            ...
            # if kind == 'cm':
            # continue
        break
        page += 1
    
    
    



