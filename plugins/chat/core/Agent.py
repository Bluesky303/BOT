from bot_core import create_at, create_text
from bot_core import MessageEvent

from .MemoryManager import MemoryManager
from .LLM import call_llm

class BaseAgent:
    """所有 Agent 的基类"""
    def __init__(self, memory: MemoryManager, tools=None):
        self.memory = memory
        self.tools = tools or {}

    async def should_handle(self, event) -> bool:
        """是否处理该事件"""
        raise NotImplementedError

    async def handle(self, event):
        """处理事件，返回消息"""
        raise NotImplementedError


class ChatAgent(BaseAgent):
    async def should_handle(self, event: MessageEvent):
        # 例如：有人@bot 或关键词触发
        return "bot" in event.raw_message.lower() or \
               str(event.user_id) in event.raw_message

    async def handle(self, event: MessageEvent):
        # 1. 写入记忆
        self.memory.add(event)

        # 2. 检索相关上下文
        context = self.memory.retrieve(event.raw_message)

        # 3. 构建 prompt 调用 LLM
        reply_text = await call_llm(context, event.raw_message)

        # 4. 返回消息
        return [create_at(event.sender["user_id"]), create_text(reply_text)]