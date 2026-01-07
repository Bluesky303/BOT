from bot_core import plugin_setup, on_event
from bot_core import create_text
from bot_core import send_message
from bot_core import BaseEvent, MessageEvent, GroupMessageEvent, PrivateMessageEvent

from .core.Router import AgentRouter
from core.Agent import ChatAgent
from core.MemoryManager import MemoryManager

@plugin_setup()
class AgentPlugin:
    def __init__(self):
        memory = MemoryManager()
        self.router = AgentRouter([
            ChatAgent(memory),
            # 未来还可以加 ToolAgent、KnowledgeAgent…
        ])

    @on_event("message", lambda event: isinstance(event, MessageEvent))
    async def on_message(self, event):
        reply = await self.router.dispatch(event)
        if reply:
            if isinstance(event, GroupMessageEvent):
                await send_message("group", event.group_id, reply)
            elif isinstance(event, PrivateMessageEvent):
                await send_message("private", event.user_id, reply)

        