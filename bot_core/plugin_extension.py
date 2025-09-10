from .plugin import plugin_setup, on_event
from .listener import Condition, Handler
from .event import BaseEvent, GroupMessageEvent

from typing import Callable, Optional, List
from functools import wraps
import re

def on_command(
    command: str,
    prefix: str = "/",
    permission: Optional[Condition] = None,
):
    def condition(event: BaseEvent):
        if type(event) == GroupMessageEvent and event.raw_message.startswith(prefix + command):
            if permission and permission(event):
                return True
        
    @on_event("on_message", condition)
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(event: GroupMessageEvent):
            options = {}
            args = ["--default"] + event.raw_message.split()[1:]
            pos, lastpos, option = 0, 0, None
            for i, a in enumerate(args):
                if a.startswith("--"):
                    lastpos, pos = pos, i
                    if option:
                        options[option] = args[lastpos + 1:pos]
                    option = a[2:]
            print(options)
            try:
                await func(event, args, **options)
            except TypeError as e:
                print(f"Need more or less arguments: {e}")
            except Exception as e:
                print(f"Error in command {command}: {e}")
        return wrapper
    return decorator
            # f"{prefix}{command} {参数1} {参数2} --{选项1} {参数11} {参数12} --{选项2} {参数21} {参数22}"
            # {天气： [参数1], 选项1: [参数11, 参数12], 选项2: []}

def on_words(
    words: str,

):
    def condition(event: BaseEvent):
        if type(event) == GroupMessageEvent and re.search(words, event.raw_message):
            return True
        
    @on_event("on_message", condition)
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(event: GroupMessageEvent):
            await func(event)
        return wrapper
    return decorator
