from dataclasses import dataclass, field

from .event import Event
from ..message import Message


@dataclass
class MessageEvent(Event):
    post_type: str = 'message'
    sub_type: str = ''
    
    user_id: int = 0
    sender: dict = field(default_factory={})
    
    message_id: int = 0
    message: list[Message] = field(default_factory=list)
    raw_message: str = ''
    
    font: int = 0 # 字体

@dataclass
class PrivateMessageEvent(MessageEvent):
    message_type: str  = 'private'
    sub_type: str = '' # 'friend', 'group', 'group_self', 'other'
    
    sender: dict = field(default_factory={
        'user_id': 0,
        'nickname': '', # 昵称 
        'card': '', # 群昵称
        'group_id': 0 # has value if sub_type is 'group'
    })
    
    message_format: str = 'array' # 'array' or 'string'
    temp_source: int = 0 # 不知道
    
    def is_private(self):
        return True

@dataclass
class GroupMessageEvent(MessageEvent):
    message_type: str = 'group'
    sub_type: str = '' # 'normal', 'anonymous', 'notice', 'other'
    
    sender: dict = field(default_factory={
        'user_id': 0, 
        'nickname': '', # 昵称
        'card': '', # 群昵称
        'role': '', # member, admin, owner
        'title': '' # 群头衔
    })