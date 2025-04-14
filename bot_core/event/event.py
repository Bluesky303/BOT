from dataclasses import dataclass

@dataclass
class Event:
    post_type: str = None # 'message', 'notice', 'request', 'meta_event'
    time: int = 0
    self_id: int = 0
    

