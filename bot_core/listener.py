from .event import Event

from typing import Callable
import asyncio
import traceback

Condition = Callable[[Event], bool]
Handler = Callable[[Event], None]

class EventListener:
    def __init__(self):
        self._events = asyncio.Queue()
        self._handlers = [] # list of (name, condition, handler)
        
    def register_handler(self, name: str, condition: Condition, handler: Handler):
        self._handlers.append((name, condition, handler))

    def unregister_handler(self, name: str):
        for i, (name, condition, handler) in enumerate(self._handlers):
            if name == name:
                del self._handlers[i]
                break

    async def put_event(self, event: Event):
        await self._events.put(event)
        
    async def _process(self, event: Event):
        try:
            for name, condition, handler in self._handlers:
                if condition(event):
                    await handler(event)
        except Exception as e:
            traceback.print_exc()
            print(f"Error in {name}, while processing {event} using {handler}")
                
    async def run(self):
        while True:
            event = await self._events.get()
            await self._process(event)
            self._events.task_done()
            