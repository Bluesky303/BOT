import uvicorn
from fastapi import FastAPI, Request
from contextlib import asynccontextmanager
import asyncio

from bot_core import EventListener, PluginManager, create_event

Listener = None

@asynccontextmanager
async def listener_setup(app: FastAPI):
    global Listener
    Listener = EventListener() # 队列需要在循环内初始化
    manager = PluginManager(Listener) # 插件加载要在循环内
    manager.load_all_plugins()
    listener_task = asyncio.create_task(Listener.run())
    yield 
    listener_task.cancel()
    try:
        await listener_task
    except asyncio.CancelledError:
        pass
    

app = FastAPI(lifespan=listener_setup)

@app.post("/onebot")
async def root(request: Request):
    data = await request.json()
    event = create_event(data)
    await Listener.put_event(event)
    await Listener._events.join()

if __name__ == "__main__":
    uvicorn.run(app, port=8070)