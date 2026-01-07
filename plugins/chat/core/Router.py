
from .Agent import BaseAgent

from typing import List

class AgentRouter:
    def __init__(self, agents: List[BaseAgent]):
        self.agents = agents

    async def dispatch(self, event):
        for agent in self.agents:
            if await agent.should_handle(event):
                reply = await agent.handle(event)
                return reply
        return None
