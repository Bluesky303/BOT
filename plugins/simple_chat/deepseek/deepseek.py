from openai import OpenAI
from pathlib import Path
import json
import asyncio

path = Path(__file__).parent / "apikey.json"
api_key = json.load(open(path))['key']
client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

init_chat = '你现在是刚加入一个群聊的一员，需要非常拟人地参与群聊的聊天之中，接下来的输入将会是群聊消息，格式为{"名称": 说话人名字, "时间": 说话时间, "内容": 说话内容}。注意回复需要尽量简短并且符合氛围，需要自行选择是否发送消息如果需要发送则回复{"state": "发送", "message" : "你想发送的消息"}，否则回复{"state": "不发送"}，不需要任何多余文字。你的名字是："心镜"，因此在别人说话对象是你时应给予回复，你需要模拟一个比较高冷而并非很活泼的人格。这条消息之后请回复{"state": "明白"}'
messages_info = json.load(open(path.parent / "messages.json"))
async def group_chat(group_id, message, name, time):
    if not group_id in messages_info:
        messages_info[group_id] = [{"role": "user", "content": init_chat}]
    else:
        messages_info[group_id].append({"role": "user", "content": f'"名称": {name}, "时间": {time}, "内容": {message}'})
    messages = messages_info[group_id]
    try:
        print('start get')
        response = client.chat.completions.create(model = "deepseek-chat", messages = messages)
        re = response.choices[0].message
        print(re)
        messages.append(re)
        messages_info[group_id] = messages
        json.dump(messages_info, open(path.parent / "messages.json", "w"))
        r = json.loads(str(re.content))
        print(r)
        if r['state'] == '发送':
            return r["message"]
    except Exception as e:
        print(e)