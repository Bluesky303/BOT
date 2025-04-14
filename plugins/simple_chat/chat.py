from bot_core import plugin_setup, on_event
from bot_core import create_text
from bot_core import send_message

from pathlib import Path
import json

path = Path(__file__).parent / "config.json"
if not path.exists():
    json.dump({'time': 0}, open(path, "w"))

@plugin_setup()
class setup:
    @on_event("call", lambda event: event.raw_message == "心镜")
    async def on_call(event):
        last_time = json.load(open(path))['time']
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
        json.dump({'time': event.time}, open(path, "w"))
        await send_message('group', event.group_id, d[emotion])