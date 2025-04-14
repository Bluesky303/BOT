from bot_core.plugin import plugin_setup, on_event
from bot_core.message import send_message

from pathlib import Path
import json


path = Path(__file__).parent
# Load Config
config = json.load(open(path / "config.json", "r"))

@plugin_setup()
class Setup:
    @on_event("message", lambda event: hasattr(event, "message_type") and event.message_type == "group" and event.user_id == config["id"])
    async def record_message(event):
        record = json.load(open(path / "record.json", "r"))
        record[event.message_id] = [event.message, event.time]
        if len(record) > 100:
            timesort = sorted(record.items(), key=lambda x: x[1][1])
            record = dict(timesort[-50:])
        json.dump(record, open(path / "record.json", "w"))

    @on_event("withdraw", lambda event: hasattr(event, "notice_type") and event.notice_type == "group_recall" and event.operator_id == event.user_id)
    async def recall(event):
        record = json.load(open(path / "record.json", "r"))
        if str(event.message_id) in record:
           await send_message("group", event.group_id, record[str(event.message_id)][0])