from bot_core.plugin import plugin_setup, on_event
from bot_core.message import send_message

import json

# Load Config
config = json.load(open("config.json", "r"))

@plugin_setup()
class Setup:
    @on_event("message", lambda event: hasattr(event, "message_type") and event.message_type == "group" and event.user_id == config["id"])
    async def record_message(event):
        record = json.load(open("record.json", "r"))
        record[event.message_id] = event.message
        json.dump(record, open("record.json", "w"))
    
    @on_event("withdraw", lambda event: hasattr(event, "notice_type") and event.notice_type == "group_recall" and event.operator_id == event.user_id)
    async def recall(event):
        record = json.load(open("record.json", "r"))
        if str(event.message_id) in record:
           await send_message("group", event.group_id, record[str(event.message_id)])