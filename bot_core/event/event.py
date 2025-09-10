from dataclasses import dataclass

from typing import ClassVar

@dataclass
class BaseEvent:
    _EVENT_ATTR: ClassVar[str] = ''
    post_type: str = '' # 'message', 'notice', 'request', 'meta_event'
    time: int = 0
    self_id: int = 0
    

