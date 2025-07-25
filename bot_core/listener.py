from .event import Event

from typing import Callable
import asyncio
import traceback

from typing import List, Tuple

Condition = Callable[[Event], bool]
Handler = Callable[[Event], None]

class EventListener:
    def __init__(self, max_concurrent: int = 10):
        self._events = asyncio.Queue()
        self._handlers: List[Tuple[str, Condition, Handler]] = []
        self._semaphore = asyncio.Semaphore(max_concurrent)
        self._pending_tasks = set()
        self._running = False
        
    def register_handler(self, name: str, condition: Condition, handler: Handler):
        self._handlers.append((name, condition, handler))

    def unregister_handler(self, name: str):
        self._handlers = [
            (n, c, h) for n, c, h in self._handlers
            if n != name
        ]

    async def put_event(self, event: Event):
        await self._events.put(event)
    
    async def _safe_handler(self, handler: Handler, event: Event, name: str):
        try:
            async with self._semaphore: 
                await handler(event)
        except Exception as e:
            traceback.print_exc()
            print(f"Error in handler '{name}': {e}\nEvent: {event}")
    
    async def _process_event(self, event: Event):
        matched = False
        for name, condition, handler in self._handlers:
            if condition(event):
                matched = True
                # 为每个处理器创建独立任务
                task = asyncio.create_task(self._safe_handler(handler, event, name))
                self._pending_tasks.add(task)
                task.add_done_callback(lambda t: self._pending_tasks.discard(t))
        
        if not matched:
            print(f"No handler matched for event: {event}")
                
    async def run(self):
        if self._running:
            raise RuntimeError("Listener is already running")
        
        self._running = True
        while self._running:
            event = await self._events.get()
            # 立即创建处理任务，不阻塞主循环
            asyncio.create_task(self._process_event(event))
            self._events.task_done()
    
    async def stop(self):
        self._running = False
        # 等待队列处理完成
        await self._events.join()
        # 等待所有处理任务完成
        await asyncio.gather(*self._pending_tasks, return_exceptions=True)