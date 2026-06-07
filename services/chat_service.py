from models.memory import Memory
from models.meeting import Meeting
from models.action_item import ActionItem
from models.participant import Participant
from ai.memory_chat_engine import MemoryChatEngine


class ChatService:
    def __init__(self, user_id):
        self.user_id = user_id
        self.engine = MemoryChatEngine(user_id)

    def ask(self, question):
        return self.engine.answer(question)
