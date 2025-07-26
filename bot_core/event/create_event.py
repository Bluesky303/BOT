from .event import BaseEvent
from .message_event import *
from .notice_event import *

ParentEvents = BaseEvent.__subclasses__()

def create_event(data: dict) -> BaseEvent:
    message_type = data.get('post_type', '')
    for ParentEvent in ParentEvents:
        if message_type == ParentEvent.post_type:
            if ParentEvent._EVENT_ATTR in data:
                attr = ParentEvent._EVENT_ATTR
                for ChildEvent in ParentEvent.__subclasses__():
                    if data[attr] == ChildEvent.__dict__[attr]:
                        return ChildEvent(**data)
            else:
                return ParentEvent(**data)
    else: 
        return BaseEvent(**data)