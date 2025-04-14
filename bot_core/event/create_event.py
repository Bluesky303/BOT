from .event import Event
from .message_event import MessageEvent, PrivateMessageEvent, GroupMessageEvent
from .notice_event import GroupMessageWithDraw

diction = { # post_type层
    'message': {
        'attr': 'message_type', # 标记本层的属性
        'private': PrivateMessageEvent,
        'group': GroupMessageEvent
    },
    'notice': {
        'attr': 'notice_type',
        'group_recall': GroupMessageWithDraw
    },
    'request': {
    
    },
    'meta_event': {
    
    },
}

def create_event(data: dict):
    layer1 = data['post_type']
    layer1_attr = diction[layer1]['attr']
    layer2 = data[layer1_attr]
    msg = diction[layer1][layer2](**data)
    return msg