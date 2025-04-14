from dataclasses import dataclass, field
from .message import Message

@dataclass
class Event:
    post_type: str = None# 'message', 'notice'
    time: int = 0
    self_id: int = 0

@dataclass
class MessageEvent(Event):
    post_type: str = 'message'

    message_type: str  = ''# 'private' or 'group'
    sub_type: str = ''
    
    message_id: int = 0
    message_seq: int = 0
    message: list[Message] = field(default_factory=list)
    raw_message: str = ''
    
    user_id: int = 0
    sender: dict = field(default_factory={
        'user_id': 0, 
        'nickname': '', # 昵称
        'card': '', # 群昵称
        'role': '', # member, admin, owner
        'title': '' # 群头衔
    })
    group_id: int = 0 # 0 if private message
    
    font: int = 0 # 字体
    message_format: str = 'array' # 'array' or 'string'
    
def create_event(data: dict):
    if data['post_type'] == 'message':
        msg = MessageEvent(**data)
        return msg
    else:
        return Event(**data)
    
