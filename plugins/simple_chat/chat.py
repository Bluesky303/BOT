from bot_core import plugin_setup, on_event
from bot_core import create_text
from bot_core import send_message
from bot_core import BaseEvent, GroupMessageEvent

from .deepseek import group_chat
from pathlib import Path
import json

path = Path(__file__).parent / "config.json"
if not path.exists():
    json.dump({'time': 0, 'state': None, 'master': None, 'group_id': []}, open(path, "w"))

config = json.load(open(path))

@plugin_setup()
class setup:
    @on_event("state_change", lambda event: type(event) == GroupMessageEvent and event.raw_message.split()[0] == "/deepseek" and event.user_id == config['master'])
    async def on_state_change(self, event: GroupMessageEvent):
        global config
        config = json.load(open(path))
        if event.raw_message.split()[1] == 'on':
            config['state'] = 'deepseek'
            await send_message('group', event.group_id, [create_text("开启ds")])
        if event.raw_message.split()[1] == 'off':
            config['state'] = None
            await send_message('group', event.group_id, [create_text("关闭ds")])
        json.dump(config, open(path, "w"))
            
    @on_event("talk", 
              lambda event: hasattr(event, "message_type") and 
              event.message_type == "group" and
              event.group_id in config['group_id'] and
              config['state'] == 'deepseek' and 
              not event.raw_message.split()[0] == "/deepseek")
    async def on_talk(self, event: GroupMessageEvent):
        print(event.raw_message)
        reply = await group_chat(event.group_id, event.message, event.sender['card'], event.time)
        print(reply)
        if reply:
            await send_message('group', event.group_id, reply)