import configparser
import aiohttp
import os 


headers = {
    "User-Agent": "Anime4Mood"}


async def create_config():
    config = configparser.ConfigParser()
    ini_path =os.path.abspath('tokens.ini')
    config.read(ini_path)
    return config

async def get_app_refresh_token():
    config = await create_config()
    tokens={
        'client_id': config.get('section_a', 'USER_AUTH_CODE'),
        'client_secret': config.get('section_a', 'USER_SECRET_CODE'),
        'refresh': config.get('section_a', 'APP_REFRESH_TOKEN')
    }
    
    return tokens

async def request_new_tokens():
    """Получение новых ключей от шикимори
    """
    tokens = await get_app_refresh_token()
    data = {
        'grant_type':'refresh_token',
        'client_id':tokens['client_id'],
        'client_secret':tokens['client_secret'],
        'refresh_token':tokens['refresh']
    }
    url = "https://shikimori.one/oauth/token"
    
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers,data=data) as response:
            token_data = await response.json()
            
    return {'message':token_data}
    await refresh_token(access=token_data['access_token'], refresh=token_data['refresh_token'])
    return {'message':'Tokens updated'}
            

async def refresh_token(access:str, refresh:str):
    config = await create_config()
    ini_path =os.path.abspath('app/tokens.ini')
    
    config.set('section_a', 'APP_ACCESS_TOKEN', access)
    config.set('section_a', 'APP_REFRESH_TOKEN', refresh)
    
    with open(ini_path, 'w') as file:
        config.write(file)
        
async def get_tokens():
    config = await create_config()
    
    return {'token':config.get('section_a', 'APP_ACCESS_TOKEN')}
        
