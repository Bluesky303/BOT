from dataclasses import dataclass

from .event import BaseEvent

from typing import ClassVar

@dataclass
class NoticeEvent(BaseEvent):
    _EVENT_ATTR: ClassVar[str] = 'notice_type'
    post_type: str = 'notice'
    notice_type: str = ''
    
@dataclass
class GroupMessageWithDraw(NoticeEvent):
    notice_type: str = 'group_recall'
    group_id: int = 0
    user_id: int = 0
    operator_id: int = 0
    message_id: int = 0