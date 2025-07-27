from .plugin import plugin_setup, on_event
from .listener import Condition, Handler
from .event import BaseEvent, GroupMessageEvent

from typing import Callable, Optional
from functools import wraps
import re

def on_command(
    command: str,
    prefix: str = "/",
    desc: Optional[str] = None,
    permission: Optional[Condition] = None,
):
    def condition(event: BaseEvent):
        if type(event) == GroupMessageEvent:
            
        return lambda event: type(event) == GroupMessageEvent and event.message.startwith(prefix + command)
    @on_event("on_message", condition)
    def decorator(func: Handler):
        @wraps(func)
        async def wrapper(event: BaseEvent):
            await func(event)
        return wrapper
        
    return decorator
            # prefix天气 参数1 参数2 --选项1 参数11 参数12 --选项2
            # {天气： [参数1], 选项1: [参数11, 参数12], 选项2: []}
            
    def 