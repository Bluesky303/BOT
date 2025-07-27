from bot_core import plugin_setup, on_event, send_message, create_text
from bot_core import BaseEvent, GroupMessageEvent

import json, pathlib, os

config_path = pathlib.Path("plugins/reread/config.json")

if not config_path.exists():
    config_path.touch()
    json.dump({"allow_group": []}, open(config_path, 'w'))
    config = {}
else:
    config = json.load(open(config_path, 'r'))


@plugin_setup()
class setup:
    @on_event("on_message", lambda event: type(event) == GroupMessageEvent and event.group_id in config["allow_group"])
    async def check_message(self, event: GroupMessageEvent):
        group_id = event.group_id
        if not config.get(group_id) or event.raw_message != config[group_id]['last_message']:
            config[group_id]['last_message'] = event.raw_message
        elif event.raw_message != config[group_id]['last_send']:
            await send_message('group', group_id, event.message)
            config[group_id]['last_send'] = event.raw_message
        json.dump(config, open(config_path, 'w'))
        