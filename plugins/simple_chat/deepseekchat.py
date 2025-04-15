from bot_core import plugin_setup, on_event
from bot_core import create_text
from bot_core import send_message

from .deepseek import balance_num

@plugin_setup()
class DeepSeekChat:
    @on_event("balance_call", lambda event: hasattr(event, "raw_message") and event.raw_message == "/余额查询")
    async def on_balance_call(event):
        if event.message_type == "group":
            await send_message("group", event.group_id, [create_text(f"余额是{balance_num()}元")])
        if event.message_type == "private":
            await send_message("private", event.user_id, [create_text(f"余额是{balance_num()}元")])