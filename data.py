'''
用于了解消息格式
'''

import uvicorn
from fastapi import FastAPI, Request


app = FastAPI()

@app.post("/onebot")
async def root(request: Request):
    data = await request.json()
    print(data)
if __name__ == "__main__":
    uvicorn.run(app, port=8070)
