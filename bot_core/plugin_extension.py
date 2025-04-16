from .plugin import plugin_setup, on_event
from .listener import Condition, Handler
from .event import Event

from typing import Callable, Optional
from functools import wraps
import re
def cut_command(prefix: str, command: str, text: str):
    d = {}



def on_command(
    command: str,
    prefix: str = "/",
    desc: Optional[str] = None,
    permission: Optional[Condition] = None,
):
    @on_event("on_message", condition=lambda event: event.raw_message.startswith(prefix + command))
    def decorator(func: Handler):
        @wraps(func)
        async def wrapper(event: Event):
            await func(event)
        return wrapper
        
    return decorator
            # prefix天气 参数1 参数2 --选项1 参数11 参数12 --选项2
            # {天气： [参数1], 选项1: [参数11, 参数12], 选项2: []}