import httpx
import lxml
from bs4 import BeautifulSoup


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0"}
    

async def fetch_animego(search:str) -> str:
    search = search.replace(' ','+')
    
    url = f'https://animego.org/search/anime?q={search}'
    session = httpx.AsyncClient(headers=headers)
    response = await session.get(url)
    
    return response.text

async def process_animego_fetched_data(data:str, search:str) -> str:
    soup = BeautifulSoup(data, 'lxml')
    whole_page = soup.find('div', class_='animes-container-list')
    try:
        anime_container = whole_page.find_all('div', class_='animes-grid-item')
        for anime in anime_container:
            if anime.find('div',class_='text-gray-dark-6').text == search:
                print(anime.find('a', href=True)['href'])
                return anime.find('a', href=True)['href']
        return 'searched'
    except Exception:
        return 'searched'
    

async def get_animego_url(search:str) -> str:
    data = await fetch_animego(search)
    return await process_animego_fetched_data(data, search)
