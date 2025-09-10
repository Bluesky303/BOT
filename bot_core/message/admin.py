import aiohttp
from .config_load import HTTP_PORT

async def set_group_ban(group_id: int, user_id: int, duration: int):
    async with aiohttp.ClientSession() as session:
        await session.post(
            f'http://localhost:{HTTP_PORT}/set_group_ban', 
            json={
                'group_id': group_id,
                'user_id': user_id,
                'duration': duration,
            })
        