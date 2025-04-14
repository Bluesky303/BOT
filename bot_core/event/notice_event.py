from dataclasses import dataclass

from .event import Event

@dataclass
class NoticeEvent(Event):
    post_type: str = 'notice'
    notice_type: str = ''
    
@dataclass
class GroupMessageWithDraw(NoticeEvent):
    notice_type: str = 'group_recall'
    
    group_id: int = 0
    user_id: int = 0
    operater_id: int = 0
    message_id: int = 0