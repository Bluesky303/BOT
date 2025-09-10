from bot_core import plugin_setup, on_event
from bot_core import create_text
from bot_core import send_message
from bot_core import BaseEvent, GroupMessageEvent

from bot_core.plugin_extension import on_command

@plugin_setup()
class setup:
    @on_command("111", prefix="1", permission=lambda e: True)
    async def handler(self, event: GroupMessageEvent, a=1, b=2):
        print(1)
        await send_message("group", event.group_id, [create_text(f"{a} {b}")])
        