from collections import Counter
from models.memory import Memory
from models.meeting import Meeting


class RecurringPatternDetector:
    def __init__(self, user_id):
        self.user_id = user_id

    def detect_patterns(self):
        memories = Memory.query.filter_by(user_id=self.user_id).all()
        content_words = []
        for m in memories:
            content_words.extend(m.content.lower().split())
        word_freq = Counter(content_words)
        common_words = [word for word, count in word_freq.most_common(20) if len(word) > 4 and count > 1]
        return {"frequent_topics": common_words, "total_memories": len(memories)}
