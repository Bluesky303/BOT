class MemoryManager:
    def __init__(self, short_term_size=30):
        self.short_term = []
        self.long_term = []  # 这里先用 list，之后换 FAISS + SQLite

    def add(self, event):
        self.short_term.append(event.raw_message)
        if len(self.short_term) > 30:
            self.short_term.pop(0)

    def retrieve(self, query: str):
        # TODO: 向量检索 + rerank
        # 现在先简单返回短期记忆
        return "\n".join(self.short_term[-10:])
