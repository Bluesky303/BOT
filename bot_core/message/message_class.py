from dataclasses import dataclass

@dataclass
class Message:
    type: str
    data: dict

def create_text(text: str):
    return Message(type='text', data={'text': text})
    
def create_at(target_id: int):
    return Message(type='at', data={'qq': target_id})
