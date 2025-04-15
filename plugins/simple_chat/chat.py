from bot_core import plugin_setup, on_event
from bot_core import create_text
from bot_core import send_message

from .deepseek import group_chat
from pathlib import Path
import json

path = Path(__file__).parent / "config.json"
if not path.exists():
    json.dump({'time': 0, 'state': None, 'master': None, 'group_id': []}, open(path, "w"))

config = json.load(open(path))

@plugin_setup()
class setup:
    @on_event("call", lambda event: event.raw_message == "心镜" and config['state'] == None)
    async def on_call(event):
        global config
        config = json.load(open(path))
        last_time = config['time']
        time = event.time - last_time
        l = [time] + [600, 60, 10]
        l = sorted(l)
        emotion = l[l.index(time) + 1] if time < 600 else 600
        d = {
            600: [create_text("我在")],
            60: [create_text("有什么事？")],
            10: [{
                'type': 'image', 
                'data': {
                    'file': '236A65D82ECF95253480016C8A3ACE6C.jpg', 
                    'subType': 1, 
                    'url': 'https://multimedia.nt.qq.com.cn/download?appid=1407&fileid=EhRysvEy7yhzdjhMgeihQxuggcwyDhjmugIg_wooxP-V7djXjAMyBHByb2RQgL2jAVoQ8dtk_mEFgsQjknJPiQmvKnoC6G4&spec=0&rkey=CAQSKAB6JWENi5LMCpIiEJodguNuidpWWtzEoJu5SnZRhiiqmdeMOS5RfA8', 
                    'file_size': '40294'}
                }]
        }
        config['time'] = event.time
        json.dump(config, open(path, "w"))
        await send_message('group', event.group_id, d[emotion])
        
    @on_event("state_change", lambda event: event.raw_message.split()[0] == "/deepseek" and event.user_id == config['master'])
    async def on_state_change(event):
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
    async def on_talk(event):
        print(event.raw_message)
        reply = await group_chat(event.group_id, event.message, event.sender['card'], event.time)
        print(reply)
        if reply:
            await send_message('group', event.group_id, reply)