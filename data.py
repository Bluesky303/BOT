'''
用于了解消息格式
'''

import uvicorn
from fastapi import FastAPI, Request

import yaml

config = yaml.safe_load(open("config.yaml"))

app = FastAPI()

@app.post("/")
async def root(request: Request):
    data = await request.json()
    print(data)
if __name__ == "__main__":
    uvicorn.run(app, host=config['POST_HOST'], port=config['POST_PORT'])
