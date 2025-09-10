import aiohttp
from .api_key import API_KEY

async def get_balance():
    url = "https://api.deepseek.com/user/balance"

    payload={}
    headers = {
        'Accept': 'application/json',
        'Authorization': f'Bearer {API_KEY}'
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers, data=payload) as response:
            return await response.json()
    
def is_available():
    re = get_balance()
    return re['is_available']

def balance_num():
    re = get_balance()
    return re['balance_infos'][0]["total_balance"]