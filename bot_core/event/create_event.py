from .event import Event
from .message_event import MessageEvent, PrivateMessageEvent, GroupMessageEvent

diction = { # post_type层
    'message': {
        'attr': 'message_type', # 标记本层的属性
        'private': PrivateMessageEvent,
        'group': GroupMessageEvent
    },
    'notice': {
        
    },
    'request': {
    
    },
    'meta_event': {
    
    },
}

def create_event(data: dict):
    msg = diction[data['post_type']][diction[data['post_type']]['attr']](**data)
    