import aiohttp
from dataclasses import asdict

from .message_class import Message
from .config_load import HTTP_PORT

async def send_message(message_type: str, id: int, message: list):
    '''
    message_type: 'group' or 'private'
    id: group id or user id
    message: list of Message
    
    return message_id
    '''
    async with aiohttp.ClientSession() as session:
        
        if type(message[0]) == Message:
            message = [asdict(m) for m in message]
        
        message_id = await session.post(
            f'http://localhost:{HTTP_PORT}/send_msg', 
            json={
                'type': message_type,
                'user_id': id, 
                'group_id': id,
                'message': message
            })
        return message_id

async def send_group_file(group_id: int, file: str, name: str):
    '''
    group_id: group id
    file: file path e.g. file:///C:/Users/123/Desktop/123.txt
    name: file name
    '''
    async with aiohttp.ClientSession() as session:
        await session.post(
            f'http://localhost:{HTTP_PORT}/upload_group_file', 
            json={
                'group_id': group_id,
                'file': file,
                'name': name,
            })